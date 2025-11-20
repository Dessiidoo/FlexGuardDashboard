export function triggerDefense(threatLevel: string) {
  switch (threatLevel) {
    case "HIGH":
      return "Airburst triggered: maximum response.";
    case "MEDIUM":
      return "Alert mode: ready to deploy countermeasures.";
    case "LOW":
      return "Monitoring: no immediate action.";
    default:
      return "Unknown threat level.";
  }
}
