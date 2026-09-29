import { ROAST_LEVELS, LANGUAGES } from "@/config/app.config";
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
    <div className="flex flex-wrap items-center gap-4 text-sm w-full justify-between font-[family-name:var(--font-jetbrains-mono)]">
      <div className="flex flex-wrap items-center gap-4">
        <div className="flex items-center gap-2">
          <span className="font-bold text-xs uppercase tracking-widest text-[var(--color-ink)]">Roast Level:</span>
          <div className="flex bg-[var(--color-cream)] border-[2px] border-[var(--color-ink)] rounded-full p-1 shadow-[2px_2px_0_var(--color-ink)]">
            {ROAST_LEVELS.map(l => (
              <button
                key={l.id}
                title={l.description}
                onClick={() => onRoastLevelChange(l.id)}
                className={`px-3 py-1 rounded-full font-bold transition-colors ${roastLevel === l.id ? "bg-[var(--color-mustard)] text-[var(--color-ink)] border-[2px] border-[var(--color-ink)] shadow-[inset_1px_1px_0_rgba(0,0,0,0.2)]" : "hover:bg-[var(--color-pale-yellow)] text-[var(--color-muted-ink)] border-[2px] border-transparent"}`}
              >
                {l.label}
              </button>
            ))}
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <span className="font-bold text-xs uppercase tracking-widest text-[var(--color-ink)]">Language:</span>
          <select
            value={language}
            onChange={e => onLanguageChange(e.target.value as LanguageId)}
            className="appearance-none bg-[var(--color-white)] border-[2px] border-[var(--color-ink)] text-[var(--color-ink)] rounded-full px-3 py-1.5 font-bold font-mono shadow-[2px_2px_0_var(--color-ink)] pr-8 cursor-pointer relative focus:outline-none"
          >
            {LANGUAGES.map(l => (
              <option key={l.id} value={l.id}>{l.label}</option>
            ))}
          </select>
        </div>

        <button
          onClick={onToggleErrorDrawer}
          className="border-[2px] border-dashed border-[var(--color-ink)] text-[var(--color-ink)] px-3 py-1.5 rounded-full font-bold hover:bg-[var(--color-cream)] transition-colors"
        >
          {errorDrawerOpen ? "− ERROR MESSAGE" : "+ ERROR MESSAGE"}
        </button>
      </div>

      <button
        onClick={onRoast}
        disabled={isRoasting}
        className={`flex items-center justify-center gap-2 px-8 py-3 rounded-full border-[3px] border-[var(--color-ink)] shadow-[4px_4px_0_var(--color-ink)] font-bold uppercase transition-all ${isRoasting ? "bg-[var(--color-mustard)] text-[var(--color-ink)] animate-pulse shadow-[1px_1px_0_var(--color-ink)] translate-y-[3px] translate-x-[3px]" : "bg-[var(--color-mustard)] text-[var(--color-ink)] hover:translate-x-[-1px] hover:translate-y-[-1px] hover:shadow-[5px_5px_0_var(--color-ink)] active:translate-y-[3px] active:translate-x-[3px] active:shadow-[1px_1px_0_var(--color-ink)]"}`}
      >
        {isRoasting ? "ANALYZING..." : "ROAST MY CODE 🔥 →"}
        {!isRoasting && <span className="bg-black/10 text-[var(--color-ink)] px-2 py-0.5 rounded text-[10px] ml-1 font-sans">Ctrl ⏎</span>}
      </button>
    </div>
  );
}
