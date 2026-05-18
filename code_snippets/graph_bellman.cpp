// Алгоритм Беллмана-Форда (динамическое программирование)
vector<int> bellmanFord(vector<vector<pair<int,int>>>& graph, int src, int n) {
    const int INF = 1e9;
    vector<int> dist(n, INF);
    dist[src] = 0;
    for (int i = 0; i < n-1; i++) {
        for (int u = 0; u < n; u++) {
            for (auto& edge : graph[u]) {
                int v = edge.first, w = edge.second;
                if (dist[u] != INF && dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                }
            }
        }
    }
    return dist;
}
