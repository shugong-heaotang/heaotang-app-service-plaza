import { describe, expect, it } from "vitest";
import {
  clubAllianceCategoryActionIds,
  clubAllianceHomepageContractVersion,
  clubAllianceHomepageStates,
  clubAllianceManagementActionId,
  clubAllianceReturnRoute,
  clubAllianceRootRoute,
} from "./clubAllianceHomepageContract";

describe("club alliance homepage contract", () => {
  it("freezes the H0 route, entry and exact eight-state boundary", () => {
    expect(clubAllianceHomepageContractVersion).toBe("club-alliance.homepage.v1");
    expect(clubAllianceRootRoute).toBe("/services/club-alliance");
    expect(clubAllianceReturnRoute).toBe("/services");
    expect(clubAllianceCategoryActionIds).toEqual([
      "public-benefit-club",
      "self-created-club",
      "family-club",
      "club-federation",
    ]);
    expect(clubAllianceManagementActionId).toBe("club-manage");
    expect(clubAllianceHomepageStates).toEqual([
      "home",
      "focused",
      "loading",
      "empty",
      "error",
      "unauthorized",
      "maintenance",
      "offline",
    ]);
  });
});
