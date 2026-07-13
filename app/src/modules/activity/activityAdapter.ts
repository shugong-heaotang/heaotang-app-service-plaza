import type {
  ActivityM1Model,
  PersonalProposal,
  PublicActivity,
  RegistrationStatus,
} from "./activityModels";

export class ActivityContractError extends Error {
  readonly code = "ACTIVITY_M1_CONTRACT_INVALID";
}

type RecordValue = Record<string, unknown>;

const object = (value: unknown, field: string): RecordValue => {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new ActivityContractError(`${field} 必须是对象`);
  }
  return value as RecordValue;
};

const array = (value: unknown, field: string): unknown[] => {
  if (!Array.isArray(value)) throw new ActivityContractError(`${field} 必须是数组`);
  return value;
};

const text = (value: unknown, field: string): string => {
  if (typeof value !== "string" || !value.trim()) {
    throw new ActivityContractError(`${field} 必须是非空文本`);
  }
  return value;
};

const count = (value: unknown, field: string): number => {
  if (!Number.isInteger(value) || Number(value) < 0) {
    throw new ActivityContractError(`${field} 必须是非负整数`);
  }
  return Number(value);
};

const isoDate = (value: unknown, field: string): string => {
  const result = text(value, field);
  if (Number.isNaN(Date.parse(result))) {
    throw new ActivityContractError(`${field} 必须是有效时间`);
  }
  return result;
};

const detailTarget = (value: unknown): string => {
  const result = text(value, "detail_target");
  if (!/^\/services\/activity\/[A-Za-z0-9_-]+$/.test(result)) {
    throw new ActivityContractError("detail_target 必须是活动内部详情路由");
  }
  return result;
};

const literal = <T extends string>(
  value: unknown,
  field: string,
  allowed: readonly T[],
): T => {
  if (typeof value !== "string" || !allowed.includes(value as T)) {
    throw new ActivityContractError(`${field} 不在允许范围内`);
  }
  return value as T;
};

const exactKeys = (value: RecordValue, field: string, keys: readonly string[]) => {
  const actual = Object.keys(value).sort();
  const expected = [...keys].sort();
  if (actual.length !== expected.length || actual.some((key, index) => key !== expected[index])) {
    throw new ActivityContractError(`${field} 包含缺失或未授权字段`);
  }
};

const registrationStatuses = ["available", "registered", "full", "ineligible"] as const;
const proposalStatuses = ["club_review", "changes_requested", "approved", "rejected"] as const;

const mapActivity = (raw: unknown): PublicActivity => {
  const value = object(raw, "activity");
  exactKeys(value, "activity", [
    "activity_id",
    "title",
    "summary",
    "club_id",
    "club_name",
    "starts_at",
    "location_label",
    "remaining_capacity",
    "registration_status",
    "detail_target",
    "club_approval_status",
    "platform_review_status",
    "lifecycle_status",
    "within_discovery_window",
    "price_minor",
  ]);
  if (
    value.club_approval_status !== "approved" ||
    value.platform_review_status !== "approved" ||
    value.lifecycle_status !== "registration_open" ||
    value.within_discovery_window !== true
  ) {
    throw new ActivityContractError("公开发现只接受已双重审核且仍可发现的活动");
  }
  if (value.price_minor !== 0) {
    throw new ActivityContractError("M1 仅允许免费报名，不接受收费或支付字段");
  }
  const remainingCapacity = count(value.remaining_capacity, "remaining_capacity");
  const registrationStatus = literal<RegistrationStatus>(
    value.registration_status,
    "registration_status",
    registrationStatuses,
  );
  if (
    (registrationStatus === "available" && remainingCapacity === 0) ||
    (registrationStatus === "full" && remainingCapacity !== 0)
  ) {
    throw new ActivityContractError("报名状态与剩余名额不一致");
  }
  return {
    activityId: text(value.activity_id, "activity_id"),
    title: text(value.title, "title"),
    summary: text(value.summary, "summary"),
    clubId: text(value.club_id, "club_id"),
    clubName: text(value.club_name, "club_name"),
    startsAt: isoDate(value.starts_at, "starts_at"),
    locationLabel: text(value.location_label, "location_label"),
    remainingCapacity,
    registrationStatus,
    detailTarget: detailTarget(value.detail_target),
  };
};

const mapProposal = (raw: unknown): PersonalProposal => {
  const value = object(raw, "proposal");
  exactKeys(value, "proposal", [
    "proposal_id",
    "title",
    "club_name",
    "status",
    "proposer_can_approve",
  ]);
  if (value.proposer_can_approve !== false) {
    throw new ActivityContractError("提案人不得成为自己的唯一审批人");
  }
  return {
    proposalId: text(value.proposal_id, "proposal_id"),
    title: text(value.title, "proposal.title"),
    clubName: text(value.club_name, "proposal.club_name"),
    status: literal(value.status, "proposal.status", proposalStatuses),
    proposerCanApprove: false,
  };
};

export function mapActivityM1Payload(raw: unknown): ActivityM1Model {
  const payload = object(raw, "payload");
  exactKeys(payload, "payload", ["activities", "proposals", "execution_mode"]);
  if (payload.execution_mode !== "mock-only") {
    throw new ActivityContractError("M1 前端当前只接受 mock-only 非生产资料");
  }
  const activities = array(payload.activities, "activities").map(mapActivity);
  const proposals = array(payload.proposals, "proposals").map(mapProposal);
  return {
    state: activities.length || proposals.length ? "ready" : "empty",
    activities,
    proposals,
  };
}
