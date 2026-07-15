import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import { ActionControl } from "../../components/ActionControl";
import { AppFrame } from "../../components/AppFrame";
import type { ServiceAction } from "../../domain/serviceActions";
import type { ActionAccessDecision } from "../../infrastructure/actionExecutor";
import { clubAllianceReturnRoute, clubAllianceRootRoute } from "./clubAllianceHomepageContract";
import {
  selfCreatedClubActionId,
  selfCreatedClubRootRoute,
} from "./self-created/selfCreatedClubContract";
import { MemberHomeShell, type MemberHomeModel } from "./member-home";
import { PublicWelfareRegionalPanel } from "./public-welfare-regional";
import "./ClubAlliancePage.css";

type BaseReadyModel = { actions: readonly ServiceAction[] };

export type ClubAlliancePageModel =
  | { status: "loading" }
  | { status: "empty" }
  | { status: "error"; message: string; errorId?: string }
  | (BaseReadyModel & { status: "member-home"; memberHome: MemberHomeModel })
  | (BaseReadyModel & {
      status: "home";
      categories: readonly ServiceAction[];
      management: ServiceAction;
    })
  | (BaseReadyModel & {
      status: "focused";
      categories: readonly ServiceAction[];
      management: ServiceAction;
      selected: ServiceAction;
    })
  | (BaseReadyModel & {
      status: "unauthorized";
      selected: ServiceAction;
      reason: Exclude<ActionAccessDecision, { allowed: true }>["reason"];
      missingScopes: readonly string[];
    })
  | (BaseReadyModel & {
      status: "maintenance";
      selected: ServiceAction;
    })
  | (BaseReadyModel & {
      status: "offline";
      selected: ServiceAction;
    });

export type ClubAlliancePageProps = {
  model: ClubAlliancePageModel;
  onRetry(): void;
};

const lifecycleLabel: Record<ServiceAction["lifecycle_status"], string> = {
  active: "入口可访问",
  preview: "预览中",
  planned: "规划中",
  maintenance: "维护中",
  offline: "已下线",
};

const backAction = (
  <Link className="back-button" to={clubAllianceReturnRoute} aria-label="返回服务广场">
    ←
  </Link>
);

function StatePanel({
  state,
  title,
  children,
}: {
  state: ClubAlliancePageModel["status"];
  title: string;
  children: ReactNode;
}) {
  const role = state === "error" ? "alert" : "status";
  return (
    <section className={`club-alliance-state state-${state}`} data-page-state={state} role={role}>
      <p className="section-kicker">俱乐部联盟</p>
      <h2>{title}</h2>
      <div>{children}</div>
    </section>
  );
}

export function ClubAlliancePage({ model, onRetry }: ClubAlliancePageProps) {
  if (model.status === "loading") {
    return (
      <AppFrame title="俱乐部联盟" backAction={backAction} actions={[]}>
        <StatePanel state="loading" title="正在加载标准入口">
          <p aria-live="polite">正在读取服务目录与动作目录…</p>
        </StatePanel>
      </AppFrame>
    );
  }

  if (model.status === "empty") {
    return (
      <AppFrame title="俱乐部联盟" backAction={backAction} actions={[]}>
        <StatePanel state="empty" title="暂时没有可用入口">
          <p>标准目录当前为空，请稍后重新加载。</p>
          <button type="button" onClick={onRetry}>重新加载</button>
        </StatePanel>
      </AppFrame>
    );
  }

  if (model.status === "error") {
    return (
      <AppFrame title="俱乐部联盟" backAction={backAction} actions={[]}>
        <StatePanel state="error" title="标准目录无法使用">
          <p>{model.message}</p>
          {model.errorId && <code>{model.errorId}</code>}
          <button type="button" onClick={onRetry}>重新加载</button>
        </StatePanel>
      </AppFrame>
    );
  }

  if (model.status === "unauthorized") {
    return (
      <AppFrame title="俱乐部联盟" backAction={backAction} actions={model.actions}>
        <StatePanel state="unauthorized" title="需要登录或相应权限">
          <p>{model.selected.label}当前不可访问。</p>
          <span data-access-reason={model.reason}>{model.reason}</span>
          {model.missingScopes.length > 0 && (
            <p>缺少权限：{model.missingScopes.join("、")}</p>
          )}
          <Link to={clubAllianceRootRoute}>返回俱乐部联盟首页</Link>
        </StatePanel>
      </AppFrame>
    );
  }

  if (model.status === "maintenance" || model.status === "offline") {
    const maintenance = model.status === "maintenance";
    return (
      <AppFrame title="俱乐部联盟" backAction={backAction} actions={model.actions}>
        <StatePanel
          state={model.status}
          title={maintenance ? "入口维护中" : "入口已下线"}
        >
          <p>{model.selected.label}{maintenance ? "正在维护，请稍后再试。" : "当前不再提供访问。"}</p>
          <Link to={clubAllianceRootRoute}>返回俱乐部联盟首页</Link>
        </StatePanel>
      </AppFrame>
    );
  }

  if (model.status === "member-home") {
    return (
      <AppFrame title="俱乐部联盟" backAction={backAction} actions={model.actions}>
        <MemberHomeShell model={model.memberHome} />
      </AppFrame>
    );
  }

  const selectedActionId = model.status === "focused" ? model.selected.action_id : null;
  return (
    <AppFrame title="俱乐部联盟" backAction={backAction} actions={model.actions}>
      <main className="club-alliance-page" data-page-state={model.status}>
        <header className="club-alliance-intro">
          <p className="section-kicker">标准服务首页</p>
          <h2>{model.status === "focused" ? model.selected.label : "选择俱乐部服务"}</h2>
          <p>
            {model.status === "focused"
              ? "该入口已由标准目录唯一定位；具体业务将在对应子项目通过门禁后开放。"
              : "四类入口均来自服务广场标准动作目录，展示顺序、权限和状态保持一致。"}
          </p>
          {selectedActionId && <code>selected_action_id={selectedActionId}</code>}
          {selectedActionId === selfCreatedClubActionId && (
            <Link className="club-alliance-return" to={selfCreatedClubRootRoute}>
              进入自建俱乐部
            </Link>
          )}
          {selectedActionId === "public-benefit-club" && (
            <p>公益俱乐部采用申请创办制，不提供普通直接创建入口。</p>
          )}
        </header>

        <section className="club-alliance-grid" aria-label="俱乐部联盟四类入口">
          {model.categories.map((action) => (
            <ActionControl
              action={action}
              className={action.action_id === selectedActionId ? "selected" : undefined}
              key={action.action_id}
            >
              <span>{action.label}</span>
              <small>{lifecycleLabel[action.lifecycle_status]}</small>
            </ActionControl>
          ))}
        </section>

        <aside className="club-alliance-management" aria-label="俱乐部联盟管理附属入口">
          <div>
            <strong>管理中心</strong>
            <p>管理入口不属于第五类俱乐部，仅向具备平台权限的用户开放。</p>
          </div>
          <ActionControl action={model.management} />
        </aside>

        {selectedActionId === "public-benefit-club" && (
          <PublicWelfareRegionalPanel mode="public-welfare" />
        )}
        {selectedActionId === "club-federation" && (
          <PublicWelfareRegionalPanel mode="regional-public" />
        )}
        {selectedActionId === "club-manage" && (
          <PublicWelfareRegionalPanel mode="management" />
        )}

        <Link className="club-alliance-return" to={clubAllianceReturnRoute}>
          ← 返回服务广场
        </Link>
      </main>
    </AppFrame>
  );
}
