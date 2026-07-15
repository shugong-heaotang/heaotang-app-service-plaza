import { Navigate, Route, Routes } from "react-router-dom";
import { ClubAllianceRoute, SelfCreatedClubRoute } from "./modules/club-alliance";
import { HealthManagerRoute } from "./modules/health-manager";
import { LifeNavigationPage } from "./modules/life-navigation";
import { ProtectionMallPage } from "./modules/protection-mall";
import { ProjectBrainPage } from "./modules/project-brain/ProjectBrainPage";
import { CoreServicePage } from "./pages/CoreServicePage";
import { NotFoundPage } from "./pages/NotFoundPage";
import { ServicePlazaPage } from "./pages/ServicePlazaPage";

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/services" replace />} />
      <Route path="/services" element={<ServicePlazaPage />} />
      <Route
        path="/internal/project-brain"
        element={import.meta.env.DEV || import.meta.env.MODE === "test-server" ? <ProjectBrainPage /> : <Navigate to="/services" replace />}
      />
      <Route path="/services/life-navigation" element={<LifeNavigationPage />} />
      <Route
        path="/services/club-alliance/self-created/applications"
        element={<SelfCreatedClubRoute mode="applications" />}
      />
      <Route
        path="/services/club-alliance/self-created/:clubId"
        element={<SelfCreatedClubRoute mode="detail" />}
      />
      <Route
        path="/services/club-alliance/self-created"
        element={<SelfCreatedClubRoute mode="list" />}
      />
      <Route path="/services/club-alliance" element={<ClubAllianceRoute />} />
      <Route path="/services/health-manager" element={<HealthManagerRoute />} />
      <Route path="/services/protection-mall" element={<ProtectionMallPage />} />
      <Route path="/services/:serviceKey" element={<CoreServicePage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
