export default function EmptyState() {
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
