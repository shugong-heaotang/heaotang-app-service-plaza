import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, ".", "");

  return {
    base: env.VITE_PUBLIC_BASE || "/",
    plugins: [react()],
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
