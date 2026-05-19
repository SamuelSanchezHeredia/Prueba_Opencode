import { postForm, postJson } from "./client";
import { AnalysisResult, ChatResponse, SessionStartResponse } from "../model/types";

export async function startSession(file: File, target_sector: string) {
  const payload = new FormData();
  payload.append("file", file);
  payload.append("target_sector", target_sector);
  return postForm<SessionStartResponse>("/session/start", payload);
}

export async function analyzeCv(session_id: string) {
  const payload = new FormData();
  payload.append("session_id", session_id);
  return postForm<AnalysisResult>("/session/analyze", payload);
}

export async function askFaq(message: string, session_id?: string) {
  return postJson<ChatResponse>("/chat", { message, session_id });
}
