class DisjointSet:
    """
    Struktur data Disjoint Set Union (Union-Find) dengan optimasi
    Path Compression dan Union by Rank untuk deteksi siklus pada Kruskal.
    """

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, i: int) -> int:
        if self.parent[i] != i:
            # Path Compression: meratakan jalur menuju akar
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i == root_j:
            return False

        # Union by Rank: menggabungkan pohon lebih pendek ke pohon lebih tinggi
        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1

        return True
