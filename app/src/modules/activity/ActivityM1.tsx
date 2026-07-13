import type { ReactNode } from "react";
import { activityM1ContractVersion, type ActivityM1Model, type RegistrationStatus } from "./activityModels";
import "./ActivityM1.css";

const registrationLabels: Record<RegistrationStatus, string> = {
  available: "可免费报名",
  registered: "已报名",
  full: "名额已满",
  ineligible: "暂不符合资格",
};

const proposalLabels = {
  club_review: "俱乐部审核中",
  changes_requested: "待修改",
  approved: "俱乐部已批准",
  rejected: "未通过",
} as const;

const State = ({ state, title, children }: { state: ActivityM1Model["state"]; title: string; children: ReactNode }) => (
  <section data-activity-state={state} role={state === "error" ? "alert" : "status"}>
    <h2>{title}</h2>
    {children}
  </section>
);

export type ActivityM1Props = {
  model: ActivityM1Model;
  onRegister?: (activityId: string) => void;
};

export function ActivityM1({ model, onRegister }: ActivityM1Props) {
  if (model.state === "loading") return <State state="loading" title="正在加载活动"><p>正在读取可公开发现的活动…</p></State>;
  if (model.state === "unauthorized") return <State state="unauthorized" title="登录后查看本人活动"><p>{model.message ?? "请先登录。"}</p></State>;
  if (model.state === "error") return <State state="error" title="活动暂时无法读取"><p>{model.message ?? "请稍后再试。"}</p></State>;

  const activities = model.activities ?? [];
  const proposals = model.proposals ?? [];
  return (
    <main
      className="activity-m1"
      data-activity-state={model.state}
      data-contract-version={activityM1ContractVersion}
      data-execution-mode="mock-only"
    >
      <header className="activity-m1__header">
        <div>
          <p>活动板块 V3.0 · M1</p>
          <h1>发现活动与我的进度</h1>
        </div>
        <span>非生产合成资料</span>
      </header>

      <section aria-labelledby="activity-public-heading">
        <h2 id="activity-public-heading">公开活动</h2>
        {activities.length === 0 ? <p>当前没有可公开发现的活动。</p> : (
          <div className="activity-m1__grid">
            {activities.map((activity) => (
              <article key={activity.activityId} data-activity-id={activity.activityId}>
                <p>{activity.clubName}</p>
                <h3>{activity.title}</h3>
                <p>{activity.summary}</p>
                <dl>
                  <div><dt>时间</dt><dd>{activity.startsAt}</dd></div>
                  <div><dt>地点</dt><dd>{activity.locationLabel}</dd></div>
                  <div><dt>剩余名额</dt><dd>{activity.remainingCapacity}</dd></div>
                </dl>
                <p className="activity-m1__status">{registrationLabels[activity.registrationStatus]}</p>
                <div className="activity-m1__actions">
                  <a href={activity.detailTarget}>查看详情</a>
                  {activity.registrationStatus === "available" && onRegister ? (
                    <button type="button" onClick={() => onRegister(activity.activityId)}>确认免费报名</button>
                  ) : null}
                </div>
              </article>
            ))}
          </div>
        )}
      </section>

      <section aria-labelledby="activity-proposal-heading">
        <h2 id="activity-proposal-heading">我的提案</h2>
        {proposals.length === 0 ? <p>暂无本人提案。</p> : (
          <ul className="activity-m1__proposals">
            {proposals.map((proposal) => (
              <li key={proposal.proposalId}>
                <div><strong>{proposal.title}</strong><span>{proposal.clubName}</span></div>
                <span>{proposalLabels[proposal.status]}</span>
              </li>
            ))}
          </ul>
        )}
        <p className="activity-m1__guard">提案只进入俱乐部待审，提案人不能审批自己的提案。</p>
      </section>

      <aside className="activity-m1__boundary" aria-label="M1 隔离边界">
        本检查点不调用 AI、关系推荐、消息、商城、订单或支付。
      </aside>
    </main>
  );
}
