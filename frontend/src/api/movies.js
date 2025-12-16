import { API_BASE, normalizeRecommendations, request } from "./client";

export async function searchMovies(query, limit = 12) {
  if (!query) return [];
  const params = new URLSearchParams({ q: query, limit: String(limit) });
  return request(`/movie/search?${params.toString()}`);
}

export async function getMovie(movieId) {
  return request(`/movie/${movieId}`);
}

export async function getSimilar(movieId, topN = 12) {
  const data = await request(`/recommend/similar/${movieId}?top_n=${topN}`);
  return normalizeRecommendations(data);
}

export async function getModelRecommendations(model, userId, topN = 12) {
  const data = await request(`/recommend/model/${model}/${userId}?top_n=${topN}`);
  return normalizeRecommendations(data);
}

// Popularity/trending support: try a dedicated endpoint; if missing, fall back to a broad search term.
export async function getTrending(topN = 12) {
  try {
    const data = await request(`/movie/top?limit=${topN}`);
    return normalizeRecommendations(data) || data;
  } catch (_) {
    // Fallback to a frequent-term search to surface widely known titles
    try {
      const results = await searchMovies("the", topN);
      return results;
    } catch {
      return [];
    }
  }
}

export async function getHybridForUser(userId, topN = 12) {
  // Use the hybrid route by default; caller can swap to other models via getModelRecommendations
  const data = await request(`/recommend/model/hybrid/${userId}?top_n=${topN}`);
  return normalizeRecommendations(data);
}

export { API_BASE };
