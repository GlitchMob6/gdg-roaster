import os

files = {
    'package.json': '''{
  "name": "code-roaster",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "check:api": "tsx --env-file=.env.local scripts/check-api.ts"
  },
  "dependencies": {
    "next": "15.0.0",
    "react": "19.0.0-rc-69d4b800-20241021",
    "react-dom": "19.0.0-rc-69d4b800-20241021",
    "tailwindcss": "^4.0.0",
    "@tailwindcss/postcss": "^4.0.0",
    "postcss": "^8",
    "@google/genai": "latest",
    "lucide-react": "latest",
    "clsx": "latest",
    "tailwind-merge": "latest"
  },
  "devDependencies": {
    "typescript": "latest",
    "@types/node": "latest",
    "@types/react": "npm:types-react@19.0.0-rc.1",
    "@types/react-dom": "npm:types-react-dom@19.0.0-rc.1",
    "eslint": "latest",
    "eslint-config-next": "15.0.0",
    "tsx": "latest"
  }
}''',
    'tsconfig.json': '''{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}''',
    'next.config.mjs': '''/** @type {import('next').NextConfig} */
const nextConfig = {};
export default nextConfig;
''',
    '.gitignore': '''node_modules
.next
.env.local
.env.development.local
.env.test.local
.env.production.local
''',
    '.env.example': '''# Get your API key at https://aistudio.google.com/apikey
GEMINI_API_KEY=
''',
    'app/globals.css': '''@import "tailwindcss";

@theme {
  --font-space-grotesk: var(--font-space-grotesk);
  --font-jetbrains-mono: var(--font-jetbrains-mono);
  
  --color-frame: #111111;
  --color-canvas: #F5F5F3;
  --color-panel: #FDFDFD;
  --color-subtle: #E6E6E2;
  --color-accent: #D94826;
}

@theme inline {
  --color-frame: #111111;
  --color-canvas: #F5F5F3;
  --color-panel: #FDFDFD;
  --color-subtle: #E6E6E2;
  --color-accent: #D94826;
}

body {
  background-color: var(--color-canvas);
  background-image: linear-gradient(rgba(17, 17, 17, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(17, 17, 17, 0.05) 1px, transparent 1px);
  background-size: 24px 24px;
}

::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: var(--color-subtle);
}
::-webkit-scrollbar-thumb {
  background: var(--color-frame);
  border-radius: 4px;
}
''',
    'app/layout.tsx': '''import type { Metadata } from "next";
import { Space_Grotesk, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { APP } from "@/config/app.config";

const spaceGrotesk = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-space-grotesk",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
});

export const metadata: Metadata = {
  title: `${APP.name} — AI Code Critique`,
  description: APP.tagline,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${spaceGrotesk.variable} ${jetbrainsMono.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col font-sans">
        {children}
      </body>
    </html>
  );
}
''',
    'app/page.tsx': '''import Workspace from "@/components/Workspace";

export default function Home() {
  return (
    <div className="flex-1 flex items-center justify-center p-4 sm:p-6 lg:p-8">
      <Workspace />
    </div>
  );
}
''',
    'config/app.config.ts': '''export const APP = { name: "Code Roaster", version: "v3", tagline: "Your code. Our problem now." };
export const AI = { model: "gemini-3.5-flash-lite", modelLabel: "Gemini 3.5 Flash-Lite", maxAttempts: 3 };

export const ROAST_LEVELS = [
  { id: "dry", label: "Dry", description: "Mild and deadpan. Gentle jabs, mostly helpful." },
  { id: "sharp", label: "Sharp", description: "Pointed and witty. Calls out every mistake directly." },
  { id: "savage", label: "Savage", description: "Maximum burn. Brutally honest, but still technically accurate." }
] as const;

export const LANGUAGES = [
  { id: "python", label: "Python", extension: "py" },
  { id: "javascript", label: "JavaScript", extension: "js" },
  { id: "typescript", label: "TypeScript", extension: "ts" },
  { id: "java", label: "Java", extension: "java" },
  { id: "c", label: "C", extension: "c" },
  { id: "cpp", label: "C++", extension: "cpp" },
  { id: "go", label: "Go", extension: "go" },
  { id: "rust", label: "Rust", extension: "rs" }
] as const;

export const DEFAULTS = { language: "python", roastLevel: "savage" } as const;
export const SEVERITIES = ["FATAL BUG", "CODE SMELL", "OPTIMIZATION"] as const;
export const LIMITS = { maxCodeLength: 20000, maxErrorMessageLength: 4000 };

export const SAMPLE = { 
  language: "python", 
  code: `def average_numbers(numbers):\\n    total = 0\\n    for number in numbers:\\n        total += numbers # Oops!\\n    return total / len(numbers)\\n\\naverage_numbers([1, 2, 3, 4, 5])`
} as const;
''',
    'types/roast.ts': '''import { ROAST_LEVELS, LANGUAGES, SEVERITIES } from "@/config/app.config";

export type LanguageId = typeof LANGUAGES[number]["id"];
export type RoastLevel = typeof ROAST_LEVELS[number]["id"];
export type Severity = typeof SEVERITIES[number];

export interface RoastRequest {
  language: LanguageId;
  code: string;
  roastLevel: RoastLevel;
  errorMessage?: string;
}

export interface RoastIssue {
  line: number;
  severity: Severity;
  title: string;
  codeSnippet: string;
  diagnosis: string;
  expected: string;
}

export interface RoastResult {
  roast: string;
  issues: RoastIssue[];
  correctedCode: string;
  takeaway: string;
}

export type ReportState = "empty" | "loading" | "results" | "error";
''',
    'lib/prompt.ts': '''import { ROAST_LEVELS } from "@/config/app.config";
import { RoastRequest } from "@/types/roast";

const roastLevelGuide = ROAST_LEVELS.map(l => `- ${l.id}: ${l.description}`).join("\\n");

export const ROAST_SYSTEM_INSTRUCTION = `You are a Code Roaster. Your job is to analyze user-submitted code and provide a structured critique.
Personality: observational, concise, deadpan, technically grounded, spontaneous; understandable to college students but never condescending; funny like a senior roasting a junior in the college lab — witty, never insulting the person, only the code.
Language and style (very important): write in Hinglish — Hindi words written in English/Roman letters, mixed naturally with simple English. Example verbatim: "Bhai, yeh loop har baar poori list add kar raha hai 😅. Python bhi soch raha hoga ki kya chal raha hai 🤦". Never use Devanagari script, only Roman letters. Short, simple sentences — students aren't fluent in English. Keep technical terms in English (loop, variable, function, list, TypeError, etc.) so students learn the real terms. Add emojis (😂 🔥 💀 🤦 😅 ✅ 🚀), roughly 1-3 per text field, don't overdo it. Use Hinglish + emojis ONLY in "roast", "title", "diagnosis", "expected", "takeaway". Do NOT use Hinglish or emojis inside "codeSnippet" or "correctedCode" — those must be valid code; comments in correctedCode may be short simple English.
Adjust the intensity of the 'roast' text to the requested roast level:
${roastLevelGuide}
Analyze the code for: fatal bugs/logic errors/syntax issues, performance bottlenecks, architectural smells, best practices violations.
Rules for the response: "line" is the 1-based line number where the issue appears; "severity" must be exactly one of the SEVERITIES values (always English, no emojis); "codeSnippet" is the exact problematic code copied from the submission; list the most serious issues first, empty issues array if none found; "correctedCode" is the complete fixed program in the same language, plain code with no markdown fences; keep technical explanations accurate even when the roast is harsh.
Return a JSON object conforming exactly to the requested schema.`;

export function buildUserPrompt({ language, code, roastLevel, errorMessage }: RoastRequest) {
  const parts = [
    `Language: ${language}`,
    `Roast Level: ${roastLevel}`
  ];
  if (errorMessage) {
    parts.push(`Error Message:\\n${errorMessage}`);
  }
  parts.push(`Code:\\n\`\`\`${language}\\n${code}\\n\`\`\``);
  return parts.filter(Boolean).join("\\n\\n");
}
''',
    'lib/schema.ts': '''import { Type, Schema } from "@google/genai";
import { SEVERITIES } from "@/config/app.config";

export const roastResponseSchema: Schema = {
  type: Type.OBJECT,
  properties: {
    roast: { type: Type.STRING },
    issues: {
      type: Type.ARRAY,
      items: {
        type: Type.OBJECT,
        properties: {
          line: { type: Type.INTEGER },
          severity: { type: Type.STRING, enum: Array.from(SEVERITIES) },
          title: { type: Type.STRING },
          codeSnippet: { type: Type.STRING },
          diagnosis: { type: Type.STRING },
          expected: { type: Type.STRING }
        },
        required: ["line", "severity", "title", "codeSnippet", "diagnosis", "expected"]
      }
    },
    correctedCode: { type: Type.STRING },
    takeaway: { type: Type.STRING }
  },
  required: ["roast", "issues", "correctedCode", "takeaway"]
};
''',
    'lib/gemini.ts': '''import { GoogleGenAI } from "@google/genai";
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
''',
    'scripts/check-api.ts': '''import { analyzeCode } from "../lib/gemini";
import { AI, SAMPLE } from "../config/app.config";

async function main() {
  console.log(`Checking API with model ${AI.model}...`);
  try {
    const result = await analyzeCode({
      language: SAMPLE.language,
      code: SAMPLE.code,
      roastLevel: "sharp",
      errorMessage: "TypeError: unsupported operand type(s) for +=: 'int' and 'list'"
    });
    console.log("Success! Roast:");
    console.log(result.roast);
    console.log(`Found ${result.issues.length} issues.`);
    process.exit(0);
  } catch (error) {
    console.error("Failed to check API:", error);
    process.exit(1);
  }
}

main();
''',
    'app/api/roast/route.ts': '''import { NextRequest, NextResponse } from "next/server";
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
''',
    'lib/api.ts': '''import { RoastRequest, RoastResult } from "@/types/roast";

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
''',
    'components/Workspace.tsx': '''"use client";

import { useState, useCallback, useEffect } from "react";
import { ReportState, RoastResult, LanguageId, RoastLevel } from "@/types/roast";
import { DEFAULTS, SAMPLE } from "@/config/app.config";
import { requestRoast } from "@/lib/api";
import TopBar from "./TopBar";
import RoastControls from "./RoastControls";
import ErrorMessageInput from "./ErrorMessageInput";
import CodeEditor from "./CodeEditor";
import RoastReport from "./RoastReport";
import StatusBar from "./StatusBar";

export default function Workspace() {
  const [roastLevel, setRoastLevel] = useState<RoastLevel>(DEFAULTS.roastLevel);
  const [language, setLanguage] = useState<LanguageId>(DEFAULTS.language);
  const [code, setCode] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [errorDrawerOpen, setErrorDrawerOpen] = useState(false);
  const [reportState, setReportState] = useState<ReportState>("empty");
  const [roastResult, setRoastResult] = useState<RoastResult | null>(null);
  const [roastedCode, setRoastedCode] = useState("");
  const [apiError, setApiError] = useState("");

  const isRoasting = reportState === "loading";

  const handleRoast = useCallback(async () => {
    if (isRoasting) return;
    if (!code.trim()) {
      setApiError("No code provided. I can't roast the void.");
      setReportState("error");
      return;
    }
    
    setReportState("loading");
    setRoastResult(null);
    setApiError("");
    
    try {
      const result = await requestRoast({ language, code, roastLevel, errorMessage: errorDrawerOpen ? errorMessage : "" });
      setRoastedCode(code);
      setRoastResult(result);
      setReportState("results");
    } catch (error: any) {
      setApiError(error.message || "An unknown error occurred.");
      setReportState("error");
    }
  }, [code, language, roastLevel, errorMessage, errorDrawerOpen, isRoasting]);

  const handleLoadSample = () => {
    setLanguage(SAMPLE.language);
    setCode(SAMPLE.code);
  };

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        handleRoast();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [handleRoast]);

  const errorLine = (reportState === "results" && code === roastedCode && roastResult?.issues?.[0]?.line) || undefined;

  return (
    <main className="w-full max-w-[1360px] h-[calc(100vh-4rem)] min-h-[600px] border-[2px] border-[var(--color-frame)] shadow-[4px_4px_0_var(--color-frame)] flex flex-col overflow-hidden bg-[var(--color-panel)] rounded-[22px]">
      <TopBar>
        <RoastControls 
          roastLevel={roastLevel}
          onRoastLevelChange={setRoastLevel}
          language={language}
          onLanguageChange={setLanguage}
          onRoast={handleRoast}
          isRoasting={isRoasting}
          errorDrawerOpen={errorDrawerOpen}
          onToggleErrorDrawer={() => setErrorDrawerOpen(!errorDrawerOpen)}
        />
      </TopBar>
      
      {errorDrawerOpen && (
        <ErrorMessageInput 
          value={errorMessage}
          onChange={setErrorMessage}
          onClose={() => setErrorDrawerOpen(false)}
        />
      )}
      
      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden min-h-0">
        <div className="w-full lg:w-[55%] border-b-[2px] lg:border-b-0 lg:border-r-[2px] border-[var(--color-frame)] flex flex-col">
          <CodeEditor 
            code={code}
            onChange={setCode}
            language={language}
            errorLine={errorLine}
            onLoadSample={handleLoadSample}
          />
        </div>
        <div className="w-full lg:w-[45%] flex flex-col overflow-y-auto">
          <RoastReport 
            state={reportState}
            roastLevel={roastLevel}
            language={language}
            result={roastResult}
            errorMsg={apiError}
            onRetry={handleRoast}
            onApplyFix={setCode}
          />
        </div>
      </div>
      
      <StatusBar isRoasting={isRoasting} />
    </main>
  );
}
''',
    'components/TopBar.tsx': '''import { APP } from "@/config/app.config";

export default function TopBar({ children }: { children: React.ReactNode }) {
  return (
    <header className="border-b-[2px] border-[var(--color-frame)] bg-[var(--color-panel)] flex flex-col lg:flex-row justify-between items-center p-3 lg:p-4 gap-4">
      <div className="flex items-center gap-3">
        <span className="font-bold uppercase tracking-[0.2em] font-[family-name:var(--font-space-grotesk)] text-xl">{APP.name}</span>
        <span className="text-xs border-[2px] border-[var(--color-frame)] rounded-full px-2 py-0.5 font-bold font-mono bg-[var(--color-canvas)]">{APP.version}</span>
      </div>
      <div className="flex flex-row items-center font-[family-name:var(--font-jetbrains-mono)] text-sm gap-2">
        {children}
      </div>
    </header>
  );
}
''',
    'components/RoastControls.tsx': '''import { ROAST_LEVELS, LANGUAGES } from "@/config/app.config";
import { RoastLevel, LanguageId } from "@/types/roast";

interface Props {
  roastLevel: RoastLevel;
  onRoastLevelChange: (l: RoastLevel) => void;
  language: LanguageId;
  onLanguageChange: (l: LanguageId) => void;
  onRoast: () => void;
  isRoasting: boolean;
  errorDrawerOpen: boolean;
  onToggleErrorDrawer: () => void;
}

export default function RoastControls({
  roastLevel, onRoastLevelChange, language, onLanguageChange, onRoast, isRoasting, errorDrawerOpen, onToggleErrorDrawer
}: Props) {
  return (
    <div className="flex flex-wrap items-center gap-4 text-sm w-full justify-end font-[family-name:var(--font-jetbrains-mono)]">
      <div className="flex items-center gap-2">
        <span className="font-bold text-xs uppercase tracking-widest">Roast Level:</span>
        <div className="flex bg-[var(--color-canvas)] border-[2px] border-[var(--color-frame)] rounded-full p-1 shadow-[2px_2px_0_var(--color-frame)]">
          {ROAST_LEVELS.map(l => (
            <button
              key={l.id}
              title={l.description}
              onClick={() => onRoastLevelChange(l.id)}
              className={`px-3 py-1 rounded-full font-bold transition-colors ${roastLevel === l.id ? "bg-[var(--color-accent)] text-[var(--color-panel)]" : "hover:bg-[var(--color-subtle)]"}`}
            >
              {l.label}
            </button>
          ))}
        </div>
      </div>
      
      <div className="flex items-center gap-2">
        <span className="font-bold text-xs uppercase tracking-widest">Language:</span>
        <select
          value={language}
          onChange={e => onLanguageChange(e.target.value as LanguageId)}
          className="appearance-none bg-[var(--color-panel)] border-[2px] border-[var(--color-frame)] rounded-full px-3 py-1.5 font-bold font-mono shadow-[2px_2px_0_var(--color-frame)] pr-8 cursor-pointer relative focus:outline-none"
        >
          {LANGUAGES.map(l => (
            <option key={l.id} value={l.id}>{l.label}</option>
          ))}
        </select>
      </div>

      <button
        onClick={onToggleErrorDrawer}
        className="border-[2px] border-dashed border-[var(--color-frame)] px-3 py-1.5 rounded-full font-bold hover:bg-[var(--color-canvas)] transition-colors"
      >
        {errorDrawerOpen ? "− ERROR MESSAGE" : "+ ERROR MESSAGE"}
      </button>

      <button
        onClick={onRoast}
        disabled={isRoasting}
        className={`flex items-center gap-2 px-6 py-2 rounded-full border-[3px] border-[var(--color-frame)] shadow-[4px_4px_0_var(--color-frame)] font-bold uppercase transition-all ${isRoasting ? "bg-[var(--color-frame)] text-[var(--color-panel)] animate-pulse shadow-[1px_1px_0_var(--color-frame)] translate-y-[3px] translate-x-[3px]" : "bg-[var(--color-frame)] text-[var(--color-panel)] hover:translate-x-[-1px] hover:translate-y-[-1px] active:translate-y-[3px] active:translate-x-[3px] active:shadow-[1px_1px_0_var(--color-frame)]"}`}
      >
        {isRoasting ? "ANALYZING..." : "ROAST MY CODE"}
        {!isRoasting && <span className="bg-white/20 text-white px-2 py-0.5 rounded text-xs ml-1 border border-white/30">Ctrl ⏎</span>}
      </button>
    </div>
  );
}
''',
    'components/ErrorMessageInput.tsx': '''interface Props {
  value: string;
  onChange: (v: string) => void;
  onClose: () => void;
}

export default function ErrorMessageInput({ value, onChange, onClose }: Props) {
  return (
    <div className="border-b-[2px] border-[var(--color-frame)] bg-[var(--color-canvas)] p-3 lg:p-4">
      <div className="flex justify-between items-center mb-2">
        <span className="font-bold text-xs uppercase font-[family-name:var(--font-jetbrains-mono)] tracking-widest text-[var(--color-accent)]">Attach Terminal Traceback / Compiler Error (Optional)</span>
        <button onClick={onClose} className="font-bold text-xs hover:underline">Dismiss ✕</button>
      </div>
      <textarea
        value={value}
        onChange={e => onChange(e.target.value)}
        placeholder="TypeError: unsupported operand type(s) for +=: 'int' and 'list'\\n  File \\"main.py\\", line 4, in average_numbers..."
        className="w-full border-[2px] border-[var(--color-frame)] p-3 font-[family-name:var(--font-jetbrains-mono)] text-sm resize-none focus:outline-none focus:shadow-[2px_2px_0_var(--color-frame)] bg-[var(--color-panel)]"
        rows={2}
      />
    </div>
  );
}
''',
    'components/CodeEditor.tsx': '''"use client";

import { useRef, useState } from "react";
import { LanguageId } from "@/types/roast";
import { LANGUAGES } from "@/config/app.config";

interface Props {
  code: string;
  onChange: (c: string) => void;
  language: LanguageId;
  errorLine?: number;
  onLoadSample: () => void;
}

export default function CodeEditor({ code, onChange, language, errorLine, onLoadSample }: Props) {
  const [cursor, setCursor] = useState({ line: 1, col: 1 });
  const gutterRef = useRef<HTMLDivElement>(null);
  
  const langLabel = LANGUAGES.find(l => l.id === language)?.label || language;
  const lines = code.split("\\n");
  const numLines = Math.max(lines.length, 10);

  const handleScroll = (e: React.UIEvent<HTMLTextAreaElement>) => {
    if (gutterRef.current) {
      gutterRef.current.scrollTop = e.currentTarget.scrollTop;
    }
  };

  const handleSelect = (e: React.SyntheticEvent<HTMLTextAreaElement>) => {
    const el = e.currentTarget;
    const textBefore = el.value.substring(0, el.selectionStart);
    const lineSplit = textBefore.split("\\n");
    setCursor({
      line: lineSplit.length,
      col: lineSplit[lineSplit.length - 1].length + 1
    });
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Tab" && !e.shiftKey) {
      e.preventDefault();
      const el = e.currentTarget;
      const start = el.selectionStart;
      const end = el.selectionEnd;
      const newText = code.substring(0, start) + "    " + code.substring(end);
      onChange(newText);
      
      requestAnimationFrame(() => {
        el.selectionStart = el.selectionEnd = start + 4;
      });
    }
  };

  return (
    <div className="flex flex-col h-full bg-[var(--color-panel)] relative font-[family-name:var(--font-jetbrains-mono)]">
      <div className="h-10 border-b-[2px] border-[var(--color-frame)] bg-[var(--color-canvas)] flex items-center justify-between px-4 shrink-0">
        <span className="text-xs uppercase font-bold text-[var(--color-frame)]/50 tracking-widest">INPUT // SRC</span>
        <span className="text-sm font-bold">Your Code</span>
        <div className="text-xs font-bold gap-3 flex text-[var(--color-accent)]">
          <button onClick={onLoadSample} className="hover:underline">SAMPLE BUG</button>
          <span className="text-[var(--color-frame)]">|</span>
          <button onClick={() => onChange("")} className="hover:underline">CLEAR</button>
        </div>
      </div>
      
      <div className="flex-1 flex overflow-hidden relative">
        <div 
          ref={gutterRef}
          className="w-12 shrink-0 bg-[var(--color-canvas)] border-r-[2px] border-[var(--color-frame)] overflow-hidden text-right pr-2 py-4 select-none text-sm leading-6 text-[var(--color-frame)]/40"
        >
          {Array.from({ length: numLines }).map((_, i) => (
            <div 
              key={i} 
              className={errorLine === i + 1 ? "text-[var(--color-accent)] font-bold bg-[var(--color-accent)]/10" : ""}
            >
              {i + 1}
            </div>
          ))}
        </div>
        
        <textarea
          value={code}
          onChange={e => onChange(e.target.value)}
          onScroll={handleScroll}
          onSelect={handleSelect}
          onKeyDown={handleKeyDown}
          spellCheck={false}
          placeholder="// Paste your code here..."
          className="flex-1 p-4 resize-none text-sm leading-6 whitespace-pre overflow-auto focus:outline-none bg-transparent"
        />
      </div>

      <div className="hidden md:flex h-8 shrink-0 bg-[var(--color-frame)] text-[var(--color-panel)] text-xs items-center justify-between px-4 absolute bottom-0 left-0 right-0 z-10 opacity-90">
        <span>Ln {cursor.line}, Col {cursor.col} · {langLabel}</span>
        <span>UTF-8 · Tab Size: 4</span>
      </div>
    </div>
  );
}
''',
    'components/SectionHeader.tsx': '''interface Props {
  number: number;
  title: string;
  children?: React.ReactNode;
}

export default function SectionHeader({ number, title, children }: Props) {
  const numStr = number.toString().padStart(2, "0");
  return (
    <div className="flex justify-between items-center border-b-[2px] border-[var(--color-frame)] pb-2 mb-4 mt-6 first:mt-0 font-[family-name:var(--font-jetbrains-mono)]">
      <span className="font-bold uppercase tracking-widest text-sm text-[var(--color-frame)]">
        {numStr} // {title}
      </span>
      {children && <div>{children}</div>}
    </div>
  );
}
''',
    'components/IssueCard.tsx': '''import { RoastIssue } from "@/types/roast";

interface Props {
  index: number;
  issue: RoastIssue;
}

export default function IssueCard({ index, issue }: Props) {
  const isFatal = issue.severity === "FATAL BUG";
  const isSmell = issue.severity === "CODE SMELL";
  
  const badgeColor = isFatal ? "bg-[#D9503F] text-white" : isSmell ? "bg-[#EDB13E] text-black" : "bg-[#4FA35A] text-white";
  
  const numStr = (index + 1).toString().padStart(2, "0");

  return (
    <div className="border-[2px] border-[var(--color-frame)] rounded-[14px] p-4 mb-4 shadow-[2px_2px_0_var(--color-frame)] bg-[var(--color-panel)] relative overflow-hidden">
      <div className={`absolute top-0 left-0 bottom-0 w-2 ${isFatal ? 'bg-[#D9503F]' : isSmell ? 'bg-[#EDB13E]' : 'bg-[#4FA35A]'}`}></div>
      <div className="pl-4 font-[family-name:var(--font-jetbrains-mono)]">
        <div className="flex justify-between items-start mb-3">
          <div className="flex items-center gap-2">
            <span className="bg-[var(--color-frame)] text-[var(--color-panel)] font-bold px-2 py-0.5 text-xs rounded">{numStr}</span>
            <span className="font-bold">LINE {issue.line}</span>
            <span className={`text-xs font-bold px-2 py-0.5 rounded border-[2px] border-[var(--color-frame)] ${badgeColor}`}>{issue.severity}</span>
          </div>
          <span className="text-xs font-medium text-[var(--color-frame)]/60 max-w-[200px] text-right break-words">{issue.title}</span>
        </div>
        
        <pre className="bg-[var(--color-canvas)] border-l-4 border-[var(--color-accent)] border-[1px] border-r-[1px] border-y-[1px] border-[var(--color-frame)] p-3 rounded text-xs mb-3 overflow-x-auto">
          <code>{issue.codeSnippet}</code>
        </pre>
        
        <div className="space-y-1 text-sm">
          <p className="text-[#D9503F]"><span className="font-bold">✕ Diagnosis:</span> {issue.diagnosis}</p>
          <p className="text-[#4FA35A]"><span className="font-bold">✓ Expected:</span> {issue.expected}</p>
        </div>
      </div>
    </div>
  );
}
''',
    'components/FixedCode.tsx': '''"use client";

import { useState } from "react";
import SectionHeader from "./SectionHeader";
import { LANGUAGES } from "@/config/app.config";
import { LanguageId } from "@/types/roast";

interface Props {
  sectionNumber: number;
  language: LanguageId;
  code: string;
  onApply: (code: string) => void;
}

export default function FixedCode({ sectionNumber, language, code, onApply }: Props) {
  const [copyStatus, setCopyStatus] = useState<"idle"|"copied"|"failed">("idle");
  const ext = LANGUAGES.find(l => l.id === language)?.extension || "txt";

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopyStatus("copied");
    } catch {
      setCopyStatus("failed");
    }
    setTimeout(() => setCopyStatus("idle"), 2000);
  };

  const copyLabel = copyStatus === "copied" ? "✓ COPIED TO CLIPBOARD" : 
                    copyStatus === "failed" ? "✕ COPY BLOCKED, SELECT MANUALLY" : 
                    "📋 COPY FIXED CODE";

  return (
    <div className="font-[family-name:var(--font-jetbrains-mono)]">
      <SectionHeader number={sectionNumber} title="Fix">
        <span className="text-[#4FA35A] font-bold text-sm">CORRECTED CODE</span>
      </SectionHeader>
      
      <div className="border-[2px] border-[var(--color-frame)] rounded-[14px] bg-[var(--color-panel)] overflow-hidden shadow-[2px_2px_0_var(--color-frame)]">
        <div className="bg-[var(--color-canvas)] border-b-[2px] border-[var(--color-frame)] flex justify-between items-center px-3 py-2 text-xs font-bold">
          <span>solution.{ext}</span>
          <span className="text-[#4FA35A]">READY TO APPLY</span>
        </div>
        <pre className="p-4 overflow-x-auto text-sm custom-scroll max-h-[400px]">
          <code>{code}</code>
        </pre>
      </div>
      
      <div className="flex flex-col sm:flex-row gap-3 mt-4">
        <button 
          onClick={handleCopy}
          className="flex-1 border-[2px] border-[var(--color-frame)] rounded-full py-2 font-bold text-sm hover:bg-[var(--color-frame)] hover:text-white transition-colors"
        >
          {copyLabel}
        </button>
        <button 
          onClick={() => onApply(code)}
          className="flex-1 border-[2px] border-[var(--color-frame)] rounded-full py-2 font-bold text-sm bg-[var(--color-canvas)] hover:bg-[var(--color-frame)] hover:text-white transition-colors"
        >
          APPLY TO EDITOR ↵
        </button>
      </div>
    </div>
  );
}
''',
    'components/RoastReport.tsx': '''import { RoastResult, ReportState, LanguageId, RoastLevel } from "@/types/roast";
import SectionHeader from "./SectionHeader";
import IssueCard from "./IssueCard";
import FixedCode from "./FixedCode";
import EmptyState from "./EmptyState";
import LoadingState from "./LoadingState";
import ErrorState from "./ErrorState";

interface Props {
  state: ReportState;
  roastLevel: RoastLevel;
  language: LanguageId;
  result: RoastResult | null;
  errorMsg: string;
  onRetry: () => void;
  onApplyFix: (code: string) => void;
}

export default function RoastReport({ state, roastLevel, language, result, errorMsg, onRetry, onApplyFix }: Props) {
  if (state === "empty") return <EmptyState />;
  if (state === "loading") return <LoadingState />;
  if (state === "error") return <ErrorState error={errorMsg} onRetry={onRetry} />;
  
  if (state === "results" && result) {
    const hasFix = !!result.correctedCode;
    const hasTakeaway = !!result.takeaway;
    const takeawaySectionNum = hasFix ? 4 : 3;

    return (
      <div className="h-full bg-[var(--color-panel)] flex flex-col">
        <div className="h-10 border-b-[2px] border-[var(--color-frame)] bg-[var(--color-canvas)] flex items-center justify-between px-4 shrink-0 font-[family-name:var(--font-jetbrains-mono)]">
          <span className="text-xs uppercase font-bold text-[var(--color-frame)]/50 tracking-widest">AUDIT // REPORT</span>
          <span className="text-sm font-bold">Roast Report</span>
          <div className="w-32"></div>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 sm:p-6">
          <SectionHeader number={1} title="Roast">
            <span className="text-xs font-[family-name:var(--font-jetbrains-mono)] font-bold bg-[var(--color-canvas)] px-2 py-0.5 border border-[var(--color-frame)] rounded">STYLE: {roastLevel}</span>
          </SectionHeader>
          <blockquote className="font-[family-name:var(--font-space-grotesk)] text-lg sm:text-xl font-bold italic mb-8 border-l-4 border-[var(--color-accent)] pl-4 text-[var(--color-frame)]">
            "{result.roast}"
          </blockquote>

          <SectionHeader number={2} title="What's Wrong">
            <span className="text-xs font-[family-name:var(--font-jetbrains-mono)] font-bold">{result.issues.length} {result.issues.length === 1 ? 'ISSUE' : 'ISSUES'}</span>
          </SectionHeader>
          
          <div className="mb-8">
            {result.issues.length === 0 ? (
              <p className="text-[#4FA35A] font-bold font-[family-name:var(--font-jetbrains-mono)] py-4">No issues found. Suspiciously clean.</p>
            ) : (
              result.issues.map((issue, idx) => (
                <IssueCard key={idx} index={idx} issue={issue} />
              ))
            )}
          </div>

          {hasFix && (
            <div className="mb-8">
              <FixedCode 
                sectionNumber={3} 
                language={language} 
                code={result.correctedCode} 
                onApply={onApplyFix} 
              />
            </div>
          )}

          {hasTakeaway && (
            <div>
              <SectionHeader number={takeawaySectionNum} title="Takeaway" />
              <p className="text-sm font-medium leading-relaxed font-[family-name:var(--font-jetbrains-mono)] bg-[var(--color-canvas)] p-4 rounded-[14px] border-[2px] border-[var(--color-frame)]">
                {result.takeaway}
              </p>
            </div>
          )}
        </div>
      </div>
    );
  }
  
  return null;
}
''',
    'components/EmptyState.tsx': '''export default function EmptyState() {
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 text-center h-full">
      <div className="w-16 h-16 border-[2px] border-dashed border-[var(--color-frame)] flex items-center justify-center mb-6 opacity-50 text-2xl font-bold font-[family-name:var(--font-jetbrains-mono)]">
        {'{ }'}
      </div>
      <h2 className="text-xl font-bold uppercase tracking-wide mb-2 font-[family-name:var(--font-space-grotesk)]">Awaiting Code Submission</h2>
      <p className="text-sm text-[var(--color-frame)]/60 max-w-[300px] leading-relaxed font-[family-name:var(--font-jetbrains-mono)]">
        Paste your code on the left, then click "ROAST MY CODE" or press Ctrl+Enter (⌘+Enter on Mac).
      </p>
    </div>
  );
}
''',
    'components/LoadingState.tsx': '''export default function LoadingState() {
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 text-center h-full">
      <div className="w-16 h-16 border-[2px] border-solid border-[var(--color-frame)] flex items-center justify-center mb-6 animate-spin text-2xl font-bold font-[family-name:var(--font-jetbrains-mono)]">
        /
      </div>
      <h2 className="text-xl font-bold uppercase tracking-wide mb-2 animate-pulse font-[family-name:var(--font-space-grotesk)]">Analyzing Code</h2>
      <p className="text-sm text-[var(--color-frame)]/60 max-w-[300px] leading-relaxed font-[family-name:var(--font-jetbrains-mono)]">
        Evaluating computational complexity and architectural purity...
      </p>
    </div>
  );
}
''',
    'components/ErrorState.tsx': '''interface Props {
  error: string;
  onRetry: () => void;
}

export default function ErrorState({ error, onRetry }: Props) {
  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 text-center h-full">
      <div className="w-16 h-16 border-[2px] border-solid border-[var(--color-accent)] text-[var(--color-accent)] flex items-center justify-center mb-6 text-3xl font-bold font-[family-name:var(--font-jetbrains-mono)]">
        !
      </div>
      <h2 className="text-xl font-bold uppercase tracking-wide mb-2 text-[var(--color-accent)] font-[family-name:var(--font-space-grotesk)]">Analysis Failed</h2>
      <p className="text-sm text-[var(--color-frame)]/60 max-w-[300px] leading-relaxed mb-6 font-[family-name:var(--font-jetbrains-mono)]">
        {error || "An unknown error occurred during code evaluation."}
      </p>
      <button 
        onClick={onRetry}
        className="px-6 py-2 rounded-full border-[2px] border-[var(--color-frame)] shadow-[4px_4px_0_var(--color-frame)] font-bold uppercase hover:-translate-y-1 hover:shadow-[4px_6px_0_var(--color-frame)] active:translate-y-1 active:shadow-[1px_1px_0_var(--color-frame)] transition-all bg-[var(--color-canvas)] font-[family-name:var(--font-jetbrains-mono)]"
      >
        RETRY ANALYSIS ↵
      </button>
    </div>
  );
}
''',
    'components/StatusBar.tsx': '''import { APP, AI } from "@/config/app.config";

export default function StatusBar({ isRoasting }: { isRoasting: boolean }) {
  return (
    <div className="border-t-[2px] border-[var(--color-frame)] bg-[var(--color-canvas)] p-2">
      <div className="flex justify-between items-center text-[10px] font-[family-name:var(--font-jetbrains-mono)] tracking-widest uppercase">
        <div className="flex items-center gap-2 text-[var(--color-frame)]/60">
          <span>STATUS: 
            {isRoasting ? (
              <span className="text-[#EDB13E] font-bold ml-1 animate-pulse">PROCESSING...</span>
            ) : (
              <span className="text-[#4FA35A] font-bold ml-1">ONLINE ({AI.modelLabel.toUpperCase()})</span>
            )}
          </span>
          <span className="hidden sm:inline">| ENGINE: GOOGLE GEMINI</span>
        </div>
        <div className="text-[var(--color-frame)]/60">
          {APP.name} {APP.version} // LIVE
        </div>
      </div>
      <div className="text-center text-[9px] text-[var(--color-frame)]/40 mt-1 uppercase tracking-widest font-[family-name:var(--font-jetbrains-mono)]">
        Made at GDG Nashik Pre-DevFest Workshop
      </div>
    </div>
  );
}
'''
}

for filepath, content in files.items():
    dirname = os.path.dirname(filepath)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print('Files generated successfully.')
