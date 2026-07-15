import { useCallback, useEffect, useState, type FormEvent } from "react";
import { ApiError } from "../../../infrastructure/apiClient";
import {
  publicWelfareRegionalApi,
  type ApplicationStatus,
  type CenterSearchInput,
  type PublicWelfareEstablishmentApplication,
  type PublicWelfareRegionalApi,
  type RegionalRoleApplication,
  type ReviewDecision,
  type ServiceCenter,
} from "./publicWelfareRegionalApi";
import "./PublicWelfareRegionalPanel.css";

export type PublicWelfareRegionalMode = "public-welfare" | "regional-public" | "management";

type Props = {
  mode: PublicWelfareRegionalMode;
  api?: PublicWelfareRegionalApi;
};

const statusLabels: Record<ApplicationStatus, string> = {
  draft: "草稿",
  submitted: "已提交",
  under_review: "审核中",
  approved: "已批准",
  rejected: "未通过",
  withdrawn: "已撤回",
};

const field = (data: FormData, name: string) => String(data.get(name) ?? "").trim();

const errorMessage = (reason: unknown) => {
  if (reason instanceof ApiError) return `${reason.message}${reason.code ? `（${reason.code}）` : ""}`;
  return reason instanceof Error ? reason.message : "操作失败，请稍后重试";
};

function ApplicationStatusList({ items }: { items: readonly PublicWelfareEstablishmentApplication[] }) {
  if (items.length === 0) return <p className="pwr-empty">您还没有公益俱乐部创办申请。</p>;
  return (
    <ul className="pwr-status-list">
      {items.map((item) => (
        <li key={item.id}>
          <strong>{item.name}</strong>
          <span>{statusLabels[item.status]}</span>
          {item.club_id && <small>已创建公益俱乐部 #{item.club_id}</small>}
          {item.review_note && <small>审核意见：{item.review_note}</small>}
        </li>
      ))}
    </ul>
  );
}

function PublicWelfareApplication({ api }: { api: PublicWelfareRegionalApi }) {
  const [items, setItems] = useState<PublicWelfareEstablishmentApplication[]>([]);
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);

  const refresh = useCallback(() => {
    void api.listMyEstablishments().then(setItems).catch((reason) => setMessage(errorMessage(reason)));
  }, [api]);
  useEffect(refresh, [refresh]);

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = event.currentTarget;
    const data = new FormData(form);
    setBusy(true);
    setMessage("");
    try {
      const application = await api.submitEstablishment({
        name: field(data, "name"), province: field(data, "province"), city: field(data, "city"),
        district: field(data, "district"), mission: field(data, "mission"),
        eligibility: field(data, "eligibility"), resources: field(data, "resources"),
        governance: field(data, "governance"), risks: field(data, "risks"),
        pdcar: {
          plan: field(data, "pdcar_plan"), do: field(data, "pdcar_do"),
          check: field(data, "pdcar_check"), act: field(data, "pdcar_act"),
          record: field(data, "pdcar_record"),
        },
      });
      setItems((current) => [application, ...current.filter((item) => item.id !== application.id)]);
      setMessage("申请已提交。联盟审核批准后，系统才会创建并对外开放公益俱乐部。");
      form.reset();
    } catch (reason) {
      setMessage(errorMessage(reason));
    } finally {
      setBusy(false);
    }
  };

  return (
    <section className="pwr-panel" aria-label="申请创办公益俱乐部">
      <header><p className="section-kicker">公益俱乐部</p><h3>申请创办</h3></header>
      <div className="pwr-rule" role="note">
        公益俱乐部不能从普通“创建俱乐部”入口直接创建。提交完整条件与 PDCAR 计划，经俱乐部联盟批准后，系统才创建 standard + charity 俱乐部并开放服务。
      </div>
      <form onSubmit={submit} className="pwr-form">
        <fieldset><legend>基本条件</legend>
          <label>拟创办名称<input required name="name" /></label>
          <div className="pwr-three"><label>省<input required name="province" /></label><label>市<input required name="city" /></label><label>区/县<input required name="district" /></label></div>
          <label>公益使命<textarea required name="mission" /></label>
          <label>申请资格与团队条件<textarea required name="eligibility" /></label>
          <label>可投入资源<textarea required name="resources" /></label>
          <label>治理与责任分工<textarea required name="governance" /></label>
          <label>风险、合规及应对<textarea required name="risks" /></label>
        </fieldset>
        <fieldset><legend>PDCAR 循环计划</legend>
          <label>P · 计划<textarea required name="pdcar_plan" /></label>
          <label>D · 执行<textarea required name="pdcar_do" /></label>
          <label>C · 检查<textarea required name="pdcar_check" /></label>
          <label>A · 改进<textarea required name="pdcar_act" /></label>
          <label>R · 记录与复盘<textarea required name="pdcar_record" /></label>
        </fieldset>
        <button disabled={busy} type="submit">{busy ? "正在提交…" : "提交创办申请"}</button>
      </form>
      {message && <p role="status" className="pwr-message">{message}</p>}
      <h4>我的申请</h4><ApplicationStatusList items={items} />
    </section>
  );
}

