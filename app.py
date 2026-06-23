from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────────────
# C++ Templates Dictionary
# ─────────────────────────────────────────────
CPP_TEMPLATES = {
    "Two Pointers": {
        "description": "Use two pointers moving toward each other or in the same direction to solve array/string problems in O(n).",
        "use_cases": ["Pair sum in sorted array", "Remove duplicates", "Container with most water", "Three Sum", "Trapping rain water"],
        "template": """\
// ── Two Pointers ──────────────────────────────
int left = 0, right = n - 1;

while (left < right) {
    int sum = nums[left] + nums[right];
    if (sum == target) {
        // found pair
        left++;
        right--;
    } else if (sum < target) {
        left++;
    } else {
        right--;
    }
}
"""
    },

    "Sliding Window": {
        "description": "Maintain a variable-size window over a sequence, expanding/shrinking it to satisfy a constraint.",
        "use_cases": ["Longest substring without repeating chars", "Minimum window substring", "Max sum subarray of size k", "At most K distinct characters"],
        "template": """\
// ── Sliding Window ────────────────────────────
int left = 0, result = 0;
unordered_map<char, int> freq;

for (int right = 0; right < n; right++) {
    freq[s[right]]++;               // expand window

    while (/* window condition violated */) {
        freq[s[left]]--;
        if (freq[s[left]] == 0) freq.erase(s[left]);
        left++;                     // shrink window
    }

    result = max(result, right - left + 1);
}
return result;
"""
    },

    "Binary Search": {
        "description": "Halve the search space each step on a sorted or monotonic domain. O(log n).",
        "use_cases": ["Search in sorted array", "Find first/last position", "Search in rotated array", "Koko eating bananas", "Capacity to ship packages"],
        "template": """\
// ── Binary Search ─────────────────────────────
int left = 0, right = n - 1;

while (left <= right) {
    int mid = left + (right - left) / 2;  // avoid overflow

    if (nums[mid] == target) {
        return mid;
    } else if (nums[mid] < target) {
        left = mid + 1;
    } else {
        right = mid - 1;
    }
}
return -1; // not found
"""
    },

    "BFS": {
        "description": "Explore nodes level-by-level with a queue. Guarantees shortest path in unweighted graphs.",
        "use_cases": ["Shortest path", "Level order traversal", "Word ladder", "Rotten oranges", "01 Matrix"],
        "template": """\
// ── BFS ───────────────────────────────────────
queue<int> q;
vector<bool> visited(n, false);
q.push(start);
visited[start] = true;
int steps = 0;

while (!q.empty()) {
    int sz = q.size();
    for (int i = 0; i < sz; i++) {
        int node = q.front(); q.pop();
        if (node == target) return steps;

        for (int neighbor : adj[node]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                q.push(neighbor);
            }
        }
    }
    steps++;
}
return -1; // unreachable
"""
    },

    "DFS": {
        "description": "Recursively explore all paths depth-first. Great for connectivity, tree problems, and combinatorics.",
        "use_cases": ["Number of islands", "Path sum in tree", "Clone graph", "Connected components", "Flood fill"],
        "template": """\
// ── DFS (Grid) ────────────────────────────────
int rows, cols;
vector<vector<int>> dirs = {{0,1},{0,-1},{1,0},{-1,0}};

void dfs(vector<vector<char>>& grid, int r, int c) {
    if (r < 0 || r >= rows || c < 0 || c >= cols) return;
    if (grid[r][c] != '1') return;

    grid[r][c] = '0'; // mark visited

    for (auto& d : dirs)
        dfs(grid, r + d[0], c + d[1]);
}

// ── DFS (Tree) ────────────────────────────────
int dfs(TreeNode* node) {
    if (!node) return 0;
    int left  = dfs(node->left);
    int right = dfs(node->right);
    return /* combine */ max(left, right) + 1;
}
"""
    },

    "Dynamic Programming": {
        "description": "Store results of overlapping subproblems to avoid recomputation. Build solution bottom-up or top-down.",
        "use_cases": ["Coin change", "Longest common subsequence", "Knapsack", "Climbing stairs", "Edit distance", "Longest increasing subsequence"],
        "template": """\
// ── 1-D DP ────────────────────────────────────
vector<int> dp(n + 1, 0);
dp[0] = /* base case */;

for (int i = 1; i <= n; i++) {
    dp[i] = /* transition: e.g. dp[i-1] + dp[i-2] */;
}
return dp[n];

// ── 2-D DP ────────────────────────────────────
vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));

for (int i = 1; i <= m; i++) {
    for (int j = 1; j <= n; j++) {
        if (a[i-1] == b[j-1])
            dp[i][j] = dp[i-1][j-1] + 1;
        else
            dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
    }
}
return dp[m][n];
"""
    },

    "Backtracking": {
        "description": "Explore all possibilities recursively; prune branches that violate constraints.",
        "use_cases": ["All permutations", "Combination sum", "Subsets", "N-Queens", "Word search", "Sudoku solver"],
        "template": """\
// ── Backtracking ──────────────────────────────
void backtrack(int start, vector<int>& current,
               vector<int>& nums, vector<vector<int>>& result) {
    // base case: valid solution found
    result.push_back(current);

    for (int i = start; i < nums.size(); i++) {
        if (/* skip condition */) continue;

        current.push_back(nums[i]);          // choose
        backtrack(i + 1, current, nums, result); // explore
        current.pop_back();                  // un-choose
    }
}

// call: backtrack(0, {}, nums, result);
"""
    },

    "Heap / Priority Queue": {
        "description": "Efficiently access the min/max of a dynamic dataset in O(log n) per operation.",
        "use_cases": ["Top K frequent elements", "K-th largest element", "Merge K sorted lists", "Task scheduler", "Find median from data stream"],
        "template": """\
// ── Min-Heap (keep K largest) ─────────────────
priority_queue<int, vector<int>, greater<int>> minHeap;

for (int num : nums) {
    minHeap.push(num);
    if ((int)minHeap.size() > k)
        minHeap.pop();
}
return minHeap.top(); // k-th largest

// ── Max-Heap (default) ────────────────────────
priority_queue<int> maxHeap;
maxHeap.push(val);
int top = maxHeap.top();
maxHeap.pop();
"""
    },

    "Hash Map": {
        "description": "O(1) average lookup/insert. Use for counting frequencies, grouping, or complement-finding.",
        "use_cases": ["Two Sum", "Group anagrams", "Longest consecutive sequence", "Subarray sum equals K", "Top K frequent"],
        "template": """\
// ── Hash Map (frequency / complement) ────────
unordered_map<int, int> seen; // val -> index

for (int i = 0; i < nums.size(); i++) {
    int complement = target - nums[i];
    if (seen.count(complement))
        return {seen[complement], i};
    seen[nums[i]] = i;
}

// ── Frequency Count ───────────────────────────
unordered_map<int, int> freq;
for (int x : nums) freq[x]++;

for (auto& [val, cnt] : freq) {
    if (cnt > threshold) { /* ... */ }
}
"""
    },

    "Greedy": {
        "description": "Make the locally optimal choice at each step. Works when local optimum leads to global optimum.",
        "use_cases": ["Jump game", "Gas station", "Minimum number of arrows", "Non-overlapping intervals", "Assign cookies"],
        "template": """\
// ── Greedy (Intervals) ────────────────────────
// Sort by end time, greedily pick non-overlapping
sort(intervals.begin(), intervals.end(),
     [](auto& a, auto& b){ return a[1] < b[1]; });

int count = 0, end = INT_MIN;
for (auto& iv : intervals) {
    if (iv[0] >= end) {   // no overlap
        count++;
        end = iv[1];
    }
}
return count;
"""
    },

    "Stack": {
        "description": "LIFO structure for matching brackets, evaluating expressions, or maintaining monotonic sequences.",
        "use_cases": ["Valid parentheses", "Next greater element", "Daily temperatures", "Largest rectangle in histogram", "Decode string"],
        "template": """\
// ── Monotonic Stack (Next Greater Element) ────
stack<int> stk;
vector<int> result(n, -1);

for (int i = 0; i < n; i++) {
    while (!stk.empty() && nums[stk.top()] < nums[i]) {
        result[stk.top()] = nums[i];
        stk.pop();
    }
    stk.push(i);
}

// ── Valid Parentheses ─────────────────────────
stack<char> st;
for (char c : s) {
    if (c == '(' || c == '{' || c == '[') st.push(c);
    else {
        if (st.empty()) return false;
        if (c == ')' && st.top() != '(') return false;
        if (c == '}' && st.top() != '{') return false;
        if (c == ']' && st.top() != '[') return false;
        st.pop();
    }
}
return st.empty();
"""
    },

    "Trie": {
        "description": "Prefix tree for fast string prefix lookups, autocomplete, and word existence checks.",
        "use_cases": ["Implement Trie", "Word search II", "Replace words", "Longest common prefix", "Design search autocomplete"],
        "template": """\
// ── Trie ──────────────────────────────────────
struct TrieNode {
    unordered_map<char, TrieNode*> children;
    bool isEnd = false;
};

class Trie {
    TrieNode* root = new TrieNode();
public:
    void insert(const string& word) {
        TrieNode* cur = root;
        for (char c : word) {
            if (!cur->children.count(c))
                cur->children[c] = new TrieNode();
            cur = cur->children[c];
        }
        cur->isEnd = true;
    }

    bool search(const string& word) {
        TrieNode* cur = root;
        for (char c : word) {
            if (!cur->children.count(c)) return false;
            cur = cur->children[c];
        }
        return cur->isEnd;
    }

    bool startsWith(const string& prefix) {
        TrieNode* cur = root;
        for (char c : prefix) {
            if (!cur->children.count(c)) return false;
            cur = cur->children[c];
        }
        return true;
    }
};
"""
    },
}

