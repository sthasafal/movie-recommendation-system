import { useNavigate } from "react-router-dom";
import { buildPosterUrl } from "../utils/images";

function MovieCard({ movie, onSelect }) {
  const navigate = useNavigate();

  const handleClick = () => {
    onSelect?.(movie);
    navigate(`/movie/${movie.movie_id}`);
  };

  return (
    <div className="movie-card" onClick={handleClick} role="button">
      {movie.poster_path && (
        <img className="poster" src={buildPosterUrl(movie.poster_path)} alt={movie.title} loading="lazy" />
      )}
      <div className="card-body">
        <h4>{movie.title}</h4>
        <div className="meta">
          {movie.vote_average ? <span className="badge">★ {Number(movie.vote_average).toFixed(1)}</span> : null}
          {typeof movie.score === "number" ? <span className="badge">Match {movie.score.toFixed(2)}</span> : null}
          <span className="badge">ID {movie.movie_id}</span>
        </div>
      </div>
    </div>
  );
}

export default MovieCard;
