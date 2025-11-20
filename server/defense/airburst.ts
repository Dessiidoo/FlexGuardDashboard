export function simulateAirburst(intensity: number) {
  // Simulate an instantaneous defensive action
  const radius = Math.min(5 + intensity / 50, 20); // meters
  const duration = Math.min(1000 + intensity * 5, 5000); // ms
  return `Airburst activated: radius ${radius}m, duration ${duration}ms`;
}
