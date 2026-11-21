from typing import List, Tuple
from src.algorithms.disjoint_set import DisjointSet

Edge = Tuple[int, int, float]


def kruskal_mst(num_vertices: int, edges: List[Edge]) -> Tuple[List[Edge], float]:
    """
    Algoritma Kruskal menggunakan Edge List dan Disjoint Set Union.
    Kompleksitas Waktu : O(E log E)
    Kompleksitas Ruang : O(V + E)
    """
    sorted_edges = sorted(edges, key=lambda edge: edge[2])
    dsu = DisjointSet(num_vertices)

    mst_edges: List[Edge] = []
    total_weight = 0.0

    for u, v, weight in sorted_edges:
        if dsu.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight
            if len(mst_edges) == num_vertices - 1:
                break

    return mst_edges, total_weight
