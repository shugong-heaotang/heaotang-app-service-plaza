export const clubAllianceHomepageContractVersion = "club-alliance.homepage.v1" as const;

export const clubAllianceRootRoute = "/services/club-alliance" as const;
export const clubAllianceReturnRoute = "/services" as const;

export const clubAllianceCategoryActionIds = [
  "public-benefit-club",
  "self-created-club",
  "family-club",
  "club-federation",
] as const;

export type ClubAllianceCategoryActionId =
  (typeof clubAllianceCategoryActionIds)[number];

export const clubAllianceManagementActionId = "club-manage" as const;

export const clubAllianceHomepageStates = [
  "home",
  "focused",
  "loading",
  "empty",
  "error",
  "unauthorized",
  "maintenance",
  "offline",
] as const;

export type ClubAllianceHomepageState =
  (typeof clubAllianceHomepageStates)[number];

export const clubAllianceQueryErrorIds = [
  "CAH0_QUERY_BLANK",
  "CAH0_QUERY_UNKNOWN",
  "CAH0_QUERY_AMBIGUOUS",
] as const;

export type ClubAllianceQueryErrorId =
  (typeof clubAllianceQueryErrorIds)[number];

export const clubAllianceActionErrorIds = [
  "CAH1_ACTION_MISSING",
  "CAH1_ACTION_DUPLICATE",
  "CAH1_ACTION_SCOPE_INVALID",
  "CAH1_ACTION_UNEXPECTED",
  "CAH1_ACTION_TARGET_INVALID",
] as const;

export type ClubAllianceActionErrorId =
  (typeof clubAllianceActionErrorIds)[number];

export type ClubAllianceHomepageErrorId =
  | ClubAllianceQueryErrorId
  | ClubAllianceActionErrorId;

export class ClubAllianceHomepageContractError extends Error {
  readonly errorId: ClubAllianceHomepageErrorId;

  constructor(errorId: ClubAllianceHomepageErrorId, message: string) {
    super(message);
    this.name = "ClubAllianceHomepageContractError";
    this.errorId = errorId;
  }
}
