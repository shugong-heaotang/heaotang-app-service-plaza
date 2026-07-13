import { useEffect, useState, type FormEvent } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../../auth/AuthContext";
import { AppFrame } from "../../components/AppFrame";
import { AuthPanel } from "../../components/AuthPanel";
import { ApiError } from "../../infrastructure/apiClient";
import {
  defaultLifeNavigationHistoryLimit,
  loadLifeNavigationApplicationHistory,
  submitLifeNavigationApplication,
  type LifeNavigationApplicationInput,
  type LifeNavigationApplicationRecord,
  type LifeNavigationHistoryState,
  type LifeNavigationSubmissionResult,
} from "./lifeNavigationApi";
import "./LifeNavigationPage.css";

export type LifeNavigationPageApi = {
  loadHistory(options?: { signal?: AbortSignal }): Promise<LifeNavigationHistoryState>;
  submitApplication(input?: LifeNavigationApplicationInput): Promise<LifeNavigationSubmissionResult>;
};

export type LifeNavigationPageProps = {
  api?: LifeNavigationPageApi;
};

type HistoryViewState =
  | Exclude<LifeNavigationHistoryState, { status: "error" }>
  | { status: "error"; error: unknown };

type SubmissionFeedback =
  | { kind: "created" | "replayed"; message: string }
  | { kind: "error"; message: string };

const productionApi: LifeNavigationPageApi = {
  loadHistory: (options = {}) =>
    loadLifeNavigationApplicationHistory(defaultLifeNavigationHistoryLimit, options),
  submitApplication: (input = {}) => submitLifeNavigationApplication(input),
};

function isAuthenticationError(reason: unknown): boolean {
  return reason instanceof ApiError && (reason.code === "AUTH_REQUIRED" || reason.status === 401);
}

function submissionErrorMessage(reason: unknown): string {
  if (!(reason instanceof ApiError)) {
    return "提交失败，请稍后重试。";
  }

  if (reason.code === "LIFE_RECORD_DAILY_LIMIT") {
    return "今日申请次数已达上限，请明日再试。";
  }
  if (reason.code === "IDEMPOTENCY_IN_PROGRESS") {
    return "同一申请正在处理中，请稍候查看申请记录。";
  }
  if (reason.code === "IDEMPOTENCY_KEY_REUSED" || reason.status === 409) {
    return "申请凭证与原内容冲突，请重新提交。";
  }
  if (reason.code === "NETWORK_ERROR" || reason.code === "REQUEST_TIMEOUT") {
    return "网络连接异常，请检查网络后重试。";
  }
  return "提交失败，请稍后重试。";
}

function formatSubmittedAt(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

function ApplicationHistory({ items }: { items: LifeNavigationApplicationRecord[] }) {
  return (
    <ul className="life-navigation-history-list" aria-label="个人申请记录">
      {items.map((item) => (
        <li key={item.id}>
          <span className="life-navigation-history-status">已提交</span>
          <time dateTime={item.createdAt}>{formatSubmittedAt(item.createdAt)}</time>
          <p>{item.note}</p>
        </li>
      ))}
    </ul>
  );
}

export function LifeNavigationPage({ api = productionApi }: LifeNavigationPageProps) {
  const { isAuthenticated, logout } = useAuth();
  const [history, setHistory] = useState<HistoryViewState>({ status: "loading" });
  const [historyRequest, setHistoryRequest] = useState(0);
  const [note, setNote] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState<SubmissionFeedback | null>(null);
  const [authNotice, setAuthNotice] = useState("");

  useEffect(() => {
    if (!isAuthenticated) {
      setHistory({ status: "loading" });
      setNote("");
      setFeedback(null);
      setSubmitting(false);
      return;
    }

    const controller = new AbortController();
    setAuthNotice("");
    setHistory({ status: "loading" });
    void api
      .loadHistory({ signal: controller.signal })
      .then((nextState) => {
        if (controller.signal.aborted) return;
        if (nextState.status === "error" && isAuthenticationError(nextState.error)) {
          setAuthNotice("登录状态已失效，请重新登录。");
          logout();
          return;
        }
        setHistory(nextState);
      })
      .catch((reason: unknown) => {
        if (!controller.signal.aborted) setHistory({ status: "error", error: reason });
      });

    return () => controller.abort();
  }, [api, historyRequest, isAuthenticated, logout]);

  const retryHistory = () => setHistoryRequest((current) => current + 1);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSubmitting(true);
    setFeedback(null);
    try {
      const result = await api.submitApplication({ note });
      setFeedback(
        result.status === "replayed"
          ? { kind: "replayed", message: "申请已处理，无需重复提交。" }
          : { kind: "created", message: "申请提交成功。" },
      );
      setNote("");
      retryHistory();
    } catch (reason) {
      if (isAuthenticationError(reason)) {
        setAuthNotice("登录状态已失效，请重新登录。");
        logout();
      } else {
        setFeedback({ kind: "error", message: submissionErrorMessage(reason) });
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AppFrame
      title="生命导航"
      backAction={
        <Link className="back-button" to="/services" aria-label="返回服务广场">
          ←
        </Link>
      }
    >
      {authNotice && <div className="feedback error" role="alert">{authNotice}</div>}

      {!isAuthenticated ? (
        <AuthPanel />
      ) : (
        <div className="life-navigation-page">
          <section className="life-navigation-card" aria-labelledby="life-navigation-application-title">
            <p className="section-kicker">生命导航申请</p>
            <h2 id="life-navigation-application-title">提交导航需求</h2>
            <p>填写希望获得协助的方向，提交后可在本页查看个人申请记录。</p>
            <form className="life-navigation-form" onSubmit={submit}>
              <label>
                申请说明（选填）
                <textarea
                  value={note}
                  onChange={(event) => setNote(event.target.value)}
                  maxLength={500}
                  placeholder="可以简要描述希望获得导航的方向"
                />
              </label>
              <button className="primary-action" type="submit" disabled={submitting}>
                {submitting ? "正在提交…" : "提交申请"}
              </button>
            </form>

            {feedback && (
              <div
                className={`feedback ${feedback.kind === "error" ? "error" : "success"}`}
                role={feedback.kind === "error" ? "alert" : "status"}
              >
                {feedback.message}
              </div>
            )}
          </section>

          <section className="life-navigation-card" aria-labelledby="life-navigation-history-title">
            <h2 id="life-navigation-history-title">我的申请记录</h2>
            <div aria-live="polite">
              {history.status === "loading" && <p role="status">正在加载申请记录…</p>}
              {history.status === "empty" && <p>暂无申请记录。</p>}
              {history.status === "ready" && <ApplicationHistory items={history.items} />}
              {history.status === "error" && (
                <div className="feedback error" role="alert">
                  <span>申请记录加载失败，请重试。</span>
                  <button type="button" onClick={retryHistory}>重新加载</button>
                </div>
              )}
            </div>
          </section>

          <Link className="return-link" to="/services">← 返回服务广场</Link>
        </div>
      )}
    </AppFrame>
  );
}
