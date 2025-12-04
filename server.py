"""
AI Math Tutor - Backend Server
==============================
Student: Aric Hurkman
Course: CSCI 250
Final Project: AI Math Tutor
Professor: Gheni Abla

This Flask server provides the backend API for the AI Math Tutor application.
It handles requests to solve math problems and generate quiz questions using
the Google Gemini API (FREE tier).

NEW FEATURE: Supports solving math problems from uploaded files:
- Images (PNG, JPG, JPEG, GIF, WEBP) - uses Gemini Vision
- PDFs - extracts text or uses vision for scanned documents
- DOCX - extracts text content

Requirements:
- Flask: Web framework for Python
- Flask-CORS: Cross-Origin Resource Sharing support
- google-generativeai: Google's Python SDK for Gemini API
- Pillow: Image processing
- pdfplumber: PDF text extraction
- python-docx: DOCX text extraction

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

# Base64 encoding for image data
import base64

# Tempfile for temporary file handling
import tempfile

# PIL for image processing
from PIL import Image
import io

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

# Configure maximum upload size (16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# =============================================================================
# GEMINI API CONFIGURATION
# =============================================================================

# Google Gemini API Key (FREE tier - 60 requests per minute!)
# Get your free key at: https://aistudio.google.com/apikey
# Set via environment variable: GEMINI_API_KEY
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY environment variable is not set.\n"
        "Get a free key at: https://aistudio.google.com/apikey\n"
        "Set it using: export GEMINI_API_KEY='your-key-here' (Mac/Linux)\n"
        "Or: $env:GEMINI_API_KEY='your-key-here' (Windows PowerShell)"
    )

# Configure the Gemini API with our key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini models
# gemini-2.0-flash is fast and free, great for educational content
model = genai.GenerativeModel('gemini-2.0-flash')

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

# System prompt for extracting math problems from images
IMAGE_EXTRACT_PROMPT = """You are an expert at reading and understanding mathematical problems from images.

Look at this image and:
1. Identify any math problems, equations, or mathematical content
2. Extract the problem(s) clearly and accurately
3. If there are multiple problems, focus on the main one or list them all

After identifying the problem, solve it step-by-step.

