import { useEffect, useMemo, useState, type ReactNode } from "react";
import { actionsInRegion, type ServiceAction } from "../domain/serviceActions";
import { useOptionalAuth } from "../auth/AuthContext";
import { serviceCatalogRepository } from "../infrastructure/serviceCatalogRepository";
import { ActionControl } from "./ActionControl";

type AppFrameProps = {
  children: ReactNode;
  title?: string;
  backAction?: ReactNode;
  actions?: readonly ServiceAction[];
};

const tabIconClass: Record<string, string> = {
  "primary-home": "home-icon",
  "primary-services": "service-icon",
  "primary-discover": "discover-icon",
  "primary-profile": "mine-icon",
};

export function AppFrame({ children, title = "服务广场", backAction, actions }: AppFrameProps) {
  const auth = useOptionalAuth();
  const [loadedActions, setLoadedActions] = useState<readonly ServiceAction[]>([]);
  const [actionError, setActionError] = useState("");

  useEffect(() => {
    if (actions) return;
    let active = true;
    void serviceCatalogRepository
      .getActions()
      .then((catalog) => {
        if (active) setLoadedActions(catalog.items);
      })
      .catch(() => {
        if (active) setActionError("导航动作加载失败");
      });
    return () => {
      active = false;
    };
  }, [actions]);

  const frameActions = actions ?? loadedActions;
  const topAiAction = useMemo(
    () => actionsInRegion(frameActions, "topbar")[0],
    [frameActions],
  );
  const tabActions = useMemo(
    () => actionsInRegion(frameActions, "primary_navigation"),
    [frameActions],
  );

  return (
    <main className="app-shell">
      <section className="phone" aria-label={`和奥堂${title}`}>
        <header className="topbar">
          <div className="brand-title">
            {backAction ?? (
              <img
                className="brand-mark"
                src={`${import.meta.env.BASE_URL}heaotang-logo.svg`}
                alt="和奥堂商标"
              />
            )}
            <h1>{title}</h1>
          </div>
          {topAiAction && (
            <ActionControl className="ai-button" action={topAiAction}>
              AI
            </ActionControl>
          )}
        </header>

        <section className="content">
          {auth?.isAuthenticated && auth.user && (
            <div className="session-bar" aria-label="当前登录账号">
              <span>当前用户：{auth.user.nickname || auth.user.phone || `#${auth.user.id}`}</span>
              <button type="button" onClick={auth.logout}>退出登录</button>
            </div>
          )}
          {children}
        </section>

        <nav className="tabbar" aria-label="主导航">
          {actionError && <span role="status">{actionError}</span>}
          {tabActions.map((action) => (
            <ActionControl action={action} key={action.action_id} nav>
              <span
                className={`tab-icon ${tabIconClass[action.action_id] ?? ""}`}
                aria-hidden="true"
              />
              {action.label}
            </ActionControl>
          ))}
        </nav>
      </section>
    </main>
  );
}
