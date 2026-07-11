import type { MouseEvent, ReactNode } from "react";
import { Link, NavLink } from "react-router-dom";
import { useActionRuntime } from "../auth/ActionRuntimeContext";
import { isEnabledAction, type ServiceAction } from "../domain/serviceActions";
import {
  evaluateActionAccess,
  type ActionAccessDecision,
  type ActionSession,
} from "../infrastructure/actionExecutor";
import { reportActionEvent } from "../infrastructure/actionTelemetry";

type ActionControlProps = {
  action: ServiceAction;
  children?: ReactNode;
  className?: string;
  nav?: boolean;
  onPlatformCommand?: (action: ServiceAction) => void;
  onOidcLaunch?: (action: ServiceAction) => void;
  onAccessRequired?: (action: ServiceAction, decision: ActionAccessDecision) => void;
  session?: ActionSession;
};

const unavailableLabel = (action: ServiceAction) =>
  action.lifecycle_status === "planned" ? "规划中" : "暂不可用";

export function ActionControl({
  action,
  children,
  className,
  nav = false,
  onPlatformCommand,
  onOidcLaunch,
  onAccessRequired,
  session,
}: ActionControlProps) {
  const runtime = useActionRuntime();
  const effectiveSession = session ?? runtime.session;
  const reportAccessRequirement = onAccessRequired ?? runtime.reportAccessRequirement;
  const contents = children ?? action.label;
  const accessDecision = evaluateActionAccess(action, effectiveSession, {
    platformCommand: Boolean(onPlatformCommand),
    oidcLaunch: Boolean(onOidcLaunch),
  });
  const sharedProps = {
    "aria-label": action.label,
    "data-action-id": action.action_id,
    "data-auth-mode": action.access.auth_mode,
    "data-telemetry-event": action.telemetry_event,
    "data-access-state": accessDecision.allowed ? "allowed" : accessDecision.reason,
  };
  const reportDecision = () => {
    if (accessDecision.allowed) {
      void reportActionEvent(action, "activated", "none");
    } else {
      void reportActionEvent(action, "blocked", accessDecision.reason);
    }
  };

  if (!isEnabledAction(action)) {
    return (
      <button
        {...sharedProps}
        className={className}
        type="button"
        disabled
        title={unavailableLabel(action)}
      >
        {contents}
      </button>
    );
  }

  if (action.action_type === "platform_command") {
    return (
      <button
        {...sharedProps}
        className={className}
        type="button"
        onClick={() => {
          reportDecision();
          onPlatformCommand?.(action);
        }}
        disabled={!accessDecision.allowed}
      >
        {contents}
      </button>
    );
  }

  if (action.target.startsWith("https://")) {
    if (action.access.auth_mode === "oidc_pkce") {
      return (
        <button
          {...sharedProps}
          className={className}
          type="button"
          disabled={!accessDecision.allowed}
          onClick={() => {
            reportDecision();
            onOidcLaunch?.(action);
          }}
        >
          {contents}
        </button>
      );
    }
    if (!accessDecision.allowed) {
      return <button {...sharedProps} className={className} type="button" disabled>{contents}</button>;
    }
    return (
      <a
        {...sharedProps}
        className={className}
        href={action.target}
        rel="noopener noreferrer"
        target="_blank"
        onClick={reportDecision}
      >
        {contents}
      </a>
    );
  }

  const notifyAccessRequirement = (event: MouseEvent<HTMLAnchorElement>) => {
    if (!accessDecision.allowed && accessDecision.reason === "scope_required") {
      event.preventDefault();
    }
    reportDecision();
    if (!accessDecision.allowed) reportAccessRequirement(action, accessDecision);
  };

  if (nav) {
    return (
      <NavLink
        {...sharedProps}
        className={({ isActive }) =>
          [className, isActive ? "active" : ""].filter(Boolean).join(" ")
        }
        to={action.target}
        onClick={notifyAccessRequirement}
      >
        {contents}
      </NavLink>
    );
  }

  return (
    <Link
      {...sharedProps}
      className={className}
      to={action.target}
      onClick={notifyAccessRequirement}
    >
      {contents}
    </Link>
  );
}
