import heapq
from typing import List, Tuple

AdjList = List[List[Tuple[int, float]]]
Edge = Tuple[int, int, float]


def prim_mst(
    num_vertices: int, adj_list: AdjList, start: int = 0
) -> Tuple[List[Edge], float]:
    """
    Algoritma Prim (versi lazy) menggunakan Adjacency List dan Binary Min-Heap.
    Setiap sisi dimasukkan ke heap paling banyak satu kali, yaitu saat ujung
    yang lebih dahulu dikunjungi diproses; entri usang dilewati saat di-pop.
    Kompleksitas Waktu : O(E log E) = O(E log V)
    Kompleksitas Ruang : O(V + E)
    """
    visited = [False] * num_vertices
    # Tuple di heap: (bobot, simpul_tujuan, simpul_asal)
    min_heap: List[Tuple[float, int, int]] = [(0.0, start, -1)]

    mst_edges: List[Edge] = []
    total_weight = 0.0
    visited_count = 0

    while min_heap and visited_count < num_vertices:
        weight, u, parent = heapq.heappop(min_heap)
        if visited[u]:
            continue

        visited[u] = True
        total_weight += weight
        visited_count += 1

        if parent != -1:
            mst_edges.append((parent, u, weight))

        for neighbor, edge_weight in adj_list[u]:
            if not visited[neighbor]:
                heapq.heappush(min_heap, (edge_weight, neighbor, u))

    return mst_edges, total_weight
