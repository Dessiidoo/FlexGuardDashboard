import { getHeartRate } from "../sensors/heartRate.js";
import { getMotion } from "../sensors/motion.js";
import { getEnvironment } from "../sensors/environmental.js";
import { predictThreat } from "../ai/predictor.js";
import { triggerDefense } from "../defense/reactive.js";
import { simulateAirburst } from "../defense/airburst.js";

export async function simulateClientCycle() {
  const heartRate = getHeartRate();
  const motion = getMotion();
  const environment = getEnvironment();

  const threat = await predictThreat({ heartRate, motion, environment });
  const defenseAction = triggerDefense(threat);
  const airburstLog = simulateAirburst(heartRate + motion);

  return {
    heartRate,
    motion,
    environment,
    threat,
    defenseAction,
    airburstLog,
  };
}

// Example usage
(async () => {
  const cycle = await simulateClientCycle();
  console.table(cycle);
})();
