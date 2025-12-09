// src/pages/Home.jsx

import React, { useEffect, useState } from "react";
import api from "../api/axiosClient";        // ✅ Correct path
import Hero from "../components/Hero";       // Hero Banner
import MovieRow from "../components/MovieRow"; // Horizontal Movie Row

export default function Home() {
  const [recommended, setRecommended] = useState([]);
  const [similar, setSimilar] = useState([]);
 // const [popular, setPopular] = useState([]);

  useEffect(() => {
    // Fetch recommended movies for demo user 6
    api.get("/recommend/6")
      .then(res => {
        if (res.data && Array.isArray(res.data.movies)) {
          setRecommended(res.data.movies);
        }
      })
      .catch(err => console.error("Recommended Error:", err));

    // Fetch similar movies for movie 50 (ex: Star Wars)
    api.get("/recommend/similar/50")
      .then(res => {
        if (res.data && Array.isArray(res.data.movies)) {
          setSimilar(res.data.movies);
        }
      })
      .catch(err => console.error("Similar Error:", err));
  }, []);

  return (
    <div className="min-h-screen bg-black text-white pb-20">
      {/* HERO SECTION */}
      <Hero movie={recommended[0]} />

      {/* MOVIE ROWS */}
      <div className="mt-10 px-8 space-y-10">
        <MovieRow title="Recommended for You" movies={recommended} />
        <MovieRow title="Because You Watched Similar Movies" movies={similar} />
      </div>
    </div>
  );
}
