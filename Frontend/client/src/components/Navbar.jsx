import React, { useState } from "react";
import { IoSearch } from "react-icons/io5";

export default function Navbar() {
  const [query, setQuery] = useState("");

  return (
    <header className="sticky top-0 left-0 right-0 z-40 bg-[#05070f]/70 backdrop-blur-md border-b border-white/5">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="h-11 w-11 rounded-2xl bg-gradient-to-br from-red-600 to-orange-400 flex items-center justify-center text-lg font-bold text-white">
            MX
          </div>
          <div>
            <p className="text-lg font-semibold">MovieX</p>
            <p className="text-xs text-gray-400">Smart picks for tonight</p>
          </div>
        </div>

        <nav className="hidden md:flex items-center gap-5 text-sm text-gray-300">
          <button className="hover:text-white transition-colors">Home</button>
          <button className="hover:text-white transition-colors">Movies</button>
          <button className="hover:text-white transition-colors">Series</button>
          <button className="hover:text-white transition-colors">My List</button>
        </nav>

        <div className="flex items-center gap-3">
          <div className="relative">
            <IoSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Find a movie..."
              className="pl-10 pr-3 py-2 w-48 md:w-64 rounded-xl bg-white/5 border border-white/10 text-sm text-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500/60"
            />
          </div>
          <img
            src="https://i.pravatar.cc/40"
            alt="User"
            className="rounded-xl w-9 h-9 border border-white/10"
          />
        </div>
      </div>
    </header>
  );
}
