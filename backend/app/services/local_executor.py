"""
Local code executor for development (without Azure Functions)
Can be used with AZURE_FUNCTION_URL=local environment variable
"""

import subprocess
import tempfile
import os
import time
from typing import Dict, Any


class LocalCodeExecutor:
    """Execute Python and JavaScript code locally for testing"""
    
    @staticmethod
    def execute_python(code: str, user_input: str = "", timeout: int = 30) -> Dict[str, Any]:
        """Execute Python code locally"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                start_time = time.time()
                result = subprocess.run(
                    ['python', temp_file],
                    input=user_input if user_input else None,
                    capture_output=True,
                    timeout=timeout,
                    text=True
                )
                execution_time = time.time() - start_time
                
                output = result.stdout
                error = result.stderr if result.returncode != 0 else None
                
                return {
                    "success": result.returncode == 0,
                    "output": output,
                    "error": error,
                    "execution_time": execution_time
                }
            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "error": f"Execution timeout (>{timeout}s)",
                "execution_time": timeout
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "execution_time": 0
            }
    
    @staticmethod
    def execute_javascript(code: str, user_input: str = "", timeout: int = 30) -> Dict[str, Any]:
        """Execute JavaScript code locally with Node.js"""
        try:
            # Wrap code to handle stdin
            wrapped_code = f"""
let output = '';
const originalLog = console.log;
console.log = function(...args) {{
    output += args.join(' ') + '\\n';
}};

const originalError = console.error;
console.error = function(...args) {{
    output += args.join(' ') + '\\n';
}};

try {{
    {code}
    process.stdout.write(output);
}} catch(error) {{
    process.stderr.write(error.message + '\\n');
    process.exit(1);
}}
"""
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(wrapped_code)
                temp_file = f.name
            
            try:
                start_time = time.time()
                result = subprocess.run(
                    ['node', temp_file],
                    input=user_input if user_input else None,
                    capture_output=True,
                    timeout=timeout,
                    text=True
                )
                execution_time = time.time() - start_time
                
                output = result.stdout
                error = result.stderr if result.returncode != 0 else None
                
                return {
                    "success": result.returncode == 0,
                    "output": output,
                    "error": error,
                    "execution_time": execution_time
                }
            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "error": f"Execution timeout (>{timeout}s)",
                "execution_time": timeout
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "execution_time": 0
            }
