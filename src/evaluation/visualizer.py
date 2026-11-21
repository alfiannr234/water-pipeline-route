import os
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt


def plot_osm_mst(
    g_clean,
    idx_to_osm: Dict[int, int],
    all_edges: List[Tuple[int, int, float]],
    mst_edges: List[Tuple[int, int, float]],
    total_raw: float,
    total_mst: float,
    save_path: str,
) -> None:
    """Menyimpan visualisasi peta jaringan jalan OSM vs rute pipa MST optimal."""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    num_v = len(idx_to_osm)
    persen_hemat = ((total_raw - total_mst) / total_raw) * 100.0

    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    titles = [
        f"Peta Jaringan Jalan Asli OSM (Kandidat)\n"
        f"V = {num_v} | E = {len(all_edges)} | Total = {total_raw:,.1f} m",
        f"Rute Pipa Air Optimal (Minimum Spanning Tree)\n"
        f"V = {num_v} | E = {len(mst_edges)} | Total = {total_mst:,.1f} m (Hemat {persen_hemat:.1f}%)",
    ]

    for idx, ax in enumerate(axes):
        for u, v, _ in all_edges:
            x1, y1 = (
                g_clean.nodes[idx_to_osm[u]]["x"],
                g_clean.nodes[idx_to_osm[u]]["y"],
            )
            x2, y2 = (
                g_clean.nodes[idx_to_osm[v]]["x"],
                g_clean.nodes[idx_to_osm[v]]["y"],
            )
            color = "#7f8c8d" if idx == 0 else "#dfe6e9"
            lw = 1.2 if idx == 0 else 0.9
            ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, zorder=1)

        if idx == 1:
            for u, v, _ in mst_edges:
                x1, y1 = (
                    g_clean.nodes[idx_to_osm[u]]["x"],
                    g_clean.nodes[idx_to_osm[u]]["y"],
                )
                x2, y2 = (
                    g_clean.nodes[idx_to_osm[v]]["x"],
                    g_clean.nodes[idx_to_osm[v]]["y"],
                )
                ax.plot([x1, x2], [y1, y2], color="#0984e3", linewidth=2.2, zorder=2)

            x0, y0 = (
                g_clean.nodes[idx_to_osm[0]]["x"],
                g_clean.nodes[idx_to_osm[0]]["y"],
            )
            ax.scatter(
                x0, y0, color="#d63031", s=70, zorder=3, label="Titik Awal / Sumber Air"
            )
            ax.legend(loc="upper right")

        ax.set_title(titles[idx], fontsize=11, fontweight="bold")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_aspect("equal")
        ax.grid(True, linestyle="--", alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close(fig)
    print(f"-> Visualisasi peta OSM disimpan ke '{save_path}'")


def plot_benchmark_results(
    results: Dict[str, Dict[str, List[float]]],
    vertex_sizes: List[int],
    save_path: str,
) -> None:
    """
    Menyimpan grafik 2x2: perbandingan Waktu Eksekusi (baris atas)
    dan Penggunaan Memori Puncak (baris bawah) untuk Sparse & Dense Graph.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    densities = ["sparse", "dense"]

    for col, density in enumerate(densities):
        # Baris 0: Waktu Eksekusi (ms)
        ax_time = axes[0, col]
        ax_time.plot(
            vertex_sizes,
            results[density]["prim_ms"],
            marker="o",
            linewidth=2,
            label="Prim O(E log V)",
        )
        ax_time.plot(
            vertex_sizes,
            results[density]["kruskal_ms"],
            marker="s",
            linewidth=2,
            label="Kruskal O(E log E)",
        )
        ax_time.set_title(f"Waktu Eksekusi: {density.upper()} Graph", fontweight="bold")
        ax_time.set_xlabel("Jumlah Simpul (V)")
        ax_time.set_ylabel("Waktu Eksekusi (ms)")
        ax_time.legend()
        ax_time.grid(True, linestyle="--", alpha=0.4)

        # Baris 1: Penggunaan Memori Puncak (KB)
        ax_mem = axes[1, col]
        ax_mem.plot(
            vertex_sizes,
            results[density]["prim_kb"],
            marker="o",
            linewidth=2,
            linestyle="--",
            label="Prim (Min-Heap)",
        )
        ax_mem.plot(
            vertex_sizes,
            results[density]["kruskal_kb"],
            marker="s",
            linewidth=2,
            linestyle="--",
            label="Kruskal (Edge List + DSU)",
        )
        ax_mem.set_title(f"Memori Puncak: {density.upper()} Graph", fontweight="bold")
        ax_mem.set_xlabel("Jumlah Simpul (V)")
        ax_mem.set_ylabel("Memori Puncak (KB)")
        ax_mem.legend()
        ax_mem.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close(fig)
    print(f"-> Grafik benchmark disimpan ke '{save_path}'")
