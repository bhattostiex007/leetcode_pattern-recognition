TEMPLATES = {
    "Two Pointers": {
        "description": "Use two index pointers on a sorted ARRAY or STRING — one starting from the left, one from the right — moving toward each other (or in the same direction) to find pairs or remove duplicates in O(n). NOT used for linked lists or cycle detection.",
        "use_cases": ["Pair sum in sorted array", "Remove duplicates from sorted array", "Container with most water", "Three Sum", "Trapping rain water", "Valid palindrome"],
        "code": {
            "C++": """\
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
""",
            "Python": """\
left, right = 0, len(nums) - 1

while left < right:
    total = nums[left] + nums[right]
    if total == target:
        # found pair
        left += 1
        right -= 1
    elif total < target:
        left += 1
    else:
        right -= 1
""",
            "Java": """\
int left = 0, right = nums.length - 1;

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
        }
    },
    "Sliding Window": {
        "description": "Maintain a contiguous window over an ARRAY or STRING, expanding the right boundary and shrinking the left boundary to satisfy a constraint. Used when the problem asks for a longest/shortest subarray or substring meeting some condition.",
        "use_cases": ["Longest substring without repeating chars", "Minimum window substring", "Max sum subarray of size k", "At most K distinct characters"],
        "code": {
            "C++": """\
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
""",
            "Python": """\
import collections
left = result = 0
freq = collections.defaultdict(int)

for right in range(len(s)):
    freq[s[right]] += 1             # expand window
    
    while False: # window condition violated
        freq[s[left]] -= 1
        if freq[s[left]] == 0:
            del freq[s[left]]
        left += 1                   # shrink window
        
    result = max(result, right - left + 1)
return result
""",
            "Java": """\
int left = 0, result = 0;
Map<Character, Integer> freq = new HashMap<>();

for (int right = 0; right < n; right++) {
    char rChar = s.charAt(right);
    freq.put(rChar, freq.getOrDefault(rChar, 0) + 1);

    while (/* window condition violated */ false) {
        char lChar = s.charAt(left);
        freq.put(lChar, freq.get(lChar) - 1);
        if (freq.get(lChar) == 0) freq.remove(lChar);
        left++;
    }

    result = Math.max(result, right - left + 1);
}
return result;
"""
        }
    },
    "Binary Search": {
        "description": "Eliminate half the search space each step on a SORTED array or a monotonic answer domain. O(log n). Use when the problem says 'sorted array', 'find minimum/maximum feasible value', or 'search in rotated array'.",
        "use_cases": ["Search in sorted array", "Find first/last position", "Search in rotated array", "Koko eating bananas", "Capacity to ship packages"],
        "code": {
            "C++": """\
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
""",
            "Python": """\
left, right = 0, len(nums) - 1

while left <= right:
    mid = left + (right - left) // 2
    
    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        left = mid + 1
    else:
        right = mid - 1
return -1
""",
            "Java": """\
int left = 0, right = nums.length - 1;

while (left <= right) {
    int mid = left + (right - left) / 2;

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
        }
    },
    "BFS": {
        "description": "Explore a GRAPH or GRID level-by-level using a queue. Guarantees the shortest path in unweighted graphs. Use when the problem asks for minimum steps, levels, or shortest distance between nodes.",
        "use_cases": ["Shortest path", "Level order traversal", "Word ladder", "Rotten oranges", "01 Matrix"],
        "code": {
            "C++": """\
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
""",
            "Python": """\
from collections import deque

q = deque([start])
visited = {start}
steps = 0

while q:
    for _ in range(len(q)):
        node = q.popleft()
        if node == target:
            return steps
            
        for neighbor in adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
    steps += 1
return -1 # unreachable
""",
            "Java": """\
Queue<Integer> q = new LinkedList<>();
boolean[] visited = new boolean[n];

q.offer(start);
visited[start] = true;
int steps = 0;

while (!q.isEmpty()) {
    int sz = q.size();
    for (int i = 0; i < sz; i++) {
        int node = q.poll();
        if (node == target) return steps;
        
        for (int neighbor : adj.get(node)) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                q.offer(neighbor);
            }
        }
    }
    steps++;
}
return -1; // unreachable
"""
        }
    },
    "DFS": {
        "description": "Recursively explore all paths depth-first in a GRAPH, GRID, or TREE. Use for connectivity (number of islands, connected components), path existence, flood fill, or tree traversal. Does not guarantee shortest path.",
        "use_cases": ["Number of islands", "Path sum in tree", "Clone graph", "Connected components", "Flood fill"],
        "code": {
            "C++": """\
int rows, cols;
vector<vector<int>> dirs = {{0,1},{0,-1},{1,0},{-1,0}};

void dfs(vector<vector<char>>& grid, int r, int c) {
    if (r < 0 || r >= rows || c < 0 || c >= cols) return;
    if (grid[r][c] != '1') return;

    grid[r][c] = '0'; // mark visited

    for (auto& d : dirs)
        dfs(grid, r + d[0], c + d[1]);
}
""",
            "Python": """\
dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def dfs(grid, r, c):
    if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
        return
    if grid[r][c] != '1':
        return
        
    grid[r][c] = '0' # mark visited
    
    for dr, dc in dirs:
        dfs(grid, r + dr, c + dc)
""",
            "Java": """\
int[][] dirs = {{0,1}, {0,-1}, {1,0}, {-1,0}};

void dfs(char[][] grid, int r, int c) {
    if (r < 0 || r >= grid.length || c < 0 || c >= grid[0].length) return;
    if (grid[r][c] != '1') return;
    
    grid[r][c] = '0'; // mark visited
    
    for (int[] d : dirs) {
        dfs(grid, r + d[0], c + d[1]);
    }
}
"""
        }
    },
    "Dynamic Programming": {
        "description": "Break a problem into overlapping subproblems, store their results to avoid recomputation. Use when the problem has optimal substructure and overlapping subproblems — keywords: 'minimum cost', 'maximum profit', 'number of ways', 'longest subsequence'.",
        "use_cases": ["Coin change", "Longest common subsequence", "Knapsack", "Climbing stairs", "Edit distance", "Longest increasing subsequence"],
        "code": {
            "C++": """\
vector<int> dp(n + 1, 0);
dp[0] = /* base case */ 0;

for (int i = 1; i <= n; i++) {
    dp[i] = /* transition */ 0;
}
return dp[n];
""",
            "Python": """\
dp = [0] * (n + 1)
dp[0] = 0 # base case

for i in range(1, n + 1):
    dp[i] = 0 # transition
    
return dp[n]
""",
            "Java": """\
int[] dp = new int[n + 1];
dp[0] = /* base case */ 0;

for (int i = 1; i <= n; i++) {
    dp[i] = /* transition */ 0;
}
return dp[n];
"""
        }
    },
    "Backtracking": {
        "description": "Explore all possible combinations/permutations/subsets recursively, pruning branches that violate constraints. Use when the problem asks to enumerate ALL valid solutions — keywords: 'all permutations', 'all subsets', 'all combinations', 'place N queens'.",
        "use_cases": ["All permutations", "Combination sum", "Subsets", "N-Queens", "Word search", "Sudoku solver"],
        "code": {
            "C++": """\
void backtrack(int start, vector<int>& current,
               vector<int>& nums, vector<vector<int>>& result) {
    // base case: valid solution found
    result.push_back(current);

    for (int i = start; i < nums.size(); i++) {
        if (/* skip condition */ false) continue;

        current.push_back(nums[i]);          // choose
        backtrack(i + 1, current, nums, result); // explore
        current.pop_back();                  // un-choose
    }
}
""",
            "Python": """\
def backtrack(start, current):
    # base case: valid solution found
    result.append(list(current))
    
    for i in range(start, len(nums)):
        if False: # skip condition
            continue
            
        current.append(nums[i])      # choose
        backtrack(i + 1, current)    # explore
        current.pop()                # un-choose

result = []
backtrack(0, [])
""",
            "Java": """\
void backtrack(int start, List<Integer> current, 
               int[] nums, List<List<Integer>> result) {
    // base case: valid solution found
    result.add(new ArrayList<>(current));
    
    for (int i = start; i < nums.length; i++) {
        if (/* skip condition */ false) continue;
        
        current.add(nums[i]);                  // choose
        backtrack(i + 1, current, nums, result); // explore
        current.remove(current.size() - 1);    // un-choose
    }
}
"""
        }
    },
    "Heap / Priority Queue": {
        "description": "Efficiently access the minimum or maximum element of a dynamic dataset in O(log n) per operation. Use when the problem asks for the K-th largest/smallest, a running median, or merging K sorted sequences.",
        "use_cases": ["Top K frequent elements", "K-th largest element", "Merge K sorted lists", "Task scheduler", "Find median from data stream"],
        "code": {
            "C++": """\
priority_queue<int, vector<int>, greater<int>> minHeap;

for (int num : nums) {
    minHeap.push(num);
    if ((int)minHeap.size() > k)
        minHeap.pop();
}
return minHeap.top(); // k-th largest
""",
            "Python": """\
import heapq
min_heap = []

for num in nums:
    heapq.heappush(min_heap, num)
    if len(min_heap) > k:
        heapq.heappop(min_heap)
        
return min_heap[0] # k-th largest
""",
            "Java": """\
PriorityQueue<Integer> minHeap = new PriorityQueue<>();

for (int num : nums) {
    minHeap.offer(num);
    if (minHeap.size() > k) {
        minHeap.poll();
    }
}
return minHeap.peek(); // k-th largest
"""
        }
    },
    "Hash Map": {
        "description": "O(1) average lookup and insert. Use when you need to count element frequencies, group elements by key, or find a complement/pair in a single pass. Typical signals: 'two sum', 'group anagrams', 'count occurrences', 'find duplicate'.",
        "use_cases": ["Two Sum", "Group anagrams", "Longest consecutive sequence", "Subarray sum equals K", "Top K frequent"],
        "code": {
            "C++": """\
unordered_map<int, int> seen; // val -> index

for (int i = 0; i < nums.size(); i++) {
    int complement = target - nums[i];
    if (seen.count(complement))
        return {seen[complement], i};
    seen[nums[i]] = i;
}
""",
            "Python": """\
seen = {} # val -> index

for i, num in enumerate(nums):
    complement = target - num
    if complement in seen:
        return [seen[complement], i]
    seen[num] = i
""",
            "Java": """\
Map<Integer, Integer> seen = new HashMap<>(); // val -> index

for (int i = 0; i < nums.length; i++) {
    int complement = target - nums[i];
    if (seen.containsKey(complement)) {
        return new int[]{seen.get(complement), i};
    }
    seen.put(nums[i], i);
}
"""
        }
    },
    "Greedy": {
        "description": "Make the locally optimal choice at each step, trusting it leads to the global optimum. No backtracking. Use for interval scheduling, jump games, or resource allocation — keywords: 'minimum number of', 'maximum non-overlapping', 'can you reach the end'.",
        "use_cases": ["Jump game", "Gas station", "Minimum number of arrows", "Non-overlapping intervals", "Assign cookies"],
        "code": {
            "C++": """\
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
""",
            "Python": """\
# Sort by end time, greedily pick non-overlapping
intervals.sort(key=lambda x: x[1])

count = 0
end = float('-inf')
for iv in intervals:
    if iv[0] >= end: # no overlap
        count += 1
        end = iv[1]
        
return count
""",
            "Java": """\
// Sort by end time, greedily pick non-overlapping
Arrays.sort(intervals, (a, b) -> Integer.compare(a[1], b[1]));

int count = 0;
long end = Long.MIN_VALUE;
for (int[] iv : intervals) {
    if (iv[0] >= end) {   // no overlap
        count++;
        end = iv[1];
    }
}
return count;
"""
        }
    },
    "Stack": {
        "description": "LIFO data structure for bracket matching, expression evaluation, or maintaining a monotonic sequence of elements. Use when you need the 'next greater/smaller element', 'valid parentheses', or 'largest rectangle in histogram'.",
        "use_cases": ["Valid parentheses", "Next greater element", "Daily temperatures", "Largest rectangle in histogram", "Decode string"],
        "code": {
            "C++": """\
stack<int> stk;
vector<int> result(n, -1);

for (int i = 0; i < n; i++) {
    while (!stk.empty() && nums[stk.top()] < nums[i]) {
        result[stk.top()] = nums[i];
        stk.pop();
    }
    stk.push(i);
}
""",
            "Python": """\
stk = []
result = [-1] * n

for i in range(n):
    while stk and nums[stk[-1]] < nums[i]:
        idx = stk.pop()
        result[idx] = nums[i]
    stk.append(i)
""",
            "Java": """\
Stack<Integer> stk = new Stack<>();
int[] result = new int[n];
Arrays.fill(result, -1);

for (int i = 0; i < n; i++) {
    while (!stk.isEmpty() && nums[stk.peek()] < nums[i]) {
        result[stk.pop()] = nums[i];
    }
    stk.push(i);
}
"""
        }
    },
    "Trie": {
        "description": "A prefix tree (digital tree) for fast string prefix lookups in O(L) time where L is word length. Use when the problem involves dictionary lookups, autocomplete, word search, or finding words with a common prefix.",
        "use_cases": ["Implement Trie", "Word search II", "Replace words", "Longest common prefix", "Design search autocomplete"],
        "code": {
            "C++": """\
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
};
""",
            "Python": """\
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        
class Trie:
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self, word):
        cur = self.root
        for c in word:
            if c not in cur.children:
                cur.children[c] = TrieNode()
            cur = cur.children[c]
        cur.is_end = True
""",
            "Java": """\
class TrieNode {
    Map<Character, TrieNode> children = new HashMap<>();
    boolean isEnd = false;
}

class Trie {
    TrieNode root = new TrieNode();
    
    public void insert(String word) {
        TrieNode cur = root;
        for (char c : word.toCharArray()) {
            cur.children.putIfAbsent(c, new TrieNode());
            cur = cur.children.get(c);
        }
        cur.isEnd = true;
    }
}
"""
        }
    },
    "Prefix Sum": {
        "description": "Precompute cumulative sums so that any subarray sum query [l, r] is answered in O(1). Use when the problem asks for count of subarrays with a given sum, range sum queries, or equilibrium indices. Often combined with a Hash Map to find subarrays summing to k.",
        "use_cases": ["Range sum query", "Subarray sum equals K", "Equilibrium index", "Continuous subarray sum"],
        "code": {
            "C++": """\
vector<int> prefixSum(n + 1, 0);
for (int i = 0; i < n; i++) {
    prefixSum[i + 1] = prefixSum[i] + nums[i];
}

// Query sum from left to right (inclusive)
int query(int left, int right) {
    return prefixSum[right + 1] - prefixSum[left];
}
""",
            "Python": """\
prefix_sum = [0] * (n + 1)
for i in range(n):
    prefix_sum[i + 1] = prefix_sum[i] + nums[i]

# Query sum from left to right (inclusive)
def query(left, right):
    return prefix_sum[right + 1] - prefix_sum[left]
""",
            "Java": """\
int[] prefixSum = new int[n + 1];
for (int i = 0; i < n; i++) {
    prefixSum[i + 1] = prefixSum[i] + nums[i];
}

// Query sum from left to right (inclusive)
int query(int left, int right) {
    return prefixSum[right + 1] - prefixSum[left];
}
"""
        }
    },
    "Fast & Slow Pointers": {
        "description": "Floyd's Tortoise-and-Hare algorithm: use two pointers on a LINKED LIST moving at different speeds (slow moves 1 node at a time, fast moves 2 nodes at a time). When they meet, a cycle exists. Also used to find the middle node of a linked list. This is DISTINCT from Two Pointers which operates on arrays/strings.",
        "use_cases": ["Detect cycle in linked list", "Find start of cycle in linked list", "Middle of the linked list", "Find the duplicate number (array as implicit linked list)", "Happy number", "Palindrome linked list"],
        "code": {
            "C++": """\
// Floyd's Cycle Detection (Tortoise & Hare)
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
""",
            "Python": """\
# Floyd's Cycle Detection (Tortoise & Hare)
slow = head
fast = head

while fast and fast.next:
    slow = slow.next          # tortoise: 1 step
    fast = fast.next.next     # hare: 2 steps
    
    if slow == fast:
        return True  # cycle detected
        
return False  # no cycle
""",
            "Java": """\
// Floyd's Cycle Detection (Tortoise & Hare)
ListNode slow = head;
ListNode fast = head;

while (fast != null && fast.next != null) {
    slow = slow.next;          // tortoise: 1 step
    fast = fast.next.next;     // hare: 2 steps
    
    if (slow == fast) {
        return true; // cycle detected
    }
}
return false; // no cycle
"""
        }
    },
    "Topological Sort": {
        "description": "Linear ordering of vertices in a Directed Acyclic Graph (DAG) using Kahn's algorithm (BFS with in-degree counting) or DFS post-order. Use when the problem involves task scheduling with prerequisites, dependency resolution, or detecting cycles in a directed graph — keywords: 'course schedule', 'prerequisites', 'build order'.",
        "use_cases": ["Course schedule", "Alien dictionary", "Build a matrix with conditions", "Sequence reconstruction"],
        "code": {
            "C++": """\
vector<int> inDegree(n, 0);
vector<vector<int>> adj(n);
for (auto& edge : edges) {
    adj[edge[0]].push_back(edge[1]);
    inDegree[edge[1]]++;
}

queue<int> q;
for (int i = 0; i < n; i++) {
    if (inDegree[i] == 0) q.push(i);
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
if (order.size() != n) return {}; // cycle detected
return order;
""",
            "Python": """\
from collections import deque

in_degree = [0] * n
adj = [[] for _ in range(n)]

for u, v in edges:
    adj[u].append(v)
    in_degree[v] += 1
    
q = deque([i for i in range(n) if in_degree[i] == 0])
order = []

while q:
    node = q.popleft()
    order.append(node)
    
    for neighbor in adj[node]:
        in_degree[neighbor] -= 1
        if in_degree[neighbor] == 0:
            q.append(neighbor)
            
if len(order) != n:
    return [] # cycle detected
return order
""",
            "Java": """\
int[] inDegree = new int[n];
List<List<Integer>> adj = new ArrayList<>();
for (int i = 0; i < n; i++) adj.add(new ArrayList<>());

for (int[] edge : edges) {
    adj.get(edge[0]).add(edge[1]);
    inDegree[edge[1]]++;
}

Queue<Integer> q = new LinkedList<>();
for (int i = 0; i < n; i++) {
    if (inDegree[i] == 0) q.offer(i);
}

List<Integer> order = new ArrayList<>();
while (!q.isEmpty()) {
    int node = q.poll();
    order.add(node);
    
    for (int neighbor : adj.get(node)) {
        inDegree[neighbor]--;
        if (inDegree[neighbor] == 0) q.offer(neighbor);
    }
}

if (order.size() != n) return new ArrayList<>(); // cycle detected
return order;
"""
        }
    }
}

PATTERN_NAMES = list(TEMPLATES.keys())
