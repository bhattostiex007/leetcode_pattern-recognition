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
# Keyword Mapping: each entry is (keyword, weight)
# Higher weight = stronger signal for that pattern.
# ─────────────────────────────────────────────
PATTERN_KEYWORDS = {
    # Array/string problems: two pointers meeting in the middle
    # STRONG: problem-specific phrases; WEAK: generic terms shared with binary search
    "Two Pointers": [
        ("two pointer", 5), ("two sum ii", 5), ("container with most water", 5),
        ("three sum", 5), ("trapping rain water", 5), ("valid palindrome", 5),
        ("move zeroes", 5), ("remove duplicates from sorted", 5),
        ("pair sum", 4), ("opposite end", 4), ("left.*right", 3),
        ("sorted array", 2),  # weak: also in binary search
    ],
    # Contiguous sub-sequence: expand/shrink a window over array or string
    "Sliding Window": [
        ("longest substring without", 5), ("minimum window substring", 5),
        ("sliding window", 5), ("at most k distinct", 5), ("permutation in string", 5),
        ("longest substring", 4), ("minimum window", 4), ("k distinct", 4),
        ("substring", 3), ("subarray", 2), ("window", 2),
        ("contiguous", 2), ("consecutive", 2),
    ],
    # Sorted/monotonic domain: halve the search space each step
    "Binary Search": [
        ("binary search", 5), ("search in rotated", 5), ("first bad version", 5),
        ("koko eating bananas", 5), ("capacity to ship", 5), ("peak element", 5),
        ("minimum in rotated sorted", 5), ("search insert position", 5),
        ("find position", 4), ("find index", 4), ("return the index", 4),
        ("sorted array", 3), ("sorted", 2),
    ],
    # Graph/grid shortest-path via queue, level-by-level
    "BFS": [
        ("level order", 5), ("word ladder", 5), ("rotten oranges", 5),
        ("01 matrix", 5), ("walls and gates", 5), ("breadth first", 5),
        ("maximum width", 4), ("minimum steps", 4), ("minimum distance", 4),
        ("shortest path", 4), ("level by level", 4), ("each level", 4),
        ("width of", 3), ("width among", 3), ("bfs", 3),
    ],
    # Graph/grid/tree deep exploration via recursion or stack
    "DFS": [
        ("number of islands", 5), ("flood fill", 5), ("clone graph", 5),
        ("all paths", 5), ("path sum", 5), ("dfs", 5), ("depth first", 5),
        ("connected components", 4), ("number of connected", 4),
        ("island", 3), ("flood", 3), ("explore all", 3),
    ],
    # Optimal substructure + overlapping subproblems
    "Dynamic Programming": [
        ("coin change", 5), ("longest common subsequence", 5), ("edit distance", 5),
        ("knapsack", 5), ("climbing stairs", 5), ("house robber", 5),
        ("longest increasing subsequence", 5), ("unique paths", 5),
        ("decode ways", 5), ("palindrome subsequence", 5),
        ("minimum number of coins", 4), ("minimum coins", 4),
        ("number of ways", 4), ("count ways", 4), ("minimum cost", 4),
        ("maximum profit", 4), ("memoization", 4), ("dp", 3),
        ("overlapping subproblem", 4), ("optimal substructure", 4),
    ],
    # Enumerate all combinations/permutations, prune invalid branches
    "Backtracking": [
        ("combination sum", 5), ("all permutations", 5), ("all combinations", 5),
        ("n-queens", 5), ("sudoku solver", 5), ("word search", 5),
        ("generate all", 4), ("palindrome partitioning", 4),
        ("restore ip addresses", 4), ("letter combinations", 4),
        ("power set", 4), ("all subsets", 4), ("subset", 3),
    ],
    # Dynamic access to min/max in O(log n)
    "Heap / Priority Queue": [
        ("kth largest", 5), ("k largest", 5), ("k smallest", 5),
        ("merge k sorted", 5), ("find median", 5), ("task scheduler", 5),
        ("top k frequent", 5), ("sliding window maximum", 5),
        ("k-th largest", 5), ("priority queue", 4), ("top k", 4),
        ("heap", 4), ("meeting rooms", 4),
    ],
    # O(1) lookup; group/count/find complement
    "Hash Map": [
        ("two sum", 5), ("group anagrams", 5), ("longest consecutive sequence", 5),
        ("subarray sum equals", 5), ("top k frequent elements", 4),
        ("find duplicate", 3), ("count occurrences", 3), ("frequency", 3),
        ("anagram", 4), ("complement", 3), ("indices of the two", 4),
        ("add up to target", 4), ("sum to target", 4),
    ],
    # Local optimal choices; no backtracking
    "Greedy": [
        ("jump game", 5), ("gas station", 5), ("minimum number of arrows", 5),
        ("non-overlapping intervals", 5), ("assign cookies", 5),
        ("minimum platforms", 4), ("maximize", 3), ("greedy", 4),
        ("activity selection", 4), ("locally optimal", 4),
        ("interval scheduling", 4), ("can you reach", 3),
    ],
    # LIFO: brackets, monotonic sequence, next greater element
    "Stack": [
        ("valid parentheses", 5), ("next greater element", 5),
        ("largest rectangle in histogram", 5), ("daily temperatures", 5),
        ("decode string", 5), ("evaluate expression", 5),
        ("matching brackets", 4), ("balanced parentheses", 4),
        ("monotonic stack", 4), ("parentheses", 3), ("brackets", 3),
    ],
    # Prefix tree: fast string lookup by prefix
    "Trie": [
        ("implement trie", 5), ("word search ii", 5), ("design search autocomplete", 5),
        ("replace words", 4), ("longest common prefix", 4),
        ("starts with", 4), ("prefix tree", 5), ("trie", 5),
        ("autocomplete", 4), ("design add and search", 4),
    ],
    # Cumulative sums for O(1) range queries
    "Prefix Sum": [
        ("subarray sum equals k", 5), ("range sum query", 5),
        ("prefix sum", 5), ("cumulative sum", 5),
        ("number of subarrays whose sum", 5), ("count subarrays", 4),
        ("sum equals to k", 4), ("equilibrium index", 4),
        ("continuous subarray sum", 4), ("subarray sum", 3),
    ],
    # Floyd cycle detection on linked lists
    "Fast & Slow Pointers": [
        ("linked list has a cycle", 5), ("cycle in a linked list", 5),
        ("linked list cycle", 5), ("detect cycle", 5), ("middle of the linked list", 5),
        ("happy number", 5), ("find the duplicate number", 5),
        ("tortoise", 5), ("hare", 4), ("cycle detection", 5),
        ("floyd", 4), ("cycle", 3), ("loop in linked list", 5),
    ],
    # DAG ordering; prerequisite / dependency resolution
    "Topological Sort": [
        ("course schedule", 5), ("prerequisite", 5), ("build order", 5),
        ("alien dictionary", 5), ("topological", 5), ("directed acyclic graph", 5),
        ("dag", 4), ("in-degree", 4), ("kahn", 4),
        ("task order", 4), ("sequence reconstruction", 4),
        ("dependency", 3), ("finish all courses", 4),
    ],
    # Tree/math: break into smaller identical subproblems
    "Recursion": [
        ("maximum depth", 5), ("minimum depth", 5), ("fibonacci", 5),
        ("tower of hanoi", 5), ("flatten nested", 5), ("power of x", 4),
        ("pow(x", 4), ("base case", 4), ("recursive", 3),
        ("divide and conquer", 4), ("merge sort", 4),
    ],
    # DSU: connectivity grouping
    "Union Find": [
        ("number of provinces", 5), ("redundant connection", 5),
        ("accounts merge", 5), ("union find", 5), ("disjoint set", 5),
        ("dsu", 5), ("find and union", 4), ("connected components", 4),
        ("kruskal", 4), ("minimum spanning tree", 4),
        ("most stones removed", 4), ("same component", 3),
    ],
    # Deque-based sliding window max/min
    "Monotonic Deque": [
        ("sliding window maximum", 5), ("sliding window minimum", 5),
        ("monotonic deque", 5), ("window max", 4), ("window min", 4),
        ("jump game vi", 5), ("constrained subsequence sum", 5),
        ("max value of equation", 4), ("deque", 3),
    ],
    # Sort + merge overlapping ranges
    "Interval Merging": [
        ("merge intervals", 5), ("insert interval", 5), ("meeting rooms", 5),
        ("non-overlapping intervals", 5), ("employee free time", 5),
        ("overlapping intervals", 4), ("minimum meeting rooms", 4),
        ("interval", 3), ("merge overlapping", 4), ("free time", 3),
    ],
    # XOR tricks and bitwise ops
    "Bit Manipulation": [
        ("single number", 5), ("number of 1 bits", 5), ("hamming weight", 5),
        ("missing number", 5), ("counting bits", 5), ("reverse bits", 5),
        ("sum of two integers", 5), ("power of two", 5),
        ("bitwise", 4), ("xor", 4), ("bit manipulation", 5),
        ("find the single", 4), ("without using", 3),
    ],
}


def detect_patterns(problem_text: str):
    """Weighted keyword detection: each keyword has a weight; highest-scoring patterns win."""
    text = problem_text.lower()
    scores = {}

    for pattern, kw_weight_pairs in PATTERN_KEYWORDS.items():
        score = sum(w for kw, w in kw_weight_pairs if kw in text)
        if score > 0:
            scores[pattern] = score

    # Sort by weighted score descending, return top 3 with score > 0
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