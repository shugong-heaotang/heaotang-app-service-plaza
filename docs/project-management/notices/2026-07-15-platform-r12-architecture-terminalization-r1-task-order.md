# Platform R12 Architecture Terminalization R1 Task Order

- work_id: `AIW-20260715-PLATFORM-R12-ARCHITECTURE-TERMINALIZATION-R1`
- base: `9f79d06d502bf11ad0bb7f6dc74c80c0175f01d3`
- branch: `codex/platform-r12-terminalization-r1`
- worktree: `C:/Users/shugo/Documents/APP系统/.codex-worktrees/platform-r12-terminalization-r1`
- owner: 平台集成负责人
- reviewer: APP 总架构独立验收负责人
- status: formally activated

## Objective

Repair the governance timing defect without rewriting history: `aa23dbe` was merged by
`f986734` before the distinct APP architecture verdict completed. File the later exact
architecture verdict with its real time, independently close the exact `8f8f2f6` and
`2f4cb9d` registry candidates, and prepare one fresh registry-only terminalization
candidate from the current authority.

## Allowed scope

Only the seven path groups registered in `agent-collaboration.v1.json` are allowed.
The legacy Activity/Mall receipt, delivery-flow policies, schemas, validators, Activity
business files, Mall states and deployment paths are forbidden.

## Required evidence

1. Current checklist and governance exam score 100, linked to the same record ID.
2. File-backed APP architecture evidence for exact `aa23dbe`, including the fact that
   `f986734` preceded the final architecture verdict and was not the verdict itself.
3. File-backed verdicts for exact `8f8f2f6` and `2f4cb9d`.
4. Fresh ancestry, evidence SHA, old receipt SHA and `applied=false` verification.
5. Registry validation proving one owner and no active path overlap.
6. Independent review before controlled integration. No backdated `reviewed_at` value.

## Next authorization

Only after this item is independently accepted and integrated may the platform register
and activate `AIW-20260715-PLATFORM-ACTIVITY-LIFECYCLE-DECOUPLING-R1`. That later item
must preserve the old five-row receipt byte-for-byte and add strict Activity-only and
Mall-only supersession records. This task does not authorize that implementation.
