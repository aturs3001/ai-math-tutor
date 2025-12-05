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
- FILE UPLOAD SUPPORT: Images (.png, .jpg, .jpeg, .gif, .webp), PDFs, and DOCX files

Requirements:
- Flask: Web framework for Python
- Flask-CORS: Cross-Origin Resource Sharing support
- google-generativeai: Google's Python SDK for Gemini API
- Pillow: Image processing library
- pdf2image: PDF to image conversion
- python-docx: Word document text extraction
- PyMuPDF (fitz): PDF text extraction

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

# OS module for environment variable access and file operations
import os

# JSON module for parsing responses
import json

# Regular expressions for cleaning JSON responses
import re

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Base64 encoding for file uploads
import base64

# IO module for handling byte streams
import io

# Temporary file handling
import tempfile

# PIL/Pillow for image processing
from PIL import Image

# PDF processing libraries
try:
    import fitz  # PyMuPDF for PDF text and image extraction
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    from pdf2image import convert_from_bytes
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

# Word document processing
try:
    from docx import Document as DocxDocument
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

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

# Configure maximum file upload size (16 MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Allowed file extensions for uploads
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'docx', 'doc'}

# =============================================================================
# SYSTEM PROMPTS
# =============================================================================

# System prompt for solving math problems
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

# System prompt for solving problems from images/files
FILE_SOLVER_SYSTEM_PROMPT = """You are an expert math tutor helping students understand mathematical concepts.
You are analyzing a math problem from an uploaded file (image, PDF, or document).

Your task:
1. Carefully examine the uploaded content for any mathematical problems
2. If you find math problems, identify and solve them step-by-step
3. If the image/document contains multiple problems, focus on the most prominent one or solve all if possible
4. If the content is unclear or not a math problem, explain what you see and ask for clarification

When solving problems:
1. First, identify what type of problem it is (algebra, calculus, geometry, trigonometry, etc.)
2. List any relevant formulas or theorems that will be used
3. Show each step clearly with explanations of WHY each step is taken
4. Use proper mathematical notation
5. Provide the final answer clearly marked
6. If applicable, verify the answer or explain how to check it

You MUST respond with ONLY valid JSON (no markdown, no code blocks) in this exact format:
{
    "problem_detected": "Description of the problem found in the file",
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

If NO math problem is found, respond with:
{
    "problem_detected": "No math problem found",
    "problem_type": "N/A",
    "concepts": [],
    "steps": [],
    "final_answer": "Unable to identify a math problem in the uploaded file. Please ensure the file contains a clear mathematical problem.",
    "verification": "N/A"
}

Always be encouraging and educational."""

# System prompt for generating quiz questions
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
    start = text.find('{')
    end = text.rfind('}')
    
    if start != -1 and end != -1:
        text = text[start:end + 1]
    
    return text.strip()


def allowed_file(filename, file_type='image'):
    """
    Check if a file has an allowed extension.
    
    Args:
        filename: Name of the uploaded file
        file_type: Type of file ('image' or 'document')
        
    Returns:
        Boolean indicating if the file extension is allowed
    """
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    if file_type == 'image':
        return ext in ALLOWED_IMAGE_EXTENSIONS
    elif file_type == 'document':
        return ext in ALLOWED_DOCUMENT_EXTENSIONS
    else:
        return ext in ALLOWED_IMAGE_EXTENSIONS or ext in ALLOWED_DOCUMENT_EXTENSIONS


def get_file_extension(filename):
    """
    Get the file extension from a filename.
    
    Args:
        filename: Name of the file
        
    Returns:
        Lowercase file extension without the dot
    """
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return ''


def process_image_file(file_data, filename):
    """
    Process an uploaded image file for Gemini API.
    
    Args:
        file_data: Raw file bytes
        filename: Original filename
        
    Returns:
        PIL Image object ready for Gemini
    """
    image = Image.open(io.BytesIO(file_data))
    
    # Convert to RGB if necessary (handles PNG with transparency, etc.)
    if image.mode in ('RGBA', 'LA', 'P'):
        # Create a white background
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
        image = background
    elif image.mode != 'RGB':
        image = image.convert('RGB')
    
    return image


