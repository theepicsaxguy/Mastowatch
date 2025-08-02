export type Sample = { name: string; labels: Record<string, string>; value: number; ts?: number };

// Simple Prometheus text exposition parser for counters/gauges/histograms
export function parseProm(text: string): Record<string, Sample[]> {
  const lines = text.split(/\r?\n/);
  const samples: Record<string, Sample[]> = {};
  for (const ln of lines) {
    if (!ln || ln.startsWith("#")) continue;
    // e.g. metric{label="a",b="c"} 12 1719868089
    const m = ln.match(/^([a-zA-Z_:][a-zA-Z0-9_:]*)(\{[^}]*\})?\s+([0-9eE+\-\.])(?:\s+([0-9]+))?$/);
    if (!m) continue;
    const [, metric, labelBlock, valStr, tsStr] = m;
    const labels: Record<string, string> = {};
    if (labelBlock) {
      const inner = labelBlock.slice(1, -1).trim();
      if (inner) {
        for (const part of inner.split(",")) {
          const [k, vRaw] = part.split("=");
          const v = vRaw?.trim().replace(/^"(.*)"$/, "$1") ?? "";
          labels[k.trim()] = v;
        }
      }
    }
    const value = Number(valStr);
    const ts = tsStr ? Number(tsStr) : undefined;
    samples[metric] = samples[metric] || [];
    samples[metric].push({ name: metric, labels, value, ts });
  }
  return samples;
}