import { RoastResult, ReportState, LanguageId, RoastLevel } from "@/types/roast";
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
      <div className="h-full bg-[var(--color-white)] flex flex-col text-[var(--color-ink)]">
        <div className="h-10 border-b-[2px] border-[var(--color-ink)] bg-[var(--color-cream)] flex items-center justify-between px-4 shrink-0 font-[family-name:var(--font-jetbrains-mono)]">
          <span className="text-xs uppercase font-bold tracking-widest opacity-60">AUDIT // REPORT</span>
          <span className="text-sm font-bold">Roast Report</span>
          <div className="w-32"></div>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 sm:p-6">
          <SectionHeader number={1} title="Roast">
            <span className="text-xs font-[family-name:var(--font-jetbrains-mono)] font-bold bg-[var(--color-cream)] px-2 py-0.5 border border-[var(--color-ink)] rounded">STYLE: {roastLevel}</span>
          </SectionHeader>
          <blockquote className="font-[family-name:var(--font-space-grotesk)] text-lg sm:text-xl font-bold italic mb-8 border-l-4 border-[var(--color-mustard)] pl-4 text-[var(--color-ink)]">
            "{result.roast}"
          </blockquote>

          <SectionHeader number={2} title="What's Wrong">
            <span className="text-xs font-[family-name:var(--font-jetbrains-mono)] font-bold">{result.issues.length} {result.issues.length === 1 ? 'ISSUE' : 'ISSUES'}</span>
          </SectionHeader>
          
          <div className="mb-8">
            {result.issues.length === 0 ? (
              <p className="text-[var(--color-google-green)] font-bold font-[family-name:var(--font-jetbrains-mono)] py-4">No issues found. Suspiciously clean.</p>
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
              <p className="text-sm font-medium leading-relaxed font-[family-name:var(--font-jetbrains-mono)] bg-[var(--color-cream)] p-4 rounded-[14px] border-[2px] border-[var(--color-ink)]">
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
