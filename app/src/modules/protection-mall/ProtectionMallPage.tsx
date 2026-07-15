import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../../auth/AuthContext";
import { AppFrame } from "../../components/AppFrame";
import { AuthPanel } from "../../components/AuthPanel";
import { ApiError } from "../../infrastructure/apiClient";
import {
  protectionMallCatalogApi,
  type ProtectionMallCatalogApi,
  type ProtectionMallSceneId,
} from "./protectionMallApi";
import type { ProtectionMallCatalogEntry } from "./protectionMallContract";
import {
  catalogRequestId,
  useProtectionMallCatalog,
} from "./useProtectionMallCatalog";
import "./ProtectionMallPage.css";

const scenes: ReadonlyArray<{ id: ProtectionMallSceneId; label: string }> = [
  { id: "all", label: "全部" },
  { id: "family-care", label: "家庭关怀" },
  { id: "health-care", label: "健康照护" },
  { id: "quality-life", label: "品质生活" },
  { id: "member", label: "会员精选" },
];

const kindLabels: Record<ProtectionMallCatalogEntry["kind"], string> = {
  product: "商品",
  service: "服务",
  course: "课程",
  activity: "活动",
};

function formatPrice({ amountMinor, currency }: ProtectionMallCatalogEntry["price"]): string {
  try {
    return new Intl.NumberFormat("zh-CN", {
      style: "currency",
      currency,
      minimumFractionDigits: 2,
    }).format(amountMinor / 100);
  } catch {
    return `${currency} ${(amountMinor / 100).toFixed(2)}`;
  }
}

function CatalogList({ items }: { items: ProtectionMallCatalogEntry[] }) {
  return (
    <ul className="protection-mall-grid" aria-label="商城目录">
      {items.map((item) => {
        const assurance = item.benefits.grants.some(
          ({ code }) => code.toLowerCase() === "assurance",
        );
        return (
          <li className="protection-mall-item" key={item.id}>
            <div className="protection-mall-item-heading">
              <span>{kindLabels[item.kind]}</span>
              <strong>{formatPrice(item.price)}</strong>
            </div>
            <h3>{item.title}</h3>
            <p>服务责任方：{item.responsibility.sellerId}</p>
            <p>履约：{item.responsibility.fulfillmentOwnerId}</p>
            <div className="protection-mall-scenes" aria-label="适用场景">
              {item.sceneIds.map((scene) => <span key={scene}>{scene}</span>)}
            </div>
            {assurance && (
              <p className="protection-mall-assurance">
                保障权益将在订单完成且售后关闭后生效
              </p>
            )}
          </li>
        );
      })}
    </ul>
  );
}

export type ProtectionMallPageProps = {
  api?: ProtectionMallCatalogApi;
};

export function ProtectionMallPage({ api = protectionMallCatalogApi }: ProtectionMallPageProps) {
  const { isAuthenticated, user, logout } = useAuth();
  const [sceneId, setSceneId] = useState<ProtectionMallSceneId>("all");
  const { state, retry } = useProtectionMallCatalog(api, sceneId, isAuthenticated);
  const retryButton = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (state.status === "error") retryButton.current?.focus();
  }, [state.status]);

  useEffect(() => {
    if (
      state.status === "error"
      && state.error instanceof ApiError
      && (state.error.status === 401 || state.error.code === "AUTH_REQUIRED")
    ) {
      logout();
    }
  }, [logout, state]);

  return (
    <AppFrame
      title="保障商城"
      backAction={
        <Link className="back-button" to="/services" aria-label="返回服务广场">←</Link>
      }
    >
      {!isAuthenticated ? (
        <AuthPanel />
      ) : (
        <section className="protection-mall-page" aria-label="保障商城内容">
          <div className="session-bar">
            <span>当前用户：{user?.nickname || user?.phone || `#${user?.id ?? ""}`}</span>
            <button type="button" onClick={logout}>退出登录</button>
          </div>

          <header className="protection-mall-intro">
            <p>商品、服务、课程与活动统一目录</p>
            <h2>按生活场景选择可信服务</h2>
            <p>当前仅开放目录浏览。下单、支付和真实权益发放尚未开放。</p>
          </header>

          <nav className="protection-mall-filter" aria-label="目录场景">
            {scenes.map((scene) => (
              <button
                key={scene.id}
                type="button"
                aria-pressed={scene.id === sceneId}
                disabled={state.status === "loading" && scene.id === sceneId}
                onClick={() => setSceneId(scene.id)}
              >
                {scene.label}
              </button>
            ))}
          </nav>

          <section className="protection-mall-results" aria-labelledby="protection-mall-results-title">
            <h2 id="protection-mall-results-title" className="sr-only">目录结果</h2>
            <div aria-live="polite" aria-busy={state.status === "loading"}>
              {state.status === "loading" && <p role="status">正在加载商城目录…</p>}
              {state.status === "empty" && (
                <div className="protection-mall-state">
                  <h3>当前场景暂无内容</h3>
                  <p>可以切换其他场景，稍后也可再次查看。</p>
                </div>
              )}
              {state.status === "ready" && <CatalogList items={state.items} />}
              {state.status === "error" && (
                <div className="protection-mall-state protection-mall-error" role="alert">
                  <h3>商城目录暂时无法加载</h3>
                  <p>请检查网络后重试。系统不会用示例商品替代真实结果。</p>
                  {catalogRequestId(state.error) && (
                    <p>请求编号：<code>{catalogRequestId(state.error)}</code></p>
                  )}
                  <button ref={retryButton} type="button" onClick={retry}>重新加载</button>
                </div>
              )}
            </div>
          </section>

          <Link className="return-link" to="/services">← 返回服务广场</Link>
        </section>
      )}
    </AppFrame>
  );
}
