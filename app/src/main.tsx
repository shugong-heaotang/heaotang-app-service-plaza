import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { AppRoutes } from "./App";
import { AuthProvider } from "./auth/AuthContext";
import { ActionRuntimeProvider } from "./auth/ActionRuntimeContext";
import "./styles.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter basename={import.meta.env.VITE_ROUTER_BASENAME || undefined}>
      <AuthProvider>
        <ActionRuntimeProvider>
          <AppRoutes />
        </ActionRuntimeProvider>
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>,
);
