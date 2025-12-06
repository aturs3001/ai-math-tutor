# AI Math Tutor

**Student:** Aric Hurkman  
**Course:** CSCI 250  
**Final Project:** AI Math Tutor  
**Professor:** Gheni Abla  

---

## 📐 Project Overview

The AI Math Tutor is a web-based application that helps students learn mathematics through AI-powered step-by-step solutions, interactive study sessions, and practice quizzes. The application uses the Google Gemini API (FREE tier) with user-provided API keys for secure, personalized tutoring.

### Core Features

1. **User Authentication**: Simple email login or Google Sign-In support
2. **Personal API Keys**: Each user provides their own Gemini API key (stored locally)
3. **Problem Solver**: Input any math problem and receive detailed, step-by-step solutions
4. **📷 File Upload**: Upload images, PDFs, or Word documents containing math problems
5. **📚 Study Mode**: Interactive guided learning with progressive hints
6. **Practice Quizzes**: Generate AI-powered practice problems with immediate feedback
7. **Multiple Topics**: Support for algebra, geometry, calculus, trigonometry, statistics, and linear algebra
8. **Adaptive Difficulty**: Choose between easy, medium, hard, or mixed difficulty levels
9. **Math Symbol Palette**: Interactive palette for inserting mathematical symbols and LaTeX commands
10. **Live LaTeX Preview**: Real-time rendering of mathematical notation using KaTeX

---

## 🆕 Recent Updates

### v1.1.0 - LaTeX Rendering & JSON Parsing Fixes

**Fixed:**

- **Critical**: Resolved JSON parsing errors when Gemini API returns markdown-wrapped responses
- **Critical**: Fixed LaTeX rendering where `\frac` and `\sqrt` commands displayed incorrectly (e.g., "rac{1}{2}" now renders as proper fractions)
- Math expressions now render properly in step results, final answers, and quiz feedback
- Improved error handling with structured fallback responses

**Added:**

- `ensureMathDelimiters()` helper for automatic LaTeX detection and wrapping
- Enhanced backslash escape handling for LaTeX-in-JSON compatibility
- Trailing comma removal for malformed JSON responses
- LaTeX category in Math Symbol Palette with common commands

---

## 📚 Study Mode Feature

The AI Math Tutor includes an interactive Study Mode where students collaborate with the AI to solve problems step-by-step!

### How Study Mode Works

1. **Enter a Problem**: Type any math problem you want to learn
2. **AI Breaks It Down**: The AI analyzes your problem and creates 3-6 guided steps
3. **Work Through Steps**: Attempt each step yourself - this is where real learning happens!
4. **Get Progressive Hints**: If stuck, request up to 3 increasingly detailed hints per step
5. **Check Your Work**: Submit your answer and get instant, encouraging feedback
6. **View Solutions**: If needed, reveal the solution for any step
7. **Track Progress**: See your overall performance at the end

### Study Mode Benefits

- **Active Learning**: Don't just see solutions - discover them yourself
- **Progressive Hints**: From gentle reminders to strong guidance
- **Immediate Feedback**: Know right away if you're on track
- **Encouraging Tone**: AI provides supportive feedback even for wrong answers
- **Concept Reinforcement**: Each step reinforces mathematical concepts

---

## 🛠️ Technology Stack

### Backend

| Technology | Purpose |
|------------|---------|
| Python 3.8+ | Programming language |
| Flask | Web framework for REST API |
| Flask-CORS | Cross-origin resource sharing |
| Google Generative AI SDK | Gemini API integration (FREE!) |
| Pillow | Image processing for uploaded files |
| PyMuPDF | PDF text extraction and page conversion |
| python-docx | Word document text extraction |

### Frontend

| Technology | Purpose |
|------------|---------|
| HTML5/CSS3 | Structure and styling |
| React 18 | UI framework (loaded via CDN) |
| Tailwind CSS | Utility-first styling |
| KaTeX | Mathematical notation rendering |
| Google Identity Services | OAuth 2.0 authentication (optional) |
| Lucide Icons | Icon library |

---

## 📋 Requirements

Before running the application, ensure you have:

