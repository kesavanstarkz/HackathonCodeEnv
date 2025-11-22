import { useState } from "react";
import Editor from "@monaco-editor/react";
import api from "../api/auth";

export default function SQLEditor({ assignment }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    setLoading(true);
    setError("");
    setResults(null);

    try {
      const response = await api.post("/assignments/submit-sql", {
        assignment_id: assignment.id,
        sql_query: query,
      });
      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Error submitting query");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h3>SQL Problem: {assignment.title}</h3>
      <p>{assignment.description}</p>

      {assignment.sql_schema && (
        <div style={{ marginBottom: "15px", padding: "10px", backgroundColor: "#f9f9f9", borderRadius: "5px" }}>
          <h4>Schema (Pre-loaded):</h4>
          <pre style={{ fontSize: "12px", overflow: "auto", maxHeight: "150px" }}>
            {assignment.sql_schema}
          </pre>
        </div>
      )}

      <div style={{ marginBottom: "15px" }}>
        <h4>Write your SQL query:</h4>
        <Editor
          height="300px"
          defaultLanguage="sql"
          value={query}
          onChange={(value) => setQuery(value || "")}
          theme="vs-light"
          options={{ minimap: { enabled: false }, fontSize: 14 }}
        />
      </div>

      <button
        onClick={handleSubmit}
        disabled={loading}
        style={{
          padding: "10px 20px",
          backgroundColor: loading ? "#ccc" : "#28a745",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: loading ? "not-allowed" : "pointer",
          fontSize: "16px",
          marginBottom: "20px",
        }}
      >
        {loading ? "Running Tests..." : "Run Tests"}
      </button>

      {error && (
        <div style={{ color: "red", marginBottom: "15px", padding: "10px", backgroundColor: "#ffe6e6", borderRadius: "5px" }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {results && (
        <div style={{ marginTop: "20px" }}>
          <div style={{
            padding: "15px",
            backgroundColor: results.success ? "#d4edda" : "#f8d7da",
            color: results.success ? "#155724" : "#721c24",
            borderRadius: "5px",
            marginBottom: "15px",
          }}>
            <h4>{results.success ? "✅ All Tests Passed!" : "❌ Some Tests Failed"}</h4>
            <p>
              Passed: {results.passed_tests} / {results.total_tests}
            </p>
          </div>

          {results.user_query_error && (
            <div style={{ color: "red", marginBottom: "15px", padding: "10px", backgroundColor: "#ffe6e6", borderRadius: "5px" }}>
              <strong>Query Syntax Error:</strong> {results.user_query_error}
            </div>
          )}

          <div>
            <h5>Test Results:</h5>
            {results.results.map((result, idx) => (
              <div
                key={idx}
                style={{
                  marginBottom: "10px",
                  padding: "10px",
                  backgroundColor: result.passed ? "#e8f5e9" : "#ffebee",
                  border: `2px solid ${result.passed ? "#4caf50" : "#f44336"}`,
                  borderRadius: "5px",
                }}
              >
                <h6>{result.passed ? "✅" : "❌"} Test {result.test_id}</h6>
                <p><strong>Query:</strong> <code>{result.query}</code></p>
                <p><strong>Message:</strong> {result.message}</p>
                {result.actual_result && (
                  <div>
                    <strong>Actual Result:</strong>
                    <pre style={{ fontSize: "12px", backgroundColor: "#f5f5f5", padding: "5px", borderRadius: "3px", overflow: "auto" }}>
                      {JSON.stringify(result.actual_result, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
