export type Level = 1 | 2 | 3;

export type CanonicalNode = {
  symbol: string;
  macro?: string | null;
  category?: string | null;
  args?: string[];
  gloss?: string | null;
  modal?: { system: string; operator: string } | null;
};

export type CompressResponse = {
  canonical: {
    source_text: string;
    version: string;
    nodes: CanonicalNode[];
    coverage: { matched_ratio: number };
  };
  renders: Record<string, string>;
  expand: string;
};

const API_BASE =
  process.env.NEXT_PUBLIC_LOGOS_API?.replace(/\/$/, "") || "http://127.0.0.1:8000";

export async function compressText(text: string): Promise<CompressResponse> {
  const res = await fetch(`${API_BASE}/v1/compress`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(detail || `HTTP ${res.status}`);
  }
  return res.json();
}
