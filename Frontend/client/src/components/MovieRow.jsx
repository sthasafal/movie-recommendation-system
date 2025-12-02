import MovieCard from "./MovieCard";

export default function MovieRow({ title, movies }) {
  return (
    <div className="px-10 mt-10">
      <h2 className="text-xl font-bold mb-3">{title}</h2>

      <div className="flex space-x-4 overflow-x-scroll scrollbar-hide pb-4">
        {movies.map((movie) => (
          <MovieCard key={movie.id || movie.movie_id} movie={movie} />
        ))}
      </div>
    </div>
  );
}
    