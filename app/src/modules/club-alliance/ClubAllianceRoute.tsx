import { useCallback, useEffect, useMemo, useState } from "react";
import { useLocation } from "react-router-dom";
import { useActionRuntime } from "../../auth/ActionRuntimeContext";
import type { ServiceAction } from "../../domain/serviceActions";
import { evaluateActionAccess } from "../../infrastructure/actionExecutor";
import {
  serviceCatalogRepository,
  type ServiceCatalogRepository,
} from "../../infrastructure/serviceCatalogRepository";
import {
  deriveClubAllianceActions,
  resolveClubAllianceQuery,
} from "./clubAllianceActionAdapter";
import { ClubAllianceHomepageContractError } from "./clubAllianceHomepageContract";
import {
  ClubAlliancePage,
  type ClubAlliancePageModel,
} from "./ClubAlliancePage";

type CatalogState =
  | { status: "loading" }
  | { status: "empty" }
  | { status: "error"; message: string; errorId?: string }
  | {
      status: "ready";
      actions: readonly ServiceAction[];
    };

export type ClubAllianceRouteProps = {
  repository?: ServiceCatalogRepository;
};

const errorState = (reason: unknown): Extract<CatalogState, { status: "error" }> => {
  if (reason instanceof ClubAllianceHomepageContractError) {
    return { status: "error", message: reason.message, errorId: reason.errorId };
  }
  return {
    status: "error",
    message: reason instanceof Error ? reason.message : "俱乐部联盟目录加载失败",
  };
};

export function ClubAllianceRoute({
  repository = serviceCatalogRepository,
}: ClubAllianceRouteProps) {
  const location = useLocation();
  const runtime = useActionRuntime();
  const [requestVersion, setRequestVersion] = useState(0);
  const [catalogState, setCatalogState] = useState<CatalogState>({ status: "loading" });

  const retry = useCallback(() => setRequestVersion((current) => current + 1), []);

  useEffect(() => {
    let active = true;
    setCatalogState({ status: "loading" });
    void Promise.all([repository.getCatalog(), repository.getActions()])
      .then(([catalog, actionCatalog]) => {
        if (!active) return;
        const hasClubManifest = catalog.items.some(
          (manifest) => manifest.service_id === "club-alliance",
        );
        if (!hasClubManifest || actionCatalog.items.length === 0) {
          setCatalogState({ status: "empty" });
          return;
        }
        deriveClubAllianceActions(actionCatalog.items);
        setCatalogState({
          status: "ready",
          actions: actionCatalog.items,
        });
      })
      .catch((reason: unknown) => {
        if (active) setCatalogState(errorState(reason));
      });

    return () => {
      active = false;
    };
  }, [repository, requestVersion]);

  const model = useMemo<ClubAlliancePageModel>(() => {
    if (catalogState.status !== "ready") return catalogState;

    try {
      const view = deriveClubAllianceActions(catalogState.actions);
      const selection = resolveClubAllianceQuery(location.search, view.categories);
      if (selection.mode === "home") {
        return {
          status: "home",
          actions: catalogState.actions,
          categories: view.categories,
          management: view.management,
        };
      }

      const selected = view.categories.find(
        (action) => action.action_id === selection.selected_action_id,
      );
      if (!selected) {
        throw new ClubAllianceHomepageContractError(
          "CAH1_ACTION_MISSING",
          `俱乐部联盟动作目录缺少 ${selection.selected_action_id}`,
        );
      }
      if (selected.lifecycle_status === "maintenance") {
        return { status: "maintenance", actions: catalogState.actions, selected };
      }
      if (selected.lifecycle_status === "offline") {
        return { status: "offline", actions: catalogState.actions, selected };
      }

      const access = evaluateActionAccess(selected, runtime.session);
      if (!access.allowed) {
        return {
          status: "unauthorized",
          actions: catalogState.actions,
          selected,
          reason: access.reason,
          missingScopes: access.missingScopes ?? [],
        };
      }

      return {
        status: "focused",
        actions: catalogState.actions,
        categories: view.categories,
        management: view.management,
        selected,
      };
    } catch (reason) {
      return errorState(reason);
    }
  }, [catalogState, location.search, runtime.session]);

  return <ClubAlliancePage model={model} onRetry={retry} />;
}