def extract_text_from_pdf(file_data):
    """
    Extract text content from a PDF file.
    
    Args:
        file_data: Raw PDF file bytes
        
    Returns:
        Tuple of (extracted_text, list_of_page_images)
    """
    text_content = ""
    page_images = []
    
    if PYMUPDF_AVAILABLE:
        # Use PyMuPDF for text extraction and image conversion
        pdf_document = fitz.open(stream=file_data, filetype="pdf")
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            
            # Extract text
            text_content += f"\n--- Page {page_num + 1} ---\n"
            text_content += page.get_text()
            
            # Convert page to image (for visual math problems)
            mat = fitz.Matrix(2, 2)  # 2x zoom for better quality
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            page_images.append(img)
        
        pdf_document.close()
    
    elif PDF2IMAGE_AVAILABLE:
        # Fallback to pdf2image
        try:
            images = convert_from_bytes(file_data, dpi=150)
            page_images = images
            text_content = "PDF converted to images for visual analysis."
        except Exception as e:
            text_content = f"Error converting PDF: {str(e)}"
    
    else:
        text_content = "PDF processing libraries not available. Please install PyMuPDF (fitz) or pdf2image."
    
    return text_content, page_images


def extract_text_from_docx(file_data):
    """
    Extract text content from a DOCX file.
    
    Args:
        file_data: Raw DOCX file bytes
        
    Returns:
        Extracted text content
    """
    if not DOCX_AVAILABLE:
        return "DOCX processing library not available. Please install python-docx."
    
    try:
        doc = DocxDocument(io.BytesIO(file_data))
        
        text_content = ""
        for para in doc.paragraphs:
            text_content += para.text + "\n"
        
        # Also extract text from tables
        for table in doc.tables:
            for row in table.rows:
                row_text = [cell.text for cell in row.cells]
                text_content += " | ".join(row_text) + "\n"
        
        return text_content.strip()
    
    except Exception as e:
        return f"Error reading DOCX file: {str(e)}"


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


def call_gemini_with_image(images, prompt, system_prompt, api_key):
    """
    Make a request to the Gemini API with image(s) using the user's API key.
    
    Args:
        images: List of PIL Image objects or single PIL Image
        prompt: Additional text prompt/question
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
    
    # Initialize the Gemini model with vision capabilities
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Prepare content parts
    content_parts = []
    
    # Add system prompt and user prompt as text
    full_prompt = f"{system_prompt}\n\nAdditional context from user: {prompt}" if prompt else system_prompt
    content_parts.append(full_prompt)
    
    # Add images
    if isinstance(images, list):
        for img in images[:5]:  # Limit to first 5 images
            content_parts.append(img)
    else:
        content_parts.append(images)
    
    # Generate response from Gemini
    response = model.generate_content(content_parts)
    
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
    
    Returns:
        JSON response with status "healthy" and HTTP 200
    """
    return jsonify({
        "status": "healthy", 
        "message": "AI Math Tutor server is running",
        "model": "Google Gemini 2.0 Flash",
        "auth": "Google Sign-In with user-provided API keys",
        "features": {
            "file_upload": True,
            "supported_formats": list(ALLOWED_IMAGE_EXTENSIONS) + list(ALLOWED_DOCUMENT_EXTENSIONS),
            "pymupdf_available": PYMUPDF_AVAILABLE,
            "pdf2image_available": PDF2IMAGE_AVAILABLE,
            "docx_available": DOCX_AVAILABLE
        }
    })


@app.route('/api/config', methods=['GET'])
def get_config():
    """
    Get frontend configuration including Google Client ID and supported file types.
    
    Returns:
        JSON response with configuration values
    """
    return jsonify({
        "google_client_id": os.getenv('GOOGLE_CLIENT_ID', ''),
        "use_google_auth": bool(os.getenv('GOOGLE_CLIENT_ID')),
        "supported_file_types": {
            "images": list(ALLOWED_IMAGE_EXTENSIONS),
            "documents": list(ALLOWED_DOCUMENT_EXTENSIONS)
        },
        "max_file_size_mb": 16
    })


