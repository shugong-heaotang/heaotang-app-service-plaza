import {
  useCallback,
  useEffect,
  useRef,
  useState,
  type FormEvent,
  type ReactNode,
} from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../../../auth/AuthContext";
import { AuthPanel } from "../../../components/AuthPanel";
import { AppFrame } from "../../../components/AppFrame";
import { ApiError } from "../../../infrastructure/apiClient";
import {
  type Paginated,
  type SelfCreatedClubApi,
  type SelfCreatedClubApplication,
  type SelfCreatedClubApplicationStatus,
  type SelfCreatedClubDetail,
  type SelfCreatedClubJoinResult,
  type SelfCreatedClubSummary,
} from "./selfCreatedClubApi";
import {
  selfCreatedClubApplicationsRoute,
  selfCreatedClubDetailPath,
  selfCreatedClubParentRoute,
  selfCreatedClubRootRoute,
} from "./selfCreatedClubContract";
import "./SelfCreatedClubPage.css";

export type SelfCreatedClubPageMode = "list" | "detail" | "applications";

export type SelfCreatedClubPageProps = {
  mode: SelfCreatedClubPageMode;
  clubId?: string;
  api: SelfCreatedClubApi;
};

type LoadState<T> =
  | { status: "loading" }
  | { status: "empty" }
  | { status: "ready"; data: T }
  | { status: "error"; error: unknown };

type JoinFeedback =
  | { status: "created" | "replayed"; result: SelfCreatedClubJoinResult }
  | { status: "error"; error: unknown };

const applicationStatusCopy: Record<SelfCreatedClubApplicationStatus, string> = {
  pending: "待审核",
  approved: "已通过",
  rejected: "未通过",
};

const makeIdempotencyKey = () => {
  const nonce =
    typeof crypto !== "undefined" && typeof crypto.randomUUID === "function"
      ? crypto.randomUUID()
      : `${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;
  return `club-alliance-join-${nonce}`;
};

const isAuthenticationError = (reason: unknown) =>
  reason instanceof ApiError &&
  (reason.status === 401 || reason.code === "AUTH_REQUIRED");

const errorMessage = (reason: unknown) => {
  if (!(reason instanceof ApiError)) return "服务暂时不可用，请稍后重试。";
  const messages: Record<string, string> = {
    CLUB_FILTER_CATEGORY_INVALID: "自建俱乐部筛选条件无效。",
    CLUB_FILTER_COMBINATION_UNSUPPORTED: "自建俱乐部筛选组合不受支持。",
    CLUB_CATEGORY_CROSSOVER_DETECTED: "俱乐部分类数据不一致，已停止展示。",
    CLUB_ID_INVALID: "俱乐部编号无效。",
    CLUB_NOT_FOUND: "未找到可访问的自建俱乐部。",
    CLUB_DETAIL_UNAVAILABLE: "俱乐部详情暂时不可用。",
    CLUB_JOIN_MESSAGE_TOO_LONG: "加入说明不能超过 500 个字。",
    INVALID_IDEMPOTENCY_KEY: "申请凭证无效，请重新提交。",
    IDEMPOTENCY_KEY_REUSED: "申请内容与原凭证冲突，请重新提交。",
    IDEMPOTENCY_IN_PROGRESS: "同一申请正在处理中，请稍后查看本人申请。",
    CLUB_NOT_ACTIVE: "该俱乐部当前不可申请加入。",
    CLUB_ALREADY_MEMBER: "您已经是该俱乐部成员。",
    CLUB_JOIN_UNAVAILABLE: "加入申请暂时不可用。",
    INVALID_PAGINATION: "分页参数无效。",
    INVALID_CLUB_APPLICATION_STATUS: "申请状态筛选无效。",
    CLUB_APPLICATIONS_UNAVAILABLE: "本人申请记录暂时不可用。",
    NETWORK_ERROR: "网络连接失败，请检查网络后重试。",
    REQUEST_TIMEOUT: "请求超时，请稍后重试。",
  };
  return messages[reason.code] ?? "服务暂时不可用，请稍后重试。";
};

const formatDate = (value: string) => {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
};

function StatePanel({
  state,
  title,
  children,
}: {
  state: string;
  title: string;
  children: ReactNode;
}) {
  return (
    <section
      className={`self-created-state state-${state}`}
      data-page-state={state}
      role={state === "error" ? "alert" : "status"}
    >
      <h2>{title}</h2>
      {children}
    </section>
  );
}

function SessionBar() {
  const { user, logout } = useAuth();
  if (!user) return null;
  return (
    <div className="session-bar">
      <span>当前用户：{user.nickname || user.phone || `#${user.id}`}</span>
      <button type="button" onClick={logout}>退出登录</button>
    </div>
  );
}

