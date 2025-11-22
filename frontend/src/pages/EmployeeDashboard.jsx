import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import { getAssignments } from "../api/assignments";
import "../styles/dashboard.css";

export default function EmployeeDashboard() {
  const navigate = useNavigate();
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchAssignments = async () => {
      try {
        console.log("Fetching assignments...");
        const data = await getAssignments();
        console.log("Assignments fetched:", data);
        setAssignments(data.data || []);
        setError("");
      } catch (err) {
        console.error("Error fetching assignments:", err);
        setError("Failed to load assignments: " + (err.message || "Unknown error"));
      } finally {
        setLoading(false);
      }
    };

    fetchAssignments();
  }, []);

  return (
    <>
      <Sidebar />
      <Navbar />

      <div className="dashboard-container">
        <h2>Welcome Employee 👨‍💻</h2>

        {error && <p style={{ color: "red" }}>{error}</p>}
        {loading && <p>Loading assignments...</p>}

        <p>Your assigned tests:</p>

        <div className="assignments-list">
          {assignments.length === 0 ? (
            <p>No assignments available yet.</p>
          ) : (
            assignments.map((assignment) => (
              <div key={assignment.id} className="assignment-card">
                <h3>{assignment.title}</h3>
                <p><strong>Domain:</strong> {assignment.domain}</p>
                <p><strong>Difficulty:</strong> {assignment.difficulty}</p>
                <p>{assignment.description}</p>
                <button
                  className="start-btn"
                  onClick={() => navigate(`/editor/${assignment.id}`)}
                >
                  Start Test
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </>
  );
}