1. **Python 3.8 or higher** installed
2. **A Google Gemini API key** (FREE - get one at <https://aistudio.google.com/apikey>)
3. **A modern web browser** (Chrome, Firefox, Safari, or Edge)

---

## 🚀 Installation & Setup

### Step 1: Download the Project Files

Ensure you have all project files in a directory:

``` ai-math-tutor/
├── server.py           # Backend Flask server with all API endpoints
├── index.html          # Frontend React application
├── requirements.txt    # Python dependencies
├── .env                # Environment configuration (optional Google Client ID)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

### Step 2: Install Python Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 3: Start the Server

In the terminal, run:

```bash
python server.py
```

You should see output like:

```============================================================
AI Math Tutor - Backend Server
============================================================

  Open your browser and go to:

     http://localhost:5000

  Features:
     ✓  Google Sign-In authentication
     ✓  User-provided Gemini API keys
     ✓  Step-by-step math solutions
     ✓  Interactive practice quizzes
     ✓  STUDY MODE - Interactive guided learning
     ✓  FILE UPLOAD SUPPORT:
        - Images: png, jpg, jpeg, gif, webp, bmp
        - Documents: pdf, docx

============================================================
```

### Step 4: Open the Application

Open your web browser and go to:

``` http://localhost:5000
```

### Step 5: Sign In and Enter API Key

1. Enter your name and email (or use Google Sign-In if configured)
2. Get a FREE Gemini API key at: <https://aistudio.google.com/apikey>
3. Enter your API key when prompted
4. Start learning!

---

## 📖 How to Use

### Problem Solver Mode

1. Click the **"Solver"** tab
2. Choose input method:
   - **Type Problem**: Enter your math problem in the text box
   - **Upload File**: Drag & drop or browse for an image/PDF/DOCX
3. Use the **Math Symbols** palette to insert special characters (√, ∫, π, etc.)
4. Click **"Solve Problem"** or **"Analyze & Solve"**
5. View the step-by-step solution with LaTeX-rendered math

### Study Mode

1. Click the **"Study"** tab
2. Enter a math problem you want to learn (or upload a file)
3. Click **"Start Learning"**
4. Work through each step:
   - Read the objective for the current step
   - Enter your answer in the input field
   - Click **"Check Answer"** to verify
   - Use **"Need a Hint?"** if stuck (up to 3 hints per step)
5. Progress through all steps to complete the session
6. Review your performance summary

### Practice Quiz Mode

1. Click the **"Quiz"** tab
2. Select a math topic (Algebra, Geometry, Calculus, etc.)
3. Choose a difficulty level (Easy, Medium, Hard, Mixed)
4. Set the number of questions (1-10)
5. Click **"Start Quiz"**
6. Answer each question and submit
7. Receive immediate feedback and see your final score

---

## 🔧 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve frontend application |
| `/api/health` | GET | Health check and feature status |
| `/api/config` | GET | Frontend configuration |
| `/api/verify-key` | POST | Validate Gemini API key |
| `/api/solve` | POST | Solve a math problem (text input) |
| `/api/solve/file` | POST | Solve from uploaded file |

### Quiz Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/quiz/generate` | POST | Generate quiz questions |
| `/api/quiz/evaluate` | POST | Evaluate student answer |

### Study Mode Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/study/start` | POST | Start a study session |
| `/api/study/hint` | POST | Get a hint for current step |
| `/api/study/check` | POST | Check student's step answer |
| `/api/study/solution` | POST | Reveal solution for a step |

---

## 🔒 Security Notes

- **API keys are stored locally** in the browser's localStorage
- API keys are **never sent to our servers** - they go directly to Google's Gemini API
- **Uploaded files are processed in memory** and not stored on disk
- Maximum file size is **16 MB**
- For production deployment, use HTTPS and proper authentication

---

## 🐛 Troubleshooting

### "Failed to verify API key" error

- Make sure your Gemini API key is correct
- Get a free key at: <https://aistudio.google.com/apikey>
- Check that the key has no extra spaces

### LaTeX not rendering correctly

- Ensure math expressions are wrapped in `$...$` for inline or `$$...$$` for display
- Check browser console for KaTeX errors
- Try refreshing the page

### Study mode not working

- Ensure you have a stable internet connection
- Try with a simpler math problem first
- Check the browser console for error messages

### Quiz not generating

- Ensure you have a stable internet connection
- Try selecting a different topic or difficulty

### File upload errors

- Check that file is under 16 MB
- Supported formats: PNG, JPG, JPEG, GIF, WEBP, PDF, DOCX
- For PDFs, ensure text is selectable (not scanned images)

---

## 📁 Project Structure

```ai-math-tutor/
│
├── server.py              # Flask backend server
│   ├── API endpoints      # /api/solve, /api/quiz/*, /api/study/*
│   ├── File processing    # Image, PDF, and DOCX handling
│   ├── System prompts     # Instructions for Gemini AI
│   ├── JSON cleaning      # Markdown stripping, LaTeX escape handling
│   └── Error handling     # Comprehensive error responses
│
├── index.html             # Frontend React application
│   ├── Login screen       # Email or Google Sign-In
│   ├── Problem Solver     # Text input AND file upload modes
│   ├── Study Mode         # Interactive guided learning
│   ├── Quiz Mode          # Interactive practice quizzes
│   ├── Math Symbol Palette # Clickable math symbols & LaTeX
│   ├── MathText component # KaTeX rendering with DOM manipulation
│   └── Styling            # Tailwind CSS + custom styles
│
├── requirements.txt       # Python dependencies
├── .env                   # Environment configuration
├── .gitignore             # Git ignore rules
└── README.md              # Documentation (this file)
```

---

## 📚 References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [KaTeX Documentation](https://katex.org/docs/api.html)

---

## 📝 Version History

### v1.1.0 (Current)

- Fixed JSON parsing for markdown-wrapped Gemini responses
- Fixed LaTeX backslash escaping for proper rendering
- Added `ensureMathDelimiters()` for automatic LaTeX detection
- Added LaTeX category to Math Symbol Palette
- Improved error handling and fallback responses

### v1.0.0

- Initial release with Problem Solver, Study Mode, and Quiz Mode
- File upload support (images, PDFs, DOCX)
- Google OAuth and email authentication
- KaTeX mathematical notation rendering
- Math Symbol Palette with 8 categories

---

## 📄 License

This project was created for educational purposes as part of CSCI 250 coursework at California State University San Marcos.

---

## 🙏 Acknowledgments

- Professor Gheni Abla for project guidance and requirements
- Google for the Gemini API (free tier) with vision capabilities
- The React, Flask, and KaTeX communities for excellent documentation
- Khan Academy for inspiration on math education approaches
