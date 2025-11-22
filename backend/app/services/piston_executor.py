"""
Piston API executor for JavaScript code execution
Uses Piston online code execution service
"""
import requests
import json
import time
from typing import Dict, Any, List

class PistonExecutor:
    """Execute JavaScript code using Piston API"""

    PISTON_API_URL = "https://emkc.org/api/v2/piston/execute"


    @staticmethod
    def execute_code(code: str, stdin: str = "", timeout: int = 30) -> Dict[str, Any]:
        """
        Execute JavaScript code using Piston API

        Args:
            code: JavaScript source code to execute
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
            payload = {
                "language": "javascript",
                "version": "18.15.0",
                "files": [
                    {
                        "name": "main.js",
                        "content": code
                    }
                ],
                "stdin": stdin
            }

            start_time = time.time()
            response = requests.post(PistonExecutor.PISTON_API_URL, json=payload, timeout=timeout + 10, verify=False)
            execution_time = time.time() - start_time

            if response.status_code != 200:
                return {
                    'success': False,
                    'output': '',
                    'error': f"Piston API error: {response.status_code} - {response.text}",
                    'execution_time': execution_time
                }

            result = response.json()

            # Check for compilation errors
            if 'compile' in result and result['compile']['code'] != 0:
                return {
                    'success': False,
                    'output': '',
                    'error': result['compile']['stderr'] or result['compile']['stdout'],
                    'execution_time': execution_time
                }

            # Check for runtime errors
            if 'run' in result and result['run']['code'] != 0:
                return {
                    'success': False,
                    'output': result['run']['stdout'],
                    'error': result['run']['stderr'] or f"Exit code: {result['run']['code']}",
                    'execution_time': execution_time
                }

            # Success
            output = result.get('run', {}).get('stdout', '')
            return {
                'success': True,
                'output': output,
                'error': None,
                'execution_time': execution_time
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
    def execute_coding_problem(user_code: str, test_cases: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Execute a JavaScript coding problem and validate against test cases using Piston

        Args:
            user_code: User's submitted JavaScript code
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

            # Execute code with test input using Piston
            exec_result = PistonExecutor.execute_code(
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
                    'actual_output': exec_result['output'],
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
