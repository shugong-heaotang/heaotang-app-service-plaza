import { ApiError, type ApiResponseMetadata } from "../../infrastructure/apiClient";
import {
  createBusinessApiAdapter,
  defineBusinessRead,
  defineBusinessWrite,
  type BusinessApiExecutionOptions,
} from "../../infrastructure/businessApiAdapter";
import { lifeNavigationServiceId } from "./lifeNavigationContract";

export const defaultLifeNavigationHistoryLimit = 30;

export type LifeNavigationRecordDto = {
  id: number;
  user_id: number;
  dimension_id: string;
  record_type: string;
  title: string;
  note: string;
  created_at: string;
};

export type LifeNavigationHistoryResponse = {
  items: LifeNavigationRecordDto[];
};

export type LifeNavigationApplicationRecord = {
  id: string;
  dimensionId: string;
  title: string;
  note: string;
  createdAt: string;
  displayStatus: "submitted";
};

export type LifeNavigationHistoryState =
  | { status: "loading" }
  | { status: "empty" }
  | { status: "ready"; items: LifeNavigationApplicationRecord[] }
  | { status: "error"; error: ApiError };

export type LifeNavigationApplicationInput = {
  note?: string;
};

export type LifeNavigationSubmissionResult =
  | {
      status: "created";
      record: LifeNavigationApplicationRecord;
      meta: ApiResponseMetadata;
    }
  | {
      status: "replayed";
      record: LifeNavigationApplicationRecord;
      meta: ApiResponseMetadata;
    };

const lifeNavigationApi = createBusinessApiAdapter(lifeNavigationServiceId);

const listApplicationHistory = defineBusinessRead<
  { limit: number },
  LifeNavigationHistoryResponse
>({
  operationId: "list-application-history",
  path: ({ limit }) => `/api/v1/life-nav/records?limit=${limit}`,
});

const createApplication = defineBusinessWrite<
  LifeNavigationApplicationInput,
  LifeNavigationRecordDto
>({
  operationId: "create-application",
  method: "POST",
  path: () => "/api/v1/life-nav/records",
  body: (input) => ({
    dimension_id: "yun",
    record_type: "application",
    title: "服务广场导航申请",
    note: input.note?.trim() || "申请生命导航服务",
  }),
});

export function resolveLifeNavigationHistoryLimit(limit = defaultLifeNavigationHistoryLimit): number {
  return Number.isInteger(limit) && limit >= 1 && limit <= defaultLifeNavigationHistoryLimit
    ? limit
    : defaultLifeNavigationHistoryLimit;
}

export function mapLifeNavigationApplicationRecord(
  record: LifeNavigationRecordDto,
): LifeNavigationApplicationRecord {
  return {
    id: String(record.id),
    dimensionId: record.dimension_id,
    title: record.title,
    note: record.note,
    createdAt: record.created_at,
    displayStatus: "submitted",
  };
}

export async function fetchLifeNavigationApplicationHistory(
  limit = defaultLifeNavigationHistoryLimit,
  options: BusinessApiExecutionOptions = {},
): Promise<LifeNavigationApplicationRecord[]> {
  const response = await lifeNavigationApi.execute(
    listApplicationHistory,
    { limit: resolveLifeNavigationHistoryLimit(limit) },
    options,
  );

  return (response.items ?? [])
    .filter((record) => record.record_type === "application")
    .map(mapLifeNavigationApplicationRecord);
}

export async function loadLifeNavigationApplicationHistory(
  limit = defaultLifeNavigationHistoryLimit,
  options: BusinessApiExecutionOptions = {},
): Promise<LifeNavigationHistoryState> {
  try {
    const items = await fetchLifeNavigationApplicationHistory(limit, options);
    return items.length === 0 ? { status: "empty" } : { status: "ready", items };
  } catch (reason) {
    if (reason instanceof ApiError) {
      return { status: "error", error: reason };
    }
    throw reason;
  }
}

export async function submitLifeNavigationApplication(
  input: LifeNavigationApplicationInput = {},
  options: BusinessApiExecutionOptions = {},
): Promise<LifeNavigationSubmissionResult> {
  const response = await lifeNavigationApi.executeWithMeta(createApplication, input, options);
  const result = {
    record: mapLifeNavigationApplicationRecord(response.data),
    meta: response.meta,
  };

  return response.meta.idempotencyReplayed
    ? { status: "replayed", ...result }
    : { status: "created", ...result };
}
