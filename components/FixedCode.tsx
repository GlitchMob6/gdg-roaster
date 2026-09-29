"use client";

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

  const copyLabel = copyStatus === "copied" ? "✓ COPIED" : 
                    copyStatus === "failed" ? "✕ COPY FAILED" : 
                    "COPY →";

  return (
    <div className="font-[family-name:var(--font-jetbrains-mono)]">
      <SectionHeader number={sectionNumber} title="Redemption Arc">
        <span className="text-[var(--color-google-green)] font-bold text-sm">Ab asli fix dekh, bhau.</span>
      </SectionHeader>
      
      <div className="border-[2px] border-[var(--color-ink)] rounded-[14px] bg-[var(--color-editor-bg)] text-[var(--color-editor-ink)] overflow-hidden shadow-[2px_2px_0_var(--color-ink)] relative">
        <div className="bg-[var(--color-ink)] text-[var(--color-cream)] border-b-[2px] border-[var(--color-ink)] flex justify-between items-center px-3 py-2 text-xs font-bold">
          <span>solution.{ext}</span>
          <button 
            onClick={handleCopy}
            className="hover:text-[var(--color-mustard)] transition-colors"
          >
            {copyLabel}
          </button>
        </div>
        <pre className="p-4 overflow-x-auto text-sm custom-scroll max-h-[400px]">
          <code>{code}</code>
        </pre>
      </div>
      
      <div className="flex flex-col sm:flex-row gap-3 mt-4">
        <button 
          onClick={() => onApply(code)}
          className="w-full border-[2px] border-[var(--color-ink)] rounded-full py-2 font-bold text-sm bg-[var(--color-cream)] hover:bg-[var(--color-ink)] hover:text-white transition-colors uppercase shadow-[2px_2px_0_var(--color-ink)]"
        >
          APPLY TO EDITOR ↵
        </button>
      </div>
    </div>
  );
}
