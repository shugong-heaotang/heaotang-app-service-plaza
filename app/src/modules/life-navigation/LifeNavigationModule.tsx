import type { ReactNode } from "react";
import type { ServiceManifest } from "../../domain/serviceCatalog";
import {
  mapLifeNavigationManifest,
  type LifeNavigationModuleContract,
} from "./lifeNavigationContract";

export type LifeNavigationModuleContext = {
  contract: LifeNavigationModuleContract;
};

/**
 * Adapter implemented by the independently evolving Life Navigation feature.
 * Replacing it does not require changing the service-plaza navigation contract.
 */
export interface LifeNavigationModuleAdapter {
  render(context: LifeNavigationModuleContext): ReactNode;
}

export type LifeNavigationModuleProps = {
  manifest: ServiceManifest;
  adapter: LifeNavigationModuleAdapter;
  onReturn?: (returnTarget: string) => void;
};

export function LifeNavigationModule({
  manifest,
  adapter,
  onReturn,
}: LifeNavigationModuleProps) {
  const contract = mapLifeNavigationManifest(manifest);
  const headingId = `${contract.serviceId}-heading`;

  return (
    <section
      aria-labelledby={headingId}
      data-contract-version={contract.contractVersion}
      data-service-id={contract.serviceId}
    >
      <header>
        <p>{contract.summary}</p>
        <h1 id={headingId}>{contract.displayName}</h1>
        {onReturn ? (
          <button type="button" onClick={() => onReturn(contract.returnTarget)}>
            返回服务广场
          </button>
        ) : (
          <a href={contract.returnTarget}>返回服务广场</a>
        )}
      </header>

      <div data-life-navigation-feature>
        {adapter.render({ contract })}
      </div>
    </section>
  );
}
