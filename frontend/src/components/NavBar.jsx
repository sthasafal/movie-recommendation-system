import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function NavBar({ onToggleTheme, theme }) {
  const { userId, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="nav">
      <div className="brand" role="button" onClick={() => navigate("/")}>
        <div className="brand-mark">MR</div>
        <div className="brand-name">Movie Recommendations</div>
      </div>
      <div className="nav-actions">
        {userId ? <span className="pill">Signed in as #{userId}</span> : null}
        <button className="toggle-btn" onClick={onToggleTheme}>
          {theme === "light" ? "☀️ Light" : "🌙 Dark"}
        </button>
        {userId ? (
          <button className="ghost-btn" onClick={() => { logout(); navigate("/login"); }}>
            Sign out
          </button>
        ) : (
          <button className="ghost-btn" onClick={() => navigate("/login")}>
            Login
          </button>
        )}
      </div>
    </div>
  );
}

export default NavBar;
