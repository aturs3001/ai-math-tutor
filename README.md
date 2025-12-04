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
4. **Practice Quizzes**: Generate AI-powered practice problems with immediate feedback
5. **Multiple Topics**: Support for algebra, geometry, calculus, trigonometry, statistics, and linear algebra
6. **Adaptive Difficulty**: Choose between easy, medium, hard, or mixed difficulty levels

---

## 🛠️ Technology Stack

### Backend

- **Python 3.8+**: Programming language
- **Flask**: Web framework for REST API
- **Flask-CORS**: Cross-origin resource sharing
- **Google Generative AI SDK**: Gemini API integration (FREE!)

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

---

## 🚀 Installation & Setup

### Step 1: Download the Project Files

Ensure you have all project files in a directory:

```ai-math-tutor/
├── server.py           # Backend Flask server
├── index.html          # Frontend React application
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

============================================================
```

### Step 4: Open the Application

Open your web browser and go to:

```http://localhost:5000
```

### Step 5: Sign In and Enter API Key

1. Enter your name and email (or use Google Sign-In if configured)
2. Get a FREE Gemini API key at: <https://aistudio.google.com/apikey>
3. Enter your API key when prompted
4. Start learning!

---

## 🔐 Authentication Options

### Option 1: Simple Email Login (Always Available)

The application always allows users to sign in with their name and email. No external configuration required.

### Option 2: Google Sign-In (Pre-configured)

Google OAuth Sign-In is already configured in the `.env` file. Users can click "Sign in with Google" or use the email form.

To use a different Google Client ID:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth credentials for a Web application
3. Add `http://localhost:5000` to **Authorized JavaScript origins**
4. Update the `GOOGLE_CLIENT_ID` in `.env`

To disable Google Sign-In:

- Remove or comment out the `GOOGLE_CLIENT_ID` line in `.env`

---

## 📖 How to Use

### Problem Solver Mode

1. Click the "Problem Solver" tab (selected by default)
2. Enter your math problem in the text area
   - Example: "Solve for x: 2x + 5 = 13"
   - Example: "Find the derivative of x³ + 2x² - 5x + 3"
3. Click "Solve Problem" or press Enter
4. View the step-by-step solution with explanations

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

### Health

```GET /api/health
```

Returns server status.

### Verify API Key

```POST /api/verify-key
Headers: X-API-Key: your-gemini-api-key
```

Validates a Gemini API key.

### Solve Problem

```POST /api/solve
Headers: X-API-Key: your-gemini-api-key
Content-Type: application/json

{
    "problem": "Solve for x: 2x + 5 = 13"
}
```

Returns step-by-step solution.

### Generate Quiz

```POST /api/quiz/generate
Headers: X-API-Key: your-gemini-api-key
Content-Type: application/json

{
    "topic": "algebra",
    "num_questions": 3,
    "difficulty": "medium"
}
```

Returns generated quiz questions.

### Evaluate Answer

```POST /api/quiz/evaluate
Headers: X-API-Key: your-gemini-api-key
Content-Type: application/json

{
    "question": "What is 2 + 2?",
    "correct_answer": "4",
    "student_answer": "4"
}
```

Returns evaluation feedback.

---

## 🔒 Security Notes

- **API keys are stored locally** in the browser's localStorage
- API keys are **never sent to our servers** - they go directly to Google's Gemini API
- For production, use HTTPS and proper authentication
- Consider rate limiting for public deployments

---

## 🐛 Troubleshooting

### "Failed to verify API key" error

- Make sure your Gemini API key is correct
- Get a free key at: <https://aistudio.google.com/apikey>
- Check that the key has no extra spaces

### "Failed to fetch" or network errors

- Make sure the backend server is running on port 5000
- Check your internet connection

### "API Error: 429"

- You've hit the rate limit (60 requests/minute on free tier)
- Wait a minute and try again

### Quiz not generating

- Ensure you have a stable internet connection
- Check the browser console for error messages

---

## 📁 Project Structure

```ai-math-tutor/
│
├── server.py              # Flask backend server
│   ├── API endpoints      # /api/solve, /api/quiz/generate, /api/quiz/evaluate, /api/config
│   ├── System prompts     # Instructions for Gemini AI
│   └── Error handling     # Comprehensive error responses
│
├── index.html             # Frontend React application
│   ├── Login screen       # Email or Google Sign-In
│   ├── Problem Solver     # Math problem input and solutions
│   ├── Quiz Mode          # Interactive practice quizzes
│   └── Styling            # Tailwind CSS + custom styles
│
├── .env                   # Environment configuration
│   └── GOOGLE_CLIENT_ID   # Google OAuth Client ID
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
- [Google Identity Services](https://developers.google.com/identity)

---

## 📝 License

This project was created for educational purposes as part of CSCI 250 coursework.

---

## 🙏 Acknowledgments

- Professor Gheni Abla for project guidance
- Google for the Gemini API (free tier)
- The React and Flask communities for excellent documentation
