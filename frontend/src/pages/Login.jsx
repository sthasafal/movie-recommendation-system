import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [userId, setUserId] = useState("1");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = userId.trim();
    if (!trimmed) {
      setError("Please enter a user id");
      return;
    }
    setError("");
    login(trimmed);
    navigate("/");
  };

  return (
    <div className="splash">
      <form className="login-card" onSubmit={handleSubmit}>
        <h1>Welcome back</h1>
        <p>Sign in to get personalized picks.</p>
        <div className="stack">
          <label className="muted" htmlFor="userId">
            User ID (numeric from the dataset)
          </label>
          <input
            id="userId"
            className="input"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="e.g., 1"
          />
          {error ? <div className="error">{error}</div> : null}
          <button className="btn" type="submit">
            Continue
          </button>
          <span className="muted">No signup required — pick any user id from MovieLens.</span>
        </div>
      </form>
    </div>
  );
}

export default Login;
