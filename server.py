"""
AI Math Tutor - Backend Server
==============================
Student: Aric Hurkman
Course: CSCI 250
Final Project: AI Math Tutor
Professor: Gheni Abla

This Flask server provides the backend API for the AI Math Tutor application.
It handles requests to solve math problems and generate quiz questions using
the Google Gemini API with user-provided API keys.

Features:
- Google OAuth integration for user authentication
- User-provided Gemini API keys (each user uses their own key)
- Problem solving with step-by-step explanations
- Quiz generation and answer evaluation

Requirements:
- Flask: Web framework for Python
- Flask-CORS: Cross-Origin Resource Sharing support
- google-generativeai: Google's Python SDK for Gemini API

Usage:
    python server.py
    
The server will start on http://localhost:5000
"""

# =============================================================================
# IMPORTS
# =============================================================================

# Flask framework for creating the web server
from flask import Flask, request, jsonify, send_from_directory

# CORS (Cross-Origin Resource Sharing) to allow frontend to communicate with backend
from flask_cors import CORS

# Google Generative AI SDK for Gemini API integration
import google.generativeai as genai

# OS module for environment variable access
import os

# JSON module for parsing responses
import json

# Regular expressions for cleaning JSON responses
import re

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# =============================================================================
# APPLICATION CONFIGURATION
# =============================================================================

# Initialize Flask application with static file serving
# static_folder='.' means serve static files from the current directory
# static_url_path='' means serve them from the root URL
app = Flask(__name__, static_folder='.', static_url_path='')

# Enable CORS for all routes
# This allows the frontend (running on a different port) to make requests to this server
CORS(app)

# =============================================================================
# SYSTEM PROMPTS
# =============================================================================

# System prompt for solving math problems
# This instructs Gemini on how to format step-by-step solutions
SOLVER_SYSTEM_PROMPT = """You are an expert math tutor helping students understand mathematical concepts. 
Your role is to solve math problems step-by-step with clear, educational explanations.

When solving problems:
1. First, identify what type of problem it is (algebra, calculus, geometry, trigonometry, etc.)
2. List any relevant formulas or theorems that will be used
3. Show each step clearly with explanations of WHY each step is taken
4. Use proper mathematical notation
5. Provide the final answer clearly marked
6. If applicable, verify the answer or explain how to check it

You MUST respond with ONLY valid JSON (no markdown, no code blocks) in this exact format:
{
    "problem_type": "The category of math problem",
    "concepts": ["List of mathematical concepts used"],
    "steps": [
        {
            "step_number": 1,
            "action": "What is being done in this step",
            "explanation": "Why this step is necessary",
            "result": "The mathematical result of this step"
        }
    ],
    "final_answer": "The final answer to the problem",
    "verification": "How to verify the answer (if applicable)"
}

Always be encouraging and educational. Remember, the goal is to help students LEARN, not just get answers."""

# System prompt for generating quiz questions
# This instructs Gemini on how to create practice problems
QUIZ_SYSTEM_PROMPT = """You are an expert math tutor creating practice problems for students.
Generate quiz questions that test understanding of mathematical concepts.

When creating quiz questions:
1. Create problems that are educational and appropriately challenging
2. Include a mix of difficulty levels when multiple questions are requested
3. Ensure problems are solvable and have clear, unique answers
4. Cover the requested topic area thoroughly

You MUST respond with ONLY valid JSON (no markdown, no code blocks) in this exact format:
{
    "quiz_topic": "The mathematical topic being tested",
    "questions": [
        {
            "question_number": 1,
            "question": "The math problem to solve",
            "difficulty": "easy/medium/hard",
            "hint": "A helpful hint without giving away the answer",
            "correct_answer": "The correct answer",
            "solution_steps": ["Brief steps to solve"]
        }
    ]
}

Create engaging problems that help students build confidence and understanding."""

# System prompt for evaluating quiz answers
EVALUATOR_SYSTEM_PROMPT = """You are an expert math tutor evaluating a student's answer to a math problem.

Compare the student's answer to the correct answer and provide feedback.

You MUST respond with ONLY valid JSON (no markdown, no code blocks) in this exact format:
{
    "is_correct": true or false,
    "feedback": "Encouraging feedback explaining if correct or what went wrong",
    "explanation": "Brief explanation of the correct approach if the answer was wrong"
}

Always be encouraging and constructive, even when the answer is incorrect.
Consider equivalent forms of answers (e.g., 0.5 = 1/2 = 50%)."""


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_api_key_from_request():
    """
    Extract the Gemini API key from the request headers.
    
    The frontend sends the API key in the 'X-API-Key' header.
    This allows each user to use their own API key.
    
    Returns:
        str: The API key from the request header, or None if not provided
    """
    return request.headers.get('X-API-Key')


