interface Props {
  value: string;
  onChange: (v: string) => void;
  onClose: () => void;
}

export default function ErrorMessageInput({ value, onChange, onClose }: Props) {
  return (
    <div className="border-b-[2px] border-[var(--color-frame)] bg-[var(--color-canvas)] p-3 lg:p-4">
      <div className="flex justify-between items-center mb-2">
        <span className="font-bold text-xs uppercase font-[family-name:var(--font-jetbrains-mono)] tracking-widest text-[var(--color-accent)]">Attach Terminal Traceback / Compiler Error (Optional)</span>
        <button onClick={onClose} className="font-bold text-xs hover:underline">Dismiss ✕</button>
      </div>
      <textarea
        value={value}
        onChange={e => onChange(e.target.value)}
        placeholder={"TypeError: unsupported operand type(s) for +=: 'int' and 'list'\n  File \"main.py\", line 4, in average_numbers..."}
        className="w-full border-[2px] border-[var(--color-frame)] p-3 font-[family-name:var(--font-jetbrains-mono)] text-sm resize-none focus:outline-none focus:shadow-[2px_2px_0_var(--color-frame)] bg-[var(--color-panel)]"
        rows={2}
      />
    </div>
  );
}
