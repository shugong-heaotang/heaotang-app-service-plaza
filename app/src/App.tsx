import { Navigate, Route, Routes } from "react-router-dom";
import { CoreServicePage } from "./pages/CoreServicePage";
import { NotFoundPage } from "./pages/NotFoundPage";
import { ServicePlazaPage } from "./pages/ServicePlazaPage";

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/services" replace />} />
      <Route path="/services" element={<ServicePlazaPage />} />
      <Route path="/services/:serviceKey" element={<CoreServicePage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
