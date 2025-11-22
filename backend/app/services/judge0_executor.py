"""
Judge0 API executor for Python code execution
Uses Judge0 online code execution service
"""
import requests
import json
import time
import base64
from typing import Dict, Any, List
from dotenv import load_dotenv
import os

load_dotenv()

# Judge0 API configuration
JUDGE0_API_URL = "https://judge0-ce.p.rapidapi.com"
JUDGE0_API_KEY = os.getenv("JUDGE0_API_KEY", "cec1a92bf7msh6d43f6fb94cd469p1ea054jsn8aefd4dc6066")
JUDGE0_HOST = "judge0-ce.p.rapidapi.com"

# Language IDs in Judge0
LANGUAGE_IDS = {
    "python": 71,  # Python 3
    "javascript": 63,  # Node.js
}

class Judge0Executor:
    """Execute code using Judge0 API"""

    @staticmethod
    def execute_code(language: str, code: str, stdin: str = "", timeout: int = 30) -> Dict[str, Any]:
        """
        Execute code using Judge0 API

        Args:
            language: 'python' or 'javascript'
            code: Source code to execute
            stdin: Input to pass to the program
            timeout: Execution timeout in seconds

        Returns:
            {
                'success': bool,
                'output': str,
                'error': str or None,
                'execution_time': float
            }
        """
        try:
            language_id = LANGUAGE_IDS.get(language.lower())
            if not language_id:
                return {
                    'success': False,
                    'output': '',
                    'error': f"Unsupported language: {language}",
                    'execution_time': 0
                }

            # Submit code for execution
            submit_url = f"{JUDGE0_API_URL}/submissions"
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": JUDGE0_API_KEY,
                "X-RapidAPI-Host": JUDGE0_HOST
            }

            payload = {
                "language_id": language_id,
                "source_code": code,
                "stdin": stdin,
                "expected_output": None,
                "cpu_time_limit": min(timeout, 20),  # Max 20 seconds for CPU time
                "cpu_extra_time": 2,
                "wall_time_limit": min(timeout + 5, 30),  # Max 30 seconds for wall time
                "memory_limit": 128000,  # 128MB
                "stack_limit": 64000,    # 64MB
                "max_file_size": 1024     # 1KB
            }

            # Submit the code
            response = requests.post(submit_url, json=payload, headers=headers, timeout=10)
            if response.status_code != 201:
                return {
                    'success': False,
                    'output': '',
                    'error': f"Judge0 API error: {response.status_code} - {response.text}",
                    'execution_time': 0
                }

            token = response.json().get('token')
            if not token:
                return {
                    'success': False,
                    'output': '',
                    'error': "No token received from Judge0",
                    'execution_time': 0
                }

            # Poll for results
            result_url = f"{JUDGE0_API_URL}/submissions/{token}?base64_encoded=true&fields=*"
            max_attempts = 30  # Maximum polling attempts
            attempt = 0

            while attempt < max_attempts:
                time.sleep(1)  # Wait 1 second between polls

                result_response = requests.get(result_url, headers={
                    "X-RapidAPI-Key": JUDGE0_API_KEY,
                    "X-RapidAPI-Host": JUDGE0_HOST
                }, timeout=10)

                if result_response.status_code != 200:
                    return {
                        'success': False,
                        'output': '',
                        'error': f"Failed to get result: {result_response.status_code}",
                        'execution_time': 0
                    }

                result = result_response.json()
                status_id = result.get('status', {}).get('id')

                # Status codes: 1=pending, 2=processing, 3=accepted, 4=wrong answer, 5=time limit, 6=compilation error, etc.
                if status_id == 3:  # Accepted
                    stdout = result.get('stdout', '')
                    if stdout:
                        stdout = base64.b64decode(stdout).decode('utf-8').strip()
                    return {
                        'success': True,
                        'output': stdout,
                        'error': None,
                        'execution_time': result.get('time', 0)
                    }
                elif status_id in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:  # Various error states
                    stderr = result.get('stderr', '')
                    compile_output = result.get('compile_output', '')
                    stdout = result.get('stdout', '')

                    if stderr:
                        stderr = base64.b64decode(stderr).decode('utf-8')
                    if compile_output:
                        compile_output = base64.b64decode(compile_output).decode('utf-8')
                    if stdout:
                        stdout = base64.b64decode(stdout).decode('utf-8').strip()

                    error_msg = stderr or compile_output or result.get('status', {}).get('description', 'Unknown error')
                    return {
                        'success': False,
                        'output': stdout,
                        'error': error_msg,
                        'execution_time': result.get('time', 0)
                    }
                elif status_id in [1, 2]:  # Still processing
                    attempt += 1
                    continue
                else:
                    return {
                        'success': False,
                        'output': '',
                        'error': f"Unknown status: {status_id}",
                        'execution_time': 0
                    }

            # Timeout
            return {
                'success': False,
                'output': '',
                'error': f"Execution timeout after {max_attempts} attempts",
                'execution_time': timeout
            }

        except requests.Timeout:
            return {
                'success': False,
                'output': '',
                'error': f"API timeout (>{timeout}s)",
                'execution_time': timeout
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': f"Execution error: {str(e)}",
                'execution_time': 0
            }

    @staticmethod
    def execute_coding_problem(language: str, user_code: str, test_cases: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Execute a coding problem and validate against test cases using Judge0

        Args:
            language: 'python' or 'javascript'
            user_code: User's submitted code
            test_cases: List of test cases with 'input' and 'expected_output'

        Returns:
            {
                'success': bool,
                'total_tests': int,
                'passed_tests': int,
                'results': [
                    {
                        'test_id': int,
                        'input': str,
                        'expected_output': str,
                        'actual_output': str,
                        'passed': bool,
                        'error': str or None
                    }
                ],
                'code_error': str or None
            }
        """
        results = []
        passed_count = 0
        code_error = None

        for idx, test_case in enumerate(test_cases):
            test_input = test_case.get('input', '')
            expected_output = test_case.get('expected_output', '').strip()

            # Execute code with test input using Judge0
            exec_result = Judge0Executor.execute_code(
                language=language,
                code=user_code,
                stdin=test_input,
                timeout=30
            )

            if not exec_result['success'] and exec_result['error']:
                # Code has syntax/runtime error
                if idx == 0:  # Only set error once
                    code_error = exec_result['error']
                results.append({
                    'test_id': idx + 1,
                    'input': test_input,
                    'expected_output': expected_output,
                    'actual_output': '',
                    'passed': False,
                    'error': exec_result['error']
                })
            else:
                # Compare output
                actual_output = exec_result['output'].strip()
                passed = actual_output == expected_output

                results.append({
                    'test_id': idx + 1,
                    'input': test_input,
                    'expected_output': expected_output,
                    'actual_output': actual_output,
                    'passed': passed,
                    'error': None
                })

                if passed:
                    passed_count += 1

        return {
            'success': passed_count == len(test_cases),
            'total_tests': len(test_cases),
            'passed_tests': passed_count,
            'results': results,
            'code_error': code_error
        }
