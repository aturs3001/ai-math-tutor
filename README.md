# AI Math Tutor

**Student:** Aric Hurkman  
**Course:** CSCI 250  
**Final Project:** AI Math Tutor  
**Professor:** Gheni Abla  

---

## 📐 Project Overview

The AI Math Tutor is a web-based application that helps students learn mathematics through AI-powered step-by-step solutions, interactive study sessions, and practice quizzes. The application uses the Google Gemini API (FREE tier) with user-provided API keys for secure, personalized tutoring.

### Core Features

1. **User Authentication**: Google Sign-In or simple email login
2. **Personal API Keys**: Each user provides their own Gemini API key (stored locally)
3. **Problem Solver**: Input any math problem and receive detailed, step-by-step solutions
4. **📚 Study Mode**: Interactive guided learning with progressive hints
5. **Practice Quizzes**: Generate AI-powered practice problems with immediate feedback
6. **Multiple Topics**: Support for algebra, geometry, calculus, trigonometry, statistics, and linear algebra
7. **Adaptive Difficulty**: Choose between easy, medium, hard, or mixed difficulty levels
8. **Math Symbol Palette**: Interactive palette for inserting mathematical symbols and LaTeX commands
9. **Live LaTeX Preview**: Real-time rendering of mathematical notation using KaTeX

---

## 🎯 Key Features

### Problem Solver Mode

- Type any math problem directly into the text area
- Use LaTeX notation for formatted equations (e.g., `$x^2$` or `$\frac{1}{2}$`)
- Interactive math symbol palette with 9 categories (Basic, Algebra, Calculus, Trig, Greek, etc.)
- Live preview shows your math formatted in real-time
- Receive step-by-step solutions with detailed explanations
- All mathematical expressions rendered beautifully with KaTeX

### Study Mode

The AI Math Tutor includes an interactive Study Mode where students collaborate with the AI to solve problems step-by-step!

**How Study Mode Works:**

1. **Enter a Problem**: Type any math problem you want to learn
2. **AI Breaks It Down**: The AI analyzes your problem and creates 3-6 guided steps
3. **Work Through Steps**: Attempt each step yourself - this is where real learning happens!
4. **Get Progressive Hints**: If stuck, request up to 3 increasingly detailed hints per step
5. **Check Your Work**: Submit your answer and get instant, encouraging feedback
6. **Track Progress**: See your overall performance at the end

**Study Mode Benefits:**

- **Active Learning**: Don't just see solutions - discover them yourself
- **Progressive Hints**: From gentle reminders to strong guidance
- **Immediate Feedback**: Know right away if you're on track
- **Encouraging Tone**: AI provides supportive feedback even for wrong answers
- **Concept Reinforcement**: Each step reinforces mathematical concepts

### Quiz Mode

- Generate AI-powered practice problems on any topic
- Choose difficulty level (Easy, Medium, Hard, Mixed)
- Select number of questions (1-10)
- Receive immediate feedback on your answers
- Track your score and performance
- Review correct answers with explanations

---

## 🛠️ Technology Stack

### Backend

| Technology | Purpose |
|------------|---------|
| Python 3.8+ | Programming language |
| Flask | Web framework for REST API |
| Flask-CORS | Cross-origin resource sharing |
| Google Generative AI SDK | Gemini API integration (FREE!) |

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

### Step 3: Configure Environment (Optional)

Create a `.env` file for optional Google OAuth:

```bash
# Optional: Google OAuth (for Google Sign-In button)
GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com

# If you don't want Google Sign-In, just leave this file empty or don't create it
```

**Note:** Google OAuth is optional. The app works perfectly with email/name login alone.

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

  Powered by Google Gemini (Users provide their own API key)

  Open your browser and go to:

     http://localhost:5000

  Features:
     ✓  Google Sign-In authentication
     ✓  User-provided Gemini API keys
     ✓  Step-by-step math solutions
     ✓  Interactive practice quizzes
     ✓  STUDY MODE - Interactive guided learning

