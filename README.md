# AI Math Tutor

**Student:** Aric Hurkman  
**Course:** CSCI 250  
**Final Project:** AI Math Tutor  
**Professor:** Gheni Abla  

---

## 📐 Project Overview

The AI Math Tutor is a web-based application that helps students learn mathematics through AI-powered step-by-step solutions, interactive study sessions, and practice quizzes. The application uses the Google Gemini API (FREE tier) with user-provided API keys for secure, personalized tutoring.

### Features

1. **User Authentication**: Simple email login or Google Sign-In support
2. **Personal API Keys**: Each user provides their own Gemini API key (stored locally)
3. **Problem Solver**: Input any math problem and receive detailed, step-by-step solutions
4. **📷 File Upload**: Upload images, PDFs, or Word documents containing math problems
5. **📚 Study Mode**: Interactive guided learning with progressive hints
6. **Practice Quizzes**: Generate AI-powered practice problems with immediate feedback
7. **Multiple Topics**: Support for algebra, geometry, calculus, trigonometry, statistics, and linear algebra
8. **Adaptive Difficulty**: Choose between easy, medium, hard, or mixed difficulty levels

---

## 🆕 Study Mode Feature

The AI Math Tutor now includes an interactive Study Mode where students collaborate with the AI to solve problems step-by-step!

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
2. **A Google Gemini API key** (FREE - get one at https://aistudio.google.com/apikey)
3. **A modern web browser** (Chrome, Firefox, Safari, or Edge)

---

## 🚀 Installation & Setup

### Step 1: Download the Project Files

Ensure you have all project files in a directory:

```
ai-math-tutor/
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
     ✓  STUDY MODE - Interactive guided learning
     ✓  FILE UPLOAD SUPPORT:
        - Images: png, jpg, jpeg, gif, webp, bmp
        - Documents: pdf, docx

============================================================
```

### Step 4: Open the Application

Open your web browser and go to:

```
http://localhost:5000
```

### Step 5: Sign In and Enter API Key

1. Enter your name and email (or use Google Sign-In if configured)
2. Get a FREE Gemini API key at: https://aistudio.google.com/apikey
3. Enter your API key when prompted
4. Start learning!

---

## 📖 How to Use

### Problem Solver Mode

1. Click the "Solver" tab
2. Enter your math problem or upload a file containing a problem
3. Click "Solve Problem"
4. View the step-by-step solution

### Study Mode (NEW!)

1. Click the "Study" tab
2. Enter a math problem you want to learn
3. Click "Start Studying"
4. Work through each step:
   - Read the objective for the current step
   - Enter your answer in the input field
   - Click "Check Answer" to verify
   - Use "Get Hint" if stuck (up to 3 hints per step)
   - Click "Show Solution" if you need to see the answer
5. Progress through all steps to complete the session
6. Review your performance summary

### Practice Quiz Mode

1. Click the "Quiz" tab
2. Select a math topic
3. Choose a difficulty level
4. Set the number of questions
5. Click "Start Quiz"
6. Answer each question and submit
7. Receive immediate feedback and see your score

---

## 🔧 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check and feature status |
| `/api/config` | GET | Frontend configuration |
| `/api/verify-key` | POST | Validate Gemini API key |
| `/api/solve` | POST | Solve a math problem |
| `/api/solve/file` | POST | Solve from uploaded file |

### Quiz Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/quiz/generate` | POST | Generate quiz questions |
| `/api/quiz/evaluate` | POST | Evaluate student answer |

### Study Mode Endpoints (NEW!)

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
- For production, use HTTPS and proper authentication

---

## 🐛 Troubleshooting

### "Failed to verify API key" error
- Make sure your Gemini API key is correct
- Get a free key at: https://aistudio.google.com/apikey
- Check that the key has no extra spaces

### Study mode not working
- Ensure you have a stable internet connection
- Try with a simpler math problem first
- Check the browser console for error messages

### Quiz not generating
- Ensure you have a stable internet connection
- Try selecting a different topic or difficulty

---

## 📁 Project Structure

```
ai-math-tutor/
│
├── server.py              # Flask backend server
│   ├── API endpoints      # /api/solve, /api/quiz/*, /api/study/*
│   ├── File processing    # Image, PDF, and DOCX handling
│   ├── System prompts     # Instructions for Gemini AI
│   └── Error handling     # Comprehensive error responses
│
├── index.html             # Frontend React application
│   ├── Login screen       # Email or Google Sign-In
│   ├── Problem Solver     # Text input AND file upload modes
│   ├── Study Mode         # Interactive guided learning (NEW!)
│   ├── Quiz Mode          # Interactive practice quizzes
│   └── Styling            # Tailwind CSS + custom styles
│
├── .env                   # Environment configuration
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # Documentation (this file)
```

---

## 📚 References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

---

## 📝 License

This project was created for educational purposes as part of CSCI 250 coursework.

---

## 🙏 Acknowledgments

- Professor Gheni Abla for project guidance
- Google for the Gemini API (free tier) with vision capabilities
- The React and Flask communities for excellent documentation