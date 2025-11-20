export function logEvent(event: any) {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}]`, event);
}
