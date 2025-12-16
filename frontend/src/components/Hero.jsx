import { useNavigate } from "react-router-dom";
import { buildPosterUrl } from "../utils/images";

function Hero({ movie, onWatch }) {
  const navigate = useNavigate();
  if (!movie) return null;

  const goToDetail = () => {
    navigate(`/movie/${movie.movie_id}`);
    onWatch?.(movie);
  };

  return (
    <div className="hero">
      <div className="hero-card">
        <div>
          <h1>{movie.title}</h1>
          <div className="meta">
            <span className="badge">ID {movie.movie_id}</span>
            {movie.vote_average ? <span className="badge">★ {Number(movie.vote_average).toFixed(1)}</span> : null}
            {typeof movie.score === "number" ? <span className="badge">Match {movie.score.toFixed(2)}</span> : null}
          </div>
          <p>{movie.overview || "Jump back into this feature film and explore similar stories."}</p>
          <div className="cta-row">
            <button className="btn" onClick={goToDetail}>
              View details
            </button>
            <button className="ghost-btn" onClick={() => onWatch?.(movie)}>
              More like this
            </button>
          </div>
        </div>
        <div>
          {movie.poster_path ? (
            <img className="hero-poster" src={buildPosterUrl(movie.poster_path)} alt={movie.title} />
          ) : (
            <div className="hero-poster" />
          )}
        </div>
      </div>
    </div>
  );
}

export default Hero;
