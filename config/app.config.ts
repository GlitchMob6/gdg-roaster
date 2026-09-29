export const APP = { name: "Code Roaster", version: "v3", tagline: "Your code. Our problem now." };
export const AI = { model: "gemini-3.5-flash-lite", modelLabel: "Gemini 3.5 Flash-Lite", maxAttempts: 3 };

export const ROAST_LEVELS = [
  { id: "dry", label: "Dry", description: "Mild and deadpan. Gentle jabs, mostly helpful." },
  { id: "sharp", label: "Sharp", description: "Pointed and witty. Calls out every mistake directly." },
  { id: "savage", label: "Savage", description: "Maximum burn. Brutally honest, but still technically accurate." }
] as const;

export const LANGUAGES = [
  { id: "python", label: "Python", extension: "py" },
  { id: "javascript", label: "JavaScript", extension: "js" },
  { id: "typescript", label: "TypeScript", extension: "ts" },
  { id: "java", label: "Java", extension: "java" },
  { id: "c", label: "C", extension: "c" },
  { id: "cpp", label: "C++", extension: "cpp" },
  { id: "go", label: "Go", extension: "go" },
  { id: "rust", label: "Rust", extension: "rs" }
] as const;

export const DEFAULTS = { language: "python", roastLevel: "savage" } as const;
export const SEVERITIES = ["FATAL BUG", "CODE SMELL", "OPTIMIZATION"] as const;
export const LIMITS = { maxCodeLength: 20000, maxErrorMessageLength: 4000 };

export const SAMPLE = { 
  language: "python", 
  code: `def average_numbers(numbers):\n    total = 0\n    for number in numbers:\n        total += numbers # Oops!\n    return total / len(numbers)\n\naverage_numbers([1, 2, 3, 4, 5])`
} as const;