def clean_json_response(text):
    """
    Clean the response text to extract valid JSON.
    
    Gemini sometimes wraps JSON in markdown code blocks or adds extra text.
    This function extracts just the JSON portion.
    
    Args:
        text: Raw response text from Gemini
        
    Returns:
        Cleaned JSON string
    """
    # Remove markdown code blocks if present
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
    # Try to find JSON object in the text
    # Look for content between first { and last }
    start = text.find('{')
    end = text.rfind('}')
    
    if start != -1 and end != -1:
        text = text[start:end + 1]
    
    return text.strip()


def call_gemini(prompt, system_prompt, api_key):
    """
    Make a request to the Gemini API using the user's API key.
    
    Args:
        prompt: The user's prompt/question
        system_prompt: Instructions for how Gemini should respond
        api_key: The user's Gemini API key
        
    Returns:
        Parsed JSON response from Gemini
        
    Raises:
        ValueError: If API key is not provided
        Exception: If API call fails
    """
    if not api_key:
        raise ValueError("API key is required. Please provide your Gemini API key.")
    
    # Configure the Gemini API with the user's key
    genai.configure(api_key=api_key)
    
    # Initialize the Gemini model
    # gemini-2.0-flash is fast and free, great for educational content
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Combine system prompt with user prompt
    full_prompt = f"{system_prompt}\n\nUser request: {prompt}"
    
    # Generate response from Gemini
    response = model.generate_content(full_prompt)
    
    # Extract text from response
    response_text = response.text
    
    # Clean and parse JSON
    cleaned_text = clean_json_response(response_text)
    
    return json.loads(cleaned_text)


# =============================================================================
# API ROUTES
# =============================================================================

