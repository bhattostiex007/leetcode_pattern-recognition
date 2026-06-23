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

def detect_patterns_with_llm(problem_text: str):
    # Extract just the descriptions and use cases to keep the prompt focused
    pattern_context = {
        name: {
            "description": info["description"],
            "use_cases": info["use_cases"]
        }
        for name, info in TEMPLATES.items()
    }
    
    prompt = f"""
    You are an expert algorithm problem classifier. 
    Read the following algorithm problem description and classify it into exactly 1, 2, or 3 of the following patterns based on their descriptions and use cases:
    {json.dumps(pattern_context, indent=2)}
    
    Return the result strictly as a JSON object with the following structure:
    {{
        "patterns": ["Pattern Name 1"],
        "time_complexity": "O(N)",
        "space_complexity": "O(1)"
    }}
    The "patterns" array must contain ONLY the exact pattern names from the keys of the JSON object above (max 3).
    Do not include any other text, reasoning, or markdown formatting.
    
    Problem description:
    {problem_text}
    """
    
    try:
        # Initialize Groq client
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            print("Error: GROQ_API_KEY environment variable not set.")
            return {"patterns": []}
            
        client = Groq(api_key=api_key)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0,
            max_tokens=1024,
            response_format={"type": "json_object"}
        )
        
        text = chat_completion.choices[0].message.content.strip()
        
        # Robust JSON extraction: find the first '{' and last '}'
        start_idx = text.find('{')
        end_idx = text.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            json_str = text[start_idx:end_idx+1]
            try:
                llm_result = json.loads(json_str)
            except json.JSONDecodeError:
                print(f"Error decoding JSON from isolated string: {json_str}")
                return {"patterns": []}
        else:
            print(f"Could not find JSON object in LLM response: {text}")
            return {"patterns": []}
        
        # filter to only known patterns
        patterns = llm_result.get("patterns", [])
        valid_patterns = [p for p in patterns if p in PATTERN_NAMES]
        
        return {
            "patterns": valid_patterns[:3],
            "time_complexity": llm_result.get("time_complexity", "Unknown"),
            "space_complexity": llm_result.get("space_complexity", "Unknown")
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