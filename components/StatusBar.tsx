import { APP, AI } from "@/config/app.config";

export default function StatusBar({ isRoasting }: { isRoasting: boolean }) {
  return (
    <div className="border-t-[2px] border-[var(--color-ink)] bg-[var(--color-cream)] p-2">
      <div className="flex justify-between items-center text-[10px] font-[family-name:var(--font-jetbrains-mono)] tracking-widest uppercase">
        <div className="flex items-center gap-2 text-[var(--color-muted-ink)]">
          <span>STATUS: 
            {isRoasting ? (
              <span className="text-[var(--color-mustard)] font-bold ml-1 animate-pulse">PROCESSING...</span>
            ) : (
              <span className="text-[var(--color-google-green)] font-bold ml-1">ONLINE ({AI.modelLabel.toUpperCase()})</span>
            )}
          </span>
          <span className="hidden sm:inline">| ENGINE: GOOGLE GEMINI</span>
        </div>
        <div className="text-[var(--color-muted-ink)]">
          {APP.name} {APP.version} // LIVE
        </div>
      </div>
      <div className="text-center text-[9px] text-[var(--color-ink)] opacity-40 mt-1 uppercase tracking-widest font-[family-name:var(--font-jetbrains-mono)]">
        Made at GDG Nashik Pre-DevFest Workshop
      </div>
    </div>
  );
}
