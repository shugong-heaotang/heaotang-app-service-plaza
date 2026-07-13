export const selfCreatedClubActionId = "self-created-club" as const;

export const selfCreatedClubRootRoute =
  "/services/club-alliance/self-created" as const;
export const selfCreatedClubApplicationsRoute =
  "/services/club-alliance/self-created/applications" as const;
export const selfCreatedClubDetailRoute =
  "/services/club-alliance/self-created/:clubId" as const;
export const selfCreatedClubParentRoute =
  "/services/club-alliance?category=%E8%87%AA%E5%BB%BA%E4%BF%B1%E4%B9%90%E9%83%A8" as const;

export const selfCreatedClubType = "standard" as const;
export const selfCreatedClubCategory = "general" as const;
export const selfCreatedClubStatus = "active" as const;

export const selfCreatedClubPageSize = 20;
export const selfCreatedClubMaximumPageSize = 100;

export const selfCreatedClubDetailPath = (clubId: number | string) =>
  `${selfCreatedClubRootRoute}/${clubId}`;
