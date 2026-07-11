import { useCallback, useEffect, useMemo, useState } from "react";
import { ActionControl } from "../components/ActionControl";
import { AppFrame } from "../components/AppFrame";
import {
  servicePlazaActionIds,
  type ServiceAction,
  type ServiceActionCatalog,
} from "../domain/serviceActions";
import type { ServiceCatalog } from "../domain/serviceCatalog";
import {
  serviceCatalogRepository,
  type ServiceCatalogRepository,
} from "../infrastructure/serviceCatalogRepository";
import { deriveClubAllianceActions } from "../modules/club-alliance/clubAllianceActionAdapter";

const iconClassByService: Record<string, string> = {
  "activity-plaza": "activity",
  "network-center": "network",
  "protection-mall": "mall",
  "secondhand-market": "market",
  "ai-assistant": "ai",
  "learning-plaza": "study",
};

const requireAction = (actions: readonly ServiceAction[], actionId: string) => {
  const action = actions.find((candidate) => candidate.action_id === actionId);
  if (!action) throw new Error(`标准动作目录缺少动作：${actionId}`);
  return action;
};

const validatePlazaActions = (
  catalog: ServiceCatalog,
  actionCatalog: ServiceActionCatalog,
) => {
  if (actionCatalog.count !== servicePlazaActionIds.length) {
    throw new Error(`服务广场当前版必须提供 ${servicePlazaActionIds.length} 项标准动作`);
  }
  servicePlazaActionIds.forEach((actionId) => requireAction(actionCatalog.items, actionId));
  const serviceIds = new Set(catalog.items.map((service) => service.service_id));
  const unknownServiceAction = actionCatalog.items.find(
    (action) => action.service_id && !serviceIds.has(action.service_id),
  );
  if (unknownServiceAction) {
    throw new Error(`动作引用了目录中不存在的服务：${unknownServiceAction.service_id}`);
  }
  deriveClubAllianceActions(actionCatalog.items);
  return actionCatalog.items;
};

const lifecycleText = (action: ServiceAction) => {
  if (action.lifecycle_status === "planned") return "规划中";
  if (action.lifecycle_status === "maintenance") return "维护中";
  if (action.lifecycle_status === "offline") return "已下线";
  return "";
};

type ServicePlazaPageProps = {
  repository?: ServiceCatalogRepository;
};

export function ServicePlazaPage({
  repository = serviceCatalogRepository,
}: ServicePlazaPageProps) {
  const [catalog, setCatalog] = useState<ServiceCatalog | null>(null);
  const [actions, setActions] = useState<readonly ServiceAction[] | null>(null);
  const [error, setError] = useState("");

  const loadCatalog = useCallback(async () => {
    setError("");
    try {
      const [loadedCatalog, loadedActions] = await Promise.all([
        repository.getCatalog(),
        repository.getActions(),
      ]);
      const validatedActions = validatePlazaActions(loadedCatalog, loadedActions);
      setCatalog(loadedCatalog);
      setActions(validatedActions);
    } catch (loadError) {
      setCatalog(null);
      setActions(null);
      setError(loadError instanceof Error ? loadError.message : "服务目录加载失败");
    }
  }, [repository]);

  useEffect(() => {
    void loadCatalog();
  }, [loadCatalog]);

  const view = useMemo(() => {
    if (!catalog || !actions) return null;
    const clubAlliance = deriveClubAllianceActions(actions);
    return {
      life: requireAction(actions, "life-navigation"),
      club: requireAction(actions, "club-alliance"),
      health: requireAction(actions, "health-manager"),
      clubManagement: clubAlliance.management,
      clubCategories: clubAlliance.categories,
      more: requireAction(actions, "common-more"),
      common: [
        "activity-plaza",
        "network-center",
        "protection-mall",
        "secondhand-market",
        "ai-assistant",
        "learning-plaza",
      ].map((actionId) => requireAction(actions, actionId)),
    };
  }, [actions, catalog]);

  if (error) {
    return (
      <AppFrame actions={[]}>
        <section className="catalog-state" role="alert">
          <strong>服务目录暂时不可用</strong>
          <span>{error}</span>
          <button type="button" onClick={() => void loadCatalog()}>重新加载</button>
        </section>
      </AppFrame>
    );
  }

  if (!view || !actions) {
    return (
      <AppFrame actions={[]}>
        <section className="catalog-state" aria-live="polite">
          正在加载标准服务与动作目录…
        </section>
      </AppFrame>
    );
  }

  return (
    <AppFrame actions={actions}>
      <ActionControl className="hero-entry life-entry" action={view.life}>
        <span className="entry-icon life-mark" aria-hidden="true">导</span>
        <span className="entry-copy">
          <span className="section-kicker">核心服务</span>
          <strong>{view.life.label}</strong>
        </span>
        <span className="entry-action">进入</span>
      </ActionControl>

      <article className="club-panel">
        <div className="club-main-row">
          <ActionControl className="club-main-button" action={view.club} />
          <ActionControl className="club-manage-button" action={view.clubManagement} />
        </div>
        <div className="club-grid" aria-label="俱乐部联盟体系">
          {view.clubCategories.map((action) => (
            <ActionControl action={action} key={action.action_id} />
          ))}
        </div>
      </article>

      <ActionControl className="hero-entry health-entry" action={view.health}>
        <span className="entry-icon health-mark health-word" aria-hidden="true">健康</span>
        <span className="entry-copy">
          <span className="section-kicker">核心服务</span>
          <strong>{view.health.label}</strong>
        </span>
        <span className="entry-action">进入</span>
      </ActionControl>

      <section className="services-panel" aria-labelledby="service-tools-title">
        <div className="panel-heading">
          <h2 id="service-tools-title">常用服务</h2>
          <ActionControl className="more-button" action={view.more} />
        </div>
        <div className="service-grid">
          {view.common.map((action) => {
            const icon = iconClassByService[action.service_id ?? ""] ?? "service";
            return (
              <ActionControl className="service-tile" action={action} key={action.action_id}>
                <span className={`tile-icon ${icon}-icon`} aria-hidden="true">
                  {icon === "ai" ? "AI" : ""}
                </span>
                <strong>{action.label}</strong>
                {lifecycleText(action) && <small>{lifecycleText(action)}</small>}
              </ActionControl>
            );
          })}
        </div>
      </section>
    </AppFrame>
  );
}
