from typing import List, Tuple

AdjList = List[List[Tuple[int, float]]]
Edge = Tuple[int, int, float]


def prim_array_mst(
    num_vertices: int, adj_list: AdjList, start: int = 0
) -> Tuple[List[Edge], float]:
    """
    Algoritma Prim versi larik (array-based), tanpa heap.
    Setiap iterasi memilih simpul di luar pohon dengan key terkecil melalui
    pemindaian linear, lalu memperbarui key tetangganya.
    Kompleksitas Waktu : O(V^2 + E) = O(V^2)  -> optimal untuk graf padat (E = Θ(V^2))
    Kompleksitas Ruang : O(V)  (di luar graf masukan)
    """
    inf = float("inf")
    key = [inf] * num_vertices
    parent = [-1] * num_vertices
    key[start] = 0.0
    remaining = set(range(num_vertices))

    mst_edges: List[Edge] = []
    total_weight = 0.0

    while remaining:
        # Pemindaian linear O(V): cari simpul dengan key terkecil
        u = min(remaining, key=key.__getitem__)
        if key[u] == inf:
            break  # graf tidak terhubung
        remaining.remove(u)
        total_weight += key[u]
        if parent[u] != -1:
            mst_edges.append((parent[u], u, key[u]))

        for neighbor, edge_weight in adj_list[u]:
            if neighbor in remaining and edge_weight < key[neighbor]:
                key[neighbor] = edge_weight
                parent[neighbor] = u

    return mst_edges, total_weight
