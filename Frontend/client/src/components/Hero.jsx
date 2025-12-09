import React from "react";

export default function Hero({ movie }) {
  if (!movie) return null;

  return (
    <div 
      className="h-[75vh] w-full bg-cover bg-center relative"
      style={{
        backgroundImage: `url(https://image.tmdb.org/t/p/original${movie.poster_path})`,
      }}
    >
      <div className="absolute inset-0 bg-gradient-to-t from-black to-transparent"></div>

      <div className="absolute bottom-20 left-10 max-w-xl">
        <h1 className="text-5xl font-bold mb-4">{movie.title}</h1>
        <p className="text-lg mb-6 line-clamp-3">{movie.overview}</p>

        <div className="flex items-center gap-4">
          <button className="bg-white text-black px-6 py-2 rounded-lg font-semibold">
            Play
          </button>
          <button className="bg-[#333] text-white px-6 py-2 rounded-lg font-semibold">
            More Info
          </button>
        </div>
      </div>
    </div>
  );
}
