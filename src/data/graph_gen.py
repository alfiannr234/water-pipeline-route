import random
from typing import List, Tuple


def generate_connected_graph(
    num_vertices: int,
    density_type: str = "sparse",
) -> Tuple[List[Tuple[int, int, float]], List[List[Tuple[int, float]]]]:
    """
    Membangkitkan graf terhubung acak dengan dua kategori kepadatan:
    - sparse: E ≈ 1.5 * V (menyerupai kepadatan jaringan jalan permukiman OSM)
    - dense : E ≈ 40% dari total kemungkinan sisi maksimum V*(V-1)/2
    """
    edges: List[Tuple[int, int, float]] = []
    edge_set = set()

    # Langkah 1: Bentuk Spanning Tree dasar agar graf dijamin terhubung
    for i in range(1, num_vertices):
        parent = random.randint(0, i - 1)
        weight = random.uniform(10.0, 200.0)
        edges.append((parent, i, weight))
        edge_set.add((min(parent, i), max(parent, i)))

    # Langkah 2: Tambahkan sisi acak hingga mencapai target kepadatan
    if density_type == "sparse":
        target_edges = int(num_vertices * 1.5)
    elif density_type == "dense":
        target_edges = int((num_vertices * (num_vertices - 1) // 2) * 0.4)
    else:
        raise ValueError("density_type harus 'sparse' atau 'dense'.")

    while len(edges) < target_edges:
        u = random.randint(0, num_vertices - 1)
        v = random.randint(0, num_vertices - 1)
        if u != v:
            pair = (min(u, v), max(u, v))
            if pair not in edge_set:
                edge_set.add(pair)
                edges.append((u, v, random.uniform(10.0, 200.0)))

    adj_list: List[List[Tuple[int, float]]] = [[] for _ in range(num_vertices)]
    for u, v, w in edges:
        adj_list[u].append((v, w))
        adj_list[v].append((u, w))

    return edges, adj_list
