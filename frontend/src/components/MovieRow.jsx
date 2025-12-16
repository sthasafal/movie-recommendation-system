import MovieCard from "./MovieCard";

function MovieRow({ title, subtitle, items = [], loading, error, onSelect }) {
  return (
    <div className="section">
      <div className="section-header">
        <div className="section-title">
          <h3>{title}</h3>
          {subtitle ? <span>{subtitle}</span> : null}
        </div>
      </div>
      {loading ? <div className="muted">Loading…</div> : null}
      {error ? <div className="error">{error}</div> : null}
      {!loading && !error && items.length === 0 ? (
        <div className="muted">No titles to show right now.</div>
      ) : null}
      <div className="scroll-row">
        {items.map((movie) => (
          <MovieCard key={movie.movie_id} movie={movie} onSelect={onSelect} />
        ))}
      </div>
    </div>
  );
}

export default MovieRow;
