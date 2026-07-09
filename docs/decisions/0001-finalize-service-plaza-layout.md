# ADR 0001: Finalize Service Plaza Layout

## Status

Accepted

## Date

2026-07-09

## Context

The APP keeps four bottom navigation tabs: Home, Service, Discover, and Mine. At this stage, Home, Discover, and Mine are not being designed. The current confirmed scope is the Service page only.

The Service page is the main place to express the core positioning of the APP. It must keep the page simple, visible, and easy to understand without hiding key entries behind horizontal scrolling.

## Decision

The Service page is finalized as the "服务广场" layout.

The top page title area uses:

- Standard brand logo: `prototype/assets/heaotang-logo.svg`
- The logo uses "和" as the central identity and avoids a closed frame around the character, using open arcs to express harmony, movement, and growth.
- Title: 服务广场
- A global AI button on the right

The first screen must prioritize three core services:

1. 生命导航
2. 俱乐部联盟
3. 健康大管家

The club section uses a top main row:

- 俱乐部联盟
- 管理中心 button on the right side of the same row

The lower club grid keeps four entries:

- 公益俱乐部
- 自建俱乐部
- 家庭俱乐部
- 俱乐部友联体

The club section does not show an extra "核心服务 / 俱乐部联盟" heading because the top main row already names the section.

The health section uses "健康大管家" as the user-facing service name. "大医健康院" remains the organization or service provider concept, not the primary entry name on the Service Plaza.

The lower section is "常用服务", currently containing:

- 活动广场
- 人脉中心
- 保障商城
- 二手集市
- AI
- 学习广场

## Premises

- The four bottom navigation tabs remain Home, Service, Discover, and Mine.
- The Service page is a first-level tab, not a submodule of Home.
- The three core services are the soul of the APP service structure: 生命导航, 俱乐部联盟, 健康大管家.
- Users may miss horizontally hidden content, so core entries must wrap to multiple rows instead of relying on horizontal scrolling.
- The Service Plaza uses the standard SVG logo at `prototype/assets/heaotang-logo.svg`, centered on an open "和" mark without a closed box around the character.

## Consequences

- Future page design should treat this Service Plaza structure as fixed unless a new decision supersedes this ADR.
- Home, Discover, and Mine can be designed later around this fixed service structure.
- Service Plaza UI changes should refine visual style, copy, and assets without changing the confirmed information hierarchy.
