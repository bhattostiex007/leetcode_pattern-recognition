# CODEPATH — Algorithm Pattern Detector

> **Paste a LeetCode problem. Instantly know how to solve it.**

CODEPATH is an AI-powered web application that analyzes algorithm problem descriptions and identifies the underlying algorithmic pattern, predicts time and space complexity, and provides ready-to-use code templates in C++, Python, and Java — all in seconds.

🔗 **Live App:** [Open CODEPATH on Streamlit](https://leetcodepattern-recognition-gtdciwsijnncse2eegz3kf.streamlit.app/)

---

## What It Does

You paste a problem statement (or pick from built-in examples), click **Detect Pattern**, and the app:

- **Identifies the algorithmic pattern(s)** — up to 3 best-matching patterns ranked by relevance
- **Predicts Big-O Complexity** — both time and space complexity
- **Generates code templates** — syntax-highlighted, language-specific boilerplate in C++, Python, or Java
- **Provides an interactive code editor** — edit and practice directly in the browser (no setup needed)
- **Tracks your session history** — every search is saved so you can reload past problems instantly

---

## Patterns Covered

| Pattern | Pattern | Pattern |
|---|---|---|
| Two Pointers | Sliding Window | Binary Search |
| BFS | DFS | Dynamic Programming |
| Backtracking | Heap / Priority Queue | Hash Map |
| Greedy | Stack | Trie |
| Prefix Sum | Fast & Slow Pointers | Topological Sort |

---

## Features

### 🧠 AI Pattern Detection
Powered by **Llama 3.1** (via Groq API), the AI reads the problem description and returns a structured JSON response classifying it into the most relevant patterns with complexity analysis.

### ⏱️ Big-O Complexity Predictor
Alongside each detected pattern, the app predicts:
- **Time Complexity** (e.g., `O(N log N)`)
- **Space Complexity** (e.g., `O(N)`)

### 💻 Interactive Code Editor
Instead of just showing static code, CODEPATH embeds a fully interactive **Ace Code Editor** with:
- Syntax highlighting for C++, Python, and Java
- Dark `twilight` theme matching the app's aesthetic
- Tab support and standard editor shortcuts

### 📂 Session History Tracker
Every successful detection is automatically saved in the "Watch Your History" expander panel. Each entry shows:
- A preview of the problem
- Detected pattern tags
- Time & Space complexity
- A "↩ Reload Problem" button to instantly bring it back

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Python · Streamlit · streamlit-ace |
| **Backend** | Python · Flask · Flask-CORS |
| **AI Engine** | Groq API · Llama 3.1 (8B) |
| **Deployment** | Streamlit Community Cloud (frontend) · Render (backend) |

---

## Project Structure

```
leetcode-pattern-detector/
│
├── frontend/
│   └── app.py              # Streamlit UI — all pages, components & styling
│
├── backend/
│   ├── app.py              # Flask API — /detect and /health routes
│   ├── templates.py        # 15 pattern definitions with code templates
│   ├── requirements.txt    # Backend dependencies
│   └── Procfile            # Render deployment config
│
├── .env.template           # Template for environment variables
└── .gitignore
```

---

## Running Locally

### Prerequisites
- Python 3.10+
- A [Groq API key](https://console.groq.com) (free)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/bhattostiex007/leetcode_pattern-recognition.git
cd leetcode_pattern-recognition

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r backend/requirements.txt
pip install streamlit streamlit-ace

# 4. Set up your API key
# Copy .env.template to backend/.env and paste your Groq API key
GROQ_API_KEY=your_key_here

# 5. Start the backend (in one terminal)
python backend/app.py

# 6. Start the frontend (in another terminal)
streamlit run frontend/app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Deployment

The app is split into two separately deployed services:

| Service | Platform | Config |
|---|---|---|
| **Frontend** (Streamlit) | Streamlit Community Cloud | Set `BACKEND_URL` env variable to the Render URL |
| **Backend** (Flask) | Render | Set `GROQ_API_KEY` env variable · uses `Procfile` |

---

## Example Problems You Can Try

- *Given an m × n binary grid, return the number of islands.* → **DFS**
- *Find the length of the longest substring without repeating characters.* → **Sliding Window**
- *Determine if you can finish all courses given prerequisites.* → **Topological Sort**
- *Return the maximum width of a binary tree.* → **BFS**
- *Given an array and target, return indices of the two numbers that add up to target.* → **Hash Map**

---

## License

This project is open-source and available under the [MIT License](LICENSE).
