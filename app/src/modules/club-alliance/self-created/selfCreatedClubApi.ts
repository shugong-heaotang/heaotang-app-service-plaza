import { ApiError, type ApiResponseMetadata } from "../../../infrastructure/apiClient";
import {
  createBusinessApiAdapter,
  defineBusinessRead,
  defineBusinessWrite,
  type BusinessApiExecutionOptions,
} from "../../../infrastructure/businessApiAdapter";
import {
  selfCreatedClubCategory,
  selfCreatedClubMaximumPageSize,
  selfCreatedClubPageSize,
  selfCreatedClubStatus,
  selfCreatedClubType,
} from "./selfCreatedClubContract";

export type SelfCreatedClubSummaryDto = {
  id: number;
  name: string;
  intro: string;
  city: string;
  type: string;
  category: string;
  status: string;
};

export type SelfCreatedClubDetailDto = SelfCreatedClubSummaryDto & {
  member_count: number;
  created_at: string;
};

export type SelfCreatedClubApplicationDto = {
  id: number;
  club_id: number;
  message?: string;
  status: "pending" | "approved" | "rejected";
  review_note?: string;
  created_at: string;
  reviewed_at?: string;
};

export type SelfCreatedClubListResponse = {
  items: SelfCreatedClubSummaryDto[];
  total: number;
  page: number;
  size: number;
};

export type SelfCreatedClubApplicationsResponse = {
  items: SelfCreatedClubApplicationDto[];
  total: number;
  page: number;
  size: number;
};

type JoinResponse = {
  status: string;
  application: SelfCreatedClubApplicationDto;
};

export type SelfCreatedClubSummary = {
  id: number;
  name: string;
  intro: string;
  city: string;
};

export type SelfCreatedClubDetail = SelfCreatedClubSummary & {
  memberCount: number;
  createdAt: string;
};

export type SelfCreatedClubApplication = {
  id: number;
  clubId: number;
  message: string;
  status: "pending" | "approved" | "rejected";
  reviewNote: string;
  createdAt: string;
  reviewedAt?: string;
};

export type Paginated<T> = {
  items: T[];
  total: number;
  page: number;
  size: number;
};

export type SelfCreatedClubSearchInput = {
  page?: number;
  size?: number;
  query?: string;
  city?: string;
};

export type SelfCreatedClubApplicationStatus =
  SelfCreatedClubApplication["status"];

export type SelfCreatedClubApplicationsInput = {
  page?: number;
  size?: number;
  status?: SelfCreatedClubApplicationStatus | "";
};

export type SelfCreatedClubJoinResult = {
  status: "created" | "replayed";
  application: SelfCreatedClubApplication;
  meta: ApiResponseMetadata;
};

export type SelfCreatedClubApi = {
  search(
    input?: SelfCreatedClubSearchInput,
    options?: BusinessApiExecutionOptions,
  ): Promise<Paginated<SelfCreatedClubSummary>>;
  detail(
    clubId: number,
    options?: BusinessApiExecutionOptions,
  ): Promise<SelfCreatedClubDetail>;
  join(
    clubId: number,
    message: string,
    options: BusinessApiExecutionOptions & { idempotencyKey: string },
  ): Promise<SelfCreatedClubJoinResult>;
  myApplications(
    input?: SelfCreatedClubApplicationsInput,
    options?: BusinessApiExecutionOptions,
  ): Promise<Paginated<SelfCreatedClubApplication>>;
};

const api = createBusinessApiAdapter("club-alliance");

const positiveInteger = (value: number | undefined, fallback: number, maximum?: number) => {
  const resolved = value ?? fallback;
  if (
    !Number.isSafeInteger(resolved) ||
    resolved < 1 ||
    (maximum !== undefined && resolved > maximum)
  ) {
    throw new ApiError("分页参数无效", 0, "INVALID_PAGINATION");
  }
  return resolved;
};

const requireClubId = (clubId: number) => {
  if (!Number.isSafeInteger(clubId) || clubId < 1) {
    throw new ApiError("俱乐部编号无效", 0, "CLUB_ID_INVALID");
  }
  return clubId;
};

