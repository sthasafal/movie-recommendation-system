export default function Loading() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0b0b0f] text-white">
      <div className="flex items-center space-x-3">
        <div className="h-10 w-10 rounded-full border-2 border-red-600 border-t-transparent animate-spin" />
        <p className="text-lg tracking-wide">Loading</p>
      </div>
    </div>
  );
}
