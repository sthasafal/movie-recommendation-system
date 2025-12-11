import React from "react";
import { X, Play, Star } from "lucide-react";

const buildPoster = (path, size = "original") => {
  if (!path) return "";
  if (path.startsWith("http")) return path;
  return `https://image.tmdb.org/t/p/${size}${path}`;
};

export default function MovieModal({ movie, onClose }) {
  const imageUrl = buildPoster(movie.backdrop_path || movie.poster_path);
  const year = movie.release_date ? movie.release_date.split("-")[0] : "—";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div className="relative bg-[#0d1118] rounded-2xl overflow-hidden max-w-4xl w-full shadow-2xl border border-white/10">
        <button
          onClick={onClose}
          aria-label="Close details"
          className="absolute top-4 right-4 z-20 p-2 bg-black/60 rounded-full hover:bg-black/80 transition"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="grid md:grid-cols-[1fr,1.2fr]">
          <div className="relative h-64 md:h-full bg-black">
            {imageUrl ? (
              <img
                src={imageUrl}
                alt={movie.title}
                className="h-full w-full object-cover"
              />
            ) : (
              <div className="h-full w-full flex items-center justify-center text-gray-500">
                No artwork
              </div>
            )}
            <div className="absolute inset-0 bg-gradient-to-t from-black via-black/40 to-transparent" />
          </div>

          <div className="p-8 space-y-4">
            <div className="flex items-center gap-3 text-xs uppercase tracking-[0.25em] text-red-400">
              Spotlight
              <span className="h-px flex-1 bg-white/10" />
            </div>

            <h2 className="text-3xl font-bold leading-tight">{movie.title}</h2>

            <div className="flex flex-wrap gap-4 text-sm text-gray-300">
              {movie.vote_average && (
                <span className="flex items-center gap-1">
                  <Star className="w-4 h-4 fill-amber-300 text-amber-300" />
                  {Number(movie.vote_average).toFixed(1)} / 10
                </span>
              )}
              <span>{year}</span>
              <span className="px-3 py-1 rounded-full bg-white/5 border border-white/10">
                {movie.original_language?.toUpperCase() || "EN"}
              </span>
            </div>

            <p className="text-gray-200 leading-relaxed">
              {movie.overview || "No synopsis yet, but this pick comes highly rated."}
            </p>

            <div className="flex flex-wrap gap-3 pt-2">
              <button className="inline-flex items-center gap-2 rounded-xl bg-red-600 px-5 py-3 font-semibold text-white shadow-lg shadow-red-600/30 transition hover:-translate-y-0.5 hover:bg-red-500">
                <Play className="w-5 h-5" />
                Watch trailer
              </button>
              <button className="inline-flex items-center gap-2 rounded-xl border border-white/15 bg-white/5 px-5 py-3 font-semibold text-white transition hover:border-white/30">
                <Star className="w-4 h-4" />
                Save to list
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
