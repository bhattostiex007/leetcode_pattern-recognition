from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────────────
# C++ Templates Dictionary
# ─────────────────────────────────────────────
CPP_TEMPLATES = {
    "Two Pointers": {
        "description": "Use two index pointers on a sorted ARRAY or STRING — one from the left, one from the right — moving toward each other to find pairs or remove duplicates in O(n). NOT used for linked lists or cycle detection.",
        "use_cases": ["Pair sum in sorted array", "Remove duplicates from sorted array", "Container with most water", "Three Sum", "Trapping rain water", "Valid palindrome"],
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
        "description": "Maintain a contiguous window over an ARRAY or STRING, expanding the right boundary and shrinking the left boundary to satisfy a constraint. Used when the problem asks for a longest/shortest subarray or substring meeting some condition.",
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
        "description": "Eliminate half the search space each step on a SORTED array or a monotonic answer domain. O(log n). Use when the problem says 'sorted array', 'find minimum/maximum feasible value', or 'search in rotated array'.",
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
        "description": "Explore a GRAPH or GRID level-by-level using a queue. Guarantees the shortest path in unweighted graphs. Use when the problem asks for minimum steps, levels, or shortest distance between nodes.",
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
        "description": "Recursively explore all paths depth-first in a GRAPH, GRID, or TREE. Use for connectivity (number of islands, connected components), path existence, flood fill, or tree traversal. Does not guarantee shortest path.",
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
        "description": "Break a problem into overlapping subproblems, store their results to avoid recomputation. Use when the problem has optimal substructure and overlapping subproblems — keywords: 'minimum cost', 'maximum profit', 'number of ways', 'longest subsequence'.",
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
        "description": "Explore all possible combinations/permutations/subsets recursively, pruning branches that violate constraints. Use when the problem asks to enumerate ALL valid solutions — keywords: 'all permutations', 'all subsets', 'all combinations', 'place N queens'.",
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
        "description": "Efficiently access the minimum or maximum element of a dynamic dataset in O(log n) per operation. Use when the problem asks for the K-th largest/smallest, a running median, or merging K sorted sequences.",
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
        "description": "O(1) average lookup and insert. Use when you need to count element frequencies, group elements by key, or find a complement/pair in a single pass. Typical signals: 'two sum', 'group anagrams', 'count occurrences', 'find duplicate'.",
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
        "description": "Make the locally optimal choice at each step, trusting it leads to the global optimum. No backtracking. Use for interval scheduling, jump games, or resource allocation — keywords: 'minimum number of', 'maximum non-overlapping', 'can you reach the end'.",
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
        "description": "LIFO data structure for bracket matching, expression evaluation, or maintaining a monotonic sequence of elements. Use when you need the 'next greater/smaller element', 'valid parentheses', or 'largest rectangle in histogram'.",
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
        "description": "A prefix tree (digital tree) for fast string prefix lookups in O(L) time where L is word length. Use when the problem involves dictionary lookups, autocomplete, word search, or finding words with a common prefix.",
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

    "Prefix Sum": {
        "description": "Precompute cumulative sums so that any subarray sum query [l, r] is answered in O(1). Use when the problem asks for count of subarrays with a given sum, range sum queries, or equilibrium indices. Often combined with a Hash Map to find subarrays summing to k.",
        "use_cases": ["Range sum query", "Subarray sum equals K", "Equilibrium index", "Continuous subarray sum"],
        "template": """\
// ── Prefix Sum ────────────────────────────────
vector<int> prefixSum(n + 1, 0);
for (int i = 0; i < n; i++) {
    prefixSum[i + 1] = prefixSum[i] + nums[i];
}

// Query sum from index left to right (inclusive, 0-indexed)
// rangeSum = prefixSum[right + 1] - prefixSum[left]

// ── Prefix Sum + Hash Map (Subarray Sum = K) ──
unordered_map<int, int> prefixCount; // prefixSum -> count
prefixCount[0] = 1;
int runningSum = 0, result = 0;
for (int x : nums) {
    runningSum += x;
    result += prefixCount[runningSum - k];
    prefixCount[runningSum]++;
}
return result;
"""
    },

    "Fast & Slow Pointers": {
        "description": "Floyd's Tortoise-and-Hare algorithm: use two pointers on a LINKED LIST moving at different speeds (slow moves 1 node at a time, fast moves 2 nodes at a time). When they meet, a cycle exists. Also used to find the middle node. DISTINCT from Two Pointers which operates on arrays/strings.",
        "use_cases": ["Detect cycle in linked list", "Find start of cycle in linked list", "Middle of the linked list", "Find the duplicate number", "Happy number", "Palindrome linked list"],
        "template": """\
// ── Floyd's Cycle Detection (Tortoise & Hare) ─
ListNode* slow = head;
ListNode* fast = head;

while (fast != nullptr && fast->next != nullptr) {
    slow = slow->next;          // tortoise: 1 step
    fast = fast->next->next;    // hare: 2 steps

    if (slow == fast) {
        return true; // cycle detected
    }
}
return false; // no cycle

// ── Find Middle of Linked List ────────────────
// When fast reaches end, slow is at the middle
ListNode* slow2 = head;
ListNode* fast2 = head;
while (fast2 && fast2->next) {
    slow2 = slow2->next;
    fast2 = fast2->next->next;
}
// slow2 is now at the middle node
"""
    },

    "Topological Sort": {
        "description": "Linear ordering of vertices in a Directed Acyclic Graph (DAG) using Kahn's algorithm (BFS with in-degree counting). Use when the problem involves task scheduling with prerequisites, dependency resolution, or detecting cycles in a directed graph — keywords: 'course schedule', 'prerequisites', 'build order'.",
        "use_cases": ["Course schedule", "Alien dictionary", "Build a matrix with conditions", "Sequence reconstruction"],
        "template": """\
// ── Topological Sort (Kahn's BFS Algorithm) ───
vector<int> inDegree(n, 0);
vector<vector<int>> adj(n);
for (auto& edge : edges) {
    adj[edge[0]].push_back(edge[1]);
    inDegree[edge[1]]++;
}

queue<int> q;
for (int i = 0; i < n; i++) {
    if (inDegree[i] == 0) q.push(i); // start with no dependencies
}

vector<int> order;
while (!q.empty()) {
    int node = q.front(); q.pop();
    order.push_back(node);

    for (int neighbor : adj[node]) {
        inDegree[neighbor]--;
        if (inDegree[neighbor] == 0) q.push(neighbor);
    }
}
if (order.size() != n) return {}; // cycle detected — not a DAG
return order;
"""
    },
}

# ─────────────────────────────────────────────
# Keyword → Pattern Mapping
# ─────────────────────────────────────────────
PATTERN_KEYWORDS = {
    "Two Pointers": [
        "two pointer", "opposite end", "pair sum", "sorted array",
        "remove duplicate", "container with most water", "three sum",
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
    "Prefix Sum": [
        "subarray sum", "range sum", "prefix sum", "cumulative sum",
        "sum equals k", "equilibrium index", "continuous subarray",
        "count subarrays", "number of subarrays"
    ],
    "Fast & Slow Pointers": [
        "cycle", "linked list cycle", "detect cycle", "tortoise", "hare",
        "slow pointer", "fast pointer", "middle of the linked list",
        "find the duplicate", "happy number", "loop in linked list",
        "cycle detection", "floyd"
    ],
    "Topological Sort": [
        "topological", "prerequisite", "course schedule", "dependency",
        "build order", "alien dictionary", "directed acyclic", "dag",
        "task order", "in-degree", "kahn", "sequence reconstruction"
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