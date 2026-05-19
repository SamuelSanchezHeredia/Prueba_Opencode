export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

export async function postForm<T>(path: string, body: FormData): Promise<T | null> {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    body,
  });

  if (!response.ok) {
    return null;
  }

  return response.json();
}

export async function postJson<T>(path: string, payload: unknown): Promise<T | null> {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    return null;
  }

  return response.json();
}
