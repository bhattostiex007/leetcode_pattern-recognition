import os
import json
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from templates import TEMPLATES, PATTERN_NAMES
from groq import Groq

load_dotenv()

app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────────────────────────────────────────────
# Model: llama-3.3-70b-versatile on Groq
# Why: 70B parameters vs 8B → far better instruction following & reasoning.
#      Same Groq API key, no extra setup needed.
# Prompt strategy: system/user split
#   • system = static expert persona + disambiguation rules + few-shot examples
#   • user   = the problem text only
# This way the model "knows the rules" before seeing the problem.
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a world-class competitive programming coach and algorithm expert.
Your ONLY job is to classify a LeetCode problem into 1, 2, or 3 algorithm patterns from a fixed list.

═══ CRITICAL DISAMBIGUATION RULES (follow exactly) ═══

1. LINKED LIST + CYCLE → always "Fast & Slow Pointers". NEVER "Two Pointers".
   "Two Pointers" is ONLY for sorted arrays or strings.

2. BINARY TREE LEVEL / WIDTH / MIN DISTANCE → always "BFS".
   Never classify tree-level problems as "Dynamic Programming".

3. "TWO SUM" (find indices that add up to target) → always "Hash Map".
   "Two Sum II" (sorted array) → "Two Pointers".

4. COIN CHANGE / CLIMBING STAIRS / MIN COINS → always "Dynamic Programming".
   These are NOT greedy (greedy fails for coin change in general).

5. PREREQUISITES / COURSE SCHEDULE / BUILD ORDER → always "Topological Sort".

6. SUBARRAY SUM EQUALS K (count subarrays) → "Prefix Sum" + optionally "Hash Map".
   NOT "Sliding Window" (sliding window doesn't work for negative numbers).

7. LONGEST SUBSTRING WITHOUT REPEATING → always "Sliding Window".
   NEVER "Two Pointers" alone.

═══ FEW-SHOT EXAMPLES ═══

Problem: "Given head of a linked list, determine if it has a cycle."
→ {"patterns": ["Fast & Slow Pointers"], "time_complexity": "O(N)", "space_complexity": "O(1)"}

Problem: "Given a sorted array and a target, return indices of two numbers that add up to target."
→ {"patterns": ["Two Pointers"], "time_complexity": "O(N)", "space_complexity": "O(1)"}

Problem: "Given an array nums and integer target, return indices of the two numbers that add up to target."
→ {"patterns": ["Hash Map"], "time_complexity": "O(N)", "space_complexity": "O(N)"}

Problem: "Return the maximum width of a binary tree."
→ {"patterns": ["BFS"], "time_complexity": "O(N)", "space_complexity": "O(N)"}

Problem: "Find minimum number of coins to make amount."
→ {"patterns": ["Dynamic Programming"], "time_complexity": "O(N*amount)", "space_complexity": "O(amount)"}

Problem: "Given prerequisites, determine if you can finish all courses."
→ {"patterns": ["Topological Sort", "BFS"], "time_complexity": "O(V+E)", "space_complexity": "O(V+E)"}

Problem: "Find total number of subarrays whose sum equals k."
→ {"patterns": ["Prefix Sum", "Hash Map"], "time_complexity": "O(N)", "space_complexity": "O(N)"}

═══ OUTPUT FORMAT (strict JSON, no extra text) ═══
{
  "patterns": ["Pattern Name 1"],
  "time_complexity": "O(...)",
  "space_complexity": "O(...)"
}
Pattern names MUST be exact matches from the provided list. Maximum 3 patterns."""


def detect_patterns_with_llm(problem_text: str):
    """Detect algorithm patterns using llama-3.3-70b-versatile on Groq."""
    
    # Build the pattern reference list for the user message
    pattern_context = {
        name: {
            "description": info["description"],
            "use_cases": info["use_cases"]
        }
        for name, info in TEMPLATES.items()
    }

    user_message = f"""Classify the following problem using ONLY patterns from this list:
{json.dumps(list(pattern_context.keys()), indent=2)}

Pattern descriptions for reference:
{json.dumps(pattern_context, indent=2)}

Problem to classify:
\"\"\"{problem_text}\"\"\"

Respond with ONLY the JSON object. No explanation."""

    try:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            print("Error: GROQ_API_KEY environment variable not set.")
            return {"patterns": []}

        client = Groq(api_key=api_key)

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_message},
            ],
            model="llama-3.3-70b-versatile",   # Upgraded from llama-3.1-8b-instant
            temperature=0,                      # Deterministic output
            max_tokens=256,                     # Classification only needs a short response
            response_format={"type": "json_object"}
        )

        raw = chat_completion.choices[0].message.content.strip()

        # Robust JSON extraction
        start_idx = raw.find('{')
        end_idx   = raw.rfind('}')
        if start_idx == -1 or end_idx == -1:
            print(f"No JSON object found in LLM response: {raw}")
            return {"patterns": []}

        try:
            llm_result = json.loads(raw[start_idx:end_idx + 1])
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e} | Raw: {raw}")
            return {"patterns": []}

        # Validate: keep only known pattern names
        raw_patterns   = llm_result.get("patterns", [])
        valid_patterns = [p for p in raw_patterns if p in PATTERN_NAMES]

        return {
            "patterns":        valid_patterns[:3],
            "time_complexity":  llm_result.get("time_complexity", "Unknown"),
            "space_complexity": llm_result.get("space_complexity", "Unknown"),
        }

    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return {"patterns": []}

# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────
@app.route('/')
def home():
    return jsonify({"status": "ok", "message": "LeetCode Pattern Detector API is running."})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json(silent=True)
    if not data or 'problem' not in data:
        return jsonify({"error": "Request body must contain a 'problem' field."}), 400

    problem_text = data['problem'].strip()
    language = data.get('language', 'C++')
    
    if not problem_text:
        return jsonify({"error": "Problem text cannot be empty."}), 400

    llm_result = detect_patterns_with_llm(problem_text)
    patterns = llm_result.get("patterns", [])
    time_comp = llm_result.get("time_complexity", "Unknown")
    space_comp = llm_result.get("space_complexity", "Unknown")

    if not patterns:
        return jsonify({
            "patterns": [],
            "message": "No pattern detected or LLM error."
        }), 200

    result = []
    for name in patterns:
        info = TEMPLATES.get(name)
        if info:
            lang_code = info["code"].get(language, info["code"]["C++"])
            result.append({
                "pattern": name,
                "description": info["description"],
                "use_cases": info["use_cases"],
                "template": lang_code,
            })

    return jsonify({
        "patterns": result,
        "time_complexity": time_comp,
        "space_complexity": space_comp
    }), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found."}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)