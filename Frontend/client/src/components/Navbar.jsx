import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between px-10 py-4 bg-black bg-opacity-40 fixed top-0 w-full z-50 backdrop-blur-md">
      <div className="flex items-center space-x-8">
        <Link to="/" className="text-red-600 text-4xl font-extrabold">
          Movie Recommendation System
        </Link>

        <div className="flex space-x-6 text-sm">
          <Link to="/" className="hover:text-gray-300">Home</Link>
          <Link to="/recommend" className="hover:text-gray-300">Recommended</Link>
        </div>
      </div>

      <div className="flex items-center space-x-4">
        <input
          className="px-3 py-1 bg-gray-800 text-white rounded focus:outline-none"
          placeholder="Search…"
        />
      </div>
    </nav>
  );
}
