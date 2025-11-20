export function calculateInstinct(data: { heartRate: number; motion: number; environment: any }) {
  const { heartRate, motion, environment } = data;

  // Animal-inspired instincts: weight heart rate, motion, and environmental stressors
  const heartWeight = heartRate * 1.5;
  const motionWeight = motion * 1.2;
  const noiseWeight = environment.noise * 1.3;
  const tempPenalty = environment.temperature > 30 ? 20 : 0;

  const instinctScore = heartWeight + motionWeight + noiseWeight + tempPenalty;
  return instinctScore;
}
