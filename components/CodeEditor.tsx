"use client";

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
  const lines = code.split("\n");
  const numLines = Math.max(lines.length, 10);

  const handleScroll = (e: React.UIEvent<HTMLTextAreaElement>) => {
    if (gutterRef.current) {
      gutterRef.current.scrollTop = e.currentTarget.scrollTop;
    }
  };

  const handleSelect = (e: React.SyntheticEvent<HTMLTextAreaElement>) => {
    const el = e.currentTarget;
    const textBefore = el.value.substring(0, el.selectionStart);
    const lineSplit = textBefore.split("\n");
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
    <div className="flex flex-col h-full bg-[var(--color-editor-bg)] text-[var(--color-editor-ink)] relative font-[family-name:var(--font-jetbrains-mono)]">
      <div className="h-10 border-b-[2px] border-[var(--color-ink)] bg-[var(--color-ink)] text-[var(--color-cream)] flex items-center justify-between px-4 shrink-0">
        <span className="text-xs uppercase font-bold tracking-widest opacity-60">INPUT // SRC</span>
        <span className="text-sm font-bold">Your Code</span>
        <div className="text-xs font-bold gap-3 flex text-[var(--color-mustard)]">
          <button onClick={onLoadSample} className="hover:underline">SAMPLE BUG</button>
          <span className="opacity-50">|</span>
          <button onClick={() => onChange("")} className="hover:underline">CLEAR</button>
        </div>
      </div>
      
      <div className="flex-1 flex overflow-hidden relative">
        <div 
          ref={gutterRef}
          className="w-12 shrink-0 bg-[var(--color-editor-bg)] border-r-[2px] border-[var(--color-ink)] overflow-hidden text-right pr-2 py-4 select-none text-sm leading-6 opacity-40"
        >
          {Array.from({ length: numLines }).map((_, i) => (
            <div 
              key={i} 
              className={errorLine === i + 1 ? "text-[var(--color-google-red)] font-bold bg-[var(--color-google-red)]/20" : ""}
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
          className="flex-1 p-4 resize-none text-sm leading-6 whitespace-pre overflow-auto focus:outline-none bg-transparent text-[var(--color-editor-ink)] caret-[var(--color-mustard)]"
        />
      </div>

      <div className="hidden md:flex h-8 shrink-0 bg-[var(--color-editor-bg)] text-[var(--color-editor-ink)] opacity-70 text-xs items-center justify-between px-4 absolute bottom-0 left-0 right-0 z-10 border-t border-[var(--color-muted-ink)]/30">
        <span>Ln {cursor.line}, Col {cursor.col} · {langLabel}</span>
        <span>UTF-8 · Tab Size: 4</span>
      </div>
    </div>
  );
}
