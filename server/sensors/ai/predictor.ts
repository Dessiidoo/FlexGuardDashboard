import { calculateInstinct } from "./instincts.js";

export async function predictThreat(data: { heartRate: number; motion: number; environment: any }) {
  const { heartRate, motion, environment } = data;

  // Simple predictive logic: higher heart rate + motion + environment noise increases threat
  const instinctScore = calculateInstinct({ heartRate, motion, environment });

  const threatLevel = instinctScore > 150 ? "HIGH" : instinctScore > 100 ? "MEDIUM" : "LOW";

  return threatLevel;
}
