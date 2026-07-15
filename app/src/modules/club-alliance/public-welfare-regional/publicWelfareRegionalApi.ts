import { ApiError } from "../../../infrastructure/apiClient";
import {
  createBusinessApiAdapter,
  defineBusinessRead,
  defineBusinessWrite,
  type BusinessApiExecutionOptions,
} from "../../../infrastructure/businessApiAdapter";

export type ApplicationStatus =
  | "draft"
  | "submitted"
  | "under_review"
  | "approved"
  | "rejected"
  | "withdrawn";

export type ReviewDecision = "approved" | "rejected";
export type RegionalRole = "regional_director" | "regional_deputy_director";
export type CenterKind =
  | "regional_management_center"
  | "public_welfare_service_center";

export type PdcarPlan = {
  plan: string;
  do: string;
  check: string;
  act: string;
  record: string;
};

export type PublicWelfareEstablishmentInput = {
  name: string;
  province: string;
  city: string;
  district: string;
  mission: string;
  eligibility: string;
  resources: string;
  governance: string;
  risks: string;
  pdcar: PdcarPlan;
};

export type PublicWelfareEstablishmentApplication =
  PublicWelfareEstablishmentInput & {
    id: number;
    applicant_id: number;
    status: ApplicationStatus;
    review_note: string;
    club_id?: number;
    created_at: string;
    reviewed_at?: string;
  };

export type RegionalRoleApplicationInput = {
  role: RegionalRole;
  province: string;
  city: string;
  district: string;
  experience: string;
  service_plan: string;
  resources: string;
  conflict_statement: string;
};

export type RegionalRoleApplication = RegionalRoleApplicationInput & {
  id: number;
  applicant_id: number;
  status: ApplicationStatus;
  review_note: string;
  created_at: string;
  reviewed_at?: string;
};

export type ServiceCenter = {
  id: number;
  kind: CenterKind;
  name: string;
  province: string;
  city: string;
  district: string;
  address: string;
  contact_name: string;
  contact_phone_masked: string;
  service_hours: string;
};

export type CenterSearchInput = {
  province?: string;
  city?: string;
  district?: string;
  query?: string;
  kind?: CenterKind | "";
};

type ListResponse<T> = { items: T[]; total: number };
type ReviewInput = { applicationId: number; decision: ReviewDecision; note: string };
type ReviewResponse<T> = { application: T };

export type PublicWelfareRegionalApi = {
  submitEstablishment(
    input: PublicWelfareEstablishmentInput,
    options?: BusinessApiExecutionOptions,
  ): Promise<PublicWelfareEstablishmentApplication>;
  listMyEstablishments(options?: BusinessApiExecutionOptions): Promise<PublicWelfareEstablishmentApplication[]>;
  listEstablishments(status?: ApplicationStatus, options?: BusinessApiExecutionOptions): Promise<PublicWelfareEstablishmentApplication[]>;
  reviewEstablishment(input: ReviewInput, options?: BusinessApiExecutionOptions): Promise<PublicWelfareEstablishmentApplication>;
  submitRegionalRole(input: RegionalRoleApplicationInput, options?: BusinessApiExecutionOptions): Promise<RegionalRoleApplication>;
  listMyRegionalRoles(options?: BusinessApiExecutionOptions): Promise<RegionalRoleApplication[]>;
  listRegionalRoles(status?: ApplicationStatus, options?: BusinessApiExecutionOptions): Promise<RegionalRoleApplication[]>;
  reviewRegionalRole(input: ReviewInput, options?: BusinessApiExecutionOptions): Promise<RegionalRoleApplication>;
  searchCenters(input?: CenterSearchInput, options?: BusinessApiExecutionOptions): Promise<ServiceCenter[]>;
};

const api = createBusinessApiAdapter("club-alliance");

