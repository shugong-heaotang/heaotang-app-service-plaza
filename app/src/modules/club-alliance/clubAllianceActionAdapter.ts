import type { ServiceAction } from "../../domain/serviceActions";
import {
  ClubAllianceHomepageContractError,
  clubAllianceCategoryActionIds,
  clubAllianceManagementActionId,
  type ClubAllianceCategoryActionId,
} from "./clubAllianceHomepageContract";

const clubAllianceRegion = "club_alliance" as const;
const clubAllianceServiceId = "club-alliance" as const;
const clubAllianceActionType = "service_variant" as const;

const expectedActionIds = new Set<string>([
  ...clubAllianceCategoryActionIds,
  clubAllianceManagementActionId,
]);

const isCorrectScope = (action: ServiceAction) =>
  action.region === clubAllianceRegion &&
  action.service_id === clubAllianceServiceId &&
  action.action_type === clubAllianceActionType;

const requireUniqueAction = (
  actions: readonly ServiceAction[],
  actionId: string,
) => {
  const matches = actions.filter((action) => action.action_id === actionId);
  if (matches.length === 0) {
    throw new ClubAllianceHomepageContractError(
      "CAH1_ACTION_MISSING",
      `俱乐部联盟动作目录缺少 ${actionId}`,
    );
  }
  if (matches.length > 1) {
    throw new ClubAllianceHomepageContractError(
      "CAH1_ACTION_DUPLICATE",
      `俱乐部联盟动作目录重复定义 ${actionId}`,
    );
  }
  const [action] = matches;
  if (!isCorrectScope(action)) {
    throw new ClubAllianceHomepageContractError(
      "CAH1_ACTION_SCOPE_INVALID",
      `俱乐部联盟动作 ${actionId} 的作用域不符合首页合同`,
    );
  }
  return action;
};

export type ClubAllianceActionView = {
  categories: readonly ServiceAction[];
  management: ServiceAction;
};

export const deriveClubAllianceActions = (
  actions: readonly ServiceAction[],
): ClubAllianceActionView => {
  const unexpected = actions.find(
    (action) => isCorrectScope(action) && !expectedActionIds.has(action.action_id),
  );
  if (unexpected) {
    throw new ClubAllianceHomepageContractError(
      "CAH1_ACTION_UNEXPECTED",
      `俱乐部联盟首页合同不接受动作 ${unexpected.action_id}`,
    );
  }

  const categories = clubAllianceCategoryActionIds
    .map((actionId) => requireUniqueAction(actions, actionId))
    .sort((left, right) => left.sort_order - right.sort_order);

  return {
    categories,
    management: requireUniqueAction(actions, clubAllianceManagementActionId),
  };
};

const categoryFromTarget = (action: ServiceAction) => {
  let target: URL;
  try {
    target = new URL(action.target, "https://heaotang.invalid");
  } catch {
    throw new ClubAllianceHomepageContractError(
      "CAH1_ACTION_TARGET_INVALID",
      `俱乐部联盟动作 ${action.action_id} 的 target 无法解析`,
    );
  }

  const values = target.searchParams.getAll("category");
  if (values.length !== 1 || values[0].trim() === "") {
    throw new ClubAllianceHomepageContractError(
      "CAH1_ACTION_TARGET_INVALID",
      `俱乐部联盟动作 ${action.action_id} 缺少唯一 category target`,
    );
  }
  return values[0];
};

export type ClubAllianceQuerySelection =
  | { mode: "home"; selected_action_id: null }
  | { mode: "focused"; selected_action_id: ClubAllianceCategoryActionId };

export const resolveClubAllianceQuery = (
  search: string | URLSearchParams,
  categories: readonly ServiceAction[],
): ClubAllianceQuerySelection => {
  const params =
    typeof search === "string"
      ? new URLSearchParams(search.startsWith("?") ? search.slice(1) : search)
      : search;
  const requestedCategories = params.getAll("category");

  if (requestedCategories.length === 0) {
    return { mode: "home", selected_action_id: null };
  }
  if (requestedCategories.length > 1) {
    throw new ClubAllianceHomepageContractError(
      "CAH0_QUERY_AMBIGUOUS",
      "category 参数必须唯一",
    );
  }

  const requestedCategory = requestedCategories[0];
  if (requestedCategory.trim() === "") {
    throw new ClubAllianceHomepageContractError(
      "CAH0_QUERY_BLANK",
      "category 参数不能为空",
    );
  }

  const matches = categories.filter(
    (action) => categoryFromTarget(action) === requestedCategory,
  );
  if (matches.length === 0) {
    throw new ClubAllianceHomepageContractError(
      "CAH0_QUERY_UNKNOWN",
      `未知俱乐部分类：${requestedCategory}`,
    );
  }
  if (matches.length > 1) {
    throw new ClubAllianceHomepageContractError(
      "CAH0_QUERY_AMBIGUOUS",
      `俱乐部分类无法唯一映射：${requestedCategory}`,
    );
  }

  return {
    mode: "focused",
    selected_action_id: matches[0].action_id as ClubAllianceCategoryActionId,
  };
};
