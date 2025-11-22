import { useState } from "react";
import api from "../api/auth";
import "../styles/auth.css";

export default function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("employee");
  const [domain, setDomain] = useState("general");

  async function handleRegister(e) {
    e.preventDefault();
    try {
      await api.post("/auth/register", {
        name,
        email,
        password,
        role,
        domain,
      });
      alert("Registration successful!");
      window.location.href = "/";
    } catch (err) {
      alert("Registration failed: " + (err.response?.data?.detail || err.message));
    }
  }

  return (
    <div className="auth-wrapper">
      <div className="auth-box">
        <h2 className="auth-title">Register</h2>

        <form onSubmit={handleRegister}>
          <input
            className="auth-input"
            placeholder="Full Name"
            onChange={(e) => setName(e.target.value)}
          />

          <input
            className="auth-input"
            placeholder="Email"
            type="email"
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            className="auth-input"
            placeholder="Password"
            type="password"
            onChange={(e) => setPassword(e.target.value)}
          />

          <select className="auth-input" value={role} onChange={(e) => setRole(e.target.value)}>
            <option value="employee">Employee</option>
            <option value="admin">Admin</option>
          </select>

          <input
            className="auth-input"
            placeholder="Domain"
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
          />

          <button className="auth-btn">Register</button>
        </form>
      </div>
    </div>
  );
}
