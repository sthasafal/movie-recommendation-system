import React from "react";
import { Star } from "lucide-react";

const buildPoster = (path, size = "w500") => {
  if (!path) return "";
  if (path.startsWith("http")) return path;
  return `https://image.tmdb.org/t/p/${size}${path}`;
};

export default function MovieCard({ movie, onClick }) {
  const title = movie.title || "Untitled";
  const imageUrl = buildPoster(movie.poster_path);
  const year = movie.release_date ? movie.release_date.split("-")[0] : "—";

  return (
    <button
      onClick={onClick}
      className="group relative w-44 sm:w-48 flex-shrink-0 text-left focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500 rounded-2xl"
    >
      <div className="relative aspect-[2/3] overflow-hidden rounded-2xl border border-white/8 bg-gradient-to-br from-[#0f172a] to-[#0b1120]">
        {imageUrl ? (
          <img
            src={imageUrl}
            alt={title}
            className="h-full w-full object-cover transition duration-300 group-hover:scale-[1.03]"
          />
        ) : (
          <div className="h-full w-full flex items-center justify-center text-sm text-gray-500">
            No image
          </div>
        )}
        <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition bg-gradient-to-t from-black/80 via-black/50 to-transparent" />
        <div className="absolute bottom-3 left-3 right-3 flex items-center justify-between text-xs text-gray-200">
          <span className="font-semibold line-clamp-1">{title}</span>
          {movie.vote_average && (
            <span className="flex items-center gap-1 text-amber-300">
              <Star className="w-3 h-3 fill-amber-300" />
              {Number(movie.vote_average).toFixed(1)}
            </span>
          )}
        </div>
      </div>
      <p className="mt-2 text-sm text-gray-400">{year}</p>
    </button>
  );
}
