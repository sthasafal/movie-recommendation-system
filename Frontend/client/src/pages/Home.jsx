import React, { useEffect, useState } from "react";
import api from "../api/axiosClient";
import { mockAPI } from "../api/mockAPI";
import Hero from "../components/Hero";
import MovieRow from "../components/MovieRow";
import Loading from "../components/Loading";
import MovieModal from "../components/MovieModal";

export default function Home() {
  const [recommended, setRecommended] = useState([]);
  const [similar, setSimilar] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeMovie, setActiveMovie] = useState(null);

  useEffect(() => {
    const loadMovies = async () => {
      setLoading(true);
      try {
        const [recommendedRes, similarRes] = await Promise.all([
          api.get("/recommend/6"),
          api.get("/recommend/similar/50"),
        ]);

        setRecommended(recommendedRes.data?.movies || []);
        setSimilar(similarRes.data?.movies || []);
      } catch (error) {
        console.error("Falling back to mock API:", error);
        const [recommendedRes, similarRes] = await Promise.all([
          mockAPI.getRecommended(6),
          mockAPI.getSimilar(50),
        ]);
        setRecommended(recommendedRes.movies || []);
        setSimilar(similarRes.movies || []);
      } finally {
        setLoading(false);
      }
    };

    loadMovies();
  }, []);

  const handleMovieClick = (movie) => setActiveMovie(movie);

  if (loading) {
    return <Loading />;
  }

  return (
    <div className="min-h-screen text-white pb-16 space-y-10">
      <Hero movie={recommended[0] || similar[0]} onMoreInfo={handleMovieClick} />

      <div className="px-4 md:px-8 space-y-8">
        <MovieRow
          title="Recommended for You"
          movies={recommended}
          onMovieClick={handleMovieClick}
        />
        <MovieRow
          title="Because You Watched Similar Movies"
          movies={similar}
          onMovieClick={handleMovieClick}
        />
      </div>

      {activeMovie && (
        <MovieModal movie={activeMovie} onClose={() => setActiveMovie(null)} />
      )}
    </div>
  );
}
