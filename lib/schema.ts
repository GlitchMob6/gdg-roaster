import { Type, Schema } from "@google/genai";
import { SEVERITIES } from "@/config/app.config";

export const roastResponseSchema: Schema = {
  type: Type.OBJECT,
  properties: {
    roast: { type: Type.STRING },
    issues: {
      type: Type.ARRAY,
      items: {
        type: Type.OBJECT,
        properties: {
          line: { type: Type.INTEGER },
          severity: { type: Type.STRING, enum: Array.from(SEVERITIES) },
          title: { type: Type.STRING },
          codeSnippet: { type: Type.STRING },
          diagnosis: { type: Type.STRING },
          expected: { type: Type.STRING }
        },
        required: ["line", "severity", "title", "codeSnippet", "diagnosis", "expected"]
      }
    },
    correctedCode: { type: Type.STRING },
    takeaway: { type: Type.STRING }
  },
  required: ["roast", "issues", "correctedCode", "takeaway"]
};
