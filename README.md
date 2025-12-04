# AI Math Tutor

**Student:** Aric Hurkman  
**Course:** CSCI 250  
**Final Project:** AI Math Tutor  
**Professor:** Gheni Abla  

---

## 📐 Project Overview

The AI Math Tutor is a web-based application that helps students learn mathematics through AI-powered step-by-step solutions and interactive quizzes. The application uses the Google Gemini API (FREE tier) to provide intelligent tutoring assistance.

### Features

1. **Problem Solver**: Input any math problem and receive detailed, step-by-step solutions with explanations
2. **File Upload Support (NEW!)**: Upload images, PDFs, or DOCX files containing math problems
   - **Images**: PNG, JPG, JPEG, GIF, WebP - Uses Gemini Vision AI
   - **PDFs**: Extracts text or uses vision for scanned documents
   - **DOCX**: Extracts text content from Word documents
3. **Practice Quizzes**: Generate AI-powered practice problems with immediate feedback
4. **Multiple Topics**: Support for algebra, geometry, calculus, trigonometry, statistics, and linear algebra
5. **Adaptive Difficulty**: Choose between easy, medium, hard, or mixed difficulty levels

---

## 🛠️ Technology Stack

### Backend

- **Python 3.8+**: Programming language
- **Flask**: Web framework for REST API
- **Flask-CORS**: Cross-origin resource sharing
- **Google Generative AI SDK**: Gemini API integration (FREE!)
- **Pillow**: Image processing
- **pdfplumber**: PDF text extraction
- **python-docx**: DOCX text extraction
- **pdf2image**: PDF to image conversion (optional, for scanned PDFs)

### Frontend

- **HTML5/CSS3**: Structure and styling
- **React 18**: UI framework (loaded via CDN)
- **Tailwind CSS**: Utility-first styling
- **Lucide Icons**: Icon library
- **KaTeX**: Mathematical notation rendering

---

## 📋 Requirements

Before running the application, ensure you have:

