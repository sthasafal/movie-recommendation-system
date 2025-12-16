const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

function normalizeRecommendations(data) {
  if (!data) return [];
  if (Array.isArray(data)) return data;
  if (data.recommendations && Array.isArray(data.recommendations)) {
    return data.recommendations;
  }
  return [];
}

async function request(path, opts = {}) {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, opts);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Request failed (${res.status})`);
  }
  const contentType = res.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return res.json();
  }
  return res.text();
}

export { API_BASE, request, normalizeRecommendations };
