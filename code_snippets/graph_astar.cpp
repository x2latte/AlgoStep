// Алгоритм A* (эвристический)
int heuristic(int a, int b) { return 0; }

vector<int> aStar(vector<vector<pair<int,int>>>& graph, int src, int target, int n) {
    const int INF = 1e9;
    vector<int> g(n, INF), f(n, INF);
    vector<int> prev(n, -1);
    g[src] = 0;
    f[src] = heuristic(src, target);
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>> pq;
    pq.push({f[src], src});
    vector<bool> closed(n, false);
    while (!pq.empty()) {
        int u = pq.top().second;
        pq.pop();
        if (closed[u]) continue;
        closed[u] = true;
        if (u == target) break;
        for (auto& edge : graph[u]) {
            int v = edge.first, w = edge.second;
            int tentative_g = g[u] + w;
            if (tentative_g < g[v]) {
                prev[v] = u;
                g[v] = tentative_g;
                f[v] = g[v] + heuristic(v, target);
                pq.push({f[v], v});
            }
        }
    }
    return g;
}
