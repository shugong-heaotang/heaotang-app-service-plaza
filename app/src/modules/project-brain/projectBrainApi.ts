import type { ProjectBrainSnapshot } from "./projectBrainTypes";

// Vite fingerprints and copies the generated read-only snapshot into the build.
// The browser never scans the repository or reads source governance files.
export const PROJECT_BRAIN_SNAPSHOT_URL = "/project-brain/project-brain.snapshot.json";

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
  const data: unknown = await response.json();
  if (
    !data ||
    typeof data !== "object" ||
    !("contract_version" in data) ||
    data.contract_version !== "project-brain.snapshot.v1"
  ) {
    throw new Error("Project Brain 快照版本无效");
  }
  return data as ProjectBrainSnapshot;
}
