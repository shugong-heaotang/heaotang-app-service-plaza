import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { MemoryRouter } from "react-router-dom";
import { MemberHomeShell, type MemberHomeModel } from "./MemberHomeShell";
import css from "./MemberHomeShell.css?inline";
const explore=[{actionId:"public-benefit-club",label:"公益俱乐部",href:"?category=公益俱乐部"},{actionId:"self-created-club",label:"自建俱乐部",href:"?category=自建俱乐部"},{actionId:"family-club",label:"家庭俱乐部",href:"?category=家庭俱乐部"},{actionId:"club-federation",label:"俱乐部友联体",href:"?category=俱乐部友联体"}];
const ready:MemberHomeModel={state:"ready",displayName:"合成会员",joinedClubCount:1,pendingTaskCount:1,unreadCount:2,clubs:[{clubId:"c1",name:"合成家庭俱乐部",kind:"家庭俱乐部",role:"成员",clubStatus:"active",membershipStatus:"active",href:"/clubs/c1"}],tasks:[{taskId:"t1",title:"确认活动",context:"今天",href:"/tasks/t1"}],activities:[{activityId:"a1",title:"公益活动",timeLabel:"周六",href:"/activities/a1"}],explore};
const renderShell=(model:MemberHomeModel)=>render(<MemberHomeShell model={model}/>,{wrapper:({children})=><MemoryRouter>{children}</MemoryRouter>});
describe("MemberHomeShell",()=>{
 it("renders separated club and membership status before exploration",()=>{renderShell(ready);const labels=[...document.querySelectorAll("[aria-label]")].map(x=>x.getAttribute("aria-label"));expect(labels.indexOf("我的俱乐部")).toBeLessThan(labels.indexOf("探索更多"));expect(screen.getByText("合成家庭俱乐部")).toBeInTheDocument();expect(screen.getByText(/俱乐部正常 · 会员有效/)).toBeInTheDocument();expect(screen.getAllByRole("link")).toHaveLength(7)});
 it("renders an optional suspended membership without treating it as club lifecycle",()=>{renderShell({...ready,clubs:[{...ready.clubs![0],membershipStatus:"suspended"}]});expect(screen.getByText(/俱乐部正常 · 会员停权/)).toBeInTheDocument()});
 it("renders new member empty state",()=>{renderShell({state:"empty",explore});expect(screen.getByText("您还没有加入俱乐部，可以从下方探索。")).toBeInTheDocument()});
 it("keeps partial failures local",()=>{renderShell({...ready,state:"partial-error",sectionErrors:{tasks:"待办暂时无法读取"}});expect(screen.getByRole("alert")).toHaveTextContent("待办暂时无法读取");expect(screen.getByText("合成家庭俱乐部")).toBeInTheDocument()});
 it.each([["loading","正在加载会员首页"],["unauthorized","登录后查看会员首页"],["maintenance","会员首页维护中"],["offline","会员首页暂未开放"],["error","会员首页暂时无法使用"]] as const)("renders %s",(state,title)=>{renderShell({state});expect(screen.getByRole(state==="error"?"alert":"status")).toHaveTextContent(title)});
 it("hides management from ordinary members",()=>{const {rerender}=renderShell(ready);expect(screen.queryByText("管理中心")).not.toBeInTheDocument();rerender(<MemberHomeShell model={{...ready,canManage:true}}/>);expect(screen.getByLabelText("俱乐部联盟管理附属入口")).toBeInTheDocument()});
 it("keeps internal links inside the deployed router basename",()=>{render(<MemoryRouter basename="/app/service-plaza" initialEntries={["/app/service-plaza/services/club-alliance"]}><MemberHomeShell model={{state:"empty",explore:[{actionId:"public-benefit-club",label:"公益俱乐部",href:"/services/club-alliance?category=公益俱乐部"}]}}/></MemoryRouter>);expect(screen.getByRole("link",{name:"公益俱乐部"})).toHaveAttribute("href","/app/service-plaza/services/club-alliance?category=公益俱乐部")});
 it("has no runtime network or mock fallback",()=>{const source=MemberHomeShell.toString();expect(source).not.toMatch(/fetch\(|mock|catch\s*\(/i)});
 it("declares 320 360 768 responsive and focus contracts",()=>{expect(css).toContain("@media (max-width:359px)");expect(css).toContain("@media (min-width:560px)");expect(css).toContain("@media (min-width:768px)");expect(css).toContain(":focus-visible");expect(css).toContain("min-width:0")});
});
