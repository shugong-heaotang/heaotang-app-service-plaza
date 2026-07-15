import { useEffect, useReducer, useRef } from "react";
import type { ApiError } from "../../infrastructure/apiClient";
import type {
  ProtectionMallCatalogApi,
  ProtectionMallSceneId,
} from "./protectionMallApi";
import type { ProtectionMallCatalogEntry } from "./protectionMallContract";

export type ProtectionMallCatalogState =
  | { status: "loading" }
  | { status: "empty" }
  | { status: "ready"; items: ProtectionMallCatalogEntry[] }
  | { status: "error"; error: unknown };

type StateAction =
  | { type: "loading" }
  | { type: "resolved"; items: ProtectionMallCatalogEntry[] }
  | { type: "rejected"; error: unknown };

function reducer(
  _state: ProtectionMallCatalogState,
  action: StateAction,
): ProtectionMallCatalogState {
  if (action.type === "loading") return { status: "loading" };
  if (action.type === "rejected") return { status: "error", error: action.error };
  return action.items.length === 0
    ? { status: "empty" }
    : { status: "ready", items: action.items };
}

export type ProtectionMallCatalogController = {
  state: ProtectionMallCatalogState;
  retry(): void;
};

export function useProtectionMallCatalog(
  api: ProtectionMallCatalogApi,
  sceneId: ProtectionMallSceneId,
  enabled = true,
): ProtectionMallCatalogController {
  const [state, dispatch] = useReducer(reducer, { status: "loading" });
  const currentRequest = useRef(0);
  const [refreshToken, forceRefresh] = useReducer((value: number) => value + 1, 0);

  useEffect(() => {
    if (!enabled) return;

    const requestId = ++currentRequest.current;
    const controller = new AbortController();
    dispatch({ type: "loading" });

    void api.loadCatalog({ sceneId }, { signal: controller.signal }).then(
      ({ items }) => {
        if (!controller.signal.aborted && requestId === currentRequest.current) {
          dispatch({ type: "resolved", items });
        }
      },
      (error: unknown) => {
        if (!controller.signal.aborted && requestId === currentRequest.current) {
          dispatch({ type: "rejected", error });
        }
      },
    );

    return () => controller.abort();
  }, [api, enabled, refreshToken, sceneId]);

  return {
    state,
    retry() {
      if (state.status === "loading") return;
      forceRefresh();
    },
  };
}

export function catalogRequestId(error: unknown): string | undefined {
  return (error as Partial<ApiError> | null)?.requestId;
}
