import { RoastRequest, RoastResult } from "@/types/roast";

export async function requestRoast(payload: RoastRequest): Promise<RoastResult> {
  let response;
  try {
    response = await fetch("/api/roast", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  } catch (error) {
    throw new Error("Could not reach the server. Is `npm run dev` still running?");
  }
  
  const data = await response.json().catch(() => null);
  
  if (!response.ok || !data) {
    throw new Error(data?.error || `Server error (${response.status}).`);
  }
  
  return data as RoastResult;
}