function PageFrame({ children }: { children: ReactNode }) {
  return (
    <AppFrame
      title="自建俱乐部"
      actions={[]}
      backAction={(
        <Link
          className="back-button"
          to={selfCreatedClubParentRoute}
          aria-label="返回俱乐部联盟"
        >
          ←
        </Link>
      )}
    >
      {children}
    </AppFrame>
  );
}

function AuthenticationRequired({ notice }: { notice?: string }) {
  return (
    <PageFrame>
      <main className="self-created-page" data-page-state="authentication-required">
        {notice && <div className="feedback error" role="alert">{notice}</div>}
        <StatePanel state="authentication-required" title="登录后使用自建俱乐部">
          <p>列表、详情、加入申请和本人状态都使用平台共享登录会话。</p>
        </StatePanel>
        <AuthPanel />
        <Link className="self-created-return" to={selfCreatedClubParentRoute}>
          ← 返回俱乐部联盟
        </Link>
      </main>
    </PageFrame>
  );
}

function Pagination({
  page,
  size,
  total,
  onPage,
}: {
  page: number;
  size: number;
  total: number;
  onPage(page: number): void;
}) {
  const lastPage = Math.max(1, Math.ceil(total / size));
  return (
    <nav className="self-created-pagination" aria-label="分页">
      <button type="button" disabled={page <= 1} onClick={() => onPage(page - 1)}>
        上一页
      </button>
      <span aria-live="polite">第 {page} / {lastPage} 页，共 {total} 项</span>
      <button
        type="button"
        disabled={page >= lastPage}
        onClick={() => onPage(page + 1)}
      >
        下一页
      </button>
    </nav>
  );
}

function ClubList({
  api,
  onAuthenticationExpired,
}: {
  api: SelfCreatedClubApi;
  onAuthenticationExpired(): void;
}) {
  const [query, setQuery] = useState("");
  const [city, setCity] = useState("");
  const [filters, setFilters] = useState({ query: "", city: "", page: 1 });
  const [requestVersion, setRequestVersion] = useState(0);
  const [state, setState] = useState<LoadState<Paginated<SelfCreatedClubSummary>>>(
    { status: "loading" },
  );

  useEffect(() => {
    const controller = new AbortController();
    setState({ status: "loading" });
    void api.search(
      { ...filters },
      { signal: controller.signal },
    ).then((result) => {
      if (controller.signal.aborted) return;
      setState(result.items.length === 0 ? { status: "empty" } : { status: "ready", data: result });
    }).catch((reason: unknown) => {
      if (controller.signal.aborted) return;
      if (isAuthenticationError(reason)) onAuthenticationExpired();
      else setState({ status: "error", error: reason });
    });
    return () => controller.abort();
  }, [api, filters, onAuthenticationExpired, requestVersion]);

  const search = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFilters({ query: query.trim(), city: city.trim(), page: 1 });
  };

  return (
    <section className="self-created-card" aria-labelledby="self-created-list-title">
      <div className="self-created-heading-row">
        <div>
          <p className="section-kicker">服务端权威分类</p>
          <h2 id="self-created-list-title">浏览自建俱乐部</h2>
        </div>
        <Link to={selfCreatedClubApplicationsRoute}>我的加入申请</Link>
      </div>
      <form className="self-created-search" onSubmit={search} role="search">
        <label>
          关键词
          <input value={query} maxLength={80} onChange={(event) => setQuery(event.target.value)} />
        </label>
        <label>
          城市
          <input value={city} maxLength={60} onChange={(event) => setCity(event.target.value)} />
        </label>
        <button type="submit">搜索</button>
      </form>

      {state.status === "loading" && (
        <StatePanel state="loading" title="正在加载自建俱乐部">
          <p aria-live="polite">正在读取服务端筛选后的列表…</p>
        </StatePanel>
      )}
      {state.status === "empty" && (
        <StatePanel state="empty" title="没有符合条件的自建俱乐部">
          <p>可以修改关键词或城市后重新搜索。</p>
        </StatePanel>
      )}
      {state.status === "error" && (
        <StatePanel state="error" title="自建俱乐部列表加载失败">
          <p>{errorMessage(state.error)}</p>
          {state.error instanceof ApiError && <code>{state.error.code}</code>}
          <button type="button" onClick={() => setRequestVersion((value) => value + 1)}>
            重新加载
          </button>
        </StatePanel>
      )}
      {state.status === "ready" && (
        <>
          <ul className="self-created-list" aria-label="自建俱乐部列表">
            {state.data.items.map((club) => (
              <li key={club.id}>
                <div>
                  <h3>{club.name}</h3>
                  <p>{club.intro || "该俱乐部暂未填写简介。"}</p>
                  {club.city && <span>{club.city}</span>}
                </div>
                <Link to={selfCreatedClubDetailPath(club.id)}>查看详情</Link>
              </li>
            ))}
          </ul>
          <Pagination
            page={state.data.page}
            size={state.data.size}
            total={state.data.total}
            onPage={(page) => setFilters((current) => ({ ...current, page }))}
          />
        </>
      )}
    </section>
  );
}