const establishmentSubmit = defineBusinessWrite<PublicWelfareEstablishmentInput, { application: PublicWelfareEstablishmentApplication }>({
  operationId: "submit-public-welfare-establishment",
  method: "POST",
  path: () => "/api/v1/clubs/public-welfare-establishment-applications",
  body: (input) => ({ ...input, type: "standard", category: "charity" }),
});
const myEstablishments = defineBusinessRead<Record<string, never>, ListResponse<PublicWelfareEstablishmentApplication>>({
  operationId: "list-my-public-welfare-establishments",
  path: () => "/api/v1/clubs/public-welfare-establishment-applications/my",
});
const establishments = defineBusinessRead<{ status?: ApplicationStatus }, ListResponse<PublicWelfareEstablishmentApplication>>({
  operationId: "list-public-welfare-establishments",
  path: ({ status }) => `/api/v1/clubs/public-welfare-establishment-applications${status ? `?status=${status}` : ""}`,
});
const establishmentReview = defineBusinessWrite<ReviewInput, ReviewResponse<PublicWelfareEstablishmentApplication>>({
  operationId: "review-public-welfare-establishment",
  method: "POST",
  path: ({ applicationId }) => `/api/v1/clubs/public-welfare-establishment-applications/${requireId(applicationId)}/review`,
  body: ({ decision, note }) => ({ decision, note: requiredText(note, "审核意见") }),
});
const regionalRoleSubmit = defineBusinessWrite<RegionalRoleApplicationInput, { application: RegionalRoleApplication }>({
  operationId: "submit-regional-role-application",
  method: "POST",
  path: () => "/api/v1/club-alliance/regional-role-applications",
  body: (input) => input,
});
const myRegionalRoles = defineBusinessRead<Record<string, never>, ListResponse<RegionalRoleApplication>>({
  operationId: "list-my-regional-role-applications",
  path: () => "/api/v1/club-alliance/regional-role-applications/my",
});
const regionalRoles = defineBusinessRead<{ status?: ApplicationStatus }, ListResponse<RegionalRoleApplication>>({
  operationId: "list-regional-role-applications",
  path: ({ status }) => `/api/v1/club-alliance/regional-role-applications${status ? `?status=${status}` : ""}`,
});
const regionalRoleReview = defineBusinessWrite<ReviewInput, ReviewResponse<RegionalRoleApplication>>({
  operationId: "review-regional-role-application",
  method: "POST",
  path: ({ applicationId }) => `/api/v1/club-alliance/regional-role-applications/${requireId(applicationId)}/review`,
  body: ({ decision, note }) => ({ decision, note: requiredText(note, "审核意见") }),
});
const centerSearch = defineBusinessRead<CenterSearchInput, ListResponse<ServiceCenter>>({
  operationId: "search-club-alliance-centers",
  authMode: "anonymous",
  path: (input) => {
    const params = new URLSearchParams();
    Object.entries(input).forEach(([key, value]) => {
      const normalized = value?.trim();
      if (normalized) params.set(key, normalized);
    });
    const query = params.toString();
    return `/api/v1/club-alliance/service-centers${query ? `?${query}` : ""}`;
  },
});

function requireId(value: number) {
  if (!Number.isSafeInteger(value) || value < 1) throw new ApiError("申请编号无效", 0, "APPLICATION_ID_INVALID");
  return value;
}

function requiredText(value: string, label: string) {
  const normalized = value.trim();
  if (!normalized) throw new ApiError(`${label}不能为空`, 0, "REQUIRED_FIELD_MISSING");
  return normalized;
}

export const publicWelfareRegionalApi: PublicWelfareRegionalApi = {
  async submitEstablishment(input, options = {}) {
    const response = await api.execute(establishmentSubmit, input, options);
    return response.application;
  },
  async listMyEstablishments(options = {}) {
    return (await api.execute(myEstablishments, {}, options)).items;
  },
  async listEstablishments(status = "submitted", options = {}) {
    return (await api.execute(establishments, { status }, options)).items;
  },
  async reviewEstablishment(input, options = {}) {
    return (await api.execute(establishmentReview, input, options)).application;
  },
  async submitRegionalRole(input, options = {}) {
    return (await api.execute(regionalRoleSubmit, input, options)).application;
  },
  async listMyRegionalRoles(options = {}) {
    return (await api.execute(myRegionalRoles, {}, options)).items;
  },
  async listRegionalRoles(status = "submitted", options = {}) {
    return (await api.execute(regionalRoles, { status }, options)).items;
  },
  async reviewRegionalRole(input, options = {}) {
    return (await api.execute(regionalRoleReview, input, options)).application;
  },
  async searchCenters(input = {}, options = {}) {
    return (await api.execute(centerSearch, input, options)).items;
  },
};
