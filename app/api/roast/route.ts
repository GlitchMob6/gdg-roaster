import { NextRequest, NextResponse } from "next/server";
import { analyzeCode } from "@/lib/gemini";
import { LANGUAGES, ROAST_LEVELS, DEFAULTS, LIMITS } from "@/config/app.config";
import { LanguageId, RoastLevel } from "@/types/roast";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    let { code = "", errorMessage = "", language = "", roastLevel = "" } = body;
    
    code = String(code);
    errorMessage = String(errorMessage).trim();
    
    if (!code) {
      return NextResponse.json({ error: "No code provided." }, { status: 400 });
    }
    if (code.length > LIMITS.maxCodeLength) {
      return NextResponse.json({ error: `Code exceeds max length of ${LIMITS.maxCodeLength} chars.` }, { status: 400 });
    }
    if (errorMessage.length > LIMITS.maxErrorMessageLength) {
      return NextResponse.json({ error: `Error message exceeds max length of ${LIMITS.maxErrorMessageLength} chars.` }, { status: 400 });
    }
    
    const validLang = LANGUAGES.find(l => l.id === language) ? (language as LanguageId) : DEFAULTS.language;
    const validRoast = ROAST_LEVELS.find(r => r.id === roastLevel) ? (roastLevel as RoastLevel) : DEFAULTS.roastLevel;
    
    const result = await analyzeCode({
      code,
      errorMessage,
      language: validLang,
      roastLevel: validRoast
    });
    
    return NextResponse.json(result, { status: 200 });
  } catch (error: any) {
    console.error("Roast API Error:", error);
    return NextResponse.json({ error: error?.message || "Internal Server Error" }, { status: 500 });
  }
}
