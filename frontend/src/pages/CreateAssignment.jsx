import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createAssignment } from "../api/assignments";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import "../styles/dashboard.css";

export default function CreateAssignment() {
  const navigate = useNavigate();
  const [problemType, setProblemType] = useState("coding");
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    domain: "fullstack",
    difficulty: "medium",
    test_input: "",
    expected_output: "",
    sql_schema: "",
    sql_query: "",
  });
  const [testCases, setTestCases] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const addTestCase = () => {
    setTestCases([
      ...testCases,
      {
        input: "",
        expected_output: "",
        sql_query: "",
        expected_result: "",
        hidden: false,
      },
    ]);
  };

  const updateTestCase = (idx, field, value) => {
    const updated = [...testCases];
    updated[idx][field] = value;
    setTestCases(updated);
  };

  const removeTestCase = (idx) => {
    setTestCases(testCases.filter((_, i) => i !== idx));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const payload = {
        ...formData,
        problem_type: problemType,
        test_cases: testCases,
      };
      await createAssignment(payload);
      alert("Assignment created successfully!");
      navigate("/admin");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create assignment");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Sidebar />
      <Navbar />
      <div className="dashboard-container">
        <h2>Create New Assignment</h2>
        {error && <p style={{ color: "red" }}>{error}</p>}

        <form onSubmit={handleSubmit} style={{ maxWidth: "800px" }}>
          {/* Problem Type */}
          <div style={{ marginBottom: "15px" }}>
            <label>Problem Type</label>
            <select
              value={problemType}
              onChange={(e) => setProblemType(e.target.value)}
              style={{ width: "100%", padding: "8px", marginTop: "5px" }}
            >
              <option value="coding">Coding Problem</option>
              <option value="sql">SQL Problem</option>
            </select>
          </div>

          <div style={{ marginBottom: "15px" }}>
            <label>Title</label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
              style={{ width: "100%", padding: "8px", marginTop: "5px" }}
            />
          </div>

          <div style={{ marginBottom: "15px" }}>
            <label>Description</label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              rows="4"
              style={{ width: "100%", padding: "8px", marginTop: "5px" }}
            />
          </div>

          <div style={{ marginBottom: "15px" }}>
            <label>Domain</label>
            <select
              name="domain"
              value={formData.domain}
              onChange={handleChange}
              style={{ width: "100%", padding: "8px", marginTop: "5px" }}
            >
              <option value="fullstack">FullStack</option>
              <option value="data">Data</option>
              <option value="aiml">AI/ML</option>
            </select>
          </div>

          <div style={{ marginBottom: "15px" }}>
            <label>Difficulty</label>
            <select
              name="difficulty"
              value={formData.difficulty}
              onChange={handleChange}
              style={{ width: "100%", padding: "8px", marginTop: "5px" }}
            >
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>

          {problemType === "coding" && (
            <>
              <div style={{ marginBottom: "15px" }}>
                <label>Test Input</label>
                <textarea
                  name="test_input"
                  value={formData.test_input}
                  onChange={handleChange}
                  rows="3"
                  style={{ width: "100%", padding: "8px", marginTop: "5px" }}
                />
              </div>

              <div style={{ marginBottom: "15px" }}>
                <label>Expected Output</label>
                <textarea
                  name="expected_output"
                  value={formData.expected_output}
                  onChange={handleChange}
                  rows="3"
                  style={{ width: "100%", padding: "8px", marginTop: "5px" }}
                />
              </div>
            </>
          )}

          {problemType === "sql" && (
            <>
              <div style={{ marginBottom: "15px" }}>
                <label>SQL Schema (CREATE TABLE + INSERT)</label>
                <textarea
                  name="sql_schema"
                  value={formData.sql_schema}
                  onChange={handleChange}
                  placeholder="CREATE TABLE users (id INT, name VARCHAR(100)); INSERT INTO users VALUES (1, 'John');"
                  rows="5"
                  required
                  style={{ width: "100%", padding: "8px", marginTop: "5px", fontFamily: "monospace" }}
                />
              </div>

              <div style={{ marginBottom: "15px" }}>
                <label>Expected SQL Query (for reference)</label>
                <textarea
                  name="sql_query"
                  value={formData.sql_query}
                  onChange={handleChange}
                  placeholder="SELECT * FROM users WHERE id = 1;"
                  rows="3"
                  style={{ width: "100%", padding: "8px", marginTop: "5px", fontFamily: "monospace" }}
                />
              </div>

              <div style={{ marginBottom: "20px", padding: "10px", backgroundColor: "#f0f0f0", borderRadius: "5px" }}>
                <h4>Test Cases</h4>
                {testCases.map((tc, idx) => (
                  <div key={idx} style={{ marginBottom: "15px", padding: "10px", border: "1px solid #ccc", borderRadius: "5px" }}>
                    <h5>Test Case {idx + 1}</h5>
                    <textarea
                      placeholder="SELECT query..."
                      value={tc.sql_query}
                      onChange={(e) => updateTestCase(idx, "sql_query", e.target.value)}
                      rows="2"
                      style={{ width: "100%", padding: "8px", marginBottom: "8px", fontFamily: "monospace" }}
                    />
                    <textarea
                      placeholder='Expected result (JSON): [{"id": 1, "name": "John"}]'
                      value={tc.expected_result}
                      onChange={(e) => updateTestCase(idx, "expected_result", e.target.value)}
                      rows="2"
                      style={{ width: "100%", padding: "8px", marginBottom: "8px", fontFamily: "monospace" }}
                    />
                    <label>
                      <input
                        type="checkbox"
                        checked={tc.hidden}
                        onChange={(e) => updateTestCase(idx, "hidden", e.target.checked)}
                      />
                      Hidden test case
                    </label>
                    <button
                      type="button"
                      onClick={() => removeTestCase(idx)}
                      style={{
                        marginLeft: "10px",
                        padding: "5px 10px",
                        backgroundColor: "#dc3545",
                        color: "white",
                        border: "none",
                        borderRadius: "3px",
                        cursor: "pointer",
                      }}
                    >
                      Remove
                    </button>
                  </div>
                ))}
                <button
                  type="button"
                  onClick={addTestCase}
                  style={{
                    padding: "8px 16px",
                    backgroundColor: "#007bff",
                    color: "white",
                    border: "none",
                    borderRadius: "5px",
                    cursor: "pointer",
                  }}
                >
                  + Add Test Case
                </button>
              </div>
            </>
          )}

          <button
            type="submit"
            disabled={loading}
            style={{
              padding: "10px 20px",
              backgroundColor: "#28a745",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: loading ? "not-allowed" : "pointer",
              fontSize: "16px",
            }}
          >
            {loading ? "Creating..." : "Create Assignment"}
          </button>
        </form>
      </div>
    </>
  );
}
