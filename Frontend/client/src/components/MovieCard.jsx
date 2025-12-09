export default function MovieCard({ movie }) {
  return (
    <div className="w-40 shrink-0 cursor-pointer hover:scale-110 transition">
      <img
        src={
          movie.poster_path
            ? `https://image.tmdb.org/t/p/w300${movie.poster_path}`
            : "/no-poster.png"
        }
        alt={movie.title}
        className="rounded-md"
      />
    </div>
  );
}
