interface Props {
  number: number;
  title: string;
  children?: React.ReactNode;
}

export default function SectionHeader({ number, title, children }: Props) {
  const numStr = number.toString().padStart(2, "0");
  return (
    <div className="flex justify-between items-center border-b-[2px] border-[var(--color-frame)] pb-2 mb-4 mt-6 first:mt-0 font-[family-name:var(--font-jetbrains-mono)]">
      <span className="font-bold uppercase tracking-widest text-sm text-[var(--color-frame)]">
        {numStr} // {title}
      </span>
      {children && <div>{children}</div>}
    </div>
  );
}
