import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import "./App.css";

export default function App() {
  return (
    <div className="app-shell">
      <Navbar />
      <Home />
    </div>
  );
}

