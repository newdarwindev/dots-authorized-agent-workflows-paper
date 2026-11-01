// A public page can report expiry, never authenticated private availability.
fetch('mock-summary.json').then(response => {
  if (!response.ok) throw new Error('Summary unavailable');
  return response.json();
}).then(summary => {
  const expiry = new Date(summary.artifact.expires_at);
  if (!Number.isFinite(expiry.getTime())) return;
  document.getElementById('mock-availability').textContent = Date.now() >= expiry.getTime()
    ? `Private evidence unavailable: the artifact expired ${expiry.toISOString()}. Historical counts remain a run record.`
    : `Private evidence expires ${expiry.toISOString()}; current availability requires authenticated verification.`;
}).catch(() => {});
