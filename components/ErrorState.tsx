interface Props {
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
