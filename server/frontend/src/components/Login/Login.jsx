import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const Login = () => {
  const navigate = useNavigate();
  const [loginForm, setLoginForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setLoginForm({
      ...loginForm,
      [e.target.name]: e.target.value,
    });
  };

  const login = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const csrfToken = getCookie("csrftoken");

      const response = await fetch("/djangoapp/login", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken || "",
          "Accept": "application/json",
        },
        body: JSON.stringify({
          username: loginForm.username,
          password: loginForm.password,
        }),
      });

      // Read as text first so we can handle JSON OR HTML error pages safely
      const raw = await response.text();

      let data = {};
      try {
        data = raw ? JSON.parse(raw) : {};
      } catch (parseErr) {
        console.error("Login response was not JSON:", raw);
        throw new Error("Server returned a non-JSON response.");
      }

      // Save user info (support both naming styles used in capstone code)
      const userName = data.userName || data.username || loginForm.username;
      const fullName = data.fullName || data.fullname || data.name || "";

      if (userName) {
        localStorage.setItem("userName", userName);
        localStorage.setItem("username", userName);
        sessionStorage.setItem("userName", userName);
        sessionStorage.setItem("username", userName);
      }

      if (fullName) {
        localStorage.setItem("fullName", fullName);
        localStorage.setItem("fullname", fullName);
        sessionStorage.setItem("fullName", fullName);
        sessionStorage.setItem("fullname", fullName);
      }

      if (response.ok && (data.status === 200 || data.userName || data.username)) {
        navigate("/dealers");
      } else {
        setError(data.message || "Invalid username or password");
      }
    } catch (err) {
      console.error("Login error:", err);
      setError(err.message || "An error occurred during login.");
    }
  };

  return (
    <div className="container mt-4">
      <h2>Login</h2>
      <form onSubmit={login} style={{ maxWidth: "400px" }}>
        <div className="mb-3">
          <label className="form-label">Username</label>
          <input
            name="username"
            type="text"
            className="form-control"
            value={loginForm.username}
            onChange={handleChange}
            required
            autoComplete="username"
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Password</label>
          <input
            name="password"
            type="password"
            className="form-control"
            value={loginForm.password}
            onChange={handleChange}
            required
            autoComplete="current-password"
          />
        </div>

        {error && <div className="alert alert-danger py-2">{error}</div>}

        <button type="submit" className="btn btn-primary">
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;