const searchPath = (input: SelfCreatedClubSearchInput = {}) => {
  const page = positiveInteger(input.page, 1);
  const size = positiveInteger(
    input.size,
    selfCreatedClubPageSize,
    selfCreatedClubMaximumPageSize,
  );
  const params = new URLSearchParams({
    type: selfCreatedClubType,
    category: selfCreatedClubCategory,
    page: String(page),
    size: String(size),
  });
  const query = input.query?.trim();
  const city = input.city?.trim();
  if (query) params.set("q", query);
  if (city) params.set("city", city);
  return `/api/v1/clubs/search?${params.toString()}`;
};

const applicationsPath = (input: SelfCreatedClubApplicationsInput = {}) => {
  const page = positiveInteger(input.page, 1);
  const size = positiveInteger(
    input.size,
    selfCreatedClubPageSize,
    selfCreatedClubMaximumPageSize,
  );
  const params = new URLSearchParams({ page: String(page), size: String(size) });
  if (input.status) params.set("status", input.status);
  return `/api/v1/clubs/join-applications/my?${params.toString()}`;
};

const searchOperation = defineBusinessRead<
  SelfCreatedClubSearchInput,
  SelfCreatedClubListResponse
>({
  operationId: "search-self-created-clubs",
  path: searchPath,
});

const detailOperation = defineBusinessRead<{ clubId: number }, SelfCreatedClubDetailDto>({
  operationId: "get-self-created-club",
  path: ({ clubId }) => `/api/v1/clubs/self-created/${requireClubId(clubId)}`,
});

const joinOperation = defineBusinessWrite<
  { clubId: number; message: string },
  JoinResponse
>({
  operationId: "join-self-created-club",
  method: "POST",
  path: ({ clubId }) => `/api/v1/clubs/${requireClubId(clubId)}/join`,
  body: ({ message }) => ({ message: message.trim() }),
});

const myApplicationsOperation = defineBusinessRead<
  SelfCreatedClubApplicationsInput,
  SelfCreatedClubApplicationsResponse
>({
  operationId: "list-my-club-applications",
  path: applicationsPath,
});

const requireSelfCreatedClub = (club: SelfCreatedClubSummaryDto) => {
  if (
    club.type !== selfCreatedClubType ||
    club.category !== selfCreatedClubCategory ||
    club.status !== selfCreatedClubStatus
  ) {
    throw new ApiError(
      "自建俱乐部数据边界不一致",
      500,
      "CLUB_CATEGORY_CROSSOVER_DETECTED",
    );
  }
};

const mapSummary = (club: SelfCreatedClubSummaryDto): SelfCreatedClubSummary => {
  requireSelfCreatedClub(club);
  return {
    id: club.id,
    name: club.name,
    intro: club.intro,
    city: club.city,
  };
};

const mapDetail = (club: SelfCreatedClubDetailDto): SelfCreatedClubDetail => {
  requireSelfCreatedClub(club);
  return {
    ...mapSummary(club),
    memberCount: club.member_count,
    createdAt: club.created_at,
  };
};

const mapApplication = (
  application: SelfCreatedClubApplicationDto,
): SelfCreatedClubApplication => ({
  id: application.id,
  clubId: application.club_id,
  message: application.message ?? "",
  status: application.status,
  reviewNote: application.review_note ?? "",
  createdAt: application.created_at,
  reviewedAt: application.reviewed_at,
});

export const selfCreatedClubApi: SelfCreatedClubApi = {
  async search(input = {}, options = {}) {
    const result = await api.execute(searchOperation, input, options);
    return {
      items: result.items.map(mapSummary),
      total: result.total,
      page: result.page,
      size: result.size,
    };
  },
  async detail(clubId, options = {}) {
    const result = await api.execute(detailOperation, { clubId }, options);
    return mapDetail(result);
  },
  async join(clubId, message, options) {
    const response = await api.executeWithMeta(
      joinOperation,
      { clubId, message },
      options,
    );
    return {
      status: response.meta.idempotencyReplayed ? "replayed" : "created",
      application: mapApplication(response.data.application),
      meta: response.meta,
    };
  },
  async myApplications(input = {}, options = {}) {
    const result = await api.execute(myApplicationsOperation, input, options);
    return {
      items: result.items.map(mapApplication),
      total: result.total,
      page: result.page,
      size: result.size,
    };
  },
};
