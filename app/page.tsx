import Workspace from "@/components/Workspace";
import Image from "next/image";

export default function Home() {
  return (
    <div className="flex flex-col items-center min-h-screen w-full relative pb-12">
      {/* Floating Navbar */}
      <nav className="fixed top-4 md:top-6 left-1/2 -translate-x-1/2 w-[90%] max-w-[1200px] bg-[var(--color-cream)] border-[2px] lg:border-[3px] border-[var(--color-ink)] shadow-[4px_4px_0_var(--color-ink)] rounded-full h-16 md:h-20 flex items-center justify-between px-4 md:px-8 z-50">
        <div className="flex items-center">
          <Image src="/GDG-Nashik_Logo.svg" alt="GDG Nashik" width={140} height={40} className="h-6 md:h-8 w-auto" />
        </div>
        <div className="absolute left-1/2 -translate-x-1/2 font-[family-name:var(--font-space-grotesk)] font-bold tracking-widest text-sm md:text-xl uppercase hidden sm:block text-[var(--color-ink)]">
          Code Roaster <span className="text-[var(--color-mustard)]">v3</span>
        </div>
        <div className="flex items-center">
          <Image src="/DevFest-26'_Logo.svg" alt="DevFest Nashik 2026" width={100} height={40} className="h-8 md:h-10 w-auto" />
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-8 flex flex-col items-center text-center px-4 w-full">
        <div className="font-[family-name:var(--font-jetbrains-mono)] text-xs md:text-sm font-bold tracking-widest uppercase mb-4 text-[var(--color-accent)]">
          CODE BOL RAHA HAI · मला वाचवा!
        </div>
        <h1 className="font-[family-name:var(--font-space-grotesk)] font-bold text-5xl md:text-7xl mb-4 text-[var(--color-ink)] tracking-tight">
          Code Roaster
        </h1>
        <p className="font-[family-name:var(--font-space-grotesk)] text-lg md:text-xl text-[var(--color-ink)] max-w-[600px] leading-relaxed font-medium mb-2">
          Paste your code. Pick your roast.<br className="hidden sm:block" /> Get humbled. Get the fix.
        </p>
        <p className="font-[family-name:var(--font-jetbrains-mono)] text-[11px] uppercase tracking-widest text-[var(--color-muted-ink)] font-bold">
          Desi debugging, powered by Gemini.
        </p>
      </section>

      {/* Main Tool */}
      <div className="w-full px-4 sm:px-6 md:px-8 flex justify-center">
        <Workspace />
      </div>

      {/* Decorative Rangoli Strip (Footer) */}
      <div className="w-full h-8 mt-12 bg-[var(--color-ink)] relative overflow-hidden flex items-center justify-center text-[var(--color-mustard)] gap-4 text-xl">
        <span>▲ ▼ ▲ ▼</span><span>• • •</span><span>▲ ▼ ▲ ▼</span>
      </div>
    </div>
  );
}