function CenterCards({ items }: { items: readonly ServiceCenter[] }) {
  if (items.length === 0) return <p className="pwr-empty">暂无匹配的管理中心或公益服务中心。</p>;
  return <ul className="pwr-center-list">{items.map((item) => <li key={item.id}>
    <span>{item.kind === "regional_management_center" ? "区域管理中心" : "公益服务中心"}</span>
    <strong>{item.name}</strong><p>{item.province}{item.city}{item.district}{item.address}</p>
    <small>{item.contact_name} · {item.contact_phone_masked} · {item.service_hours}</small>
  </li>)}</ul>;
}

function RegionalPublicPage({ api }: { api: PublicWelfareRegionalApi }) {
  const [centers, setCenters] = useState<ServiceCenter[]>([]);
  const [roleItems, setRoleItems] = useState<RegionalRoleApplication[]>([]);
  const [message, setMessage] = useState("");
  useEffect(() => { void api.searchCenters().then(setCenters).catch((reason) => setMessage(errorMessage(reason))); }, [api]);
  useEffect(() => { void api.listMyRegionalRoles().then(setRoleItems).catch(() => undefined); }, [api]);

  const search = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); const data = new FormData(event.currentTarget);
    const input: CenterSearchInput = { province: field(data, "province"), city: field(data, "city"), district: field(data, "district"), query: field(data, "query"), kind: field(data, "kind") as CenterSearchInput["kind"] };
    try { setCenters(await api.searchCenters(input)); setMessage(""); } catch (reason) { setMessage(errorMessage(reason)); }
  };
  const apply = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); const form = event.currentTarget; const data = new FormData(form);
    try {
      const application = await api.submitRegionalRole({
        role: field(data, "role") as RegionalRoleApplication["role"], province: field(data, "province"),
        city: field(data, "city"), district: field(data, "district"), experience: field(data, "experience"),
        service_plan: field(data, "service_plan"), resources: field(data, "resources"), conflict_statement: field(data, "conflict_statement"),
      });
      setRoleItems((current) => [application, ...current]); setMessage("区域岗位申请已提交，批准后才会获得对应区域角色权限。"); form.reset();
    } catch (reason) { setMessage(errorMessage(reason)); }
  };
  return <section className="pwr-panel" aria-label="区域管理中心">
    <header><p className="section-kicker">俱乐部联盟</p><h3>区域管理中心</h3><p>查找离您最近的管理中心或公益服务中心，也可以申请承担区域服务职责。</p></header>
    <form className="pwr-search" onSubmit={search} aria-label="查找服务中心">
      <input name="province" placeholder="省" aria-label="省"/><input name="city" placeholder="市" aria-label="市"/><input name="district" placeholder="区县" aria-label="区县"/>
      <select name="kind" aria-label="中心类型"><option value="">全部中心</option><option value="regional_management_center">区域管理中心</option><option value="public_welfare_service_center">公益服务中心</option></select>
      <input name="query" placeholder="名称或地址" aria-label="名称或地址"/><button type="submit">查找</button>
    </form><CenterCards items={centers}/>
    <form className="pwr-form" onSubmit={apply} aria-label="申请区域岗位">
      <fieldset><legend>申请成为区域负责人</legend>
        <label>申请角色<select required name="role"><option value="regional_director">主任</option><option value="regional_deputy_director">副主任</option></select></label>
        <div className="pwr-three"><label>省<input required name="province" /></label><label>市<input required name="city" /></label><label>区/县<input required name="district" /></label></div>
        <label>相关经历<textarea required name="experience" /></label><label>区域服务计划<textarea required name="service_plan" /></label>
        <label>可协调资源<textarea required name="resources" /></label><label>利益冲突声明<textarea required name="conflict_statement" /></label>
      </fieldset><button type="submit">提交岗位申请</button>
    </form>
    {message && <p role="status" className="pwr-message">{message}</p>}
    {roleItems.length > 0 && <ul className="pwr-status-list">{roleItems.map((item) => <li key={item.id}><strong>{item.role === "regional_director" ? "主任" : "副主任"} · {item.province}{item.city}{item.district}</strong><span>{statusLabels[item.status]}</span></li>)}</ul>}
  </section>;
}

