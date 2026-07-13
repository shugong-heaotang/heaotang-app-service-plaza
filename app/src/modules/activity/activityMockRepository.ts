import { mapActivityM1Payload } from "./activityAdapter";
import type { ActivityM1Model } from "./activityModels";

export const activityM1SyntheticPayload = {
  execution_mode: "mock-only",
  activities: [
    {
      activity_id: "activity-synthetic-001",
      title: "俱乐部周末共创会",
      summary: "由俱乐部主办的非生产合成活动，用于验证公开发现和免费报名状态。",
      club_id: "club-synthetic-001",
      club_name: "合成共创俱乐部",
      starts_at: "2026-07-18T02:00:00Z",
      location_label: "合成活动空间",
      remaining_capacity: 12,
      registration_status: "available",
      detail_target: "/services/activity/activity-synthetic-001",
      club_approval_status: "approved",
      platform_review_status: "approved",
      lifecycle_status: "registration_open",
      within_discovery_window: true,
      price_minor: 0,
    },
  ],
  proposals: [
    {
      proposal_id: "proposal-synthetic-001",
      title: "会员主题分享提案",
      club_name: "合成共创俱乐部",
      status: "club_review",
      proposer_can_approve: false,
    },
  ],
} as const;

export interface ActivityM1Repository {
  load(): ActivityM1Model;
}

export function createActivityM1MockRepository(
  payload: unknown = activityM1SyntheticPayload,
): ActivityM1Repository {
  return { load: () => mapActivityM1Payload(payload) };
}
