export default function TopBar({ children }: { children: React.ReactNode }) {
  return (
    <header className="border-b-[2px] border-[var(--color-ink)] bg-[var(--color-white)] p-3 lg:p-4 w-full">
      {children}
    </header>
  );
}
