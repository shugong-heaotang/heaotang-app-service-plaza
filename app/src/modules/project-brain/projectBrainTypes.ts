export type ProjectBrainVerdict = "go" | "partial-go" | "no-go" | "unknown";

export interface ProjectBrainWorkItem {
  work_id: string;
  title?: string;
  owner_role?: string;
  status: string;
  next_checkpoint?: string;
  handoff_record?: string;
}

export interface ProjectBrainModule {
  module_id: string;
  name: string;
  status: string;
  development_status?: string;
  acceptance_status?: string;
  next_checkpoint: string;
  source_path: string;
  source_updated_at: string;
}

export interface ProjectBrainDecision {
  decision_id: string;
  question: string;
  status: string;
  recommendation?: string;
  source_path: string;
}

export interface ProjectBrainRisk {
  risk_id: string;
  title: string;
  status: string;
  impact: string;
  mitigation?: string;
  source_path: string;
}

export interface ProjectBrainSnapshot {
  contract_version: "project-brain.snapshot.v1";
  generated_at: string;
  source_commit: string;
  source_freshness: "current" | "unknown";
  overall_verdict: ProjectBrainVerdict;
  modules: ProjectBrainModule[];
  work_summary: Record<string, number>;
  active_work: ProjectBrainWorkItem[];
  pending_decisions: ProjectBrainDecision[];
  risks: ProjectBrainRisk[];
  acceptance_queue: ProjectBrainWorkItem[];
  recent_integrations: ProjectBrainWorkItem[];
  audit_summary: Record<string, number>;
}
