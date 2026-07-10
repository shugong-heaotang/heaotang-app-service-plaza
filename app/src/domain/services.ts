export type ServiceKey = "life-navigation" | "club-alliance" | "health-manager";

export type ServiceDefinition = {
  key: ServiceKey;
  title: string;
  kicker: string;
  description: string;
  actionLabel: string;
  pendingLabel: string;
  icon: string;
  theme: "life" | "club" | "health";
};

export const serviceDefinitions: Record<ServiceKey, ServiceDefinition> = {
  "life-navigation": {
    key: "life-navigation",
    title: "生命导航",
    kicker: "核心服务",
    description: "从目标梳理开始，提交一份导航申请，后续由服务人员协助推进。",
    actionLabel: "提交导航申请",
    pendingLabel: "导航申请已提交，等待服务人员处理。",
    icon: "导",
    theme: "life",
  },
  "club-alliance": {
    key: "club-alliance",
    title: "俱乐部联盟",
    kicker: "核心服务",
    description: "选择适合的俱乐部类型，提交加入申请并等待管理员审核。",
    actionLabel: "申请加入俱乐部",
    pendingLabel: "加入申请已提交，等待管理员审核。",
    icon: "盟",
    theme: "club",
  },
  "health-manager": {
    key: "health-manager",
    title: "健康大管家",
    kicker: "核心服务",
    description: "描述当前健康需求，提交咨询后由健康服务人员跟进。",
    actionLabel: "提交健康咨询",
    pendingLabel: "健康咨询已提交，等待服务人员回复。",
    icon: "健康",
    theme: "health",
  },
};

export const isServiceKey = (value: string | undefined): value is ServiceKey =>
  Boolean(value && value in serviceDefinitions);
