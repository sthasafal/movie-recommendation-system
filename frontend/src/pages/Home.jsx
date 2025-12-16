import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getHybridForUser, getModelRecommendations, getSimilar, getTrending, searchMovies } from "../api/movies";
import Hero from "../components/Hero";
import MovieRow from "../components/MovieRow";
import SearchBar from "../components/SearchBar";
import { useAuth } from "../context/AuthContext";

function Home({ onThemeToggle, theme }) {
  const { isAuthed, userId } = useAuth();
  const navigate = useNavigate();

  const [trending, setTrending] = useState([]);
  const [trendingStatus, setTrendingStatus] = useState({ loading: true, error: "" });

  const [recommended, setRecommended] = useState([]);
  const [recommendedStatus, setRecommendedStatus] = useState({ loading: true, error: "" });

  const [community, setCommunity] = useState([]);
  const [communityStatus, setCommunityStatus] = useState({ loading: true, error: "" });

  const [anchorMovie, setAnchorMovie] = useState(null);
  const [anchorSimilar, setAnchorSimilar] = useState([]);
  const [anchorStatus, setAnchorStatus] = useState({ loading: true, error: "" });

  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [searchStatus, setSearchStatus] = useState({ loading: false, error: "" });

  useEffect(() => {
    if (!isAuthed) {
      navigate("/login");
    }
  }, [isAuthed, navigate]);

  useEffect(() => {
    if (!userId) return;
    const loadTrending = async () => {
      setTrendingStatus({ loading: true, error: "" });
      try {
        const data = await getTrending(18);
        setTrending(Array.isArray(data) ? data : data?.recommendations || []);
      } catch (err) {
        setTrendingStatus({ loading: false, error: err.message || "Could not load trending" });
        return;
      }
      setTrendingStatus({ loading: false, error: "" });
    };

    const loadRecommended = async () => {
      setRecommendedStatus({ loading: true, error: "" });
      try {
        const data = await getHybridForUser(userId, 18);
        setRecommended(data);
      } catch (err) {
        setRecommendedStatus({ loading: false, error: err.message || "Could not load personalized picks" });
        return;
      }
      setRecommendedStatus({ loading: false, error: "" });
    };

    const loadCommunity = async () => {
      setCommunityStatus({ loading: true, error: "" });
      try {
        const data = await getModelRecommendations("svd", userId, 12);
        setCommunity(data);
      } catch (err) {
        setCommunityStatus({ loading: false, error: err.message || "Could not load community picks" });
        return;
      }
      setCommunityStatus({ loading: false, error: "" });
    };

    loadTrending();
    loadRecommended();
    loadCommunity();
  }, [userId]);

  const anchorSource = useMemo(() => {
    if (trending.length) return trending[0];
    if (recommended.length) return recommended[0];
    return null;
  }, [trending, recommended]);

  useEffect(() => {
    if (!anchorSource) return;
    setAnchorMovie(anchorSource);
    const load = async () => {
      setAnchorStatus({ loading: true, error: "" });
      try {
        const data = await getSimilar(anchorSource.movie_id, 12);
        setAnchorSimilar(data);
      } catch (err) {
        setAnchorStatus({ loading: false, error: err.message || "Could not load similar titles" });
        return;
      }
      setAnchorStatus({ loading: false, error: "" });
    };
    load();
  }, [anchorSource]);

  const runSearch = async () => {
    if (!searchTerm.trim()) {
      setSearchResults([]);
      return;
    }
    setSearchStatus({ loading: true, error: "" });
    try {
      const data = await searchMovies(searchTerm.trim(), 20);
      setSearchResults(data || []);
    } catch (err) {
      setSearchStatus({ loading: false, error: err.message || "Search failed" });
      return;
    }
    setSearchStatus({ loading: false, error: "" });
  };

  return (
    <div className="page">
      <div className="nav">
        <div className="brand" role="button" onClick={() => navigate("/")}>
          <div className="brand-mark">MR</div>
          <div>
            <div className="brand-name">Movie Recommendations</div>
            <div className="muted" style={{ fontSize: "0.9rem" }}>
              Personalized picks without the jargon.
            </div>
          </div>
        </div>
        <div className="nav-actions">
          <span className="pill">User #{userId || "guest"}</span>
          <button className="toggle-btn" onClick={onThemeToggle}>
            {theme === "light" ? "☀️ Light" : "🌙 Dark"}
          </button>
          <button className="ghost-btn" onClick={() => navigate("/login")}>
            Switch user
          </button>
        </div>
      </div>

      <Hero movie={anchorMovie} onWatch={(m) => setAnchorMovie(m)} />

      <div className="section">
        <div className="section-header">
          <div className="section-title">
            <h3>Search</h3>
            <span>Find any title and jump into details.</span>
          </div>
        </div>
        <SearchBar
          value={searchTerm}
          onChange={setSearchTerm}
          onSubmit={runSearch}
          placeholder="Search movies by title or keywords"
        />
        {searchStatus.error ? <div className="error">{searchStatus.error}</div> : null}
        {searchStatus.loading ? <div className="muted">Searching…</div> : null}
        {searchResults.length > 0 ? (
          <MovieRow title="Search results" subtitle="From the catalog" items={searchResults} />
        ) : null}
      </div>

      <MovieRow
        title="Trending Now"
        subtitle="Popular with viewers right now"
        items={trending}
        loading={trendingStatus.loading}
        error={trendingStatus.error}
      />

      <MovieRow
        title="Recommended For You"
        subtitle="Based on your watch history"
        items={recommended}
        loading={recommendedStatus.loading}
        error={recommendedStatus.error}
      />

      <MovieRow
        title="Because you watched"
        subtitle={anchorMovie ? anchorMovie.title : "Similar picks"}
        items={anchorSimilar}
        loading={anchorStatus.loading}
        error={anchorStatus.error}
      />

      <MovieRow
        title="From viewers like you"
        subtitle="What similar viewers enjoy"
        items={community}
        loading={communityStatus.loading}
        error={communityStatus.error}
      />
    </div>
  );
}

export default Home;
