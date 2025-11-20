export function getEnvironment() {
  // Simulate environmental factors: noise (0-100) and temperature (°C)
  return {
    noise: Math.floor(Math.random() * 101),
    temperature: 20 + Math.floor(Math.random() * 15), // 20-35°C
  };
}