============================================================
```

### Step 5: Open the Application

Open your web browser and go to:

```
http://localhost:5000
```

### Step 6: Sign In and Enter API Key

1. Sign in using Google Sign-In or enter your name and email
2. Get a FREE Gemini API key at: <https://aistudio.google.com/apikey>
3. Enter your API key when prompted
4. Start learning!

---

## 📖 How to Use

### Problem Solver Mode

1. Click the **"Solver"** tab
2. Enter your math problem in the text box
3. Use the **Math Symbols** palette to insert special characters (√, ∫, π, etc.)
4. Toggle **Live Preview** to see your math rendered in real-time
5. Click **"Solve Problem"**
6. View the step-by-step solution with LaTeX-rendered math

**Example Problems:**

- `Solve for x: 2x + 5 = 13`
- `Find the derivative of f(x) = x³ + 2x² - 5x + 3`
- `Calculate the area of a triangle with base 8 and height 12`
- `Simplify: (3x² + 2x - 1) + (x² - 4x + 5)`

**LaTeX Notation Examples:**

- Fractions: `$\frac{1}{2}$` displays as ½
- Square roots: `$\sqrt{x}$` displays as √x
- Exponents: `$x^2$` displays as x²
- Integrals: `$\int x dx$` displays as ∫x dx

### Study Mode

1. Click the **"Study"** tab
2. Enter a math problem you want to learn
3. Click **"Start Learning"**
4. Work through each step:
   - Read the objective for the current step
   - Enter your answer in the input field (with live LaTeX preview!)
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

---

## 🎨 Using LaTeX Notation

The AI Math Tutor supports LaTeX notation for beautiful mathematical formatting:

### Inline Math

Wrap expressions in single dollar signs: `$x^2 + 5$`

### Display Math

Wrap expressions in double dollar signs for centered display: `$$\int_0^1 x^2 dx$$`

### Common LaTeX Commands

| Symbol | LaTeX | Display |
|--------|-------|---------|
| Fraction | `$\frac{a}{b}$` | a/b |
| Square Root | `$\sqrt{x}$` | √x |
| Exponent | `$x^2$` | x² |
| Subscript | `$x_1$` | x₁ |
| Sum | `$\sum_{i=1}^{n}$` | Σ |
| Integral | `$\int_a^b$` | ∫ |
| Limit | `$\lim_{x \to 0}$` | lim |
| Greek Letters | `$\alpha, \beta, \gamma$` | α, β, γ |

---

## 🔒 Security Notes

- **API keys are stored locally** in the browser's localStorage
- API keys are **never sent to our servers** - they go directly to Google's Gemini API
- **No file uploads** - avoiding rate limit issues with free tier API keys
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

### Rate limit errors (429)

If you see "Rate limit exceeded" errors:

- Wait 60 seconds before trying again
- Get a fresh API key from <https://aistudio.google.com/apikey>
- Use the Settings (⚙️) button to update your API key
- Avoid making too many requests in quick succession

### Google OAuth not working

If Google Sign-In shows errors:

- Just use email/name login instead (works perfectly!)
- Or follow setup guide in Google Cloud Console
- Or remove `GOOGLE_CLIENT_ID` from `.env` to hide the Google button

---

## Demo Video
<https://youtu.be/o1BO2XXgcSM>
---
## 📁 Project Structure

```
ai-math-tutor/
│
├── server.py              # Flask backend server
│   ├── API endpoints      # /api/solve, /api/quiz/*, /api/study/*
│   ├── System prompts     # Instructions for Gemini AI
│   ├── JSON cleaning      # Response parsing and validation
│   └── Error handling     # Comprehensive error responses
│
├── index.html             # Frontend React application
│   ├── Login screen       # Google Sign-In or email authentication
│   ├── Problem Solver     # Text input with LaTeX support
│   ├── Study Mode         # Interactive guided learning
│   ├── Quiz Mode          # Practice problems with scoring
│   ├── Math Symbol Palette # Clickable math symbols & LaTeX
│   ├── MathText component # KaTeX rendering
│   ├── Settings Modal     # Update API key without logout
│   └── Styling            # Tailwind CSS + custom styles
│
├── requirements.txt       # Python dependencies
├── .env                   # Environment configuration (optional)
├── .gitignore             # Git ignore rules
└── README.md              # Documentation (this file)
```

---

## 🎓 For Students and Educators

This project demonstrates:

- **LLM Integration**: Working with Google's Gemini API
- **Web Development**: Full-stack application with Flask and React
- **User Authentication**: Multiple authentication methods
- **API Design**: RESTful endpoints with proper error handling
- **Frontend Skills**: Modern React with hooks and component design
- **Mathematical Notation**: LaTeX rendering with KaTeX
- **Educational Technology**: Interactive learning features

---

## 📚 References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [KaTeX Documentation](https://katex.org/docs/api.html)
- [LaTeX Math Symbols](https://www.overleaf.com/learn/latex/List_of_Greek_letters_and_math_symbols)

---

## 📝 Version History

### v1.2.0 (Current)

- Removed file upload feature (optimized for free tier API usage)
- Enhanced LaTeX support with live preview
- Improved math symbol palette
- Fixed Google OAuth integration
- Added settings modal for API key management
- Optimized for stable, reliable demos

### v1.1.0

- Fixed JSON parsing for markdown-wrapped Gemini responses
- Fixed LaTeX backslash escaping for proper rendering
- Added LaTeX category to Math Symbol Palette
- Improved error handling and fallback responses

### v1.0.0

- Initial release with Problem Solver, Study Mode, and Quiz Mode
- Google OAuth and email authentication
- KaTeX mathematical notation rendering
- Math Symbol Palette with 8 categories

---

## 📄 License

This project was created for educational purposes as part of CSCI 250 coursework at California State University San Marcos.

---

## 🙏 Acknowledgments

- Professor Gheni Abla for project guidance and requirements
- Google for the Gemini API (free tier)
- The React, Flask, and KaTeX communities for excellent documentation
- Khan Academy for inspiration on math education approaches

---

## 💡 Future Enhancements (If Expanding Beyond Free Tier)

With a paid Gemini API key, you could add:

- File upload support (images, PDFs, Word documents)
- Handwriting recognition
- Graph plotting and visualization
- Multi-page document processing
- Batch problem solving

For this academic project, the text-based approach provides a solid, reliable foundation that works perfectly with the free API tier.

---

## ✅ Ready to Present

Your AI Math Tutor is complete and ready for demonstration:

- ✓ Clean, professional interface
- ✓ Multiple learning modes
- ✓ Reliable performance with free tier
- ✓ Full LaTeX support
- ✓ Interactive features
- ✓ Comprehensive error handling

Good luck with your presentation! 🚀
