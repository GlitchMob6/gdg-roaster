import { RoastIssue } from "@/types/roast";

interface Props {
  index: number;
  issue: RoastIssue;
}

export default function IssueCard({ index, issue }: Props) {
  const isFatal = issue.severity === "FATAL BUG";
  const isSmell = issue.severity === "CODE SMELL";
  
  const badgeColor = isFatal ? "bg-[var(--color-google-red)] text-white" : isSmell ? "bg-[var(--color-google-yellow)] text-[var(--color-ink)]" : "bg-[var(--color-google-green)] text-white";
  const sideColor = isFatal ? "bg-[var(--color-google-red)]" : isSmell ? "bg-[var(--color-google-yellow)]" : "bg-[var(--color-google-green)]";
  
  const numStr = (index + 1).toString().padStart(2, "0");

  return (
    <div className="border-[2px] border-[var(--color-ink)] rounded-[14px] p-4 mb-4 shadow-[2px_2px_0_var(--color-ink)] bg-[var(--color-white)] relative overflow-hidden">
      <div className={`absolute top-0 left-0 bottom-0 w-2 ${sideColor}`}></div>
      <div className="pl-4 font-[family-name:var(--font-jetbrains-mono)]">
        <div className="flex justify-between items-start mb-3">
          <div className="flex items-center gap-2">
            <span className="bg-[var(--color-ink)] text-[var(--color-white)] font-bold px-2 py-0.5 text-xs rounded">{numStr}</span>
            <span className="font-bold">LINE {issue.line}</span>
            <span className={`text-xs font-bold px-2 py-0.5 rounded border-[2px] border-[var(--color-ink)] ${badgeColor}`}>{issue.severity}</span>
          </div>
          <span className="text-xs font-medium text-[var(--color-muted-ink)] max-w-[200px] text-right break-words">{issue.title}</span>
        </div>
        
        <pre className="bg-[var(--color-cream)] border-l-4 border-[var(--color-mustard)] border-[1px] border-r-[1px] border-y-[1px] border-[var(--color-ink)] p-3 rounded text-xs mb-3 overflow-x-auto">
          <code>{issue.codeSnippet}</code>
        </pre>
        
        <div className="space-y-1 text-sm">
          <p className="text-[var(--color-google-red)]"><span className="font-bold">✕ Diagnosis:</span> {issue.diagnosis}</p>
          <p className="text-[var(--color-google-green)]"><span className="font-bold">✓ Expected:</span> {issue.expected}</p>
        </div>
      </div>
    </div>
  );
}