You MUST respond with ONLY valid JSON (no markdown, no code blocks) in this exact format:
{
    "extracted_problem": "The math problem extracted from the image",
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

If you cannot find any math problem in the image, respond with:
{
    "error": "No math problem found in the image",
    "suggestion": "Please upload an image containing a math problem"
}"""

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


def call_gemini(prompt, system_prompt):
    """
    Make a request to the Gemini API.
    
    Args:
        prompt: The user's prompt/question
        system_prompt: Instructions for how Gemini should respond
        
    Returns:
        Parsed JSON response from Gemini
    """
    # Combine system prompt with user prompt
    full_prompt = f"{system_prompt}\n\nUser request: {prompt}"
    
    # Generate response from Gemini
    response = model.generate_content(full_prompt)
    
    # Extract text from response
    response_text = response.text
    
    # Clean and parse JSON
    cleaned_text = clean_json_response(response_text)
    
    return json.loads(cleaned_text)


def call_gemini_with_image(image_data, mime_type, prompt):
    """
    Make a request to the Gemini API with an image.
    
    Gemini 2.0 Flash supports vision, allowing it to analyze images
    containing math problems.
    
    Args:
        image_data: Base64 encoded image data or bytes
        mime_type: MIME type of the image (e.g., 'image/png')
        prompt: The prompt to send with the image
        
    Returns:
        Parsed JSON response from Gemini
    """
    # Create image part for multimodal input
    image_part = {
        "mime_type": mime_type,
        "data": image_data if isinstance(image_data, bytes) else base64.b64decode(image_data)
    }
    
    # Generate response with image
    response = model.generate_content([prompt, image_part])
    
    # Extract text from response
    response_text = response.text
    
    # Clean and parse JSON
    cleaned_text = clean_json_response(response_text)
    
    return json.loads(cleaned_text)


def extract_text_from_pdf(file_data):
    """
    Extract text content from a PDF file.
    
    Uses pdfplumber for text extraction. Falls back to image-based
    extraction if text extraction fails (for scanned PDFs).
    
    Args:
        file_data: Binary PDF file data
        
    Returns:
        Tuple of (text_content, is_image_based)
    """
    try:
        import pdfplumber
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(file_data)
            tmp_path = tmp.name
        
        try:
            text_content = ""
            with pdfplumber.open(tmp_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n"
            
            # If we got meaningful text, return it
            if text_content.strip() and len(text_content.strip()) > 20:
                return text_content.strip(), False
            
            # Otherwise, try to convert PDF to image for vision
            return None, True
            
        finally:
            os.unlink(tmp_path)
            
    except ImportError:
        # pdfplumber not installed, try image-based extraction
        return None, True
    except Exception as e:
        print(f"PDF text extraction error: {e}")
        return None, True


def convert_pdf_to_image(file_data):
    """
    Convert first page of PDF to image for vision-based extraction.
    
    Uses pdf2image library to convert PDF pages to images.
    
    Args:
        file_data: Binary PDF file data
        
    Returns:
        Tuple of (image_bytes, mime_type) or (None, None) on failure
    """
    try:
        from pdf2image import convert_from_bytes
        
        # Convert first page of PDF to image
        images = convert_from_bytes(file_data, first_page=1, last_page=1, dpi=150)
        
        if images:
            # Convert PIL Image to bytes
            img_byte_arr = io.BytesIO()
            images[0].save(img_byte_arr, format='PNG')
            return img_byte_arr.getvalue(), 'image/png'
            
    except ImportError:
        print("pdf2image not installed. Install with: pip install pdf2image")
    except Exception as e:
        print(f"PDF to image conversion error: {e}")
    
    return None, None


def extract_text_from_docx(file_data):
    """
    Extract text content from a DOCX file.
    
    Uses python-docx library to read Word documents.
    
    Args:
        file_data: Binary DOCX file data
        
    Returns:
        Extracted text content as string
    """
    try:
        from docx import Document
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
            tmp.write(file_data)
            tmp_path = tmp.name
        
        try:
            doc = Document(tmp_path)
            
            # Extract text from all paragraphs
            text_content = []
            for para in doc.paragraphs:
                if para.text.strip():
                    text_content.append(para.text)
            
            # Also extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    row_text = []
                    for cell in row.cells:
                        if cell.text.strip():
                            row_text.append(cell.text.strip())
                    if row_text:
                        text_content.append(" | ".join(row_text))
            
            return "\n".join(text_content)
            
        finally:
            os.unlink(tmp_path)
            
    except ImportError:
        raise ValueError("python-docx not installed. Install with: pip install python-docx")
    except Exception as e:
        raise ValueError(f"Failed to read DOCX file: {str(e)}")


def get_mime_type(filename):
    """
    Get MIME type from filename extension.
    
    Args:
        filename: Name of the file
        
    Returns:
        MIME type string
    """
    extension = filename.lower().split('.')[-1] if '.' in filename else ''
    
    mime_types = {
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'gif': 'image/gif',
        'webp': 'image/webp',
        'pdf': 'application/pdf',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'doc': 'application/msword'
    }
    
    return mime_types.get(extension, 'application/octet-stream')


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
        "features": ["text_input", "image_upload", "pdf_upload", "docx_upload"]
    })


@app.route('/api/solve', methods=['POST'])
def solve_problem():
    """
    Solve a math problem with step-by-step explanations.
    
    This endpoint accepts a math problem from the user and uses Gemini AI
    to generate a detailed, educational solution with explanations for each step.
    
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
        500: API error or server error
    """
    try:
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
            SOLVER_SYSTEM_PROMPT
        )
        
        # Return the solution to the frontend
        return jsonify(solution)
        
    except json.JSONDecodeError as je:
        # Handle JSON parsing errors
        return jsonify({
            "error": "Failed to parse AI response. Please try again.",
            "details": str(je)
        }), 500
        
    except Exception as e:
        # Handle any unexpected errors
        error_message = str(e)
        
        # Check for common API errors
        if "API_KEY" in error_message or "invalid" in error_message.lower():
            return jsonify({
                "error": "API Key Error: Please set a valid Gemini API key in server.py",
                "help": "Get a free key at: https://aistudio.google.com/apikey"
            }), 500
            
        return jsonify({"error": f"Server Error: {error_message}"}), 500


@app.route('/api/solve/file', methods=['POST'])
def solve_from_file():
    """
    Solve a math problem from an uploaded file (image, PDF, or DOCX).
    
    This endpoint accepts file uploads and uses Gemini AI to:
    1. Extract the math problem from the file
    2. Solve it with step-by-step explanations
    
    Supported File Types:
        - Images: PNG, JPG, JPEG, GIF, WEBP (uses Gemini Vision)
        - PDF: Extracts text or uses vision for scanned documents
        - DOCX: Extracts text content
    
    Request:
        multipart/form-data with 'file' field containing the uploaded file
    
    Returns:
        JSON response containing:
        - extracted_problem: The problem found in the file
        - problem_type: Category of the math problem
        - concepts: List of mathematical concepts used
        - steps: Array of solution steps with explanations
        - final_answer: The final answer
        - verification: How to verify the answer
        
    Error Responses:
        400: Missing file or unsupported file type
        500: API error or server error
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                "error": "No file uploaded",
                "help": "Please upload an image (PNG, JPG), PDF, or DOCX file"
            }), 400
        
        file = request.files['file']
        
        # Check if filename is empty
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Get file extension and MIME type
        filename = file.filename.lower()
        extension = filename.split('.')[-1] if '.' in filename else ''
        mime_type = get_mime_type(filename)
        
        # Read file data
        file_data = file.read()
        
        # Supported image extensions
        image_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        
        # Process based on file type
        if extension in image_extensions:
            # Direct image processing with Gemini Vision
            solution = call_gemini_with_image(
                file_data,
                mime_type,
                IMAGE_EXTRACT_PROMPT
            )
            return jsonify(solution)
            
        elif extension == 'pdf':
            # Try text extraction first
            text_content, needs_vision = extract_text_from_pdf(file_data)
            
            if text_content and not needs_vision:
                # Use extracted text
                solution = call_gemini(
                    f"Please find and solve any math problem(s) in this document:\n\n{text_content}",
                    SOLVER_SYSTEM_PROMPT
                )
                solution['extracted_problem'] = text_content[:500] + "..." if len(text_content) > 500 else text_content
                return jsonify(solution)
            else:
                # Try converting PDF to image
                image_bytes, img_mime_type = convert_pdf_to_image(file_data)
                
                if image_bytes:
                    solution = call_gemini_with_image(
                        image_bytes,
                        img_mime_type,
                        IMAGE_EXTRACT_PROMPT
                    )
                    return jsonify(solution)
                else:
                    return jsonify({
                        "error": "Could not extract content from PDF",
                        "help": "Try uploading a clearer image or a text-based PDF"
                    }), 400
                    
        elif extension in {'docx', 'doc'}:
            # Extract text from Word document
            text_content = extract_text_from_docx(file_data)
            
            if text_content.strip():
                solution = call_gemini(
                    f"Please find and solve any math problem(s) in this document:\n\n{text_content}",
                    SOLVER_SYSTEM_PROMPT
                )
                solution['extracted_problem'] = text_content[:500] + "..." if len(text_content) > 500 else text_content
                return jsonify(solution)
            else:
                return jsonify({
                    "error": "No text content found in the document",
                    "help": "The document appears to be empty or contains only images"
                }), 400
        else:
            return jsonify({
                "error": f"Unsupported file type: .{extension}",
                "supported": ["png", "jpg", "jpeg", "gif", "webp", "pdf", "docx"]
            }), 400
            
    except json.JSONDecodeError:
        return jsonify({
            "error": "Failed to parse AI response. Please try again.",
        }), 500
        
    except Exception as e:
        error_message = str(e)
        
        if "API_KEY" in error_message or "invalid" in error_message.lower():
            return jsonify({
                "error": "API Key Error: Please set a valid Gemini API key",
                "help": "Get a free key at: https://aistudio.google.com/apikey"
            }), 500
            
        return jsonify({"error": f"Server Error: {error_message}"}), 500


