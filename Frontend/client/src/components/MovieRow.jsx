import React, { useRef } from "react";
import { ChevronLeft, ChevronRight, Star, TrendingUp, Film } from "lucide-react";
import MovieCard from "./MovieCard";

export default function MovieRow({ title, movies = [], onMovieClick }) {
  const rowRef = useRef(null);

  const scroll = (direction) => {
    if (rowRef.current) {
      const scrollAmount = direction === "left" ? -700 : 700;
      rowRef.current.scrollBy({ left: scrollAmount, behavior: "smooth" });
    }
  };

  const getIcon = () => {
    if (title?.toLowerCase().includes("recommended")) return <Star className="w-5 h-5" />;
    if (title?.toLowerCase().includes("trending")) return <TrendingUp className="w-5 h-5" />;
    return <Film className="w-5 h-5" />;
  };

  if (!movies.length) {
    return (
      <div className="px-1">
        <div className="flex items-center gap-3 mb-3 text-gray-400">
          <div className="text-red-500">{getIcon()}</div>
          <h2 className="text-xl font-semibold">{title}</h2>
        </div>
        <div className="rounded-2xl border border-dashed border-white/10 bg-white/5 px-4 py-6 text-sm text-gray-400">
          No movies yet. We&apos;ll add picks as soon as they load.
        </div>
      </div>
    );
  }

  return (
    <div className="group">
      <div className="flex items-center gap-3 mb-4">
        <div className="text-red-500">{getIcon()}</div>
        <h2 className="text-2xl font-bold">{title}</h2>
      </div>

      <div className="relative">
        <button
          type="button"
          onClick={() => scroll("left")}
          className="absolute left-0 top-0 bottom-0 z-10 w-12 bg-gradient-to-r from-[#05070f] to-transparent opacity-0 group-hover:opacity-100 transition flex items-center justify-center"
        >
          <ChevronLeft className="w-8 h-8" />
        </button>

        <div
          ref={rowRef}
          className="flex gap-4 overflow-x-auto scrollbar-hide scroll-smooth pb-4 pr-6"
          style={{ scrollbarWidth: "none" }}
        >
          {movies.map((movie) => (
            <MovieCard
              key={movie.id || movie.movie_id}
              movie={movie}
              onClick={() => onMovieClick?.(movie)}
            />
          ))}
        </div>

        <button
          type="button"
          onClick={() => scroll("right")}
          className="absolute right-0 top-0 bottom-0 z-10 w-12 bg-gradient-to-l from-[#05070f] to-transparent opacity-0 group-hover:opacity-100 transition flex items-center justify-center"
        >
          <ChevronRight className="w-8 h-8" />
        </button>
      </div>
    </div>
  );
}
