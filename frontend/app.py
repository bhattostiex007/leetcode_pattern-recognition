import streamlit as st
import requests
from streamlit_ace import st_ace

import os

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LeetCode Pattern Detector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:5000")

# ─────────────────────────────────────────────
# Session State Init
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "reload_problem" not in st.session_state:
    st.session_state.reload_problem = None

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    }

    /* Animated background -> Flat Dark LeetCode */
    .stApp {
        background-color: #1a1a1a;
    }

    /* Typography */
    .hero-title {
        font-family: 'Times New Roman', Times, serif;
        font-size: 4.5rem;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0.2rem;
        letter-spacing: 0.05em;
        line-height: 1.2;
    }

    .hero-sub {
        text-align: center;
        color: #8c8c8c;
        font-size: 1.15rem;
        font-weight: 400;
        margin-bottom: 2.5rem;
    }

    /* Flat Cards */
    .pattern-card {
        background: #282828;
        border: 1px solid #3e3e3e;
        border-radius: 8px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.2rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        animation: fadeInUp 0.3s ease-out forwards;
        opacity: 0;
    }

    .pattern-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        border-color: #ffa116;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .pattern-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #eff1f6;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .pattern-desc {
        color: #8c8c8c;
        font-size: 0.95rem;
        margin-bottom: 1rem;
        line-height: 1.5;
    }

    /* Sleek Badges - LeetCode Tags */
    .badge {
        display: inline-block;
        background: rgba(255, 161, 22, 0.1);
        color: #ffa116;
        border: 1px solid transparent;
        border-radius: 12px;
        padding: 4px 10px;
        font-size: 0.75rem;
        font-weight: 500;
        margin: 3px 6px 3px 0;
        transition: all 0.2s ease;
    }

    .badge:hover {
        background: rgba(255, 161, 22, 0.2);
    }

    /* Status indicators */
    .status-ok {
        background: rgba(34, 197, 94, 0.1);
        color: #22c55e;
        border-radius: 16px;
        padding: 6px 16px;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .status-err {
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
        border-radius: 16px;
        padding: 6px 16px;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* Input & Buttons */
    .stTextArea textarea {
        font-family: Consolas, monospace !important;
        background-color: #282828 !important;
        color: #eff1f6 !important;
        border: 1px solid #3e3e3e !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
    }
    .stTextArea textarea:focus {
        border-color: #ffa116 !important;
        box-shadow: 0 0 0 1px #ffa116 !important;
        background-color: #282828 !important;
    }

    /* Add the gradient effect on every click as user requested */
    div.stButton > button {
        background: linear-gradient(135deg, #ffa116 0%, #ffb800 100%) !important;
        color: #1a1a1a !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        padding: 0.5rem 2rem !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.2s ease !important;
        position: relative;
        overflow: hidden;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #ffb800 0%, #ffc833 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3) !important;
    }
    
    div.stButton > button:active {
        transform: translateY(1px) !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
        background: linear-gradient(135deg, #e69114 0%, #ffa116 100%) !important;
    }

    /* Empty state */
    .no-pattern {
        text-align: center;
        color: #8c8c8c;
        padding: 3rem 2rem;
        background: #282828;
        border: 1px dashed #3e3e3e;
        border-radius: 8px;
    }

    /* Custom Scrollbars */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    ::-webkit-scrollbar-thumb {
        background: #3e3e3e;
        border-radius: 5px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #555555;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Living Background: Particle Network + Orbs
# ─────────────────────────────────────────────
st.markdown("""
<canvas id="codepath-particles" style="
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0;
    pointer-events: none;
"></canvas>

<!-- Floating ambient orbs -->
<div style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;pointer-events:none;overflow:hidden;">
    <div style="
        position:absolute; width:420px; height:420px; border-radius:50%;
        background: radial-gradient(circle, rgba(255,161,22,0.07) 0%, transparent 70%);
        top: -80px; left: -100px;
        animation: orbFloat1 18s ease-in-out infinite alternate;
    "></div>
    <div style="
        position:absolute; width:320px; height:320px; border-radius:50%;
        background: radial-gradient(circle, rgba(255,161,22,0.05) 0%, transparent 70%);
        bottom: 5%; right: 2%;
        animation: orbFloat2 22s ease-in-out infinite alternate;
    "></div>
    <div style="
        position:absolute; width:200px; height:200px; border-radius:50%;
        background: radial-gradient(circle, rgba(255,255,255,0.03) 0%, transparent 70%);
        top: 45%; left: 55%;
        animation: orbFloat3 14s ease-in-out infinite alternate;
    "></div>
</div>

<style>
@keyframes orbFloat1 {
    0%   { transform: translate(0px, 0px) scale(1); }
    100% { transform: translate(60px, 80px) scale(1.15); }
}
@keyframes orbFloat2 {
    0%   { transform: translate(0px, 0px) scale(1); }
    100% { transform: translate(-50px, -60px) scale(1.1); }
}
@keyframes orbFloat3 {
    0%   { transform: translate(0px, 0px) scale(1); }
    100% { transform: translate(30px, -40px) scale(0.9); }
}
</style>

<script>
(function() {
    const canvas = document.getElementById('codepath-particles');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let W = window.innerWidth, H = window.innerHeight;
    canvas.width = W; canvas.height = H;

    window.addEventListener('resize', () => {
        W = window.innerWidth; H = window.innerHeight;
        canvas.width = W; canvas.height = H;
    });

    const PARTICLE_COUNT = 70;
    const MAX_DIST = 130;
    const ORANGE = 'rgba(255, 161, 22,';
    const WHITE  = 'rgba(255, 255, 255,';

    const particles = Array.from({ length: PARTICLE_COUNT }, () => ({
        x: Math.random() * W,
        y: Math.random() * H,
        vx: (Math.random() - 0.5) * 0.45,
        vy: (Math.random() - 0.5) * 0.45,
        r: Math.random() * 1.8 + 0.8,
        color: Math.random() > 0.7 ? ORANGE : WHITE,
    }));

    function draw() {
        ctx.clearRect(0, 0, W, H);

        // Draw connections
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx*dx + dy*dy);
                if (dist < MAX_DIST) {
                    const alpha = (1 - dist / MAX_DIST) * 0.25;
                    ctx.strokeStyle = ORANGE + alpha + ')';
                    ctx.lineWidth = 0.6;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }

        // Draw dots
        particles.forEach(p => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = p.color + '0.55)';
            ctx.fill();

            // Move
            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0 || p.x > W) p.vx *= -1;
            if (p.y < 0 || p.y > H) p.vy *= -1;
        });

        requestAnimationFrame(draw);
    }
    draw();
})();
</script>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
SVG_LOGO = """
<svg width="60" height="60" viewBox="0 0 100 100" style="vertical-align: middle; margin-right: 12px; margin-bottom: 12px; filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.5));">
    <!-- Left Bracket -->
    <path d="M 35 15 C 20 15, 20 40, 10 50 C 20 60, 20 85, 35 85" stroke="#ffa116" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round" />
    <!-- Right Bracket -->
    <path d="M 65 15 C 80 15, 80 40, 90 50 C 80 60, 80 85, 65 85" stroke="#ffffff" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round" />
    <!-- Trending Arrow Line -->
    <path d="M 25 75 L 45 50 L 60 65 L 85 30" stroke="#1a1a1a" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round" />
    <path d="M 25 75 L 45 50 L 60 65 L 85 30" stroke="#ffffff" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round" />
    <!-- Arrow Head -->
    <polygon points="75,25 90,25 90,40" fill="#ffa116" />
</svg>
"""

st.markdown(f'<div class="hero-title">{SVG_LOGO}CODEP<span style="color: #ffa116;">A</span>TH</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub" style="font-weight: 600; letter-spacing: 0.15em; color: #ffffff; margin-bottom: 0.5rem; font-size: 1.05rem;">PRACTICE &bull; SOLVE &bull; GROW</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub" style="font-size: 0.95rem;">Paste a problem description — get the matching algorithm pattern + C++/Python/Java template instantly.</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Backend Status Check
# ─────────────────────────────────────────────
def check_backend():
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=2)
        return r.status_code == 200
    except Exception:
        return False

col_status, _ = st.columns([2, 5])
with col_status:
    if check_backend():
        st.markdown('<span class="status-ok">Backend connected</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-err">Backend offline — run: python backend/app.py</span>', unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────
# Session History Expander
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Style the expander header */
    div[data-testid="stExpander"] > details > summary {
        background: linear-gradient(90deg, #1f1f1f 0%, #282828 100%);
        border: 1px solid #3a3a3a;
        border-radius: 10px;
        padding: 0.7rem 1.2rem;
        color: #ffa116;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        transition: border-color 0.25s, box-shadow 0.25s;
    }
    div[data-testid="stExpander"] > details > summary:hover {
        border-color: #ffa116;
        box-shadow: 0 0 12px rgba(255,161,22,0.18);
    }
    div[data-testid="stExpander"] > details > summary > span {
        color: #ffa116;
    }
    div[data-testid="stExpander"] > details[open] > summary {
        border-bottom-left-radius: 0;
        border-bottom-right-radius: 0;
        border-color: #ffa116;
    }
    div[data-testid="stExpander"] > details > div {
        background: #1a1a1a;
        border: 1px solid #ffa116;
        border-top: none;
        border-bottom-left-radius: 10px;
        border-bottom-right-radius: 10px;
        padding: 1rem 1.2rem;
    }
    .hist-entry { background: #222222; border: 1px solid #2e2e2e; border-radius: 8px;
        padding: 0.65rem 0.9rem; margin-bottom: 0.6rem;
        transition: border-color 0.2s, box-shadow 0.2s; }
    .hist-entry:hover { border-color: #ffa116; box-shadow: 0 0 8px rgba(255,161,22,0.12); }
    .hist-problem { color: #eff1f6; font-size: 0.8rem; line-height: 1.45;
        overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2;
        -webkit-box-orient: vertical; margin-bottom: 0.35rem; }
    .hist-pattern-tag { display:inline-block; background:#ffa116; color:#000;
        border-radius:4px; padding:1px 8px; font-size:0.7rem; font-weight:700;
        margin-right:3px; margin-bottom:3px; }
    .hist-meta { color:#666; font-size:0.7rem; margin-top:0.35rem; }
</style>
""", unsafe_allow_html=True)

history_label = f"📂 Watch Your History  ({len(st.session_state.history)} entr{'y' if len(st.session_state.history) == 1 else 'ies'})"
with st.expander(history_label):
    if not st.session_state.history:
        st.markdown('<p style="color:#666;font-size:0.85rem;text-align:center;padding:1rem 0;">No history yet — detect a pattern to start tracking! 🚀</p>', unsafe_allow_html=True)
    else:
        col_hist_clear, _ = st.columns([1, 4])
        with col_hist_clear:
            if st.button("🗑️ Clear History", key="clear_history"):
                st.session_state.history = []
                st.rerun()

        cols = st.columns(3)
        for idx, entry in enumerate(reversed(st.session_state.history)):
            real_idx = len(st.session_state.history) - 1 - idx
            col = cols[idx % 3]
            with col:
                pattern_tags = "".join(f'<span class="hist-pattern-tag">{p}</span>' for p in entry["patterns"])
                short_problem = entry["problem"][:100] + "..." if len(entry["problem"]) > 100 else entry["problem"]
                st.markdown(f"""
                <div class="hist-entry">
                    <div class="hist-problem">{short_problem}</div>
                    <div style="margin:0.25rem 0">{pattern_tags}</div>
                    <div class="hist-meta">⏱️ {entry['time_complexity']} &nbsp;•&nbsp; 💾 {entry['space_complexity']} &nbsp;•&nbsp; {entry['timestamp']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("↩ Reload Problem", key=f"reload_{real_idx}", use_container_width=True):
                    st.session_state.reload_problem = entry["problem"]
                    st.rerun()


# ─────────────────────────────────────────────
# Input Area
# ─────────────────────────────────────────────
left_col, right_col = st.columns([1, 1], gap="large")

EXAMPLE_PROBLEMS = {
    "Maximum Width of Binary Tree (BFS)": "Given the root of a binary tree, return the maximum width of the given tree. The maximum width of a tree is the maximum width among all levels.",
    "Course Schedule (Topological Sort)": "There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai. Return true if you can finish all courses. Otherwise, return false.",
    "Subarray Sum Equals K (Prefix Sum)": "Given an array of integers nums and an integer k, return the total number of subarrays whose sum equals to k.",
    "Linked List Cycle (Fast & Slow Pointers)": "Given head, the head of a linked list, determine if the linked list has a cycle in it. There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer.",
    "Two Sum (Hash Map)": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution.",
    "Longest Substring (Sliding Window)": "Given a string s, find the length of the longest substring without repeating characters.",
    "Number of Islands (DFS)": "Given an m x n 2D binary grid which represents a map of 1s (land) and 0s (water), return the number of islands.",
    "Coin Change (DP)": "Given coins of different denominations and a total amount, find the minimum number of coins needed. Return -1 if it's not possible.",
    "Binary Search": "Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be inserted.",
}

with left_col:
    st.markdown("#### Problem Description")

    if "prev_example" not in st.session_state:
        st.session_state.prev_example = "— custom input —"
    if "problem_text" not in st.session_state:
        st.session_state.problem_text = ""

    # If user clicked Reload from history, inject the problem text
    if st.session_state.reload_problem is not None:
        st.session_state.problem_text = st.session_state.reload_problem
        st.session_state.reload_problem = None

    def on_example_change():
        ex = st.session_state.example_select
        if ex != "— custom input —":
            st.session_state.problem_text = EXAMPLE_PROBLEMS[ex]

    example = st.selectbox(
        "Load an example problem", 
        ["— custom input —"] + list(EXAMPLE_PROBLEMS.keys()),
        key="example_select",
        on_change=on_example_change
    )

    problem_input = st.text_area(
        label="Paste your LeetCode problem here",
        height=280,
        placeholder="e.g. Given a sorted array and a target, return the index using binary search...",
        label_visibility="collapsed",
        key="problem_text"
    )

    language = st.radio("Language Template", ["C++", "Python", "Java"], horizontal=True, key="lang_radio")

    detect_btn = st.button("Detect Pattern", use_container_width=True)


# ─────────────────────────────────────────────
# Results
# ─────────────────────────────────────────────
with right_col:
    st.markdown("#### Detected Patterns")

    if detect_btn:
        if not problem_input.strip():
            st.warning("Please enter or select a problem description first.")
        elif not check_backend():
            st.error("Cannot reach the Flask backend. Start it with:\n```\npython backend/app.py\n```")
        else:
            with st.spinner("Analyzing problem..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/detect",
                        json={"problem": problem_input, "language": language},
                        timeout=20,
                    )

                    if response.status_code == 200:
                        data = response.json()
                        patterns = data.get("patterns", [])

                        if not patterns:
                            st.markdown('<div class="no-pattern">No pattern detected.<br>Try adding more details to the problem.</div>', unsafe_allow_html=True)
                        else:
                            time_comp = data.get("time_complexity", "Unknown")
                            space_comp = data.get("space_complexity", "Unknown")

                            # Save to session history
                            from datetime import datetime
                            pattern_names = [p["pattern"] for p in patterns]
                            st.session_state.history.append({
                                "problem": problem_input,
                                "patterns": pattern_names,
                                "time_complexity": time_comp,
                                "space_complexity": space_comp,
                                "timestamp": datetime.now().strftime("%H:%M:%S")
                            })
                            
                            st.markdown(f"""
                            <div style="display:flex;gap:1rem;margin-bottom:1rem;">
                                <div style="background:#282828;border:1px solid #3e3e3e;padding:0.6rem 1rem;border-radius:8px;color:#eff1f6;font-size:0.95rem;width:50%;">
                                    ⏱️ <b>Time:</b> <span style="color:#ffa116;font-family:Consolas, monospace;font-size:1.05rem;">{time_comp}</span>
                                </div>
                                <div style="background:#282828;border:1px solid #3e3e3e;padding:0.6rem 1rem;border-radius:8px;color:#eff1f6;font-size:0.95rem;width:50%;">
                                    💾 <b>Space:</b> <span style="color:#ffa116;font-family:Consolas, monospace;font-size:1.05rem;">{space_comp}</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            for i, p in enumerate(patterns):
                                rank_labels = ["#1 Best Match", "#2 Match", "#3 Match"]
                                label = rank_labels[i] if i < len(rank_labels) else f"#{i+1}"
                                
                                badges = "".join(f'<span class="badge">{uc}</span>' for uc in p["use_cases"])
                                html_content = f"""
                                <div class="pattern-card">
                                    <div class="pattern-title">{label} — {p['pattern']}</div>
                                    <div class="pattern-desc">{p['description']}</div>
                                    <div style="margin-bottom:0.8rem">{badges}</div>
                                </div>
                                """
                                st.markdown(html_content, unsafe_allow_html=True)

                                with st.expander(f"Interactive Editor: {language} Template — {p['pattern']}"):
                                    lang_map = {"C++": "c_cpp", "Python": "python", "Java": "java"}
                                    st.markdown(f"**Practice your solution for {p['pattern']} below:**")
                                    st_ace(
                                        value=p["template"],
                                        language=lang_map.get(language, "c_cpp"),
                                        theme="twilight",
                                        font_size=14,
                                        tab_size=4,
                                        height=300,
                                        key=f"ace_editor_{i}"
                                    )

                    else:
                        st.error(f"Backend error {response.status_code}: {response.text}")

                except requests.ConnectionError:
                    st.error("Connection refused. Make sure Flask backend is running on port 5000.")
                except requests.Timeout:
                    st.error("Request timed out. Backend may be overloaded.")
                except Exception as ex:
                    st.error(f"Unexpected error: {ex}")
    else:
        st.markdown('<div class="no-pattern" style="margin-top:1rem">Select an example or type a problem,<br>then click <b>Detect Pattern</b>.</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="text-align:center;color:#475569;font-size:0.82rem;">LeetCode Pattern Detector — 15 patterns covered: Two Pointers, Sliding Window, Binary Search, BFS, DFS, Dynamic Programming, Backtracking, Heap, Hash Map, Greedy, Stack, Trie, Prefix Sum, Fast & Slow Pointers, Topological Sort</p>',
    unsafe_allow_html=True,
)