# ─────────────────────────────────────────────
# Keyword → Pattern Mapping
# ─────────────────────────────────────────────
PATTERN_KEYWORDS = {
    "Two Pointers": [
        "two pointer", "opposite end", "pair sum", "palindrome", "sorted array",
        "remove duplicate", "reverse", "container with most water", "three sum",
        "trapping rain", "two sum ii", "valid palindrome", "move zeroes"
    ],
    "Sliding Window": [
        "subarray", "substring", "window", "consecutive", "contiguous",
        "longest substring", "minimum window", "max sum subarray", "sliding",
        "at most k", "exactly k", "k distinct", "permutation in string"
    ],
    "Binary Search": [
        "sorted", "binary search", "log n", "search in", "find position",
        "rotated", "peak element", "first bad version", "search insert",
        "koko", "split array", "minimum in rotated", "capacity to ship"
    ],
    "BFS": [
        "shortest path", "level order", "bfs", "breadth first", "word ladder",
        "01 matrix", "walls and gates", "rotten orange", "jump game ii",
        "minimum step", "nearest", "spread", "infection", "minimum distance"
    ],
    "DFS": [
        "dfs", "depth first", "all path", "connected component", "island",
        "flood fill", "number of island", "path exist", "clone graph",
        "traversal", "preorder", "inorder", "postorder", "tree path"
    ],
    "Dynamic Programming": [
        "maximum", "minimum", "optimal", "ways to", "count the number",
        "longest common", "edit distance", "knapsack", "coin change",
        "fibonacci", "climbing stair", "house robber", "longest increasing",
        "palindrome subsequence", "unique path", "dp", "memoization",
        "subproblem", "overlapping", "decode ways", "partition"
    ],
    "Backtracking": [
        "all combination", "all permutation", "generate all", "subset",
        "combination sum", "letter combination", "n-queen", "sudoku",
        "word search", "palindrome partition", "restore ip", "power set"
    ],
    "Heap / Priority Queue": [
        "k largest", "k smallest", "k-th", "top k", "merge k sorted",
        "priority", "heap", "meeting room", "task scheduler",
        "find median", "sliding window maximum", "kth largest"
    ],
    "Hash Map": [
        "frequency", "count", "anagram", "duplicate", "two sum",
        "group anagram", "subarray sum equal", "longest consecutive",
        "hash", "lookup", "occurrence", "unique", "complement"
    ],
    "Greedy": [
        "greedy", "locally optimal", "activity selection", "jump game",
        "gas station", "assign cookie", "minimum arrow", "non-overlapping",
        "interval", "meeting", "schedule", "minimum platform", "maximize profit"
    ],
    "Stack": [
        "parenthese", "bracket", "valid parenthese", "next greater",
        "daily temperature", "largest rectangle", "monotonic",
        "decode string", "evaluate expression", "stack", "balanced"
    ],
    "Trie": [
        "prefix", "trie", "autocomplete", "word search ii", "longest common prefix",
        "replace word", "design add and search", "implement trie", "starts with"
    ],
}


def detect_patterns(problem_text: str):
    text = problem_text.lower()
    scores = {}

    for pattern, keywords in PATTERN_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[pattern] = score

    # Sort by score, return top 3
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [p for p, _ in ranked[:3]]


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
    if not problem_text:
        return jsonify({"error": "Problem text cannot be empty."}), 400

    patterns = detect_patterns(problem_text)

    if not patterns:
        return jsonify({
            "patterns": [],
            "message": "No pattern detected. Try adding more detail to the problem description."
        }), 200

    result = []
    for name in patterns:
        info = CPP_TEMPLATES[name]
        result.append({
            "pattern": name,
            "description": info["description"],
            "use_cases": info["use_cases"],
            "template": info["template"],
        })

    return jsonify({"patterns": result}), 200


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found."}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error."}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)