// Полный перебор (DFS) всех путей
void dfs(int v, int target, int curDist, vector<bool>& visited, vector<vector<pair<int,int>>>& graph, int& bestDist) {
    if (v == target) {
        if (curDist < bestDist) bestDist = curDist;
        return;
    }
    visited[v] = true;
    for (auto& edge : graph[v]) {
        int to = edge.first, w = edge.second;
        if (!visited[to]) {
            dfs(to, target, curDist + w, visited, graph, bestDist);
        }
    }
    visited[v] = false;
}

int bruteForceShortestPath(vector<vector<pair<int,int>>>& graph, int src, int target, int n) {
    int bestDist = INT_MAX;
    vector<bool> visited(n, false);
    dfs(src, target, 0, visited, graph, bestDist);
    return bestDist;
}
