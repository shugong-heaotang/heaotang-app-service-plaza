import { useParams } from "react-router-dom";
import {
  SelfCreatedClubPage,
  type SelfCreatedClubPageMode,
} from "./SelfCreatedClubPage";
import {
  selfCreatedClubApi,
  type SelfCreatedClubApi,
} from "./selfCreatedClubApi";

export type SelfCreatedClubRouteProps = {
  mode: SelfCreatedClubPageMode;
  api?: SelfCreatedClubApi;
};

export function SelfCreatedClubRoute({
  mode,
  api = selfCreatedClubApi,
}: SelfCreatedClubRouteProps) {
  const { clubId } = useParams();
  return <SelfCreatedClubPage api={api} clubId={clubId} mode={mode} />;
}
