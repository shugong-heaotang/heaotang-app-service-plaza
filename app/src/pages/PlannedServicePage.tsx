import { Link } from "react-router-dom";
import { AppFrame } from "../components/AppFrame";

type PlannedService = "activity-plaza" | "ai-assistant";

const serviceCopy: Record<PlannedService, {
  title: string;
  state: string;
  heading: string;
  description: string;
}> = {
  "activity-plaza": {
    title: "活动广场",
    state: "public-placeholder",
    heading: "活动列表",
    description: "活动发布与报名能力正在接入；当前页面仅展示公开入口，不读取会员或报名数据。",
  },
  "ai-assistant": {
    title: "Nova AI 助手",
    state: "offline",
    heading: "AI 能力尚未开放",
    description: "Nova AI 当前按离线状态处理，不提供对话、工具调用或任何状态变更能力。",
  },
};

export function PlannedServicePage({ service }: { service: PlannedService }) {
  const copy = serviceCopy[service];
  return (
    <AppFrame title={copy.title} actions={[]}>
      <section data-page-state={copy.state} aria-labelledby={`${service}-title`}>
        <p>服务状态</p>
        <h2 id={`${service}-title`}>{copy.heading}</h2>
        <p>{copy.description}</p>
        <Link to="/services">← 返回服务广场</Link>
      </section>
    </AppFrame>
  );
}
