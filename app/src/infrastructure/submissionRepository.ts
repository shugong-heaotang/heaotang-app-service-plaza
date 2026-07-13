import type { ServiceKey } from "../domain/services";
import {
  createBusinessApiAdapter,
  defineBusinessRead,
  defineBusinessWrite,
} from "./businessApiAdapter";

export type Submission = {
  id: string;
  service: ServiceKey;
  status: "pending";
  createdAt: string;
};

export interface SubmissionRepository {
  submit(service: ServiceKey, input?: SubmissionInput): Promise<Submission>;
}

export type SubmissionInput = {
  note?: string;
  clubId?: number;
  patientName?: string;
  symptoms?: string;
};

const delay = (milliseconds: number) =>
  new Promise<void>((resolve) => window.setTimeout(resolve, milliseconds));

export const mockSubmissionRepository: SubmissionRepository = {
  async submit(service) {
    await delay(180);
    return {
      id: `${service}-${Date.now()}`,
      service,
      status: "pending",
      createdAt: new Date().toISOString(),
    };
  },
};

type ClubListResponse = {
  items: Array<{ id: number; name: string; category?: string; type?: string }>;
};

type ClubJoinResponse = {
  status: string;
  application: { id: number; status: string };
};

type WriteResponse = { id?: number; status?: string };

const lifeNavigationApi = createBusinessApiAdapter("life-navigation");
const clubAllianceApi = createBusinessApiAdapter("club-alliance");
const healthManagerApi = createBusinessApiAdapter("health-manager");

const createLifeNavigationRecord = defineBusinessWrite<SubmissionInput, WriteResponse>({
  operationId: "create-record",
  method: "POST",
  path: () => "/api/v1/life-nav/records",
  body: (input) => ({
    dimension_id: "yun",
    record_type: "application",
    title: "服务广场导航申请",
    note: input.note?.trim() || "申请生命导航服务",
  }),
});

const joinClub = defineBusinessWrite<SubmissionInput & { clubId: number }, ClubJoinResponse>({
  operationId: "join-club",
  method: "POST",
  path: (input) => `/api/v1/clubs/${input.clubId}/join`,
  body: (input) => ({ message: input.note?.trim() || "申请加入俱乐部" }),
});

const createHealthConsultation = defineBusinessWrite<SubmissionInput, WriteResponse>({
  operationId: "create-consultation",
  method: "POST",
  path: () => "/api/v1/health/consultations",
  body: (input) => ({
    patient_name: input.patientName!.trim(),
    symptoms: input.symptoms?.trim() ?? "",
  }),
});

const listClubs = defineBusinessRead<void, ClubListResponse>({
  operationId: "list-clubs",
  path: () => "/api/v1/clubs",
});

export const realSubmissionRepository: SubmissionRepository = {
  async submit(service, input = {}) {
    let result: { id?: number; status?: string } = {};

    if (service === "life-navigation") {
      result = await lifeNavigationApi.execute(createLifeNavigationRecord, input);
    }

    if (service === "club-alliance") {
      if (!input.clubId) throw new Error("请选择要申请加入的俱乐部");
      const clubResult = await clubAllianceApi.execute(joinClub, {
        ...input,
        clubId: input.clubId,
      });
      result = { id: clubResult.application.id, status: clubResult.status };
    }

    if (service === "health-manager") {
      if (!input.patientName?.trim()) throw new Error("请填写咨询人姓名");
      result = await healthManagerApi.execute(createHealthConsultation, input);
    }

    return {
      id: String(result.id ?? `${service}-${Date.now()}`),
      service,
      status: "pending",
      createdAt: new Date().toISOString(),
    };
  },
};

export const isRealSubmissionMode =
  import.meta.env.MODE !== "test" && import.meta.env.VITE_SUBMISSION_MODE !== "mock";

export const submissionRepository = isRealSubmissionMode
  ? realSubmissionRepository
  : mockSubmissionRepository;

export async function listAvailableClubs() {
  const result = await clubAllianceApi.execute(listClubs, undefined);
  return result.items ?? [];
}
