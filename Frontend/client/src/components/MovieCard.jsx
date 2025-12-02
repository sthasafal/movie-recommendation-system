export default function MovieCard({ movie }) {
  return (
    <div className="min-w-[180px] transform transition duration-300 hover:scale-110 cursor-pointer">
      {movie.poster_path ? (
        <img
          src={`https://image.tmdb.org/t/p/w300${movie.poster_path}`}
          alt={movie.title}
          className="rounded-md shadow-lg"
        />
      ) : (
        <div className="w-[180px] h-[270px] bg-gray-700 rounded-md"></div>
      )}
    </div>
  );
}
