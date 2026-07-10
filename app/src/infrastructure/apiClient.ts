export type ApiEnvelope<T> = {
  success?: boolean;
  data?: T;
  error?: string;
  code?: string;
  message?: string;
};

export type ApiRetryPolicy = {
  /** Total attempts, including the first request. Limited to three. */
  maxAttempts?: number;
  /** Initial exponential-backoff delay. */
  baseDelayMs?: number;
  /** Must be declared for a write request and accompanied by Idempotency-Key. */
  mode?: "safe-method" | "idempotency-key";
  /** A subset of the SDK's transient-status allowlist. */
  retryableStatuses?: readonly number[];
};

export type ApiRequestOptions = {
  auth?: boolean;
  /** Timeout for each network attempt. */
  timeoutMs?: number;
  signal?: AbortSignal;
  /** Logical request ID. The same value is retained across controlled retries. */
  requestId?: string;
  /** Retries are opt-in. `true` uses the safe-method defaults. */
  retry?: boolean | ApiRetryPolicy;
  /** Versioned APIs are strict by default; use compatible only for declared legacy endpoints. */
  envelope?: "strict" | "compatible";
};

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly code: string = "REQUEST_FAILED",
    readonly requestId?: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export const DEFAULT_API_TIMEOUT_MS = 15_000;
export const MAX_API_TIMEOUT_MS = 120_000;

const MAX_RETRY_ATTEMPTS = 3;
const DEFAULT_RETRY_ATTEMPTS = 2;
const DEFAULT_RETRY_DELAY_MS = 200;
const MAX_RETRY_DELAY_MS = 2_000;
const SAFE_METHODS = new Set(["GET", "HEAD", "OPTIONS"]);
const TRANSIENT_STATUSES = new Set([408, 425, 429, 500, 502, 503, 504]);
const DEFAULT_RETRYABLE_STATUSES = [408, 425, 429, 502, 503, 504] as const;

const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL ?? "").replace(/\/$/, "");

export const tokenStorage = {
  get: () => sessionStorage.getItem("heaotang_access_token"),
  set: (token: string) => sessionStorage.setItem("heaotang_access_token", token),
  clear: () => sessionStorage.removeItem("heaotang_access_token"),
};

