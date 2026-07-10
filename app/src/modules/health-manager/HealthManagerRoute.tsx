import { CoreServicePage } from "../../pages/CoreServicePage";

export function HealthManagerRoute() {
  return (
    <div data-testid="health-manager-module-route">
      <CoreServicePage serviceKeyOverride="health-manager" />
    </div>
  );
}
