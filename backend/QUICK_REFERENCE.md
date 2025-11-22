# Code Execution Setup - Quick Reference

## Code Execution

The application uses Judge0 API for Python execution and local execution for JavaScript.

### Supported Languages
- Python (via Judge0 API - requires JUDGE0_API_KEY)
- JavaScript (via Piston API - no API key required)

### Environment Setup

Add to `backend/.env`:
```env
JUDGE0_API_KEY=your_rapidapi_key_here
```

Get your API key from: https://rapidapi.com/judge0-official/api/judge0-ce

### Testing Code Execution

```bash
cd backend
python create_sample_python_assignment.py
```

Expected output:
```
All tests passed: True
Passed: 4/4
```

## File Locations

- Judge0 executor: `backend/app/services/judge0_executor.py`
- Local executor: `backend/app/services/local_executor.py`
- Assignment router: `backend/app/routers/assignments.py`

## Next Steps

JavaScript support has been implemented:
- ✅ CodingEditor.jsx supports JavaScript with appropriate syntax highlighting and initial code templates
- ✅ JavaScript assignment example created (create_sample_javascript_assignment.py)
- ✅ Tested both Python and JavaScript assignments - all working!

Ready to test the full application or add more features.
