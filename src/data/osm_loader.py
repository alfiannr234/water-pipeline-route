from typing import Dict, List, Tuple
import networkx as nx
import osmnx as ox


def load_osm_water_graph(
    center_point: Tuple[float, float],
    radius_meter: int = 500,
):
    """
    Mengunduh peta jaringan jalan dari OpenStreetMap lalu membersihkannya
    menjadi graf tak berarah sederhana yang terhubung penuh
    (Largest Connected Component).
    """
    print(f"Mengunduh peta OpenStreetMap radius {radius_meter}m dari {center_point}...")
    g_raw = ox.graph_from_point(center_point, dist=radius_meter, network_type="all")

    # Konversi MultiDiGraph -> Simple Undirected Graph
    g_undirected = nx.Graph()
    for node_id, data in g_raw.nodes(data=True):
        g_undirected.add_node(node_id, x=data["x"], y=data["y"])

    for u, v, data in g_raw.edges(data=True):
        if u == v:
            continue  # Abaikan self-loop
        length = float(data.get("length", 0.0))
        if g_undirected.has_edge(u, v):
            if length < g_undirected[u][v]["length"]:
                g_undirected[u][v]["length"] = length
        else:
            g_undirected.add_edge(u, v, length=length)

    # Ambil Largest Connected Component agar MST menjangkau seluruh simpul
    largest_cc = max(nx.connected_components(g_undirected), key=len)
    g_clean = g_undirected.subgraph(largest_cc).copy()

    nodes = list(g_clean.nodes())
    osm_to_idx: Dict[int, int] = {osm_id: idx for idx, osm_id in enumerate(nodes)}
    idx_to_osm: Dict[int, int] = {idx: osm_id for idx, osm_id in enumerate(nodes)}

    edges: List[Tuple[int, int, float]] = []
    adj_list: List[List[Tuple[int, float]]] = [[] for _ in range(len(nodes))]

    for u_osm, v_osm, data in g_clean.edges(data=True):
        u = osm_to_idx[u_osm]
        v = osm_to_idx[v_osm]
        w = data["length"]
        edges.append((u, v, w))
        adj_list[u].append((v, w))
        adj_list[v].append((u, w))

    return g_clean, idx_to_osm, edges, adj_list