@app.route('/api/verify-key', methods=['POST'])
def verify_api_key():
    """
    Verify that a user's Gemini API key is valid.
    
    Request Headers:
        X-API-Key: The Gemini API key to verify
    
    Returns:
        JSON response indicating if the key is valid
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
    
    Request Headers:
        X-API-Key: The user's Gemini API key
    
    Request Body (JSON):
        {
            "problem": "The math problem to solve (string)"
        }
    
    Returns:
        JSON response containing step-by-step solution
    """
    try:
        api_key = get_api_key_from_request()
        
        if not api_key:
            return jsonify({
                "error": "API key is required. Please sign in and provide your Gemini API key.",
                "code": "NO_API_KEY"
            }), 401
        
        data = request.get_json()
        
        if not data or 'problem' not in data:
            return jsonify({
                "error": "Missing 'problem' in request body",
                "example": {"problem": "Solve for x: 2x + 5 = 13"}
            }), 400
        
        problem = data['problem']
        
        if not problem.strip():
            return jsonify({"error": "Problem cannot be empty"}), 400
        
        solution = call_gemini(
            f"Please solve this math problem step-by-step:\n\n{problem}",
            SOLVER_SYSTEM_PROMPT,
            api_key
        )
        
        return jsonify(solution)
        
    except json.JSONDecodeError as je:
        return jsonify({
            "error": "Failed to parse AI response. Please try again.",
            "details": str(je)
        }), 500
        
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


@app.route('/api/solve/file', methods=['POST'])
def solve_from_file():
    """
    Solve a math problem from an uploaded file (image, PDF, or DOCX).
    
    This endpoint accepts file uploads containing math problems and uses
    Gemini's vision capabilities to analyze and solve them.
    
    Request Headers:
        X-API-Key: The user's Gemini API key
    
    Request Form Data:
        file: The uploaded file (image, PDF, or DOCX)
        additional_context: Optional additional context or question about the problem
    
    Supported File Types:
        - Images: .png, .jpg, .jpeg, .gif, .webp, .bmp
        - Documents: .pdf, .docx
    
    Returns:
        JSON response containing:
        - problem_detected: Description of the problem found
        - problem_type: Category of the math problem
        - concepts: List of mathematical concepts used
        - steps: Array of solution steps with explanations
        - final_answer: The final answer
        - verification: How to verify the answer
        
    Error Responses:
        400: Missing or invalid file
        401: Missing or invalid API key
        413: File too large
        415: Unsupported file type
        500: Server error
    """
    try:
        # Get API key
        api_key = get_api_key_from_request()
        
        if not api_key:
            return jsonify({
                "error": "API key is required. Please sign in and provide your Gemini API key.",
                "code": "NO_API_KEY"
            }), 401
        
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                "error": "No file uploaded. Please upload an image, PDF, or DOCX file containing a math problem.",
                "supported_types": list(ALLOWED_IMAGE_EXTENSIONS) + list(ALLOWED_DOCUMENT_EXTENSIONS)
            }), 400
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Get additional context if provided
        additional_context = request.form.get('additional_context', '')
        
        # Get file extension
        file_ext = get_file_extension(file.filename)
        
        # Validate file type
        if not allowed_file(file.filename, 'all'):
            return jsonify({
                "error": f"Unsupported file type: .{file_ext}",
                "supported_types": list(ALLOWED_IMAGE_EXTENSIONS) + list(ALLOWED_DOCUMENT_EXTENSIONS)
            }), 415
        
        # Read file data
        file_data = file.read()
        
        # Process based on file type
        if file_ext in ALLOWED_IMAGE_EXTENSIONS:
            # Process image file
            try:
                image = process_image_file(file_data, file.filename)
                solution = call_gemini_with_image(
                    image,
                    additional_context,
                    FILE_SOLVER_SYSTEM_PROMPT,
                    api_key
                )
            except Exception as img_error:
                return jsonify({
                    "error": f"Failed to process image: {str(img_error)}"
                }), 400
        
        elif file_ext == 'pdf':
            # Process PDF file
            text_content, page_images = extract_text_from_pdf(file_data)
            
            if page_images:
                # Use images for visual analysis (better for math problems with diagrams)
                solution = call_gemini_with_image(
                    page_images,
                    f"Extracted text for reference:\n{text_content}\n\nAdditional context: {additional_context}",
                    FILE_SOLVER_SYSTEM_PROMPT,
                    api_key
                )
            elif text_content:
                # Fallback to text-only analysis
                solution = call_gemini(
                    f"The following math problem was extracted from a PDF file:\n\n{text_content}\n\nAdditional context: {additional_context}",
                    SOLVER_SYSTEM_PROMPT,
                    api_key
                )
            else:
                return jsonify({
                    "error": "Could not extract content from PDF. Please ensure the PDF is not password-protected and contains readable content.",
                    "hint": "Try taking a screenshot of the problem instead."
                }), 400
        
        elif file_ext in ['docx', 'doc']:
            # Process DOCX file
            text_content = extract_text_from_docx(file_data)
            
            if text_content and not text_content.startswith("Error"):
                solution = call_gemini(
                    f"The following math problem was extracted from a Word document:\n\n{text_content}\n\nAdditional context: {additional_context}",
                    SOLVER_SYSTEM_PROMPT,
                    api_key
                )
            else:
                return jsonify({
                    "error": text_content if text_content else "Could not extract content from DOCX file.",
                    "hint": "Try copying the problem text and using the text input instead."
                }), 400
        
        else:
            return jsonify({"error": "Unsupported file type"}), 415
        
        # Add file info to response
        solution['source_file'] = {
            'filename': file.filename,
            'type': file_ext,
            'size_bytes': len(file_data)
        }
        
        return jsonify(solution)
        
    except json.JSONDecodeError as je:
        return jsonify({
            "error": "Failed to parse AI response. Please try again.",
            "details": str(je)
        }), 500
        
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
        
        if "too large" in error_message.lower() or "size" in error_message.lower():
            return jsonify({
                "error": "File too large. Maximum file size is 16 MB.",
                "code": "FILE_TOO_LARGE"
            }), 413
            
        return jsonify({"error": f"Server Error: {error_message}"}), 500


