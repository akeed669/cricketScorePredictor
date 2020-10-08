import http from "./httpService";
import { apiUrl } from "../config.json";

export function getBattingTeams() {
  return http.get(apiUrl + "/batTeams");
}
