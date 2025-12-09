import MovieCard from "./MovieCard";

export default function MovieRow({ title, movies }) {
  return (
    <div className="my-8">
      <h2 className="text-xl font-semibold mb-4">{title}</h2>
      <div className="flex gap-4 overflow-x-auto no-scrollbar pb-4">
        {movies.map((m) => (
          <MovieCard key={m.movie_id || m.id} movie={m} />
        ))}
      </div>
    </div>
  );
}
