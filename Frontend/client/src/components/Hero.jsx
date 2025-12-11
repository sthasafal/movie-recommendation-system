import React from "react";
import { Play, Info } from "lucide-react";

const buildPoster = (path, size = "original") => {
  if (!path) return "";
  if (path.startsWith("http")) return path;
  return `https://image.tmdb.org/t/p/${size}${path}`;
};

export default function Hero({ movie, onMoreInfo }) {
  const featured =
    movie ||
    {
      title: "MovieX Recommendations",
      overview:
        "Discover hand-picked films tailored to your taste. Fresh picks, timeless classics, and hidden gems, all in one place.",
      poster_path: "/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
      vote_average: 8.5,
      release_date: "2024",
    };

  const imageUrl = buildPoster(featured.backdrop_path || featured.poster_path);

  return (
    <section className="px-4 md:px-8 pt-24">
      <div className="relative overflow-hidden rounded-3xl border border-white/5 bg-gradient-to-br from-[#0f172a] via-[#0b1120] to-[#0a0f1c]">
        {imageUrl && (
          <img
            src={imageUrl}
            alt={featured.title}
            className="absolute inset-0 h-full w-full object-cover opacity-40"
          />
        )}
        <div className="absolute inset-0 bg-gradient-to-r from-[#05070f] via-[#05070f]/70 to-transparent" />

        <div className="relative grid gap-10 md:grid-cols-[1.2fr_0.8fr] items-end p-8 md:p-12">
          <div className="space-y-4 md:space-y-6 max-w-3xl">
            <p className="text-xs uppercase tracking-[0.35em] text-red-400">
              Featured pick
            </p>
            <h1 className="text-4xl md:text-5xl font-bold leading-tight">
              {featured.title}
            </h1>
            <p className="text-gray-200 leading-relaxed max-w-2xl line-clamp-4">
              {featured.overview}
            </p>

            <div className="flex flex-wrap gap-4 text-sm text-gray-300">
              {featured.vote_average && (
                <span className="flex items-center gap-1">
                  ⭐ {Number(featured.vote_average).toFixed(1)} / 10
                </span>
              )}
              {featured.release_date && (
                <span>{String(featured.release_date).split("-")[0]}</span>
              )}
              <span className="px-3 py-1 rounded-full bg-white/5 border border-white/10">
                Curated for you
              </span>
            </div>

            <div className="flex flex-wrap gap-3">
              <button className="inline-flex items-center gap-2 rounded-xl bg-red-600 px-6 py-3 font-semibold text-white shadow-lg shadow-red-600/30 transition hover:-translate-y-0.5 hover:bg-red-500">
                <Play className="w-5 h-5" />
                Watch now
              </button>
              <button
                onClick={() => onMoreInfo?.(featured)}
                className="inline-flex items-center gap-2 rounded-xl border border-white/15 bg-white/5 px-6 py-3 font-semibold text-white transition hover:-translate-y-0.5 hover:border-white/30"
              >
                <Info className="w-5 h-5" />
                More info
              </button>
            </div>
          </div>

          <div className="w-full max-w-sm ml-auto bg-white/5 border border-white/10 rounded-2xl p-6 backdrop-blur-sm">
            <p className="text-sm text-gray-300 mb-3">Tonight&apos;s highlights</p>
            <div className="space-y-3 text-sm text-gray-200">
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Mood</span>
                <span className="font-semibold">Thoughtful & bold</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Genre mix</span>
                <span className="font-semibold">Drama · Thriller · Sci-Fi</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Best served with</span>
                <span className="font-semibold">Headphones & low lights</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
