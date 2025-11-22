import React, { useState, useEffect } from 'react';
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import { getAssignments, getAssignmentStats, getCompletionStats } from '../api/assignments';
import "../styles/dashboard.css";

export default function SubmissionsPage() {
  const [assignments, setAssignments] = useState([]);
  const [stats, setStats] = useState({});
  const [completionStats, setCompletionStats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const assignmentsResponse = await getAssignments();

        setAssignments(assignmentsResponse.data || []);
        // Temporarily disable completion stats due to backend issue
        setCompletionStats([]);

        // Fetch stats for all assignments individually to handle errors
        const statsMap = {};
        for (const assignment of assignmentsResponse.data || []) {
          try {
            const statResponse = await getAssignmentStats(assignment.id);
            statsMap[assignment.id] = statResponse.data;
          } catch (statError) {
            console.error(`Error fetching stats for assignment ${assignment.id}:`, statError);
            // Set default stats
            statsMap[assignment.id] = { submitted: 0, remaining: 0, total_submissions: 0 };
          }
        }
        setStats(statsMap);
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Failed to load data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const calculateProgress = (submitted, remaining) => {
    const total = submitted + remaining;
    return total > 0 ? (submitted / total) * 100 : 0;
  };

  if (loading) {
    return (
      <>
        <Sidebar />
        <Navbar />
        <div className="dashboard-container">
          <h2>Submissions Overview</h2>
          <p>Loading...</p>
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <Sidebar />
        <Navbar />
        <div className="dashboard-container">
          <h2>Submissions Overview</h2>
          <p style={{ color: 'red' }}>{error}</p>
        </div>
      </>
    );
  }

  return (
    <>
      <Sidebar />
      <Navbar />

      <div className="dashboard-container">
        <h2>Submissions Overview</h2>

        {/* Completion Stats Section */}
        <div className="completion-stats-section">
          <h3>Employee Completion Statistics</h3>
          <p>How many employees completed how many assignments</p>
          {completionStats.length === 0 ? (
            <p>No completion data available.</p>
          ) : (
            <div className="completion-stats-grid">
              {completionStats.map((stat, index) => (
                <div key={index} className="completion-stat-card">
                  <div className="completion-number">{stat.assignments_completed}</div>
                  <div className="completion-label">
                    {stat.assignments_completed === 1 ? 'Assignment' : 'Assignments'}
                  </div>
                  <div className="completion-users">{stat.user_count} Employees</div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Assignments Section */}
        <div className="assignments-section">
          <h3>Assignment Submission Status</h3>
          {assignments.length === 0 ? (
            <p>No assignments found.</p>
          ) : (
            <div className="assignments-list">
              {assignments.map(assignment => (
                <div key={assignment.id} className="assignment-card">
                  <h4>{assignment.title}</h4>
                  <p>{assignment.description}</p>
                  <p>Domain: {assignment.domain} | Difficulty: {assignment.difficulty}</p>
                  {stats[assignment.id] && (
                    <div className="stats">
                      <div className="stat-item">
                        <span>Employees Submitted: {stats[assignment.id].submitted}</span>
                        <span>Remaining: {stats[assignment.id].remaining}</span>
                      </div>
                      <div className="progress-bar">
                        <div
                          className="progress-fill"
                          style={{
                            width: `${calculateProgress(stats[assignment.id].submitted, stats[assignment.id].remaining)}%`
                          }}
                        ></div>
                      </div>
                      <p className="progress-text">
                        {Math.round(calculateProgress(stats[assignment.id].submitted, stats[assignment.id].remaining))}% Submitted
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
}
