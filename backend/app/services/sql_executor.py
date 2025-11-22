import sqlite3
import json
from typing import Dict, List, Tuple, Any

class SQLExecutor:
    """Execute SQL queries safely in an isolated SQLite database"""
    
    def __init__(self):
        # Use in-memory database for each execution
        self.conn = None
    
    def setup_schema(self, schema_sql: str) -> Tuple[bool, str]:
        """
        Setup the database schema.
        Args:
            schema_sql: SQL commands to create tables and initial data
        Returns:
            (success, message)
        """
        try:
            self.conn = sqlite3.connect(":memory:")
            self.conn.row_factory = sqlite3.Row
            cursor = self.conn.cursor()
            
            # Execute schema setup
            cursor.executescript(schema_sql)
            self.conn.commit()
            
            return True, "Schema setup successful"
        except Exception as e:
            return False, f"Schema setup failed: {str(e)}"
    
    def execute_query(self, query: str) -> Tuple[bool, Any]:
        """
        Execute a SQL query and return results.
        Args:
            query: SQL query to execute
        Returns:
            (success, result_or_error)
        """
        if not self.conn:
            return False, "Database not initialized"
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            
            # Fetch results
            if query.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall()
                results = [dict(row) for row in rows]
                return True, results
            else:
                # For INSERT/UPDATE/DELETE, return affected rows count
                self.conn.commit()
                return True, {"affected_rows": cursor.rowcount}
        except Exception as e:
            return False, f"Query execution failed: {str(e)}"
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
    
    def compare_results(self, actual: Any, expected_json: str) -> Tuple[bool, str]:
        """
        Compare actual results with expected results.
        Args:
            actual: Query result (list of dicts)
            expected_json: Expected result as JSON string
        Returns:
            (match, message)
        """
        try:
            expected = json.loads(expected_json)
            
            # Convert dicts to comparable format
            actual_data = json.loads(json.dumps(actual, default=str))
            
            if actual_data == expected:
                return True, "Results match!"
            else:
                return False, f"Results don't match.\nExpected: {json.dumps(expected, indent=2)}\nActual: {json.dumps(actual_data, indent=2)}"
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON in expected result: {str(e)}"
        except Exception as e:
            return False, f"Comparison failed: {str(e)}"


def execute_sql_problem(schema_sql: str, user_query: str, test_cases: List[Dict]) -> Dict:
    """
    Execute a SQL problem and return test results.
    
    Args:
        schema_sql: SQL schema setup
        user_query: User's submitted SQL query (THIS QUERY IS TESTED)
        test_cases: List of test cases with expected results (what user_query SHOULD produce)
    
    Returns:
        {
            'success': bool,
            'total_tests': int,
            'passed_tests': int,
            'results': [
                {
                    'test_id': int,
                    'passed': bool,
                    'message': str,
                    'expected_result': any
                }
            ],
            'user_query': str,
            'user_query_error': str or None  # If user query syntax is wrong
        }
    """
    executor = SQLExecutor()
    
    # Setup schema
    schema_ok, schema_msg = executor.setup_schema(schema_sql)
    if not schema_ok:
        executor.close()
        return {
            'success': False,
            'total_tests': len(test_cases),
            'passed_tests': 0,
            'results': [],
            'user_query': user_query,
            'user_query_error': schema_msg
        }
    
    # Execute user's query
    user_query_error = None
    user_result = None
    success_exec, user_result = executor.execute_query(user_query)
    
    if not success_exec:
        user_query_error = user_result
        executor.close()
        return {
            'success': False,
            'total_tests': len(test_cases),
            'passed_tests': 0,
            'results': [],
            'user_query': user_query,
            'user_query_error': user_query_error
        }
    
    # Compare user's result against each test case
    results = []
    passed_count = 0
    
    for idx, test_case in enumerate(test_cases):
        expected_result_json = test_case.get('expected_result')
        
        if not expected_result_json:
            results.append({
                'test_id': idx + 1,
                'passed': False,
                'message': 'Invalid test case configuration'
            })
            continue
        
        # Compare user's result with this test case
        match, msg = executor.compare_results(user_result, expected_result_json)
        
        results.append({
            'test_id': idx + 1,
            'passed': match,
            'message': msg,
            'actual_result': user_result,
            'expected_result': json.loads(expected_result_json)
        })
        
        if match:
            passed_count += 1
    
    executor.close()
    
    return {
        'success': passed_count == len(test_cases),
        'total_tests': len(test_cases),
        'passed_tests': passed_count,
        'results': results,
        'user_query': user_query,
        'user_query_error': user_query_error
    }
