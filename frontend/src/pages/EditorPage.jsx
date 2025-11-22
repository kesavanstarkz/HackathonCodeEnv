import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import Editor from "@monaco-editor/react";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import SQLEditor from "../components/SQLEditor";
import { getAssignments } from "../api/assignments";
import "../styles/editor.css";

export default function EditorPage() {
  const { id } = useParams();
  const [assignment, setAssignment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchAssignment = async () => {
      try {
        // Fetch single assignment by id
        const response = await fetch(`http://127.0.0.1:8000/assignments/${id}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        if (!response.ok) throw new Error("Failed to load assignment");
        const data = await response.json();
        setAssignment(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAssignment();
  }, [id]);

  if (loading) return <div className="editor-container"><p>Loading...</p></div>;
  if (error) return <div className="editor-container"><p style={{ color: "red" }}>{error}</p></div>;
  if (!assignment) return <div className="editor-container"><p>Assignment not found</p></div>;

  return (
    <>
      <Sidebar />
      <Navbar />

      <div className="editor-container">
        {assignment.problem_type === "sql" ? (
          <SQLEditor assignment={assignment} />
        ) : (
          <CodingEditor assignment={assignment} />
        )}
      </div>
    </>
  );
}

function CodingEditor({ assignment }) {
  const getInitialCode = (language) => {
    if (language === 'javascript') {
      return `// Write your solution for: ${assignment.title}\n\n// Read input from stdin\nconst fs = require('fs');\nconst input = fs.readFileSync(0, 'utf-8').trim();\n\n// Your code here\n\nconsole.log('Hello, World!');`;
    } else {
      return `# Write your solution for: ${assignment.title}\n\n# Read input from stdin\nimport sys\ninput_data = sys.stdin.read().strip()\n\n# Your code here\n\nprint("Hello, World!")`;
    }
  };

  const [code, setCode] = useState(getInitialCode(assignment.language));
  const [testResults, setTestResults] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  function handleCodeChange(value) {
    setCode(value);
  }

  async function runCode() {
    setSubmitting(true);
    setTestResults(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/assignments/submit-code", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          assignment_id: assignment.id,
          code: code,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to submit code");
      }

      const results = await response.json();
      setTestResults(results);
    } catch (error) {
      alert("Error submitting code: " + error.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="assignment-section">
      <h2 className="editor-title">{assignment.title}</h2>
      <p className="assignment-description">{assignment.description}</p>

      {/* Show test cases if available */}
      {assignment.test_cases && assignment.test_cases.length > 0 && (
        <div className="test-cases-container">
          <h4>Test Cases:</h4>
          {assignment.test_cases.filter(tc => !tc.hidden).map((tc, index) => (
            <div key={index} className="test-case">
              <strong>Test Case {index + 1}:</strong>
              <div><strong>Input:</strong> <code>{tc.input || "None"}</code></div>
              <div><strong>Expected Output:</strong> <code>{tc.expected_output}</code></div>
            </div>
          ))}
          {assignment.test_cases.some(tc => tc.hidden) && (
            <p><em>Note: Some test cases are hidden and will be tested when you submit.</em></p>
          )}
        </div>
      )}

      <div className="editor-box">
        <Editor
          height="100%"
          width="100%"
          defaultLanguage={assignment.language || "python"}
          theme="vs-dark"
          value={code}
          onChange={handleCodeChange}
        />
      </div>

      <button className="run-btn" onClick={runCode} disabled={submitting}>
        {submitting ? "Submitting..." : "Submit Code"}
      </button>

      {/* Display test results */}
      {testResults && (
        <div className="results-section">
          <h4>Test Results:</h4>
          <p><strong>Overall:</strong> {testResults.success ? "PASSED" : "FAILED"} ({testResults.passed_tests}/{testResults.total_tests} tests passed)</p>

          {testResults.code_error && (
            <div className="code-error">
              <strong>Code Error:</strong> {testResults.code_error}
            </div>
          )}

          <div className="detailed-results">
            <strong>Detailed Results:</strong>
            {testResults.results.map((result, index) => (
              <div key={index} className={`result-item ${result.passed ? 'pass' : 'fail'}`}>
                Test {result.test_id}: {result.passed ? "PASS" : "FAIL"}
                {result.error && ` - Error: ${result.error}`}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
