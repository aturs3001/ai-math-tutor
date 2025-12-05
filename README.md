# AI Math Tutor

**Student:** Aric Hurkman  
**Course:** CSCI 250  
**Final Project:** AI Math Tutor  
**Professor:** Gheni Abla  

---

## 📐 Project Overview

The AI Math Tutor is a web-based application that helps students learn mathematics through AI-powered step-by-step solutions and interactive quizzes. The application uses the Google Gemini API (FREE tier) with user-provided API keys for secure, personalized tutoring.

### Features

1. **User Authentication**: Simple email login or Google Sign-In support
2. **Personal API Keys**: Each user provides their own Gemini API key (stored locally)
3. **Problem Solver**: Input any math problem and receive detailed, step-by-step solutions
4. **📷 FILE UPLOAD**: Upload images, PDFs, or Word documents containing math problems
5. **Practice Quizzes**: Generate AI-powered practice problems with immediate feedback
6. **Multiple Topics**: Support for algebra, geometry, calculus, trigonometry, statistics, and linear algebra
7. **Adaptive Difficulty**: Choose between easy, medium, hard, or mixed difficulty levels

---

## 🆕 File Upload Feature

The AI Math Tutor now supports solving math problems from uploaded files! Simply upload an image of your homework, a PDF worksheet, or a Word document, and the AI will analyze and solve the problems.

### Supported File Types

| Type | Extensions | Description |
|------|-----------|-------------|
| **Images** | .png, .jpg, .jpeg, .gif, .webp, .bmp | Photos of handwritten or printed math problems |
| **PDF** | .pdf | PDF documents, worksheets, or scanned homework |
| **Word** | .docx | Microsoft Word documents with math problems |

### How It Works

1. Click the "Upload File" tab in the Problem Solver
2. Drag and drop your file or click to browse
3. (Optional) Add additional context about the problem
4. Click "Analyze & Solve"
5. The AI will detect the math problem and provide a step-by-step solution

### Tips for Best Results

- **Clear Images**: Ensure math problems are clearly visible and well-lit
- **Single Problem**: Focus on one problem per file for best results
- **Legible Text**: For handwritten problems, write clearly
- **PDF Quality**: Use high-resolution PDFs for better text extraction
- **Maximum Size**: Files must be under 16 MB

---

## 🛠️ Technology Stack

### Backend

- **Python 3.8+**: Programming language
- **Flask**: Web framework for REST API
- **Flask-CORS**: Cross-origin resource sharing
- **Google Generative AI SDK**: Gemini API integration (FREE!)
- **Pillow**: Image processing for uploaded files
- **PyMuPDF**: PDF text extraction and page conversion
- **python-docx**: Word document text extraction

### Frontend

- **HTML5/CSS3**: Structure and styling
- **React 18**: UI framework (loaded via CDN)
- **Tailwind CSS**: Utility-first styling
- **Google Identity Services**: OAuth 2.0 authentication (optional)
- **Lucide Icons**: Icon library

---

## 📋 Requirements

Before running the application, ensure you have:

