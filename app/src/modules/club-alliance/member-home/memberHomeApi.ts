import { ApiError, apiRequest } from "../../../infrastructure/apiClient";
import type { ExploreEntry, MemberActivity, MemberClub, MemberHomeModel, MemberTask } from "./MemberHomeShell";
export const memberHomeEndpoint="/api/v1/clubs/member-home" as const;
type Payload={display_name:unknown;joined_club_count:unknown;pending_task_count:unknown;unread_count:unknown;clubs:unknown;tasks:unknown;activities:unknown;feed:unknown;can_manage:unknown;section_errors?:unknown};
const obj=(v:unknown):v is Record<string,unknown>=>typeof v==="object"&&v!==null&&!Array.isArray(v);
const text=(v:unknown,n:string)=>{if(typeof v!=="string"||!v.trim())throw new ApiError(`${n} 无效`,200,"CMH_CONTRACT_INVALID");return v};
const count=(v:unknown,n:string)=>{if(!Number.isInteger(v)||Number(v)<0)throw new ApiError(`${n} 无效`,200,"CMH_CONTRACT_INVALID");return Number(v)};
const bool=(v:unknown,n:string)=>{if(typeof v!=="boolean")throw new ApiError(`${n} 无效`,200,"CMH_CONTRACT_INVALID");return v};
const list=(v:unknown,n:string)=>{if(!Array.isArray(v))throw new ApiError(`${n} 无效`,200,"CMH_CONTRACT_INVALID");return v};
const clubStatus=(v:unknown):MemberClub["clubStatus"]=>{const value=text(v,"club_status");if(value!=="active")throw new ApiError("club_status 无效",200,"CMH_CONTRACT_INVALID");return value};
const membershipStatus=(v:unknown):MemberClub["membershipStatus"]=>{const value=text(v,"membership_status");if(value!=="active"&&value!=="suspended")throw new ApiError("membership_status 无效",200,"CMH_CONTRACT_INVALID");return value};
export function mapMemberHomePayload(raw:unknown,explore:readonly ExploreEntry[]):MemberHomeModel{
 if(!obj(raw))throw new ApiError("会员首页响应无效",200,"CMH_CONTRACT_INVALID");const p=raw as Payload;
 const clubs:MemberClub[]=list(p.clubs,"clubs").map((v)=>{if(!obj(v))throw new ApiError("club 无效",200,"CMH_CONTRACT_INVALID");if("status" in v)throw new ApiError("旧 status 字段不再接受",200,"CMH_CONTRACT_INVALID");const kind=text(v.kind,"kind");if(!["公益俱乐部","自建俱乐部","家庭俱乐部"].includes(kind))throw new ApiError("kind 无效",200,"CMH_CONTRACT_INVALID");return{clubId:text(v.club_id,"club_id"),name:text(v.name,"name"),kind:kind as MemberClub["kind"],role:text(v.member_role,"member_role"),clubStatus:clubStatus(v.club_status),membershipStatus:membershipStatus(v.membership_status),href:text(v.target,"target")}});
 const tasks:MemberTask[]=list(p.tasks,"tasks").map(v=>{if(!obj(v))throw new ApiError("task 无效",200,"CMH_CONTRACT_INVALID");return{taskId:text(v.task_id,"task_id"),title:text(v.title,"title"),context:text(v.context,"context"),href:text(v.target,"target")}});
 const activities:MemberActivity[]=list(p.activities,"activities").map(v=>{if(!obj(v))throw new ApiError("activity 无效",200,"CMH_CONTRACT_INVALID");return{activityId:text(v.activity_id,"activity_id"),title:text(v.title,"title"),timeLabel:text(v.time_label,"time_label"),href:text(v.target,"target")}});
 const feed=list(p.feed,"feed").map(v=>{if(!obj(v))throw new ApiError("feed 无效",200,"CMH_CONTRACT_INVALID");return{itemId:text(v.item_id,"item_id"),title:text(v.title,"title"),href:text(v.target,"target")}});
 const sectionErrors:MemberHomeModel["sectionErrors"]={};
 if(p.section_errors!==undefined){
  if(!obj(p.section_errors))throw new ApiError("section_errors 无效",200,"CMH_CONTRACT_INVALID");
  const messages:Record<string,string>={tasks:"待办暂时无法读取",activities:"最近活动暂时无法读取",feed:"联盟动态暂时无法读取"};
  for(const key of Object.keys(p.section_errors)){
   if(!(key in messages)||typeof p.section_errors[key]!=="string")throw new ApiError("section_errors 无效",200,"CMH_CONTRACT_INVALID");
   sectionErrors[key as keyof typeof sectionErrors]=messages[key];
  }
 }
 const partial=Object.keys(sectionErrors).length>0;
 return{state:partial?"partial-error":clubs.length||tasks.length||activities.length?"ready":"empty",displayName:text(p.display_name,"display_name"),joinedClubCount:count(p.joined_club_count,"joined_club_count"),pendingTaskCount:count(p.pending_task_count,"pending_task_count"),unreadCount:count(p.unread_count,"unread_count"),clubs,tasks,activities,feed,explore,sectionErrors,canManage:bool(p.can_manage,"can_manage")};
}
export async function loadMemberHome(explore:readonly ExploreEntry[],signal?:AbortSignal){const data=await apiRequest<unknown>(memberHomeEndpoint,{}, {auth:true,envelope:"strict",retry:{mode:"safe-method",maxAttempts:2},signal});return mapMemberHomePayload(data,explore)}
