import { createContext, useContext, useEffect, useMemo, useState } from "react";

const AuthContext = createContext(null);

function AuthProvider({ children }) {
  const [userId, setUserId] = useState(() => {
    const stored = localStorage.getItem("user_id");
    return stored || "";
  });

  useEffect(() => {
    if (userId) {
      localStorage.setItem("user_id", userId);
    } else {
      localStorage.removeItem("user_id");
    }
  }, [userId]);

  const value = useMemo(
    () => ({
      userId,
      isAuthed: Boolean(userId),
      login: (id) => setUserId(id),
      logout: () => setUserId(""),
    }),
    [userId]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
}

export { AuthProvider, useAuth };
