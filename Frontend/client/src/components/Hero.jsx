export default function Hero() {
  return (
    <div className="relative h-[70vh] w-full">
      <img
        src="https://image.tmdb.org/t/p/original/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg"
        className="w-full h-full object-cover brightness-75"
        alt="Hero Movie"
      />

      <div className="absolute inset-0 bg-gradient-to-t from-[#141414] to-transparent"></div>

      <div className="absolute bottom-20 left-10 space-y-4 max-w-xl">
        <h1 className="text-5xl font-extrabold">Movie Title Here</h1>
        <p className="text-gray-300">
          A short overview or tagline describing the movie. This will be replaced later with real data.
        </p>

        <div className="flex space-x-3">
          <button className="bg-white text-black px-6 py-2 rounded font-semibold hover:bg-gray-300">
            ▶ Play
          </button>
          <button className="bg-gray-700 bg-opacity-80 px-6 py-2 rounded font-semibold hover:bg-gray-600">
            More Info
          </button>
        </div>
      </div>
    </div>
  );
}
