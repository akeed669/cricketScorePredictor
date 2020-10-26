import http from "./httpService";
import { apiUrl } from "../config.json";

export function getSelectValues() {
  return http.get(apiUrl + "/listdata");
}

export function predictScore(match) {
  return http.post(apiUrl + "/predict", match);
}