@app.route('/api/quiz/generate', methods=['POST'])
def generate_quiz():
    """
    Generate quiz questions for a specified math topic.
    
    Request Headers:
        X-API-Key: The user's Gemini API key
    
    Request Body (JSON):
        {
            "topic": "Math topic (e.g., 'algebra', 'calculus', 'trigonometry')",
            "num_questions": Number of questions to generate (default: 3),
            "difficulty": "easy", "medium", "hard", or "mixed" (default: "mixed")
        }
    
    Returns:
        JSON response containing quiz questions
    """
    try:
        api_key = get_api_key_from_request()
        
        if not api_key:
            return jsonify({
                "error": "API key is required. Please sign in and provide your Gemini API key.",
                "code": "NO_API_KEY"
            }), 401
        
        data = request.get_json()
        
        if not data or 'topic' not in data:
            return jsonify({
                "error": "Missing 'topic' in request body",
                "example": {"topic": "algebra", "num_questions": 3, "difficulty": "medium"}
            }), 400
        
        topic = data['topic']
        num_questions = data.get('num_questions', 3)
        difficulty = data.get('difficulty', 'mixed')
        
        # Validate number of questions (limit to prevent abuse)
        num_questions = min(max(1, num_questions), 10)
        
        quiz = call_gemini(
            f"Generate {num_questions} {difficulty} difficulty quiz questions about {topic}.",
            QUIZ_SYSTEM_PROMPT,
            api_key
        )
        
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
    
    Request Headers:
        X-API-Key: The user's Gemini API key
    
    Request Body (JSON):
        {
            "question": "The quiz question that was asked",
            "correct_answer": "The correct answer",
            "student_answer": "The student's submitted answer"
        }
    
    Returns:
        JSON response containing evaluation feedback
    """
    try:
        api_key = get_api_key_from_request()
        
        if not api_key:
            return jsonify({
                "error": "API key is required. Please sign in and provide your Gemini API key.",
                "code": "NO_API_KEY"
            }), 401
        
        data = request.get_json()
        
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
        
        evaluation = call_gemini(
            f"""Evaluate this student's answer:
            
Question: {question}
Correct Answer: {correct_answer}
Student's Answer: {student_answer}

Please determine if the student's answer is correct (considering equivalent forms) and provide feedback.""",
            EVALUATOR_SYSTEM_PROMPT,
            api_key
        )
        
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
    2. Enable debug mode for development
    3. Listen on all interfaces (0.0.0.0) on port 5000
    4. Serve both the API and the frontend
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
    print("     ✓  FILE UPLOAD SUPPORT:")
    print(f"        - Images: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}")
    print(f"        - Documents: {', '.join(ALLOWED_DOCUMENT_EXTENSIONS)}")
    print()
    print("  Library Status:")
    print(f"     {'✓' if PYMUPDF_AVAILABLE else '✗'}  PyMuPDF (PDF processing)")
    print(f"     {'✓' if PDF2IMAGE_AVAILABLE else '✗'}  pdf2image (PDF to image)")
    print(f"     {'✓' if DOCX_AVAILABLE else '✗'}  python-docx (Word documents)")
    print()
    print("=" * 60)
    
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)