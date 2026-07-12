import { useCallback, useEffect, useMemo, useState } from "react";
import { useLocation } from "react-router-dom";
import { useActionRuntime } from "../../auth/ActionRuntimeContext";
import type { ServiceAction } from "../../domain/serviceActions";
import { evaluateActionAccess } from "../../infrastructure/actionExecutor";
import { ApiError } from "../../infrastructure/apiClient";
import { serviceCatalogRepository, type ServiceCatalogRepository } from "../../infrastructure/serviceCatalogRepository";
import { deriveClubAllianceActions, resolveClubAllianceQuery } from "./clubAllianceActionAdapter";
import { ClubAllianceHomepageContractError } from "./clubAllianceHomepageContract";
import { ClubAlliancePage, type ClubAlliancePageModel } from "./ClubAlliancePage";
import type { ExploreEntry, MemberHomeModel } from "./member-home";
import { loadMemberHome } from "./member-home/memberHomeApi";

type CatalogState =
  | { status: "loading" }
  | { status: "empty" }
  | { status: "error"; message: string; errorId?: string }
  | { status: "ready"; actions: readonly ServiceAction[] };

export type ClubAllianceRouteProps = {
  repository?: ServiceCatalogRepository;
  memberHomeLoader?: (explore: readonly ExploreEntry[], signal?: AbortSignal) => Promise<MemberHomeModel>;
};

const errorState = (reason: unknown): Extract<CatalogState, { status: "error" }> => {
  if (reason instanceof ClubAllianceHomepageContractError) return { status: "error", message: reason.message, errorId: reason.errorId };
  return { status: "error", message: reason instanceof Error ? reason.message : "俱乐部联盟目录加载失败" };
};

const memberHomeFailure = (reason: unknown): MemberHomeModel => {
  if (reason instanceof ApiError && (reason.status === 401 || reason.code === "AUTH_REQUIRED" || reason.code === "CMH_AUTH_REQUIRED")) return { state: "unauthorized", message: "请先完成登录。" };
  if (reason instanceof ApiError && (reason.status === 410 || reason.code === "CMH_OFFLINE" || reason.code === "FEATURE_DISABLED")) return { state: "offline" };
  if (reason instanceof ApiError && (reason.status === 503 || reason.code === "CMH_MAINTENANCE")) return { state: "maintenance" };
  if (reason instanceof ApiError && (reason.code === "NETWORK_ERROR" || reason.code === "REQUEST_TIMEOUT")) return { state: "offline", message: "网络连接异常，请检查网络后重试。" };
  return { state: "error", message: reason instanceof Error ? reason.message : "无法读取您的俱乐部信息。" };
};

export function ClubAllianceRoute({ repository = serviceCatalogRepository, memberHomeLoader = loadMemberHome }: ClubAllianceRouteProps) {
  const location = useLocation();
  const runtime = useActionRuntime();
  const [requestVersion, setRequestVersion] = useState(0);
  const [catalogState, setCatalogState] = useState<CatalogState>({ status: "loading" });
  const [memberHome, setMemberHome] = useState<MemberHomeModel>({ state: "loading" });
  const retry = useCallback(() => setRequestVersion((current) => current + 1), []);
  const isMemberHome = new URLSearchParams(location.search).size === 0;

  useEffect(() => {
    let active = true;
    setCatalogState({ status: "loading" });
    void Promise.all([repository.getCatalog(), repository.getActions()])
      .then(([catalog, actionCatalog]) => {
        if (!active) return;
        if (!catalog.items.some((manifest) => manifest.service_id === "club-alliance") || actionCatalog.items.length === 0) {
          setCatalogState({ status: "empty" });
          return;
        }
        deriveClubAllianceActions(actionCatalog.items);
        setCatalogState({ status: "ready", actions: actionCatalog.items });
      })
      .catch((reason: unknown) => { if (active) setCatalogState(errorState(reason)); });
    return () => { active = false; };
  }, [repository, requestVersion]);

  useEffect(() => {
    if (!isMemberHome || catalogState.status !== "ready") return;
    let active = true;
    const controller = new AbortController();
    try {
      const view = deriveClubAllianceActions(catalogState.actions);
      const explore = view.categories.map((action) => ({ actionId: action.action_id, label: action.label, href: action.target }));
      if (!runtime.session.authenticated) {
        setMemberHome({ state: "unauthorized", message: "请先完成登录。", explore });
        return () => controller.abort();
      }
      setMemberHome({ state: "loading", explore });
      void memberHomeLoader(explore, controller.signal)
        .then((model) => { if (active) setMemberHome(model); })
        .catch((reason: unknown) => { if (active && !controller.signal.aborted) setMemberHome({ ...memberHomeFailure(reason), explore }); });
    } catch (reason) {
      setMemberHome(memberHomeFailure(reason));
    }
    return () => { active = false; controller.abort(); };
  }, [catalogState, isMemberHome, memberHomeLoader, requestVersion, runtime.session.authenticated]);

  const model = useMemo<ClubAlliancePageModel>(() => {
    if (catalogState.status !== "ready") return catalogState;
    try {
      const view = deriveClubAllianceActions(catalogState.actions);
      if (isMemberHome) return { status: "member-home", actions: catalogState.actions, memberHome };
      const selection = resolveClubAllianceQuery(location.search, view.categories, view.management);
      if (selection.mode === "home") return { status: "home", actions: catalogState.actions, categories: view.categories, management: view.management };
      const selected = selection.selected_action_id === view.management.action_id
        ? view.management
        : view.categories.find((action) => action.action_id === selection.selected_action_id);
      if (!selected) throw new ClubAllianceHomepageContractError("CAH1_ACTION_MISSING", `俱乐部联盟动作目录缺少 ${selection.selected_action_id}`);
      if (selected.lifecycle_status === "maintenance") return { status: "maintenance", actions: catalogState.actions, selected };
      if (selected.lifecycle_status === "offline") return { status: "offline", actions: catalogState.actions, selected };
      const access = evaluateActionAccess(selected, runtime.session);
      if (!access.allowed) return { status: "unauthorized", actions: catalogState.actions, selected, reason: access.reason, missingScopes: access.missingScopes ?? [] };
      return { status: "focused", actions: catalogState.actions, categories: view.categories, management: view.management, selected };
    } catch (reason) {
      return errorState(reason);
    }
  }, [catalogState, isMemberHome, location.search, memberHome, runtime.session]);

  return <ClubAlliancePage model={model} onRetry={retry} />;
}
