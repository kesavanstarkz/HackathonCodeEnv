import "../styles/dashboard.css";

export default function Navbar() {

  function logout() {
    localStorage.removeItem("token");
    window.location.href = "/";
  }

  return (
    <div className="navbar">
      <h1 className="navbar-title">Coding Assessment Admin Panel</h1>
      <button className="logout-btn" onClick={logout}>Logout</button>
    </div>
  );
}
