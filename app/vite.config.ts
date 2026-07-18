import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv, type Plugin } from "vite";

const projectBrainSnapshotPlugin = (): Plugin => ({
  name: "heaotang-project-brain-truthful-snapshot",
  apply: "build",
  generateBundle() {
    const snapshot = {
      contract_version: "project-brain.snapshot.v1",
      generated_at: new Date().toISOString(),
      source_commit: "unknown",
      source_freshness: "unknown",
      overall_verdict: "no-go",
      modules: [],
      work_summary: {},
      active_work: [],
      pending_decisions: [],
      risks: [{
        risk_id: "PB-BUILD-PROVENANCE-UNKNOWN",
        title: "当前项目事实尚未绑定可信快照",
        status: "open",
        impact: "high",
        mitigation: "保持 No-Go/Unknown，等待独立生成并验证当前权威快照。",
        source_path: "build:test-server",
      }],
      acceptance_queue: [],
      recent_integrations: [],
      audit_summary: { error: 1 },
    };
    this.emitFile({
      type: "asset",
      fileName: "project-brain/project-brain.snapshot.json",
      source: `${JSON.stringify(snapshot, null, 2)}\n`,
    });
  },
});

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, ".", "");

  return {
    base: env.VITE_PUBLIC_BASE || "/",
    plugins: [react(), projectBrainSnapshotPlugin()],
    server: {
      proxy: {
        "/api": {
          target: env.VITE_DEV_PROXY_TARGET || "https://47.94.159.60",
          changeOrigin: true,
          secure: false,
        },
      },
    },
  };
});
