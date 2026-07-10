import { useEffect, useState } from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { AppFrame } from "../components/AppFrame";
import { AuthPanel } from "../components/AuthPanel";
import { isServiceKey, serviceDefinitions } from "../domain/services";
import {
  isRealSubmissionMode,
  listAvailableClubs,
  submissionRepository,
} from "../infrastructure/submissionRepository";
import { NotFoundPage } from "./NotFoundPage";

type ViewState = "normal" | "no-permission" | "empty" | "error";

const stateCopy: Record<Exclude<ViewState, "normal">, { title: string; body: string }> = {
  "no-permission": {
    title: "暂时没有访问权限",
    body: "请先登录具备该服务权限的会员账号，再重新进入。",
  },
  empty: {
    title: "暂时没有可展示内容",
    body: "当前没有历史记录，你仍可以返回正常状态发起新的申请。",
  },
  error: {
    title: "服务暂时不可用",
    body: "连接服务时发生异常，请稍后重试或返回服务广场。",
  },
};

export function CoreServicePage() {
  const { serviceKey } = useParams();
  const { isAuthenticated, user, logout } = useAuth();
  const [searchParams] = useSearchParams();
  const [viewState, setViewState] = useState<ViewState>("normal");
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [submitError, setSubmitError] = useState("");
  const [note, setNote] = useState("");
  const [patientName, setPatientName] = useState("");
  const [symptoms, setSymptoms] = useState("");
  const [clubId, setClubId] = useState("");
  const [clubs, setClubs] = useState<Array<{ id: number; name: string }>>([]);
  const [clubsError, setClubsError] = useState("");

  const service = isServiceKey(serviceKey) ? serviceDefinitions[serviceKey] : null;
  const selectedCategory = searchParams.get("category");
  const isManageView = searchParams.get("view") === "manage";
  const canManageClub = Boolean(user?.scopes.includes("club:manage"));

  useEffect(() => {
    if (!service || !isRealSubmissionMode || !isAuthenticated || service.key !== "club-alliance" || isManageView) return;
    let active = true;
    listAvailableClubs()
      .then((items) => {
        if (active) setClubs(items);
      })
      .catch((reason) => {
        if (active) setClubsError(reason instanceof Error ? reason.message : "俱乐部列表加载失败");
      });
    return () => {
      active = false;
    };
  }, [isAuthenticated, isManageView, service]);

  const submit = async () => {
    if (!service) return;
    setSubmitting(true);
    setSubmitError("");
    try {
      await submissionRepository.submit(service.key, {
        note,
        clubId: clubId ? Number(clubId) : undefined,
        patientName,
        symptoms,
      });
      setSubmitted(true);
    } catch (reason) {
      setSubmitError(reason instanceof Error ? reason.message : "提交失败，请稍后重试");
    } finally {
      setSubmitting(false);
    }
  };

  if (!service) {
    return <NotFoundPage />;
  }

  return (
    <AppFrame
      title={service.title}
      backAction={
        <Link className="back-button" to="/services" aria-label="返回服务广场">←</Link>
      }
    >
      <div className="integration-banner">
        第一阶段联调 · {isRealSubmissionMode ? "真实 API 适配层" : "模拟适配层"}
      </div>

      {isRealSubmissionMode && !isAuthenticated ? (
        <AuthPanel />
      ) : (
        <>
          {isRealSubmissionMode && user && (
            <div className="session-bar">
              <span>当前用户：{user.nickname || user.phone || `#${user.id}`}</span>
              <button type="button" onClick={logout}>退出登录</button>
            </div>
          )}

          <article className={`service-detail theme-${service.theme}`}>
        <div className="service-detail-heading">
          <span className="service-detail-icon" aria-hidden="true">{service.icon}</span>
          <div>
            <p className="section-kicker">{service.kicker}</p>
            <h2>{isManageView ? `${service.title}管理中心` : service.title}</h2>
          </div>
        </div>
        <p className="service-description">{service.description}</p>
        {selectedCategory && <p className="selection-note">当前选择：{selectedCategory}</p>}

        {isManageView && (
          canManageClub ? (
            <div className="feedback empty" role="status">
              <strong>管理权限验证通过 · 试用入口</strong>
              <span>公共权限与导航接口已经接通；俱乐部业务管理功能将在需求冻结后按依赖计划接入。</span>
            </div>
          ) : (
            <div className="feedback no-permission" role="status">
              <strong>暂时没有俱乐部管理权限</strong>
              <span>该入口需要 club:manage，普通会员仍可返回俱乐部联盟申请加入。</span>
            </div>
          )
        )}

        {!isManageView && viewState === "normal" && !submitted && (
          <div className="service-form">
            {service.key === "club-alliance" && (
              <label>
                选择俱乐部
                <select value={clubId} onChange={(event) => setClubId(event.target.value)}>
                  <option value="">请选择</option>
                  {clubs.map((club) => (
                    <option value={club.id} key={club.id}>{club.name}</option>
                  ))}
                </select>
                {clubsError && <span className="field-error">{clubsError}</span>}
              </label>
            )}
            {service.key === "health-manager" && (
              <label>
                咨询人姓名
                <input
                  value={patientName}
                  onChange={(event) => setPatientName(event.target.value)}
                  placeholder="请输入姓名"
                  maxLength={40}
                />
              </label>
            )}
            <label>
              {service.key === "health-manager" ? "健康需求" : "补充说明"}
              <textarea
                value={service.key === "health-manager" ? symptoms : note}
                onChange={(event) =>
                  service.key === "health-manager"
                    ? setSymptoms(event.target.value)
                    : setNote(event.target.value)
                }
                placeholder={
                  service.key === "life-navigation"
                    ? "可以简要描述希望获得导航的方向"
                    : service.key === "club-alliance"
                      ? "可以填写加入理由"
                      : "请简要描述希望咨询的健康问题"
                }
                maxLength={500}
              />
            </label>
          </div>
        )}

        {!isManageView && <div className="state-switcher" aria-label="联调状态切换">
          {([
            ["normal", "正常"],
            ["no-permission", "无权限"],
            ["empty", "空状态"],
            ["error", "异常"],
          ] as const).map(([state, label]) => (
            <button
              className={viewState === state ? "active" : ""}
              type="button"
              key={state}
              onClick={() => {
                setViewState(state);
                setSubmitted(false);
              }}
            >
              {label}
            </button>
          ))}
        </div>}

        {!isManageView && (viewState === "normal" ? (
          submitted ? (
            <div className="feedback success" role="status">
              <strong>提交成功</strong>
              <span>{service.pendingLabel}</span>
            </div>
          ) : (
            <>
              {submitError && <div className="feedback error" role="alert">{submitError}</div>}
              <button className="primary-action" type="button" onClick={submit} disabled={submitting}>
                {submitting ? "正在提交…" : service.actionLabel}
              </button>
            </>
          )
        ) : (
          <div className={`feedback ${viewState}`} role="status">
            <strong>{stateCopy[viewState].title}</strong>
            <span>{stateCopy[viewState].body}</span>
          </div>
        ))}
          </article>

          <Link className="return-link" to="/services">← 返回服务广场</Link>
        </>
      )}
    </AppFrame>
  );
}