type ReviewItem = { id: number; title: string; detail: string; kind: "establishment" | "role" };

function ManagementPage({ api }: { api: PublicWelfareRegionalApi }) {
  const [items, setItems] = useState<ReviewItem[]>([]); const [note, setNote] = useState(""); const [message, setMessage] = useState("");
  const refresh = useCallback(async () => {
    try {
      const [establishments, roles] = await Promise.all([api.listEstablishments("submitted"), api.listRegionalRoles("submitted")]);
      setItems([
        ...establishments.map((item): ReviewItem => ({ id: item.id, title: `公益创办：${item.name}`, detail: `${item.province}${item.city}${item.district} · ${item.mission}`, kind: "establishment" })),
        ...roles.map((item): ReviewItem => ({ id: item.id, title: `区域岗位：${item.role === "regional_director" ? "主任" : "副主任"}`, detail: `${item.province}${item.city}${item.district} · ${item.service_plan}`, kind: "role" })),
      ]);
    } catch (reason) { setMessage(errorMessage(reason)); }
  }, [api]);
  useEffect(() => { void refresh(); }, [refresh]);
  const review = async (item: ReviewItem, decision: ReviewDecision) => {
    try {
      if (item.kind === "establishment") await api.reviewEstablishment({ applicationId: item.id, decision, note });
      else await api.reviewRegionalRole({ applicationId: item.id, decision, note });
      setMessage(decision === "approved" ? "已批准并执行对应授权结果。" : "已驳回申请。"); setNote(""); await refresh();
    } catch (reason) { setMessage(errorMessage(reason)); }
  };
  return <section className="pwr-panel" aria-label="公益与区域审批中心"><header><p className="section-kicker">俱乐部联盟管理</p><h3>公益与区域审批</h3><p>批准公益申请会原子创建公益俱乐部；批准区域岗位会授予相应行政区域角色。两类操作均须记录审核意见。</p></header>
    <label>统一审核意见<textarea value={note} onChange={(event) => setNote(event.target.value)} /></label>
    {items.length === 0 ? <p className="pwr-empty">当前没有待审核申请。</p> : <ul className="pwr-review-list">{items.map((item) => <li key={`${item.kind}-${item.id}`}><div><strong>{item.title}</strong><p>{item.detail}</p></div><div><button disabled={!note.trim()} onClick={() => void review(item, "approved")} type="button">批准</button><button disabled={!note.trim()} onClick={() => void review(item, "rejected")} type="button">驳回</button></div></li>)}</ul>}
    {message && <p role="status" className="pwr-message">{message}</p>}
  </section>;
}

export function PublicWelfareRegionalPanel({ mode, api = publicWelfareRegionalApi }: Props) {
  if (mode === "public-welfare") return <PublicWelfareApplication api={api} />;
  if (mode === "regional-public") return <RegionalPublicPage api={api} />;
  return <ManagementPage api={api} />;
}