function createRequestId(): string {
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    return crypto.randomUUID();
  }
  return `web-${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;
}

function invalidOptions(message: string, requestId: string): ApiError {
  return new ApiError(message, 0, "INVALID_REQUEST_OPTIONS", requestId);
}

function resolveTimeout(value: number, requestId: string): number {
  if (!Number.isFinite(value) || value <= 0 || value > MAX_API_TIMEOUT_MS) {
    throw invalidOptions(`timeoutMs 必须是 1 到 ${MAX_API_TIMEOUT_MS} 之间的有限数值`, requestId);
  }
  return value;
}

function resolveRetryPolicy(
  method: string,
  headers: Headers,
  retry: ApiRequestOptions["retry"],
  requestId: string,
): Required<Omit<ApiRetryPolicy, "retryableStatuses">> & { retryableStatuses: Set<number> } | undefined {
  if (!retry) {
    return undefined;
  }

  const input = retry === true ? {} : retry;
  const maxAttempts = input.maxAttempts ?? DEFAULT_RETRY_ATTEMPTS;
  if (!Number.isInteger(maxAttempts) || maxAttempts < 2 || maxAttempts > MAX_RETRY_ATTEMPTS) {
    throw invalidOptions(`maxAttempts 必须是 2 到 ${MAX_RETRY_ATTEMPTS} 之间的整数`, requestId);
  }

  const baseDelayMs = input.baseDelayMs ?? DEFAULT_RETRY_DELAY_MS;
  if (!Number.isFinite(baseDelayMs) || baseDelayMs < 0 || baseDelayMs > MAX_RETRY_DELAY_MS) {
    throw invalidOptions(`baseDelayMs 必须是 0 到 ${MAX_RETRY_DELAY_MS} 之间的有限数值`, requestId);
  }

  const mode = input.mode ?? "safe-method";
  if (SAFE_METHODS.has(method)) {
    if (mode === "idempotency-key" && !headers.get("Idempotency-Key")?.trim()) {
      throw invalidOptions("idempotency-key 重试模式必须携带 Idempotency-Key", requestId);
    }
  } else if (mode !== "idempotency-key" || !headers.get("Idempotency-Key")?.trim()) {
    throw invalidOptions("写请求不得盲目重试；必须携带 Idempotency-Key 并声明 idempotency-key 模式", requestId);
  }

  const statuses = input.retryableStatuses ?? DEFAULT_RETRYABLE_STATUSES;
  if (statuses.length === 0 || statuses.some((status) => !TRANSIENT_STATUSES.has(status))) {
    throw invalidOptions("retryableStatuses 只能使用 SDK 允许的瞬时故障状态码", requestId);
  }

  return {
    maxAttempts,
    baseDelayMs,
    mode,
    retryableStatuses: new Set(statuses),
  };
}

type AttemptContext = {
  signal: AbortSignal;
  timedOut: () => boolean;
  cleanup: () => void;
};

function createAttemptContext(signals: Array<AbortSignal | null | undefined>, timeoutMs: number): AttemptContext {
  const controller = new AbortController();
  let didTimeout = false;
  const removers: Array<() => void> = [];

  for (const signal of signals) {
    if (!signal) continue;
    if (signal.aborted) {
      controller.abort(signal.reason);
      break;
    }
    const abort = () => controller.abort(signal.reason);
    signal.addEventListener("abort", abort, { once: true });
    removers.push(() => signal.removeEventListener("abort", abort));
  }

  const timer = setTimeout(() => {
    didTimeout = true;
    controller.abort(new DOMException("Request timed out", "TimeoutError"));
  }, timeoutMs);

  return {
    signal: controller.signal,
    timedOut: () => didTimeout,
    cleanup: () => {
      clearTimeout(timer);
      removers.forEach((remove) => remove());
    },
  };
}

function isCallerAborted(signals: Array<AbortSignal | null | undefined>): boolean {
  return signals.some((signal) => signal?.aborted);
}

function waitForRetry(delayMs: number, signals: Array<AbortSignal | null | undefined>, requestId: string): Promise<void> {
  if (isCallerAborted(signals)) {
    return Promise.reject(new ApiError("请求已取消", 0, "REQUEST_ABORTED", requestId));
  }
  if (delayMs === 0) {
    return Promise.resolve();
  }

  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      cleanup();
      resolve();
    }, delayMs);
    const listeners: Array<[AbortSignal, () => void]> = [];
    const cleanup = () => listeners.forEach(([signal, listener]) => signal.removeEventListener("abort", listener));

    for (const signal of signals) {
      if (!signal) continue;
      const abort = () => {
        clearTimeout(timer);
        cleanup();
        reject(new ApiError("请求已取消", 0, "REQUEST_ABORTED", requestId));
      };
      signal.addEventListener("abort", abort, { once: true });
      listeners.push([signal, abort]);
    }
  });
}

export async function apiRequest<T>(
  path: string,
  init: RequestInit = {},
  options: ApiRequestOptions = {},
): Promise<T> {
  const headers = new Headers(init.headers);
  const requestId = options.requestId?.trim() || headers.get("X-Request-ID")?.trim() || createRequestId();
  const timeoutMs = resolveTimeout(options.timeoutMs ?? DEFAULT_API_TIMEOUT_MS, requestId);
  const method = (init.method ?? "GET").toUpperCase();
  if (!headers.has("Content-Type") && init.body) {
    headers.set("Content-Type", "application/json");
  }
  headers.set("X-Request-ID", requestId);

  if (options.auth) {
    const token = tokenStorage.get();
    if (!token) {
      throw new ApiError("请先登录后再使用该服务", 401, "AUTH_REQUIRED", requestId);
    }
    headers.set("Authorization", `Bearer ${token}`);
  }

  const retryPolicy = resolveRetryPolicy(method, headers, options.retry, requestId);
  const maxAttempts = retryPolicy?.maxAttempts ?? 1;
  const callerSignals = [init.signal, options.signal];

  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    const context = createAttemptContext(callerSignals, timeoutMs);
    try {
      const response = await fetch(`${apiBaseUrl}${path}`, { ...init, method, headers, signal: context.signal });
      const responseRequestId = response.headers.get("X-Request-ID") || requestId;
      if (retryPolicy?.retryableStatuses.has(response.status) && attempt < maxAttempts) {
        const delayMs = Math.min(retryPolicy.baseDelayMs * 2 ** (attempt - 1), MAX_RETRY_DELAY_MS);
        await waitForRetry(delayMs, callerSignals, requestId);
        continue;
      }

      const payload = (await response.json().catch(() => ({}))) as ApiEnvelope<T>;
      if (!response.ok || payload.success === false || payload.error) {
        if (response.status === 401) {
          tokenStorage.clear();
        }
        throw new ApiError(
          payload.error || payload.message || `请求失败（${response.status}）`,
          response.status,
          payload.code || "REQUEST_FAILED",
          responseRequestId,
        );
      }

      const strictEnvelope = options.envelope === "strict"
        || (options.envelope !== "compatible" && path.startsWith("/api/v1/"));
      if (
        strictEnvelope
        && (payload.success !== true || !Object.prototype.hasOwnProperty.call(payload, "data"))
      ) {
        throw new ApiError(
          "服务端响应不符合统一接口信封",
          response.status,
          "INVALID_API_ENVELOPE",
          responseRequestId,
        );
      }

      return (payload.data ?? payload) as T;
    } catch (reason) {
      if (reason instanceof ApiError) {
        throw reason;
      }

      const callerAborted = isCallerAborted(callerSignals);
      if (callerAborted) {
        throw new ApiError("请求已取消", 0, "REQUEST_ABORTED", requestId);
      }

      const code = context.timedOut() ? "REQUEST_TIMEOUT" : "NETWORK_ERROR";
      const message = context.timedOut() ? `请求超时（${timeoutMs}ms）` : "网络连接失败";
      if (retryPolicy && attempt < maxAttempts) {
        const delayMs = Math.min(retryPolicy.baseDelayMs * 2 ** (attempt - 1), MAX_RETRY_DELAY_MS);
        await waitForRetry(delayMs, callerSignals, requestId);
        continue;
      }
      throw new ApiError(message, 0, code, requestId);
    } finally {
      context.cleanup();
    }
  }

  throw new ApiError("请求失败", 0, "REQUEST_FAILED", requestId);
}