1. **Python 3.8 or higher** installed
2. **A Google Gemini API key** (FREE - get one at <https://aistudio.google.com/apikey>)
3. **A modern web browser** (Chrome, Firefox, Safari, or Edge)
4. **(Optional) Poppler** - For scanned PDF support:
   - **Mac**: `brew install poppler`
   - **Ubuntu/Debian**: `sudo apt-get install poppler-utils`
   - **Windows**: Download from <https://github.com/oschwartz10612/poppler-windows/releases>

---

## 🚀 Installation & Setup

### Step 1: Download the Project Files

Ensure you have all project files in a directory:

```ai-math-tutor/
├── server.py           # Backend Flask server
├── index.html          # Frontend React application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

### Step 2: Install Python Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 3: Set Your Gemini API Key

1. Get a FREE API key from: <https://aistudio.google.com/apikey>
2. Set the environment variable:

**Windows PowerShell:**

```powershell
$env:GEMINI_API_KEY='your-api-key-here'
```

**Mac/Linux:**

```bash
export GEMINI_API_KEY='your-api-key-here'
```

**Alternative (Optional):** Create a `.env` file in the project directory:

```GEMINI_API_KEY=your-api-key-here
```

Then install python-dotenv: `pip install python-dotenv`

### Step 4: Start the Server

In the terminal, run:

```bash
python server.py
```

```You should see output like:
============================================================
AI Math Tutor - Backend Server
============================================================

  Powered by Google Gemini (FREE tier)

  NEW: Upload images, PDFs, or DOCX files with math problems!

  Open your browser and go to:

     http://localhost:5000

  ✓  Gemini API Key loaded from environment

============================================================
```

### Step 5: Open the Application

Open your web browser and go to:

```http://localhost:5000
```

That's it! The server serves both the backend API and the frontend from the same URL.

---

## 📖 How to Use

### Problem Solver Mode

#### Option 1: Type a Problem

1. Click the "Problem Solver" tab (selected by default)
2. Make sure "Type Problem" is selected
3. Enter your math problem in the text area
   - Example: "Solve for x: 2x + 5 = 13"
   - Example: "Find the derivative of x³ + 2x² - 5x + 3"
4. Click "Solve Problem" or press Enter
5. View the step-by-step solution with explanations

#### Option 2: Upload a File (NEW!)

1. Click the "Problem Solver" tab
2. Click "Upload File" to switch to file upload mode
3. Drag and drop a file or click to browse
   - **Supported formats**: PNG, JPG, JPEG, GIF, WebP, PDF, DOCX
   - **Max file size**: 16MB
4. Click "Solve from File"
5. The AI will extract the math problem from your file and solve it

### Practice Quiz Mode

1. Click the "Practice Quiz" tab
2. Select a math topic (Algebra, Geometry, Calculus, etc.)
3. Choose a difficulty level (Easy, Medium, Hard, or Mixed)
4. Set the number of questions (1-10)
5. Click "Start Quiz"
6. Answer each question and submit
7. Receive immediate feedback and see your score

---

## 🔧 API Endpoints

The backend provides the following REST API endpoints:

### Health Check

```GET /api/health
```

```Returns server status and supported features.
```

### Solve Problem (Text Input)

```POST /api/solve
Content-Type: application/json

{
    "problem": "Solve for x: 2x + 5 = 13"
}
```Returns step-by-step solution.

### Solve Problem (File Upload) - NEW!

```POST /api/solve/file
Content-Type: multipart/form-data

file: <uploaded file>
```Accepts image (PNG, JPG, GIF, WebP), PDF, or DOCX files.
Returns extracted problem and step-by-step solution.

### Generate Quiz

```POST /api/quiz/generate
Content-Type: application/json

{
    "topic": "algebra",
    "num_questions": 3,
    "difficulty": "medium"
}
```Returns generated quiz questions.

### Evaluate Answer

```POST /api/quiz/evaluate
Content-Type: application/json

{
    "question": "What is 2 + 2?",
    "correct_answer": "4",
    "student_answer": "4"
}
```Returns evaluation feedback.
---

## 📸 File Upload Examples

### Supported Image Formats

- **PNG**: Best for screenshots and diagrams
- **JPG/JPEG**: Good for photos of handwritten problems
- **GIF**: Animated or static images
- **WebP**: Modern web format

### PDF Documents

- **Text-based PDFs**: Text is extracted directly
- **Scanned PDFs**: Converted to images and processed with Gemini Vision
  - Requires poppler-utils for scanned PDF support

### Word Documents (DOCX)

- Extracts text from paragraphs and tables
- Works with Microsoft Word and compatible applications

---

## 🌐 Cloud Deployment

To deploy this application to the cloud:

### Using Heroku

1. Create a `Procfile`: web: gunicorn server:app

2. Add `gunicorn` to requirements.txt

3. Deploy:

```bash
heroku create
heroku config:set GEMINI_API_KEY='your-api-key'
git push heroku main
```

### Using AWS/GCP/Azure

1. Set up a virtual machine or container service
2. Install dependencies (including poppler-utils for scanned PDF support)
3. Set environment variables
4. Use nginx as a reverse proxy (recommended)
5. Use gunicorn as the WSGI server

---

## 📁 Project Structure

```ai-math-tutor/
│
├── server.py              # Flask backend server
│   ├── API endpoints      # /api/solve, /api/solve/file, /api/quiz/*
│   ├── File processing    # Image, PDF, DOCX handlers
│   ├── System prompts     # Instructions for Gemini AI
│   └── Error handling     # Comprehensive error responses
│
├── index.html             # Frontend React application
│   ├── React components   # App, ProblemSolver, QuizMode, FileUpload
│   ├── API services       # Functions to call backend
│   ├── UI components      # LoadingSpinner, ErrorAlert, TabButton
│   └── Styling            # Tailwind CSS + custom styles
│
├── requirements.txt       # Python dependencies
│
└── README.md             # Documentation (this file)
```

---

## 🔒 Security Notes

- **Never commit your API key** to version control
- The API key should always be set via environment variables
- For production, use HTTPS and proper authentication
- Consider rate limiting for public deployments
- File uploads are limited to 16MB for security

---

## 🐛 Troubleshooting

### "GEMINI_API_KEY environment variable is not set" error

- Make sure you've set the environment variable before running the server
- **Windows PowerShell:** `$env:GEMINI_API_KEY='your-key-here'`
- **Mac/Linux:** `export GEMINI_API_KEY='your-key-here'`
- Verify the key is correct (no extra spaces)
- Get a free key at: <https://aistudio.google.com/apikey>

### "Failed to fetch" or CORS errors

- Make sure the backend server is running on port 5000
- Check that both frontend and backend are running

### "API Error: 429"

- You've hit the rate limit (60 requests/minute on free tier)
- Wait a minute and try again

### File upload not working

- Check file size (max 16MB)
- Ensure file format is supported (PNG, JPG, GIF, WebP, PDF, DOCX)
- For PDFs, make sure they're not password-protected

### Scanned PDFs not extracting text

- Install poppler-utils:
  - **Mac**: `brew install poppler`
  - **Ubuntu/Debian**: `sudo apt-get install poppler-utils`
  - **Windows**: Download from <https://github.com/oschwartz10612/poppler-windows/releases>

### Quiz not generating

- Ensure you have a stable internet connection
- Check the browser console for error messages

---

## 📚 References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [pdfplumber Documentation](https://github.com/jsvine/pdfplumber)
- [python-docx Documentation](https://python-docx.readthedocs.io/)

---

## 📝 License

This project was created for educational purposes as part of CSCI 250 coursework.

---

## 🙏 Acknowledgments

- Professor Gheni Abla for project guidance
- Google for the Gemini API (free tier!)
- The React and Flask communities for excellent documentation