1. **Python 3.8 or higher** installed
2. **A Google Gemini API key** (FREE - get one at <https://aistudio.google.com/apikey>)
3. **A modern web browser** (Chrome, Firefox, Safari, or Edge)

### System Dependencies (for PDF processing)

```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler

# Windows
# Download from: https://github.com/oschwartz10612/poppler-windows
```

---

## 🚀 Installation & Setup

### Step 1: Download the Project Files

Ensure you have all project files in a directory:

```
ai-math-tutor/
├── server.py           # Backend Flask server with file upload support
├── index.html          # Frontend React application with file upload UI
├── requirements.txt    # Python dependencies
├── .env                # Environment configuration (Google Client ID)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

### Step 2: Install Python Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 3: Install System Dependencies (Optional, for PDF support)

```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler
```

### Step 4: Start the Server

In the terminal, run:

```bash
python server.py
```

You should see output like:

```
============================================================
AI Math Tutor - Backend Server
============================================================

  Open your browser and go to:

     http://localhost:5000

  Features:
     ✓  Google Sign-In authentication
     ✓  User-provided Gemini API keys
     ✓  Step-by-step math solutions
     ✓  Interactive practice quizzes
     ✓  FILE UPLOAD SUPPORT:
        - Images: png, jpg, jpeg, gif, webp, bmp
        - Documents: pdf, docx, doc

============================================================
```

### Step 5: Open the Application

Open your web browser and go to:

```
http://localhost:5000
```

### Step 6: Sign In and Enter API Key

1. Enter your name and email (or use Google Sign-In if configured)
2. Get a FREE Gemini API key at: <https://aistudio.google.com/apikey>
3. Enter your API key when prompted
4. Start learning!

---

## 📖 How to Use

### Problem Solver Mode

#### Text Input
1. Click the "Problem Solver" tab (selected by default)
2. Select "Type Problem" mode
3. Enter your math problem in the text area
4. Click "Solve Problem" or press Enter
5. View the step-by-step solution

#### File Upload
1. Click the "Problem Solver" tab
2. Select "Upload File" mode
3. Drag and drop your file or click to browse
4. Supported formats: PNG, JPG, JPEG, GIF, WEBP, BMP, PDF, DOCX
5. (Optional) Add context about the specific problem
6. Click "Analyze & Solve"
7. View the detected problem and step-by-step solution

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

### Health Check
```
GET /api/health
```
Returns server status and supported file types.

### Configuration
```
GET /api/config
```
Returns frontend configuration including supported file types.

### Verify API Key
```
POST /api/verify-key
Headers: X-API-Key: your-gemini-api-key
```
Validates a Gemini API key.

### Solve Problem (Text)
```
POST /api/solve
Headers: X-API-Key: your-gemini-api-key
Content-Type: application/json

{
    "problem": "Solve for x: 2x + 5 = 13"
}
```

### Solve Problem (File Upload) 🆕
```
POST /api/solve/file
Headers: X-API-Key: your-gemini-api-key
Content-Type: multipart/form-data

Form Data:
  - file: (binary file data)
  - additional_context: (optional string)
```

Supported file types:
- Images: png, jpg, jpeg, gif, webp, bmp
- Documents: pdf, docx

### Generate Quiz
```
POST /api/quiz/generate
Headers: X-API-Key: your-gemini-api-key
Content-Type: application/json

{
    "topic": "algebra",
    "num_questions": 3,
    "difficulty": "medium"
}
```

### Evaluate Answer
```
POST /api/quiz/evaluate
Headers: X-API-Key: your-gemini-api-key
Content-Type: application/json

{
    "question": "What is 2 + 2?",
    "correct_answer": "4",
    "student_answer": "4"
}
```

---

## 🔒 Security Notes

- **API keys are stored locally** in the browser's localStorage
- API keys are **never sent to our servers** - they go directly to Google's Gemini API
- **Uploaded files are processed in memory** and not stored on disk
- Maximum file size is **16 MB**
- For production, use HTTPS and proper authentication

---

## 🐛 Troubleshooting

### "Failed to verify API key" error
- Make sure your Gemini API key is correct
- Get a free key at: <https://aistudio.google.com/apikey>
- Check that the key has no extra spaces

### "Failed to solve problem from file" error
- Ensure the file is a supported format (PNG, JPG, PDF, DOCX)
- Check that the file is under 16 MB
- Make sure the math problem is clearly visible in the image/document

### "PDF processing libraries not available" warning
- Install PyMuPDF: `pip install PyMuPDF`
- Or install poppler-utils for pdf2image fallback

### "DOCX processing library not available" warning
- Install python-docx: `pip install python-docx`

### Quiz not generating
- Ensure you have a stable internet connection
- Check the browser console for error messages

---

## 📁 Project Structure

```
ai-math-tutor/
│
├── server.py              # Flask backend server
│   ├── API endpoints      # /api/solve, /api/solve/file, /api/quiz/*
│   ├── File processing    # Image, PDF, and DOCX handling
│   ├── System prompts     # Instructions for Gemini AI
│   └── Error handling     # Comprehensive error responses
│
├── index.html             # Frontend React application
│   ├── Login screen       # Email or Google Sign-In
│   ├── Problem Solver     # Text input AND file upload modes
│   ├── FileUploadZone     # Drag-and-drop file upload component
│   ├── Quiz Mode          # Interactive practice quizzes
│   └── Styling            # Tailwind CSS + custom styles
│
├── .env                   # Environment configuration
│   └── GOOGLE_CLIENT_ID   # Google OAuth Client ID (optional)
│
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
│
└── README.md             # Documentation (this file)
```

---

## 📚 References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [python-docx Documentation](https://python-docx.readthedocs.io/)

---

## 📝 License

This project was created for educational purposes as part of CSCI 250 coursework.

---

## 🙏 Acknowledgments

- Professor Gheni Abla for project guidance
- Google for the Gemini API (free tier) with vision capabilities
- The React and Flask communities for excellent documentation
