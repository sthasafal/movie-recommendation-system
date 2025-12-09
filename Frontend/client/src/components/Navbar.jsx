import React from "react";
import { IoSearch } from "react-icons/io5";

export default function Navbar() {
  return (
    <div className="fixed top-0 left-0 w-full z-50 bg-black bg-opacity-60 backdrop-blur-sm">
      <div className="flex items-center justify-between px-8 py-4">
        <h1 className="text-3xl font-bold text-red-600">MovieX</h1>

        <div className="flex items-center gap-4">
          <IoSearch className="text-2xl cursor-pointer" />
          <img
            src="https://i.pravatar.cc/40"
            alt="User"
            className="rounded-full w-8 h-8 cursor-pointer"
          />
        </div>
      </div>
    </div>
  );
}
