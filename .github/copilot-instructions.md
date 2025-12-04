# AI Math Tutor - Development Guide

## Architecture Overview

This is a **single-file full-stack application** for CSCI 250 coursework:
- `server.py`: Flask backend serving both API endpoints and static frontend
- `index.html`: Self-contained React 18 app (CDN-loaded, no build step)
- Gemini AI integration (FREE tier, 60 requests/minute)

The backend serves the frontend from root (`/`) and API from `/api/*`.

## Core Technologies

### Backend (server.py)
- **Flask**: Web framework with static file serving (`static_folder='.'`)
- **Flask-CORS**: Enables cross-origin requests
- **google-generativeai**: Official Gemini Python SDK
- **Model**: `gemini-2.0-flash` (fast, free, educational-focused)

### Frontend (index.html)
- **React 18**: CDN-loaded (`react.production.min.js`, `react-dom.production.min.js`)
- **Babel Standalone**: In-browser JSX transformation (development convenience)
- **Tailwind CSS**: CDN-loaded with custom config inline
- **Lucide Icons**: SVG icons via CDN
- **KaTeX**: LaTeX math rendering

## Key Patterns

### 1. System Prompts (server.py lines 71-159)
Three specialized prompts guide Gemini's responses:
- `SOLVER_SYSTEM_PROMPT`: Generates step-by-step solutions with JSON structure
- `QUIZ_SYSTEM_PROMPT`: Creates practice questions with hints/answers
- `EVALUATOR_SYSTEM_PROMPT`: Evaluates student answers with feedback

**Critical**: All prompts enforce JSON-only responses (no markdown wrappers) - see `clean_json_response()` helper.

### 2. API Response Format
Gemini responses follow strict JSON schemas:
```python
# Solver response
{
    "problem_type": str,
    "concepts": [str],
    "steps": [{"step_number": int, "action": str, "explanation": str, "result": str}],
    "final_answer": str,
    "verification": str
}
```

**Error handling**: Always catch `json.JSONDecodeError` and provide user-friendly messages.

### 3. React State Management (index.html)
- **ProblemSolver**: Uses `useState` for `problem`, `solution`, `loading`, `error`
- **QuizMode**: Tracks `quiz`, `currentQuestion`, `userAnswers`, `results`, `quizComplete`
- No global state - each component is self-contained

### 4. Custom Styling System
- Tailwind config extended inline (lines 74-138) with custom colors:
  - `tutor-*`: Primary teal brand colors (50-900)
  - `accent-*`: Warm amber for highlights
  - `cream/chalk`: Background and contrast colors
- Custom animations: `fade-in`, `slide-up`, `pulse-soft`

## Development Workflows

### Running Locally
```bash
pip install -r requirements.txt
python server.py  # Runs on http://localhost:5000
```
**No separate frontend server needed** - Flask serves everything.

### API Key Setup
Set the environment variable before running:
```bash
# Windows PowerShell
$env:GEMINI_API_KEY='your-key-here'

# Mac/Linux
export GEMINI_API_KEY='your-key-here'
```
Get free keys at: https://aistudio.google.com/apikey

### Testing Endpoints
Use example problems from `index.html` lines 1276-1283 or curl:
```bash
curl -X POST http://localhost:5000/api/solve \
  -H "Content-Type: application/json" \
  -d '{"problem": "Solve for x: 2x + 5 = 13"}'
```

### Debugging Gemini Responses
Check `clean_json_response()` (lines 164-184) if JSON parsing fails - it strips markdown code blocks.

## Project Conventions

1. **Extensive Comments**: Every section heavily documented (educational context)
2. **No Build Process**: Entire frontend runs via CDN + Babel (intentional simplicity)
3. **Single-Port Deployment**: Flask serves both API and frontend on port 5000
4. **Educational Focus**: Prompts emphasize step-by-step learning, not just answers
5. **Rate Limiting**: Free tier = 60 req/min; handle 429 errors gracefully

## Common Tasks

### Adding New API Endpoint
Follow pattern in `server.py`:
```python
@app.route('/api/new-endpoint', methods=['POST'])
def new_endpoint():
    try:
        data = request.get_json()
        # Validate input
        result = call_gemini(prompt, SYSTEM_PROMPT)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

### Adding React Component
In `index.html` after line 1133:
```jsx
const NewComponent = () => {
    const [state, setState] = useState(null);
    return <div>...</div>;
};
```

### Modifying Gemini Behavior
Edit system prompts (lines 71-159) - they control response structure and tone.

## File References

- **API endpoints**: `server.py` lines 252-458
- **React components**: `index.html` lines 1133-1859
- **Tailwind config**: `index.html` lines 74-138
- **System prompts**: `server.py` lines 71-159
- **Dependencies**: `requirements.txt` (Flask 3.0+, google-generativeai 0.3+)

## Production Considerations

Current setup uses `debug=True` - for production:
1. **API key**: Already uses environment variables (`GEMINI_API_KEY`)
2. Switch to production WSGI server: `gunicorn -w 4 server:app`
3. Disable debug mode: Set `app.run(debug=False)`
4. Add rate limiting middleware
5. Use HTTPS and proper authentication
