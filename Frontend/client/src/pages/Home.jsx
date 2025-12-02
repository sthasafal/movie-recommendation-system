import Hero from "../components/Hero";
import MovieRow from "../components/MovieRow";

export default function Home() {
  // Temporary static data before connecting backend
  const sampleMovies = [
    { id: 1, title: "Movie 1", poster_path: "/kqjL17yufvn9OVLyXYpvtyrFfak.jpg" },
    { id: 2, title: "Movie 2", poster_path: "/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg" },
    { id: 3, title: "Movie 3", poster_path: "/mW6hFjlH5OFQvSW2tNpjj9i7nBg.jpg" },
  ];

  return (
    <div>
      <Hero />
      <MovieRow title="Trending Now" movies={sampleMovies} />
      <MovieRow title="Top Picks For You" movies={sampleMovies} />
      <MovieRow title="New Releases" movies={sampleMovies} />
    </div>
  );
}
