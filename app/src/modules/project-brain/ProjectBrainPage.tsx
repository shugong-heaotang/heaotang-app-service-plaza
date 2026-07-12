import { useEffect, useState } from "react";
import { loadProjectBrainSnapshot } from "./projectBrainApi";
import type {
  ProjectBrainDecision,
  ProjectBrainModule,
  ProjectBrainRisk,
  ProjectBrainSnapshot,
  ProjectBrainWorkItem,
} from "./projectBrainTypes";
import "./projectBrain.css";

const labels: Record<string, string> = {
  go: "可以推进",
  "partial-go": "部分可推进",
  "no-go": "暂不可推进",
  unknown: "尚未确认",
  active: "进行中",
  "handoff-ready": "待交接",
  blocked: "已阻塞",
  planned: "已计划",
};

function Source({ path, updatedAt }: { path?: string; updatedAt?: string }) {
  return (
    <small className="project-brain__source">
      来源：{path || "未登记"}{updatedAt ? ` · ${updatedAt}` : ""}
    </small>
  );
}

function WorkCard({ item }: { item: ProjectBrainWorkItem }) {
  return (
    <article className="project-brain__card">
      <span className={`project-brain__pill is-${item.status}`}>{labels[item.status] || item.status}</span>
      <h3>{item.title || item.work_id}</h3>
      <p>{item.next_checkpoint || "尚未登记下一检查点"}</p>
      <Source path={item.handoff_record || item.work_id} />
    </article>
  );
}

function ModuleCard({ item }: { item: ProjectBrainModule }) {
  return (
    <article className="project-brain__card">
      <span className={`project-brain__pill is-${item.status}`}>{labels[item.status] || item.status}</span>
      <h3>{item.name}</h3>
      <p>{item.next_checkpoint}</p>
      <Source path={item.source_path} updatedAt={item.source_updated_at} />
    </article>
  );
}

function DecisionCard({ item }: { item: ProjectBrainDecision }) {
  return (
    <article className="project-brain__card">
      <span className="project-brain__pill is-handoff-ready">待你决定</span>
      <h3>{item.question}</h3><p>{item.recommendation || "尚无建议"}</p>
      <Source path={item.source_path} />
    </article>
  );
}

function RiskCard({ item }: { item: ProjectBrainRisk }) {
  return (
    <article className="project-brain__card">
      <span className={`project-brain__pill is-${item.impact === "critical" ? "blocked" : item.status}`}>
        {item.impact === "critical" ? "重大风险" : item.impact}
      </span>
      <h3>{item.title}</h3><p>{item.mitigation || "尚未登记缓解措施"}</p>
      <Source path={item.source_path} />
    </article>
  );
}

function Empty({ children }: { children: string }) {
  return <div className="project-brain__empty">{children}</div>;
}

export function ProjectBrainPage({ snapshot: supplied }: { snapshot?: ProjectBrainSnapshot }) {
  const [snapshot, setSnapshot] = useState<ProjectBrainSnapshot | undefined>(supplied);
  const [error, setError] = useState<string>();

  useEffect(() => {
    if (supplied) return;
    const controller = new AbortController();
    loadProjectBrainSnapshot(controller.signal).then(setSnapshot).catch((reason: unknown) => {
      if (!controller.signal.aborted) setError(reason instanceof Error ? reason.message : "Project Brain 读取失败");
    });
    return () => controller.abort();
  }, [supplied]);

  if (error) return <main className="project-brain project-brain--state"><h1>项目大脑暂不可用</h1><p>{error}</p><p>当前状态按 Unknown 处理，请检查审计输出。</p></main>;
  if (!snapshot) return <main className="project-brain project-brain--state" aria-busy="true"><h1>正在读取项目事实</h1></main>;

  const summary = snapshot.work_summary;
  return (
    <main className="project-brain">
      <header className="project-brain__hero">
        <span>HEAOTANG PROJECT BRAIN · READ ONLY</span>
        <h1>和奥堂项目大脑</h1>
        <p>看事实、看风险、看下一步。所有结论都能追溯到权威项目文件。</p>
        <strong>{labels[snapshot.overall_verdict] || snapshot.overall_verdict}</strong>
      </header>
      <section className="project-brain__metrics" aria-label="项目状态统计">
        {[["进行中", summary.active], ["待交接", snapshot.acceptance_queue.length], ["审计错误", snapshot.audit_summary.error], ["待你决定", snapshot.pending_decisions.length]].map(([label, value]) => (
          <article key={String(label)}><b>{value || 0}</b><span>{label}</span></article>
        ))}
      </section>
      <div className="project-brain__layout">
        <div>
          <section className="project-brain__panel"><h2>正在推进</h2><div className="project-brain__cards">{snapshot.active_work.length ? snapshot.active_work.map(item => <WorkCard key={item.work_id} item={item} />) : <Empty>当前没有活动工作项</Empty>}</div></section>
          <section className="project-brain__panel"><h2>模块全景</h2><div className="project-brain__cards">{snapshot.modules.length ? snapshot.modules.map(item => <ModuleCard key={item.module_id} item={item} />) : <Empty>模块权威登记尚未建立</Empty>}</div></section>
          <section className="project-brain__panel"><h2>待独立验收</h2><div className="project-brain__cards">{snapshot.acceptance_queue.length ? snapshot.acceptance_queue.map(item => <WorkCard key={item.work_id} item={item} />) : <Empty>当前没有待独立验收事项</Empty>}</div></section>
        </div>
        <aside>
          <section className="project-brain__panel"><h2>待你决定</h2><div className="project-brain__cards">{snapshot.pending_decisions.length ? snapshot.pending_decisions.map(item => <DecisionCard key={item.decision_id} item={item} />) : <Empty>当前没有登记待决定事项</Empty>}</div></section>
          <section className="project-brain__panel"><h2>风险</h2><div className="project-brain__cards">{snapshot.risks.length ? snapshot.risks.map(item => <RiskCard key={item.risk_id} item={item} />) : <Empty>风险权威登记尚未建立</Empty>}</div></section>
        </aside>
      </div>
      <footer>数据生成时间：{snapshot.generated_at} · 来源提交：{snapshot.source_commit} · 新鲜度：{snapshot.source_freshness === "current" ? "当前" : "未知"} · 此页面不提供修改或审批操作</footer>
    </main>
  );
}
