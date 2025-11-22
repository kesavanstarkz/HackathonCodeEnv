import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import { getAssignments, getAssignmentStats } from '../api/assignments';
import "../styles/dashboard.css";

export default function AdminDashboard() {
  const navigate = useNavigate();
  const [assignments, setAssignments] = useState([]);
  const [stats, setStats] = useState({});

  useEffect(() => {
    const fetchAssignments = async () => {
      try {
        const response = await getAssignments();
        setAssignments(response.data || []);
      } catch (error) {
        console.error('Error fetching assignments:', error);
        setAssignments([]);
      }
    };

    fetchAssignments();
  }, []);

  const fetchStats = async (assignmentId) => {
    try {
      const response = await getAssignmentStats(assignmentId);
      setStats(prevStats => ({
        ...prevStats,
        [assignmentId]: response.data
      }));
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  return (
    <>
      <Sidebar />
      <Navbar />

      <div className="dashboard-container">
        <h2>Welcome Admin 👋</h2>

        <div style={{ marginBottom: "20px" }}>
          <button
            onClick={() => navigate("/admin/create-assignment")}
            style={{
              padding: "10px 20px",
              backgroundColor: "#28a745",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
              fontSize: "16px",
            }}
          >
            + Create New Assignment
          </button>
        </div>

        <div className="assignments-list">
          {assignments.map(assignment => (
            <div key={assignment.id} className="assignment-card">
              <h3>{assignment.title}</h3>
              <p>{assignment.description}</p>
              <p>Domain: {assignment.domain} | Difficulty: {assignment.difficulty}</p>
              <button onClick={() => fetchStats(assignment.id)} className="stats-button">View Submission Stats</button>
              {stats[assignment.id] && (
                <div className="stats">
                  <div className="stat-item">
                    <span>Submitted: {stats[assignment.id].submitted}</span>
                    <span>Remaining: {stats[assignment.id].remaining}</span>
                  </div>
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{
                        width: `${(stats[assignment.id].submitted / (stats[assignment.id].submitted + stats[assignment.id].remaining)) * 100}%`
                      }}
                    ></div>
                  </div>
                  <p className="progress-text">
                    {Math.round((stats[assignment.id].submitted / (stats[assignment.id].submitted + stats[assignment.id].remaining)) * 100)}% Submitted
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
