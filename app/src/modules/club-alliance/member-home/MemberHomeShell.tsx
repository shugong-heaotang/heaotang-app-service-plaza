import type { ReactNode } from "react";
import "./MemberHomeShell.css";

export type MemberHomeState = "loading" | "ready" | "empty" | "partial-error" | "error" | "unauthorized" | "maintenance" | "offline";
export type MemberClub = {
  clubId: string;
  name: string;
  kind: "公益俱乐部" | "自建俱乐部" | "家庭俱乐部";
  role: string;
  clubStatus: "active";
  membershipStatus: "active" | "suspended";
  href: string;
};
export type MemberTask = { taskId: string; title: string; context: string; href: string };
export type MemberActivity = { activityId: string; title: string; timeLabel: string; href: string };
export type ExploreEntry = { actionId: string; label: string; href: string };
export type MemberHomeModel = {
  state: MemberHomeState; displayName?: string; joinedClubCount?: number; pendingTaskCount?: number; unreadCount?: number;
  clubs?: readonly MemberClub[]; tasks?: readonly MemberTask[]; activities?: readonly MemberActivity[]; feed?: readonly { itemId: string; title: string; href: string }[];
  explore?: readonly ExploreEntry[]; sectionErrors?: Partial<Record<"tasks" | "activities" | "feed", string>>; canManage?: boolean; message?: string;
};

const State = ({ state, title, children }: { state: MemberHomeState; title: string; children: ReactNode }) => (
  <section className="member-home-state" data-member-home-state={state} role={state === "error" ? "alert" : "status"}><h2>{title}</h2>{children}</section>
);
const Section = ({ title, label, children }: { title: string; label: string; children: ReactNode }) => <section className="member-home-section" aria-label={label}><h3>{title}</h3>{children}</section>;
const Empty = ({ children }: { children: ReactNode }) => <p className="member-home-empty">{children}</p>;
const clubStatusLabel: Record<MemberClub["clubStatus"], string> = { active: "俱乐部正常" };
const membershipStatusLabel: Record<MemberClub["membershipStatus"], string> = { active: "会员有效", suspended: "会员停权" };

export function MemberHomeShell({ model }: { model: MemberHomeModel }) {
  if (model.state === "loading") return <State state="loading" title="正在加载会员首页"><p>正在读取您的俱乐部与会员事项…</p></State>;
  if (model.state === "unauthorized") return <State state="unauthorized" title="登录后查看会员首页"><p>{model.message ?? "请先完成登录。"}</p></State>;
  if (model.state === "maintenance") return <State state="maintenance" title="会员首页维护中"><p>{model.message ?? "请稍后再试。"}</p></State>;
  if (model.state === "offline") return <State state="offline" title="会员首页暂未开放"><p>{model.message ?? "当前入口已下线。"}</p></State>;
  if (model.state === "error") return <State state="error" title="会员首页暂时无法使用"><p>{model.message ?? "无法读取您的俱乐部信息。"}</p></State>;

  const clubs = model.clubs ?? [];
  return <main className="member-home" data-member-home-state={model.state}>
    <header className="member-home-summary">
      <p>会员工作台</p><h2>{model.displayName ? `${model.displayName}，您好` : "您好"}</h2>
      <dl><div><dt>我的俱乐部</dt><dd>{model.joinedClubCount ?? clubs.length}</dd></div><div><dt>今日待办</dt><dd>{model.pendingTaskCount ?? 0}</dd></div><div><dt>未读消息</dt><dd>{model.unreadCount ?? 0}</dd></div></dl>
    </header>
    <Section title="我的俱乐部" label="我的俱乐部">
      {clubs.length ? <div className="member-home-list">{clubs.map(c => <article key={c.clubId}><div><strong>{c.name}</strong><p>{c.kind} · {c.role} · {clubStatusLabel[c.clubStatus]} · {membershipStatusLabel[c.membershipStatus]}</p></div><a href={c.href}>进入</a></article>)}</div> : <Empty>您还没有加入俱乐部，可以从下方探索。</Empty>}
    </Section>
    <div className="member-home-columns">
      <Section title="今日待办" label="今日待办">{model.sectionErrors?.tasks ? <p role="alert">{model.sectionErrors.tasks}</p> : model.tasks?.length ? <ul>{model.tasks.map(t => <li key={t.taskId}><a href={t.href}>{t.title}</a><span>{t.context}</span></li>)}</ul> : <Empty>今天暂无待办。</Empty>}</Section>
      <Section title="最近活动" label="最近活动">{model.sectionErrors?.activities ? <p role="alert">{model.sectionErrors.activities}</p> : model.activities?.length ? <ul>{model.activities.map(a => <li key={a.activityId}><a href={a.href}>{a.title}</a><span>{a.timeLabel}</span></li>)}</ul> : <Empty>暂无即将开始的活动。</Empty>}</Section>
    </div>
    {model.sectionErrors?.feed ? <Section title="联盟动态" label="联盟动态"><p role="alert">{model.sectionErrors.feed}</p></Section> : model.feed?.length ? <Section title="联盟动态" label="联盟动态"><ul>{model.feed.map(i => <li key={i.itemId}><a href={i.href}>{i.title}</a></li>)}</ul></Section> : null}
    <Section title="探索更多" label="探索更多"><nav className="member-home-explore">{model.explore?.map(e => <a key={e.actionId} data-action-id={e.actionId} href={e.href}>{e.label}</a>)}</nav></Section>
    {model.canManage && <aside className="member-home-management" aria-label="俱乐部联盟管理附属入口"><a href="/services/club-alliance?view=manage">管理中心</a></aside>}
  </main>;
}
