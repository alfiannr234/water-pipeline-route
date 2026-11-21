from typing import Dict, List, Tuple
import networkx as nx
import osmnx as ox


def load_osm_water_graph(
    center_point: Tuple[float, float],
    radius_meter: int = 500,
    network_type: str = "all",
):
    """
    Mengunduh peta jaringan jalan dari OpenStreetMap lalu membersihkannya
    menjadi graf tak berarah sederhana yang terhubung penuh
    (Largest Connected Component).
    """
    print(
        f"Mengunduh peta OpenStreetMap radius {radius_meter}m ({network_type}) dari {center_point}..."
    )
    g_raw = ox.graph_from_point(
        center_point, dist=radius_meter, network_type=network_type
    )

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


def nearest_node_index(
    g_clean, idx_to_osm: Dict[int, int], lat: float, lon: float
) -> int:
    """Indeks simpul graf yang paling dekat (jarak haversine) dengan koordinat (lat, lon)."""
    import math

    def haversine(lat1, lon1, lat2, lon2):
        r = 6371000.0
        p1, p2 = math.radians(lat1), math.radians(lat2)
        dp, dl = p2 - p1, math.radians(lon2 - lon1)
        a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
        return 2 * r * math.asin(math.sqrt(a))

    return min(
        idx_to_osm,
        key=lambda i: haversine(
            lat,
            lon,
            g_clean.nodes[idx_to_osm[i]]["y"],
            g_clean.nodes[idx_to_osm[i]]["x"],
        ),
    )
