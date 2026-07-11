import { ApiError, apiRequest } from "../../../infrastructure/apiClient";
import type { ExploreEntry, MemberActivity, MemberClub, MemberHomeModel, MemberTask } from "./MemberHomeShell";
export const memberHomeEndpoint="/api/v1/clubs/member-home" as const;
type Payload={display_name:unknown;joined_club_count:unknown;pending_task_count:unknown;unread_count:unknown;clubs:unknown;tasks:unknown;activities:unknown;feed:unknown};
const obj=(v:unknown):v is Record<string,unknown>=>typeof v==="object"&&v!==null&&!Array.isArray(v);
const text=(v:unknown,n:string)=>{if(typeof v!=="string"||!v.trim())throw new ApiError(`${n} 无效`,200,"CMH_CONTRACT_INVALID");return v};
const count=(v:unknown,n:string)=>{if(!Number.isInteger(v)||Number(v)<0)throw new ApiError(`${n} 无效`,200,"CMH_CONTRACT_INVALID");return Number(v)};
const list=(v:unknown,n:string)=>{if(!Array.isArray(v))throw new ApiError(`${n} 无效`,200,"CMH_CONTRACT_INVALID");return v};
export function mapMemberHomePayload(raw:unknown,explore:readonly ExploreEntry[]):MemberHomeModel{
 if(!obj(raw))throw new ApiError("会员首页响应无效",200,"CMH_CONTRACT_INVALID");const p=raw as Payload;
 const clubs:MemberClub[]=list(p.clubs,"clubs").map((v)=>{if(!obj(v))throw new ApiError("club 无效",200,"CMH_CONTRACT_INVALID");const kind=text(v.kind,"kind");if(!["公益俱乐部","自建俱乐部","家庭俱乐部"].includes(kind))throw new ApiError("kind 无效",200,"CMH_CONTRACT_INVALID");return{clubId:text(v.club_id,"club_id"),name:text(v.name,"name"),kind:kind as MemberClub["kind"],role:text(v.member_role,"member_role"),status:text(v.status,"status"),href:text(v.target,"target")}});
 const tasks:MemberTask[]=list(p.tasks,"tasks").map(v=>{if(!obj(v))throw new ApiError("task 无效",200,"CMH_CONTRACT_INVALID");return{taskId:text(v.task_id,"task_id"),title:text(v.title,"title"),context:text(v.context,"context"),href:text(v.target,"target")}});
 const activities:MemberActivity[]=list(p.activities,"activities").map(v=>{if(!obj(v))throw new ApiError("activity 无效",200,"CMH_CONTRACT_INVALID");return{activityId:text(v.activity_id,"activity_id"),title:text(v.title,"title"),timeLabel:text(v.time_label,"time_label"),href:text(v.target,"target")}});
 const feed=list(p.feed,"feed").map(v=>{if(!obj(v))throw new ApiError("feed 无效",200,"CMH_CONTRACT_INVALID");return{itemId:text(v.item_id,"item_id"),title:text(v.title,"title"),href:text(v.target,"target")}});
 return{state:clubs.length||tasks.length||activities.length?"ready":"empty",displayName:text(p.display_name,"display_name"),joinedClubCount:count(p.joined_club_count,"joined_club_count"),pendingTaskCount:count(p.pending_task_count,"pending_task_count"),unreadCount:count(p.unread_count,"unread_count"),clubs,tasks,activities,feed,explore};
}
export async function loadMemberHome(explore:readonly ExploreEntry[],signal?:AbortSignal){const data=await apiRequest<unknown>(memberHomeEndpoint,{}, {auth:true,envelope:"strict",retry:{mode:"safe-method",maxAttempts:2},signal});return mapMemberHomePayload(data,explore)}
