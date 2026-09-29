import { GoogleGenAI } from "@google/genai";
import { AI } from "@/config/app.config";
import { RoastRequest, RoastResult } from "@/types/roast";
import { ROAST_SYSTEM_INSTRUCTION, buildUserPrompt } from "./prompt";
import { roastResponseSchema } from "./schema";

function friendlyErrorMessage(status: number, error: any) {
  if (status === 400) return "Bad request. The code might be too long or malformed.";
  if (status === 403) return "GEMINI_API_KEY is invalid or missing permissions.";
  if (status === 404) return `Model ${AI.model} not found. Check AI.model in config.`;
  if (status === 429) return "Rate limit exceeded. Please wait a moment and try again.";
  if (status === 503) return "Gemini API is currently overloaded. Please try again later.";
  return `Gemini API error: ${error?.message || "Unknown error"}`;
}

export async function analyzeCode(request: RoastRequest): Promise<RoastResult> {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    throw new Error("GEMINI_API_KEY is missing. Copy .env.example to .env.local, add your key, and restart the server.");
  }

  const ai = new GoogleGenAI({ apiKey });
  const contents = buildUserPrompt(request);
  
  let attempt = 0;
  while (attempt < AI.maxAttempts) {
    try {
      const response = await ai.models.generateContent({
        model: AI.model,
        contents,
        config: {
          systemInstruction: ROAST_SYSTEM_INSTRUCTION,
          responseMimeType: "application/json",
          responseSchema: roastResponseSchema,
        }
      });
      
      if (!response.text) {
        throw new Error("Empty response from Gemini.");
      }
      
      let result;
      try {
        result = JSON.parse(response.text);
      } catch (e) {
        throw new Error("Failed to parse JSON response from Gemini.");
      }
      
      return {
        roast: result.roast ?? "",
        issues: Array.isArray(result.issues) ? result.issues : [],
        correctedCode: result.correctedCode ?? "",
        takeaway: result.takeaway ?? ""
      };
    } catch (error: any) {
      attempt++;
      const status = error?.status;
      if (status === 503 && attempt < AI.maxAttempts) {
        await new Promise(r => setTimeout(r, attempt * 1000));
        continue;
      }
      throw new Error(friendlyErrorMessage(status, error));
    }
  }
  throw new Error("Max retries exceeded.");
}
