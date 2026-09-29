import { analyzeCode } from "../lib/gemini";
import { AI, SAMPLE } from "../config/app.config";

async function main() {
  console.log(`Checking API with model ${AI.model}...`);
  try {
    const result = await analyzeCode({
      language: SAMPLE.language,
      code: SAMPLE.code,
      roastLevel: "sharp",
      errorMessage: "TypeError: unsupported operand type(s) for +=: 'int' and 'list'"
    });
    console.log("Success! Roast:");
    console.log(result.roast);
    console.log(`Found ${result.issues.length} issues.`);
    process.exit(0);
  } catch (error) {
    console.error("Failed to check API:", error);
    process.exit(1);
  }
}

main();
