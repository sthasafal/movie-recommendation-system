import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getMovie, getSimilar } from "../api/movies";
import MovieRow from "../components/MovieRow";
import { useAuth } from "../context/AuthContext";
import { buildPosterUrl } from "../utils/images";

function MovieDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { userId } = useAuth();

  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [similar, setSimilar] = useState([]);
  const [similarStatus, setSimilarStatus] = useState({ loading: true, error: "" });

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      setError("");
      try {
        const data = await getMovie(id);
        setMovie(data);
      } catch (err) {
        setError(err.message || "Could not load movie");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id]);

  useEffect(() => {
    const loadSimilar = async () => {
      setSimilarStatus({ loading: true, error: "" });
      try {
        const data = await getSimilar(id, 12);
        setSimilar(data);
      } catch (err) {
        setSimilarStatus({ loading: false, error: err.message || "Could not load similar titles" });
        return;
      }
      setSimilarStatus({ loading: false, error: "" });
    };
    loadSimilar();
  }, [id]);

  if (loading) {
    return (
      <div className="section">
        <div className="muted">Loading movie…</div>
      </div>
    );
  }

  if (error || !movie) {
    return (
      <div className="section">
        <div className="error">{error || "Movie not found"}</div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="nav">
        <div className="brand" role="button" onClick={() => navigate("/")}>
          <div className="brand-mark">MR</div>
          <div className="brand-name">Movie Recommendations</div>
        </div>
        <div className="nav-actions">
          <span className="pill">User #{userId || "guest"}</span>
          <button className="ghost-btn" onClick={() => navigate("/")}>
            Back to home
          </button>
        </div>
      </div>

      <div className="section">
        <div className="layout">
          <div className="stack">
            <h1>{movie.title}</h1>
            <div className="meta">
              <span className="badge">ID {movie.movie_id}</span>
              {movie.vote_average ? <span className="badge">★ {Number(movie.vote_average).toFixed(1)}</span> : null}
            </div>
            <p className="muted">{movie.overview || "No description available."}</p>
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

      <MovieRow
        title="More like this"
        subtitle="Because you watched this title"
        items={similar}
        loading={similarStatus.loading}
        error={similarStatus.error}
      />
    </div>
  );
}

export default MovieDetail;
