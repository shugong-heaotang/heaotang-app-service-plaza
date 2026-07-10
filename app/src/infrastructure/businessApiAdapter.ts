import { ApiError, apiRequest, type ApiRequestOptions } from "./apiClient";

export type BusinessApiExecutionOptions = Pick<
  ApiRequestOptions,
  "requestId" | "signal" | "timeoutMs"
> & {
  /**
   * Reuse this key only when deliberately replaying the same logical write.
   * Normal callers should omit it and let the adapter create one.
   */
  idempotencyKey?: string;
};

type BusinessApiOperationBase<Input, Output> = {
  operationId: string;
  path: (input: Input) => string;
  /** Compile-time carrier for the response type; never read at runtime. */
  readonly __output?: Output;
};

export type BusinessApiReadOperation<Input, Output> = BusinessApiOperationBase<
  Input,
  Output
> & {
  kind: "read";
  authMode?: "shared-session" | "anonymous";
};

export type BusinessApiWriteOperation<Input, Output> = BusinessApiOperationBase<
  Input,
  Output
> & {
  kind: "write";
  authMode?: "shared-session";
  method: "POST" | "PUT" | "PATCH" | "DELETE";
  body: (input: Input) => unknown;
};

export type BusinessApiOperation<Input, Output> =
  | BusinessApiReadOperation<Input, Output>
  | BusinessApiWriteOperation<Input, Output>;

export const defineBusinessRead = <Input, Output>(
  operation: Omit<BusinessApiReadOperation<Input, Output>, "kind">,
): BusinessApiReadOperation<Input, Output> => ({ ...operation, kind: "read" });

export const defineBusinessWrite = <Input, Output>(
  operation: Omit<BusinessApiWriteOperation<Input, Output>, "kind">,
): BusinessApiWriteOperation<Input, Output> => ({ ...operation, kind: "write" });

const IDENTIFIER_PATTERN = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const IDEMPOTENCY_KEY_PATTERN = /^[A-Za-z0-9._:-]{8,128}$/;

function randomNonce(): string {
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    return crypto.randomUUID();
  }
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;
}

function definitionError(message: string, requestId?: string): ApiError {
  return new ApiError(message, 0, "INVALID_ADAPTER_DEFINITION", requestId);
}

function validateIdentifier(label: string, value: string): void {
  if (!IDENTIFIER_PATTERN.test(value) || value.length > 40) {
    throw definitionError(`${label} 必须使用不超过 40 位的小写 kebab-case`);
  }
}

function validatePath(path: string, requestId?: string): void {
  if (
    !path.startsWith("/api/v1/")
    || path.includes("://")
    || path.includes("..")
    || path.includes("\\")
    || path.includes("#")
    || /[\u0000-\u001f\u007f\s]/.test(path)
  ) {
    throw definitionError("业务 API 适配器只能调用平台 /api/v1/ 接口", requestId);
  }
}

function resolveIdempotencyKey(
  serviceId: string,
  operationId: string,
  supplied: string | undefined,
  requestId?: string,
): string {
  const key = supplied ?? `${serviceId}-${operationId}-${randomNonce()}`;
  if (!IDEMPOTENCY_KEY_PATTERN.test(key)) {
    throw new ApiError(
      "Idempotency-Key 必须为 8 到 128 位安全字符",
      0,
      "INVALID_IDEMPOTENCY_KEY",
      requestId,
    );
  }
  return key;
}

export type BusinessApiAdapter = {
  readonly serviceId: string;
  execute<Input, Output>(
    operation: BusinessApiOperation<Input, Output>,
    input: Input,
    options?: BusinessApiExecutionOptions,
  ): Promise<Output>;
};

/**
 * Platform-owned boundary for module API access. It owns authentication,
 * strict envelopes, request correlation, cancellation, timeouts, safe retry,
 * write idempotency and ApiError preservation so feature modules do not copy
 * those policies.
 */
export function createBusinessApiAdapter(serviceId: string): BusinessApiAdapter {
  validateIdentifier("serviceId", serviceId);

  return {
    serviceId,
    async execute<Input, Output>(
      operation: BusinessApiOperation<Input, Output>,
      input: Input,
      options: BusinessApiExecutionOptions = {},
    ): Promise<Output> {
      validateIdentifier("operationId", operation.operationId);
      const path = operation.path(input);
      validatePath(path, options.requestId);

      const commonOptions: ApiRequestOptions = {
        auth: operation.authMode !== "anonymous",
        envelope: "strict",
        requestId: options.requestId,
        signal: options.signal,
        timeoutMs: options.timeoutMs,
      };

      if (operation.kind === "read") {
        return apiRequest<Output>(path, { method: "GET" }, {
          ...commonOptions,
          retry: { mode: "safe-method", maxAttempts: 2, baseDelayMs: 200 },
        });
      }

      const idempotencyKey = resolveIdempotencyKey(
        serviceId,
        operation.operationId,
        options.idempotencyKey,
        options.requestId,
      );
      return apiRequest<Output>(path, {
        method: operation.method,
        headers: { "Idempotency-Key": idempotencyKey },
        body: JSON.stringify(operation.body(input)),
      }, {
        ...commonOptions,
        retry: { mode: "idempotency-key", maxAttempts: 2, baseDelayMs: 200 },
      });
    },
  };
}