@app.route('/')
def serve_frontend():
    """
    Serve the main frontend HTML file.
    
    This allows the entire application to be accessed from a single URL:
    http://localhost:5000
    
    Returns:
        The index.html file containing the React frontend
    """
    return send_from_directory('.', 'index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the server is running.
    
    This endpoint is useful for:
    - Monitoring server status
    - Verifying deployment success
    - Load balancer health checks
    
    Returns:
        JSON response with status "healthy" and HTTP 200
    """
    return jsonify({
        "status": "healthy", 
        "message": "AI Math Tutor server is running",
        "model": "Google Gemini 2.0 Flash",
        "auth": "Google Sign-In with user-provided API keys"
    })


@app.route('/api/config', methods=['GET'])
def get_config():
    """
    Get frontend configuration including Google Client ID.
    
    This endpoint provides the Google OAuth Client ID to the frontend
    so it can be configured via environment variables instead of hardcoded.
    
    Returns:
        JSON response with configuration values
    """
    return jsonify({
        "google_client_id": os.getenv('GOOGLE_CLIENT_ID', ''),
        "use_google_auth": bool(os.getenv('GOOGLE_CLIENT_ID'))
    })


@app.route('/api/verify-key', methods=['POST'])
def verify_api_key():
    """
    Verify that a user's Gemini API key is valid.
    
    This endpoint tests the API key by making a simple request to Gemini.
    Used during the login/setup process to validate the user's key.
    
    Request Headers:
        X-API-Key: The Gemini API key to verify
    
    Returns:
        JSON response indicating if the key is valid
        
    Error Responses:
        400: Missing API key
        401: Invalid API key
    """
    try:
        api_key = get_api_key_from_request()
        
        if not api_key:
            return jsonify({
                "valid": False,
                "error": "API key is required"
            }), 400
        
        # Configure and test the API key with a simple request
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Make a simple test request
        response = model.generate_content("Reply with just the word 'OK'")
        
        # If we get here, the key is valid
        return jsonify({
            "valid": True,
            "message": "API key is valid!"
        })
        
    except Exception as e:
        error_message = str(e)
        
        # Check for common API key errors
        if "API_KEY" in error_message.upper() or "invalid" in error_message.lower() or "401" in error_message:
            return jsonify({
                "valid": False,
                "error": "Invalid API key. Please check your key and try again."
            }), 401
        
        return jsonify({
            "valid": False,
            "error": f"Error verifying API key: {error_message}"
        }), 500


@app.route('/api/solve', methods=['POST'])
def solve_problem():
    """
    Solve a math problem with step-by-step explanations.
    
    This endpoint accepts a math problem from the user and uses Gemini AI
    to generate a detailed, educational solution with explanations for each step.
    
    Request Headers:
        X-API-Key: The user's Gemini API key
    
    Request Body (JSON):
        {
            "problem": "The math problem to solve (string)"
        }
    
    Returns:
        JSON response containing:
        - problem_type: Category of the math problem
        - concepts: List of mathematical concepts used
        - steps: Array of solution steps with explanations
        - final_answer: The final answer
        - verification: How to verify the answer
        
    Error Responses:
        400: Missing or invalid problem in request
        401: Missing or invalid API key
        500: API error or server error
    """
    try:
        # Get the API key from request headers
        api_key = get_api_key_from_request()
        
        if not api_key:
            return jsonify({
                "error": "API key is required. Please sign in and provide your Gemini API key.",
                "code": "NO_API_KEY"
            }), 401
        
        # Extract the problem from the request body
        data = request.get_json()
        
        # Validate that a problem was provided
        if not data or 'problem' not in data:
            return jsonify({
                "error": "Missing 'problem' in request body",
                "example": {"problem": "Solve for x: 2x + 5 = 13"}
            }), 400
        
        problem = data['problem']
        
        # Validate that the problem is not empty
        if not problem.strip():
            return jsonify({"error": "Problem cannot be empty"}), 400
        
        # Call Gemini to solve the problem
        solution = call_gemini(
            f"Please solve this math problem step-by-step:\n\n{problem}",
            SOLVER_SYSTEM_PROMPT,
            api_key
        )
        
        # Return the solution to the frontend
        return jsonify(solution)
        
    except json.JSONDecodeError as je:
        # Handle JSON parsing errors
        return jsonify({
            "error": "Failed to parse AI response. Please try again.",
            "details": str(je)
        }), 500
        
    except ValueError as ve:
        # Handle API key errors
        return jsonify({
            "error": str(ve),
            "code": "API_KEY_ERROR"
        }), 401
        
    except Exception as e:
        # Handle any unexpected errors
        error_message = str(e)
        
        # Check for common API errors
        if "API_KEY" in error_message.upper() or "invalid" in error_message.lower() or "401" in error_message:
            return jsonify({
                "error": "Invalid API key. Please check your Gemini API key.",
                "code": "INVALID_API_KEY",
                "help": "Get a free key at: https://aistudio.google.com/apikey"
            }), 401
            
        return jsonify({"error": f"Server Error: {error_message}"}), 500


@app.route('/api/quiz/generate', methods=['POST'])
def generate_quiz():
    """
    Generate quiz questions for a specified math topic.
    
    This endpoint creates practice problems based on the requested topic
    and difficulty level to help students test their understanding.
    
    Request Headers:
        X-API-Key: The user's Gemini API key
    
    Request Body (JSON):
        {
            "topic": "Math topic (e.g., 'algebra', 'calculus', 'trigonometry')",
            "num_questions": Number of questions to generate (default: 3),
            "difficulty": "easy", "medium", "hard", or "mixed" (default: "mixed")
        }
    
    Returns:
        JSON response containing:
        - quiz_topic: The topic of the quiz
        - questions: Array of quiz questions with hints and answers
        
    Error Responses:
        400: Missing or invalid topic in request
        401: Missing or invalid API key
        500: API error or server error
    """
    try:
        # Get the API key from request headers
        api_key = get_api_key_from_request()
        
        if not api_key:
            return jsonify({
                "error": "API key is required. Please sign in and provide your Gemini API key.",
                "code": "NO_API_KEY"
            }), 401
        
        # Extract quiz parameters from the request body
        data = request.get_json()
        
        # Validate that a topic was provided
        if not data or 'topic' not in data:
            return jsonify({
                "error": "Missing 'topic' in request body",
                "example": {"topic": "algebra", "num_questions": 3, "difficulty": "medium"}
            }), 400
        
        topic = data['topic']
        num_questions = data.get('num_questions', 3)  # Default to 3 questions
        difficulty = data.get('difficulty', 'mixed')  # Default to mixed difficulty
        
        # Validate number of questions (limit to prevent abuse)
        num_questions = min(max(1, num_questions), 10)  # Between 1 and 10
        
        # Call Gemini to generate the quiz
        quiz = call_gemini(
            f"Generate {num_questions} {difficulty} difficulty quiz questions about {topic}.",
            QUIZ_SYSTEM_PROMPT,
            api_key
        )
        
        # Return the generated quiz
        return jsonify(quiz)
        
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to generate quiz. Please try again."}), 500
        
    except ValueError as ve:
        return jsonify({
            "error": str(ve),
            "code": "API_KEY_ERROR"
        }), 401
        
    except Exception as e:
        error_message = str(e)
        
        if "API_KEY" in error_message.upper() or "invalid" in error_message.lower() or "401" in error_message:
            return jsonify({
                "error": "Invalid API key. Please check your Gemini API key.",
                "code": "INVALID_API_KEY",
                "help": "Get a free key at: https://aistudio.google.com/apikey"
            }), 401
            
        return jsonify({"error": f"Server Error: {error_message}"}), 500


@app.route('/api/quiz/evaluate', methods=['POST'])
def evaluate_answer():
    """
    Evaluate a student's answer to a quiz question.
    
    This endpoint compares the student's answer to the correct answer
    and provides educational feedback.
    
    Request Headers:
        X-API-Key: The user's Gemini API key
    
    Request Body (JSON):
        {
            "question": "The quiz question that was asked",
            "correct_answer": "The correct answer",
            "student_answer": "The student's submitted answer"
        }
    
    Returns:
        JSON response containing:
        - is_correct: Boolean indicating if the answer is correct
        - feedback: Encouraging feedback for the student
        - explanation: Explanation of the correct approach (if wrong)
        
    Error Responses:
        400: Missing required fields in request
        401: Missing or invalid API key
        500: API error or server error
    """
    try:
        # Get the API key from request headers
        api_key = get_api_key_from_request()
        
        if not api_key:
            return jsonify({
                "error": "API key is required. Please sign in and provide your Gemini API key.",
                "code": "NO_API_KEY"
            }), 401
        
        # Extract evaluation parameters from the request body
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['question', 'correct_answer', 'student_answer']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"Missing '{field}' in request body",
                    "required_fields": required_fields
                }), 400
        
        question = data['question']
        correct_answer = data['correct_answer']
        student_answer = data['student_answer']
        
        # Call Gemini to evaluate the answer
        evaluation = call_gemini(
            f"""Evaluate this student's answer:
            
Question: {question}
Correct Answer: {correct_answer}
Student's Answer: {student_answer}

Please determine if the student's answer is correct (considering equivalent forms) and provide feedback.""",
            EVALUATOR_SYSTEM_PROMPT,
            api_key
        )
        
        # Return the evaluation
        return jsonify(evaluation)
        
    except json.JSONDecodeError:
        # If parsing fails, do a simple string comparison
        is_correct = str(student_answer).strip().lower() == str(correct_answer).strip().lower()
        return jsonify({
            "is_correct": is_correct,
            "feedback": "Correct! Great job!" if is_correct else "Not quite right. Keep practicing!",
            "explanation": "" if is_correct else f"The correct answer was: {correct_answer}"
        })
        
    except ValueError as ve:
        return jsonify({
            "error": str(ve),
            "code": "API_KEY_ERROR"
        }), 401
        
    except Exception as e:
        error_message = str(e)
        
        if "API_KEY" in error_message.upper() or "invalid" in error_message.lower() or "401" in error_message:
            return jsonify({
                "error": "Invalid API key. Please check your Gemini API key.",
                "code": "INVALID_API_KEY",
                "help": "Get a free key at: https://aistudio.google.com/apikey"
            }), 401
            
        return jsonify({"error": f"Server Error: {error_message}"}), 500


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    """
    Main entry point for the Flask application.
    
    When running this file directly (python server.py), it will:
    1. Start the Flask development server
    2. Enable debug mode for development (auto-reload on changes)
    3. Listen on all interfaces (0.0.0.0) on port 5000
    4. Serve both the API and the frontend
    
    For production deployment, use a production WSGI server like Gunicorn:
        gunicorn -w 4 -b 0.0.0.0:5000 server:app
    """
    print("=" * 60)
    print("AI Math Tutor - Backend Server")
    print("=" * 60)
    print()
    print("  Powered by Google Gemini (Users provide their own API key)")
    print()
    print("  Open your browser and go to:")
    print()
    print("     http://localhost:5000")
    print()
    print("  Features:")
    print("     ✓  Google Sign-In authentication")
    print("     ✓  User-provided Gemini API keys")
    print("     ✓  Step-by-step math solutions")
    print("     ✓  Interactive practice quizzes")
    print()
    print("=" * 60)
    
    # Run the Flask development server
    # debug=True enables auto-reload and detailed error messages
    # host='0.0.0.0' allows connections from any IP (needed for Docker/cloud)
    app.run(debug=True, host='0.0.0.0', port=5000)