function ClubDetail({
  api,
  clubId,
  onAuthenticationExpired,
}: {
  api: SelfCreatedClubApi;
  clubId: string | undefined;
  onAuthenticationExpired(): void;
}) {
  const parsedClubId = Number(clubId);
  const [requestVersion, setRequestVersion] = useState(0);
  const [state, setState] = useState<LoadState<SelfCreatedClubDetail>>({ status: "loading" });
  const [message, setMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState<JoinFeedback | null>(null);
  const attempt = useRef<{ payload: string; key: string } | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    setState({ status: "loading" });
    void api.detail(parsedClubId, { signal: controller.signal }).then((detail) => {
      if (!controller.signal.aborted) setState({ status: "ready", data: detail });
    }).catch((reason: unknown) => {
      if (controller.signal.aborted) return;
      if (isAuthenticationError(reason)) onAuthenticationExpired();
      else setState({ status: "error", error: reason });
    });
    return () => controller.abort();
  }, [api, onAuthenticationExpired, parsedClubId, requestVersion]);

  const join = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const payload = message.trim();
    if ([...payload].length > 500) {
      setFeedback({
        status: "error",
        error: new ApiError("加入说明过长", 400, "CLUB_JOIN_MESSAGE_TOO_LONG"),
      });
      return;
    }
    if (!attempt.current || attempt.current.payload !== payload) {
      attempt.current = { payload, key: makeIdempotencyKey() };
    }
    setSubmitting(true);
    setFeedback(null);
    try {
      const result = await api.join(parsedClubId, payload, {
        idempotencyKey: attempt.current.key,
      });
      setFeedback({ status: result.status, result });
    } catch (reason) {
      if (isAuthenticationError(reason)) onAuthenticationExpired();
      else {
        if (
          reason instanceof ApiError &&
          (reason.code === "INVALID_IDEMPOTENCY_KEY" ||
            reason.code === "IDEMPOTENCY_KEY_REUSED")
        ) {
          attempt.current = null;
        }
        setFeedback({ status: "error", error: reason });
      }
    } finally {
      setSubmitting(false);
    }
  };

  if (state.status === "loading") {
    return <StatePanel state="loading" title="正在加载俱乐部详情"><p>请稍候…</p></StatePanel>;
  }
  if (state.status === "error") {
    return (
      <StatePanel state="error" title="俱乐部详情加载失败">
        <p>{errorMessage(state.error)}</p>
        {state.error instanceof ApiError && <code>{state.error.code}</code>}
        <button type="button" onClick={() => setRequestVersion((value) => value + 1)}>
          重新加载
        </button>
        <Link to={selfCreatedClubRootRoute}>返回自建俱乐部列表</Link>
      </StatePanel>
    );
  }
  if (state.status !== "ready") return null;

  const completed = feedback?.status === "created" || feedback?.status === "replayed";
  return (
    <section className="self-created-card" aria-labelledby="self-created-detail-title">
      <p className="section-kicker">自建俱乐部详情</p>
      <h2 id="self-created-detail-title">{state.data.name}</h2>
      <p>{state.data.intro || "该俱乐部暂未填写简介。"}</p>
      <dl className="self-created-facts">
        <div><dt>城市</dt><dd>{state.data.city || "未填写"}</dd></div>
        <div><dt>成员数</dt><dd>{state.data.memberCount}</dd></div>
        <div><dt>创建时间</dt><dd>{formatDate(state.data.createdAt)}</dd></div>
      </dl>

      <form className="self-created-join" onSubmit={join}>
        <label>
          加入说明（选填）
          <textarea
            value={message}
            maxLength={500}
            disabled={completed}
            onChange={(event) => {
              setMessage(event.target.value);
              setFeedback(null);
            }}
          />
        </label>
        <button type="submit" disabled={submitting || completed}>
          {submitting ? "正在提交…" : completed ? "申请已提交" : "申请加入"}
        </button>
      </form>

      {feedback?.status === "created" && (
        <div className="feedback success" role="status">申请提交成功，可在本人申请中查看状态。</div>
      )}
      {feedback?.status === "replayed" && (
        <div className="feedback success" role="status">该申请已处理，无需重复提交。</div>
      )}
      {feedback?.status === "error" && (
        <div className="feedback error" role="alert">
          <span>{errorMessage(feedback.error)}</span>
          {feedback.error instanceof ApiError && <code>{feedback.error.code}</code>}
        </div>
      )}
      <div className="self-created-actions">
        <Link to={selfCreatedClubApplicationsRoute}>查看我的加入申请</Link>
        <Link to={selfCreatedClubRootRoute}>返回自建俱乐部列表</Link>
      </div>
    </section>
  );
}