@app.route('/api/quiz/generate', methods=['POST'])
def generate_quiz():
    """
    Generate quiz questions for a specified math topic.
    
    This endpoint creates practice problems based on the requested topic
    and difficulty level to help students test their understanding.
    
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
        500: API error or server error
    """
    try:
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
            QUIZ_SYSTEM_PROMPT
        )
        
        # Return the generated quiz
        return jsonify(quiz)
        
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to generate quiz. Please try again."}), 500
        
    except Exception as e:
        error_message = str(e)
        
        if "API_KEY" in error_message or "invalid" in error_message.lower():
            return jsonify({
                "error": "API Key Error: Please set a valid Gemini API key in server.py",
                "help": "Get a free key at: https://aistudio.google.com/apikey"
            }), 500
            
        return jsonify({"error": f"Server Error: {error_message}"}), 500


@app.route('/api/quiz/evaluate', methods=['POST'])
def evaluate_answer():
    """
    Evaluate a student's answer to a quiz question.
    
    This endpoint compares the student's answer to the correct answer
    and provides educational feedback.
    
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
        500: API error or server error
    """
    try:
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
            EVALUATOR_SYSTEM_PROMPT
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
        
    except Exception as e:
        error_message = str(e)
        
        if "API_KEY" in error_message or "invalid" in error_message.lower():
            return jsonify({
                "error": "API Key Error: Please set a valid Gemini API key in server.py",
                "help": "Get a free key at: https://aistudio.google.com/apikey"
            }), 500
            
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
    print("  Powered by Google Gemini (FREE tier)")
    print()
    print("  NEW: Upload images, PDFs, or DOCX files with math problems!")
    print()
    print("  Open your browser and go to:")
    print()
    print("     http://localhost:5000")
    print()
    print("  ✓  Gemini API Key loaded from environment")
    print()
    print("=" * 60)
    
    # Run the Flask development server
    # debug=True enables auto-reload and detailed error messages
    # host='0.0.0.0' allows connections from any IP (needed for Docker/cloud)
    app.run(debug=True, host='0.0.0.0', port=5000)