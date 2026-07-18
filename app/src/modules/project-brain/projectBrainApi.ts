import type { ProjectBrainSnapshot } from "./projectBrainTypes";

// Vite fingerprints and copies the generated read-only snapshot into the build.
// The browser never scans the repository or reads source governance files.
export const PROJECT_BRAIN_SNAPSHOT_URL = "/project-brain/project-brain.snapshot.json";

const isRecord = (value: unknown): value is Record<string, unknown> =>
  Boolean(value) && typeof value === "object" && !Array.isArray(value);

const isString = (value: unknown): value is string => typeof value === "string";
const isOptionalString = (value: unknown): value is string | undefined =>
  value === undefined || isString(value);
const isCountSummary = (value: unknown): value is Record<string, number> =>
  isRecord(value) && Object.values(value).every(
    item => typeof item === "number" && Number.isInteger(item) && item >= 0,
  );

const isWorkItem = (value: unknown): boolean =>
  isRecord(value) &&
  isString(value.work_id) &&
  isString(value.status) &&
  isOptionalString(value.title) &&
  isOptionalString(value.owner_role) &&
  isOptionalString(value.next_checkpoint) &&
  isOptionalString(value.handoff_record);

const isModule = (value: unknown): boolean =>
  isRecord(value) &&
  isString(value.module_id) &&
  isString(value.name) &&
  isString(value.status) &&
  isOptionalString(value.development_status) &&
  isOptionalString(value.acceptance_status) &&
  isString(value.next_checkpoint) &&
  isString(value.source_path) &&
  isString(value.source_updated_at);

const isDecision = (value: unknown): boolean =>
  isRecord(value) &&
  isString(value.decision_id) &&
  isString(value.question) &&
  isString(value.status) &&
  isOptionalString(value.recommendation) &&
  isString(value.source_path);

const isRisk = (value: unknown): boolean =>
  isRecord(value) &&
  isString(value.risk_id) &&
  isString(value.title) &&
  isString(value.status) &&
  isString(value.impact) &&
  isOptionalString(value.mitigation) &&
  isString(value.source_path);

const isSnapshot = (value: unknown): value is ProjectBrainSnapshot => {
  if (!isRecord(value)) return false;
  return value.contract_version === "project-brain.snapshot.v1" &&
    typeof value.generated_at === "string" &&
    typeof value.source_commit === "string" &&
    (value.source_freshness === "current" || value.source_freshness === "unknown") &&
    ["go", "partial-go", "no-go", "unknown"].includes(String(value.overall_verdict)) &&
    isCountSummary(value.work_summary) &&
    Array.isArray(value.modules) && value.modules.every(isModule) &&
    Array.isArray(value.active_work) && value.active_work.every(isWorkItem) &&
    Array.isArray(value.pending_decisions) && value.pending_decisions.every(isDecision) &&
    Array.isArray(value.risks) && value.risks.every(isRisk) &&
    Array.isArray(value.acceptance_queue) && value.acceptance_queue.every(isWorkItem) &&
    Array.isArray(value.recent_integrations) && value.recent_integrations.every(isWorkItem) &&
    isCountSummary(value.audit_summary) &&
    !(value.source_freshness === "current" && value.source_commit === "unknown");
};

export async function loadProjectBrainSnapshot(
  signal?: AbortSignal,
): Promise<ProjectBrainSnapshot> {
  const response = await fetch(PROJECT_BRAIN_SNAPSHOT_URL, {
    credentials: "same-origin",
    signal,
  });
  if (!response.ok) {
    throw new Error(`Project Brain 快照读取失败 (${response.status})`);
  }
  const contentType = response.headers.get("Content-Type")?.toLowerCase() ?? "";
  if (!contentType.includes("application/json")) {
    throw new Error("Project Brain 快照格式不可用");
  }
  let data: unknown;
  try {
    data = JSON.parse(await response.text());
  } catch {
    throw new Error("Project Brain 快照格式不可用");
  }
  if (!isSnapshot(data)) {
    throw new Error("Project Brain 快照版本无效");
  }
  return data;
}
