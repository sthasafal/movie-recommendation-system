import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-gray-800 px-6 py-4 flex justify-between items-center shadow-lg">
      <Link to="/" className="text-2xl font-bold text-blue-400">
        🎬 Movie Recommender
      </Link>

      <div className="flex space-x-6">
        <Link to="/" className="hover:text-blue-300">Home</Link>
        <Link to="/recommend" className="hover:text-blue-300">For You</Link>
      </div>
    </nav>
  );
}