function ApplicationsList({
  api,
  onAuthenticationExpired,
}: {
  api: SelfCreatedClubApi;
  onAuthenticationExpired(): void;
}) {
  const [filter, setFilter] = useState<SelfCreatedClubApplicationStatus | "">("");
  const [page, setPage] = useState(1);
  const [requestVersion, setRequestVersion] = useState(0);
  const [state, setState] = useState<LoadState<Paginated<SelfCreatedClubApplication>>>(
    { status: "loading" },
  );

  useEffect(() => {
    const controller = new AbortController();
    setState({ status: "loading" });
    void api.myApplications({ page, status: filter }, { signal: controller.signal })
      .then((result) => {
        if (controller.signal.aborted) return;
        setState(result.items.length === 0 ? { status: "empty" } : { status: "ready", data: result });
      })
      .catch((reason: unknown) => {
        if (controller.signal.aborted) return;
        if (isAuthenticationError(reason)) onAuthenticationExpired();
        else setState({ status: "error", error: reason });
      });
    return () => controller.abort();
  }, [api, filter, onAuthenticationExpired, page, requestVersion]);

  return (
    <section className="self-created-card" aria-labelledby="self-created-applications-title">
      <div className="self-created-heading-row">
        <div>
          <p className="section-kicker">本人资源</p>
          <h2 id="self-created-applications-title">我的加入申请</h2>
        </div>
        <Link to={selfCreatedClubRootRoute}>浏览自建俱乐部</Link>
      </div>
      <label className="self-created-status-filter">
        申请状态
        <select
          value={filter}
          onChange={(event) => {
            setFilter(event.target.value as SelfCreatedClubApplicationStatus | "");
            setPage(1);
          }}
        >
          <option value="">全部</option>
          <option value="pending">待审核</option>
          <option value="approved">已通过</option>
          <option value="rejected">未通过</option>
        </select>
      </label>

      {state.status === "loading" && (
        <StatePanel state="loading" title="正在加载本人申请"><p>请稍候…</p></StatePanel>
      )}
      {state.status === "empty" && (
        <StatePanel state="empty" title="暂无加入申请">
          <p>选择一个自建俱乐部后即可提交加入申请。</p>
        </StatePanel>
      )}
      {state.status === "error" && (
        <StatePanel state="error" title="本人申请加载失败">
          <p>{errorMessage(state.error)}</p>
          {state.error instanceof ApiError && <code>{state.error.code}</code>}
          <button type="button" onClick={() => setRequestVersion((value) => value + 1)}>
            重新加载
          </button>
        </StatePanel>
      )}
      {state.status === "ready" && (
        <>
          <ul className="self-created-applications" aria-label="本人加入申请列表">
            {state.data.items.map((application) => (
              <li key={application.id}>
                <div>
                  <strong>{applicationStatusCopy[application.status]}</strong>
                  <time dateTime={application.createdAt}>{formatDate(application.createdAt)}</time>
                </div>
                {application.message && <p>{application.message}</p>}
                {application.reviewNote && <p>审核说明：{application.reviewNote}</p>}
                <Link to={selfCreatedClubDetailPath(application.clubId)}>查看对应俱乐部</Link>
              </li>
            ))}
          </ul>
          <Pagination
            page={state.data.page}
            size={state.data.size}
            total={state.data.total}
            onPage={setPage}
          />
        </>
      )}
    </section>
  );
}

export function SelfCreatedClubPage({ mode, clubId, api }: SelfCreatedClubPageProps) {
  const { isAuthenticated, logout } = useAuth();
  const [authNotice, setAuthNotice] = useState("");

  const authenticationExpired = useCallback(() => {
    setAuthNotice("登录状态已失效，请重新登录。");
    logout();
  }, [logout]);

  if (!isAuthenticated) return <AuthenticationRequired notice={authNotice} />;

  return (
    <PageFrame>
      <main className="self-created-page" data-page-state={mode}>
        {authNotice && <div className="feedback error" role="alert">{authNotice}</div>}
        <SessionBar />
        {mode === "list" && (
          <ClubList api={api} onAuthenticationExpired={authenticationExpired} />
        )}
        {mode === "detail" && (
          <ClubDetail
            api={api}
            clubId={clubId}
            onAuthenticationExpired={authenticationExpired}
          />
        )}
        {mode === "applications" && (
          <ApplicationsList api={api} onAuthenticationExpired={authenticationExpired} />
        )}
        <nav className="self-created-footer" aria-label="自建俱乐部返回路径">
          <Link to={selfCreatedClubParentRoute}>← 返回俱乐部联盟</Link>
          <Link to="/services">返回服务广场</Link>
        </nav>
      </main>
    </PageFrame>
  );
}
