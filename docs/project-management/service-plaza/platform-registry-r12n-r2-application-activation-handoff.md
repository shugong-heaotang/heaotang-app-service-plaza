# Platform Registry R12-N-R2 Legacy Application Activation Handoff

- work_id: `AIW-20260715-PLATFORM-REGISTRY-R12N-R2-APPLICATION-ACTIVATION`
- record_id: `IR-20260715-PLATFORM-REGISTRY-R12N-R2-APPLICATION-ACTIVATION`
- base: `9f79d06d502bf11ad0bb7f6dc74c80c0175f01d3`
- developer: 平台注册表R12-N-R2实施负责人
- reviewer: APP总架构独立验收负责人
- state: `ready for independent review`

## R3 deadlock regression

The frozen first R12-N registry draft was executed as a read-only semantic fixture. Old v3 validator bytes from authority `06047119...` returned exactly `DELIVERY_LEGACY_CURRENT_REGISTRY_DRIFT`. The same frozen registry bytes under R3.1 authority `9f79d06...` returned no errors. This proves R3.1 removes only the whole-file deadlock while preserving historical identity and audit-row gates.

Audit rows47/88/89/90/92/132 remain completely equal to authority in the R12-N-R2 candidate. Their canonical SHA-256 values are respectively:

- 47: `62275da8d039d2ed22c9dd4d408d4e921351157687b04fe280dbbef3fd22b9f8`
- 88: `fb99417a88c282462209df58c44eed5d5777a76dabf09ff30ead1004b4f994eb`
- 89: `3a53fb999df10c792c951ec732ed2a388d4edba0e8a34abef2215cbedd35e07c`
- 90: `6d395bd3568d4d9f8bde347df267055537d5c009bd1974ef722e7784136eff31`
- 92: `d44824bc69a7abaaa594b36157cd188a7104c3c2f0bf569c8dbe8eb4d18b5527`
- 132: `daee316c8cc7ef789bb29afcd3d27184eaf90180c7475b5838735ff308d7cac5`

## Atomic activation result

1. Existing changes are exactly row136 and row137; appended rows are exactly R4, R12-N-R2 and R12-O.
2. Row136 changes `active -> cancelled` as `superseded-by-R4`, releases twelve implementation paths and retains only a non-write tombstone plus immutable task-order/checklist provenance. It is not falsely marked integrated.
3. Row137 remains active, preserves five immutable R12-M governance paths and releases only `contracts/foundation/agent-collaboration.v1.json`.
4. R4 is active from clean authority `9f79d06...` and owns exactly twelve authorized paths. It may build content-addressed application/review/post-state contracts but cannot modify or execute a receipt or registry transaction.
5. R12-N-R2 owns only its five fresh governance paths and does not retain registry ownership.
6. R12-O is the unique registry owner after integration. It remains No-Write until R4 content-addressed intent and policy are independently accepted and controlled-integrated, followed by separate authorization.

## Preserved bytes and states

- Rows47/88/89/90/92/132/133 and Activity/Mall rows109/111/112/113/114 are unchanged.
- Activity/Mall receipt remains SHA-256 `5e85735d7c70a942efca1b8a8c6d9aecee4805a40282ae8cfbac27beab3207b1`.
- Batch receipt remains SHA-256 `13b5096c9af214b9f5c010b0ece65802cdbcef7fb19602c76aa8c6e0c9873cf6`.
- No receipt, application, Social activation or projected lifecycle transaction is executed.

## Governance and stop boundary

- global preflight: ready;
- fresh checklist: 26/26 complete;
- fresh governance exam attempt 1: 100;
- registry and direct R3.1 policy validation: passed;
- task order starts `# 平台` and contains exact `platform scope; module_id=null`, work ID and developer role;
- targeted platform identity, total contract, encoding, scope, secret and diff gates are required before commit.

The developer stops at one unpushed exact candidate. No push, self-review, integration, R12-O write, receipt/application execution, deployment, production, real-data or funds access is authorized.
