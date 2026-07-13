export const activityM1ContractVersion = "activity.m1.frontend.v1" as const;

export type ActivityPageState =
  | "loading"
  | "ready"
  | "empty"
  | "unauthorized"
  | "error";

export type RegistrationStatus =
  | "available"
  | "registered"
  | "full"
  | "ineligible";

export type PublicActivity = {
  activityId: string;
  title: string;
  summary: string;
  clubId: string;
  clubName: string;
  startsAt: string;
  locationLabel: string;
  remainingCapacity: number;
  registrationStatus: RegistrationStatus;
  detailTarget: string;
};

export type PersonalProposal = {
  proposalId: string;
  title: string;
  clubName: string;
  status: "club_review" | "changes_requested" | "approved" | "rejected";
  proposerCanApprove: false;
};

export type ActivityM1Model = {
  state: ActivityPageState;
  activities?: readonly PublicActivity[];
  proposals?: readonly PersonalProposal[];
  message?: string;
};
