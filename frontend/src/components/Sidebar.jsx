import { Link } from "react-router-dom";
import "../styles/dashboard.css";

export default function Sidebar() {
  return (
    <div className="sidebar">
      <h2 className="sidebar-title">Admin</h2>

      <ul className="sidebar-menu">
        <li><Link to="/admin">Dashboard</Link></li>
        <li><Link to="/admin/create-assignment">Create Assignment</Link></li>
        <li><Link to="/admin/submissions">Submissions</Link></li>
      </ul>
    </div>
  );
}
