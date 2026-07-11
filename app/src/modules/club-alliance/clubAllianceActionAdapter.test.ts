import { describe, expect, it } from "vitest";
import type { ServiceAction } from "../../domain/serviceActions";
import { mockActions } from "../../infrastructure/serviceCatalogRepository";
import {
  deriveClubAllianceActions,
  resolveClubAllianceQuery,
} from "./clubAllianceActionAdapter";
import { ClubAllianceHomepageContractError } from "./clubAllianceHomepageContract";

const cloneActions = () => mockActions.map((action) => structuredClone(action));

const expectContractError = (
  operation: () => unknown,
  errorId: ClubAllianceHomepageContractError["errorId"],
) => {
  try {
    operation();
    throw new Error("expected operation to fail closed");
  } catch (error) {
    expect(error).toBeInstanceOf(ClubAllianceHomepageContractError);
    expect((error as ClubAllianceHomepageContractError).errorId).toBe(errorId);
  }
};

describe("deriveClubAllianceActions", () => {
  it("derives four entries from shuffled upstream actions and preserves upstream order", () => {
    const actions = cloneActions().reverse();
    const view = deriveClubAllianceActions(actions);

    expect(view.categories.map((action) => action.action_id)).toEqual([
      "public-benefit-club",
      "self-created-club",
      "family-club",
      "club-federation",
    ]);
    expect(view.categories.map((action) => action.sort_order)).toEqual([50, 60, 70, 80]);
    expect(view.management.action_id).toBe("club-manage");
    expect(view.categories).not.toContain(view.management);
  });

  it("fails closed for a missing or duplicate category action", () => {
    expectContractError(
      () =>
        deriveClubAllianceActions(
          cloneActions().filter((action) => action.action_id !== "family-club"),
        ),
      "CAH1_ACTION_MISSING",
    );

    const actions = cloneActions();
    const duplicate = structuredClone(
      actions.find((action) => action.action_id === "family-club") as ServiceAction,
    );
    actions.push(duplicate);
    expectContractError(
      () => deriveClubAllianceActions(actions),
      "CAH1_ACTION_DUPLICATE",
    );
  });

  it("requires one management adjunct without treating it as a category", () => {
    expectContractError(
      () =>
        deriveClubAllianceActions(
          cloneActions().filter((action) => action.action_id !== "club-manage"),
        ),
      "CAH1_ACTION_MISSING",
    );

    const actions = cloneActions();
    actions.push(
      structuredClone(
        actions.find((action) => action.action_id === "club-manage") as ServiceAction,
      ),
    );
    expectContractError(
      () => deriveClubAllianceActions(actions),
      "CAH1_ACTION_DUPLICATE",
    );
  });

  it("fails closed for an expected action in the wrong scope", () => {
    const actions = cloneActions().map((action) =>
      action.action_id === "self-created-club"
        ? { ...action, service_id: "another-service" }
        : action,
    );
    expectContractError(
      () => deriveClubAllianceActions(actions),
      "CAH1_ACTION_SCOPE_INVALID",
    );
  });

  it("rejects a fifth category while retaining club-manage as an adjunct", () => {
    const actions = cloneActions();
    actions.push({
      ...(structuredClone(
        actions.find((action) => action.action_id === "family-club") as ServiceAction,
      )),
      action_id: "fifth-club-category",
    });
    expectContractError(
      () => deriveClubAllianceActions(actions),
      "CAH1_ACTION_UNEXPECTED",
    );
  });

  it.each([
    ["missing", "/services/club-alliance"],
    ["blank", "/services/club-alliance?category=%20"],
    ["repeated", "/services/club-alliance?category=公益俱乐部&category=公益俱乐部"],
    ["multiple", "/services/club-alliance?category=公益俱乐部&category=自建俱乐部"],
    ["malformed", "http://["],
  ])("fails home derivation closed for a %s category target", (_kind, target) => {
    const actions = cloneActions().map((action) =>
      action.action_id === "public-benefit-club" ? { ...action, target } : action,
    );
    expectContractError(
      () => deriveClubAllianceActions(actions),
      "CAH1_ACTION_TARGET_INVALID",
    );
  });

  it("fails home derivation closed when different actions map to one category", () => {
    const actions = cloneActions();
    const publicBenefit = actions.find(
      (action) => action.action_id === "public-benefit-club",
    ) as ServiceAction;
    const duplicatedCategory = actions.map((action) =>
      action.action_id === "self-created-club"
        ? { ...action, target: publicBenefit.target }
        : action,
    );
    expectContractError(
      () => deriveClubAllianceActions(duplicatedCategory),
      "CAH1_ACTION_TARGET_INVALID",
    );
  });
});

