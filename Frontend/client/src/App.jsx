import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Movie from "./pages/Movie";
import Recommendations from "./pages/Recommendations";

function App() {
  return (
    <div className="bg-gray-900 min-h-screen text-white">
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/movie/:id" element={<Movie />} />
        <Route path="/recommend" element={<Recommendations />} />
      </Routes>
    </div>
  );
}

export default App;
