"""
Penghitung struktural (tidak bergantung perangkat) untuk menjelaskan
perbedaan waktu dan memori antaralgoritma:
- jumlah operasi push dan ukuran maksimum heap pada Prim lazy
- jumlah sisi terurut yang diperiksa Kruskal sebelum berhenti dini
"""

import heapq
from typing import Dict, List, Tuple

from src.algorithms.disjoint_set import DisjointSet


def prim_heap_counts(num_vertices: int, adj_list, start: int = 0) -> Dict[str, int]:
    visited = [False] * num_vertices
    heap: List[Tuple[float, int]] = [(0.0, start)]
    pushes, max_heap, count = 1, 1, 0
    while heap and count < num_vertices:
        _, u = heapq.heappop(heap)
        if visited[u]:
            continue
        visited[u] = True
        count += 1
        for v, w in adj_list[u]:
            if not visited[v]:
                heapq.heappush(heap, (w, v))
                pushes += 1
                if len(heap) > max_heap:
                    max_heap = len(heap)
    return {"prim_pushes": pushes, "prim_max_heap": max_heap}


def kruskal_scan_count(num_vertices: int, edges) -> Dict[str, int]:
    dsu = DisjointSet(num_vertices)
    taken, scanned = 0, 0
    for u, v, _ in sorted(edges, key=lambda e: e[2]):
        scanned += 1
        if dsu.union(u, v):
            taken += 1
            if taken == num_vertices - 1:
                break
    return {"kruskal_edges_scanned": scanned}
