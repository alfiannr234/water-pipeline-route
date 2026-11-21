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
    source_idx: int = 0,
) -> None:
    """Menyimpan visualisasi peta jaringan jalan OSM vs rute pipa MST optimal."""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    num_v = len(idx_to_osm)
    persen_hemat = ((total_raw - total_mst) / total_raw) * 100.0

    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    titles = [
        f"Peta Jaringan Jalan Asli OSM (Kandidat)\n"
        f"V = {num_v} | E = {len(all_edges)} | Total = {total_raw:,.1f} m",
        f"Tata Letak Pipa Minimum (Minimum Spanning Tree)\n"
        f"V = {num_v} | E = {len(mst_edges)} | Total = {total_mst:,.1f} m ({persen_hemat:.1f}% lebih pendek dari total ruas jalan)",
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
                g_clean.nodes[idx_to_osm[source_idx]]["x"],
                g_clean.nodes[idx_to_osm[source_idx]]["y"],
            )
            ax.scatter(
                x0, y0, color="#d63031", s=70, zorder=3, label="Simpul Sumber (asumsi)"
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


LABELS = {
    "prim_heap": ("Prim heap O(E log V)", "o"),
    "prim_array": ("Prim larik O(V²)", "^"),
    "kruskal": ("Kruskal O(E log E)", "s"),
}


def plot_benchmark_results(results, vertex_sizes: List[int], save_path: str) -> None:
    """
    Grafik 2x2: waktu eksekusi (median, batang galat = min-maks) di baris atas
    dan memori puncak di baris bawah, untuk Sparse & Dense Graph.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    for col, density in enumerate(["sparse", "dense"]):
        ax_time, ax_mem = axes[0, col], axes[1, col]
        for name, (label, marker) in LABELS.items():
            r = results[density][name]
            lower = [m - lo for m, lo in zip(r["med"], r["min"])]
            upper = [hi - m for m, hi in zip(r["med"], r["max"])]
            ax_time.errorbar(
                vertex_sizes,
                r["med"],
                yerr=[lower, upper],
                marker=marker,
                linewidth=2,
                capsize=4,
                label=label,
            )
            ax_mem.plot(
                vertex_sizes,
                r["kb"],
                marker=marker,
                linewidth=2,
                linestyle="--",
                label=label,
            )

        ax_time.set_title(
            f"Waktu Eksekusi (median): {density.upper()} Graph", fontweight="bold"
        )
        ax_time.set_ylabel("Waktu Eksekusi (ms)")
        ax_mem.set_title(f"Memori Puncak: {density.upper()} Graph", fontweight="bold")
        ax_mem.set_ylabel("Memori Puncak (KB)")
        for ax in (ax_time, ax_mem):
            ax.set_xlabel("Jumlah Simpul (V)")
            ax.legend()
            ax.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close(fig)
    print(f"-> Grafik benchmark disimpan ke '{save_path}'")