describe("resolveClubAllianceQuery", () => {
  it("maps no query to home and each upstream category target to focused state", () => {
    const { categories } = deriveClubAllianceActions(cloneActions());
    expect(resolveClubAllianceQuery("", categories)).toEqual({
      mode: "home",
      selected_action_id: null,
    });

    categories.forEach((action) => {
      const query = new URL(action.target, "https://heaotang.invalid").search;
      expect(resolveClubAllianceQuery(query, categories)).toEqual({
        mode: "focused",
        selected_action_id: action.action_id,
      });
    });
  });

  it("fails closed with stable error ids for blank, unknown and repeated category", () => {
    const { categories } = deriveClubAllianceActions(cloneActions());
    expectContractError(
      () => resolveClubAllianceQuery("?category=%20", categories),
      "CAH0_QUERY_BLANK",
    );
    expectContractError(
      () => resolveClubAllianceQuery("?category=unknown", categories),
      "CAH0_QUERY_UNKNOWN",
    );
    expectContractError(
      () => resolveClubAllianceQuery("?category=a&category=b", categories),
      "CAH0_QUERY_AMBIGUOUS",
    );
  });

  it("detects ambiguous upstream target mappings without hardcoded Chinese labels", () => {
    const { categories } = deriveClubAllianceActions(cloneActions());
    const duplicatedTarget = categories.map((action, index) =>
      index === 1 ? { ...action, target: categories[0].target } : action,
    );
    const query = new URL(categories[0].target, "https://heaotang.invalid").search;
    expectContractError(
      () => resolveClubAllianceQuery(query, duplicatedTarget),
      "CAH0_QUERY_AMBIGUOUS",
    );
  });

  it("fails closed when an upstream category target is missing or malformed", () => {
    const { categories } = deriveClubAllianceActions(cloneActions());
    const missingCategory = categories.map((action, index) =>
      index === 0 ? { ...action, target: "/services/club-alliance" } : action,
    );
    expectContractError(
      () => resolveClubAllianceQuery("?category=公益俱乐部", missingCategory),
      "CAH1_ACTION_TARGET_INVALID",
    );

    const malformedTarget = categories.map((action, index) =>
      index === 0 ? { ...action, target: "http://[" } : action,
    );
    expectContractError(
      () => resolveClubAllianceQuery("?category=公益俱乐部", malformedTarget),
      "CAH1_ACTION_TARGET_INVALID",
    );
  });

  it("maps the upstream management target to the management adjunct", () => {
    const { categories, management } = deriveClubAllianceActions(cloneActions());
    const query = new URL(management.target, "https://heaotang.invalid").search;

    expect(resolveClubAllianceQuery(query, categories, management)).toEqual({
      mode: "focused",
      selected_action_id: "club-manage",
    });
  });

  it.each([
    ["blank", "?view=%20", "CAH0_QUERY_BLANK"],
    ["unknown", "?view=unknown", "CAH0_QUERY_UNKNOWN"],
    ["repeated", "?view=manage&view=manage", "CAH0_QUERY_AMBIGUOUS"],
    ["mixed", "?view=manage&category=公益俱乐部", "CAH0_QUERY_AMBIGUOUS"],
  ] as const)("fails a %s management query closed", (_kind, query, errorId) => {
    const { categories, management } = deriveClubAllianceActions(cloneActions());
    expectContractError(
      () => resolveClubAllianceQuery(query, categories, management),
      errorId,
    );
  });

  it("fails management query resolution closed when the target is not unique", () => {
    const actions = cloneActions().map((action) =>
      action.action_id === "club-manage"
        ? { ...action, target: "/services/club-alliance" }
        : action,
    );
    const { categories, management } = deriveClubAllianceActions(actions);
    expectContractError(
      () => resolveClubAllianceQuery("?view=manage", categories, management),
      "CAH1_ACTION_TARGET_INVALID",
    );
  });
});
