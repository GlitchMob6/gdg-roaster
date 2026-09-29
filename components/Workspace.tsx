"use client";

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
    <main className="w-full max-w-[1360px] h-[calc(100vh-4rem)] min-h-[600px] border-[2px] border-[var(--color-ink)] shadow-[4px_4px_0_var(--color-ink)] flex flex-col overflow-hidden bg-[var(--color-white)] rounded-[22px]">
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
        <div className="w-full lg:w-[55%] border-b-[2px] lg:border-b-0 lg:border-r-[2px] border-[var(--color-ink)] flex flex-col">
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
