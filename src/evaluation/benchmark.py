import csv
import gc
import os
import time
import tracemalloc
from typing import Any, Callable, Dict, List

from src.algorithms.kruskal import kruskal_mst
from src.algorithms.prim import prim_mst
from src.data.graph_gen import generate_connected_graph


def measure_algorithm(func: Callable, *args) -> Dict[str, Any]:
    """
    Mengukur waktu eksekusi (ms) dan memori puncak (KB) secara terpisah
    agar overhead tracemalloc tidak memengaruhi hasil waktu eksekusi.
    """
    # Putaran 1: Pengukuran Waktu Eksekusi Murni (ms)
    gc.collect()
    t0 = time.perf_counter()
    result = func(*args)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    # Putaran 2: Pengukuran Memori Puncak (KB)
    gc.collect()
    tracemalloc.start()
    _ = func(*args)
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "result": result,
        "time_ms": elapsed_ms,
        "peak_kb": peak_bytes / 1024.0,
    }


def save_osm_summary_csv(summary: Dict[str, Any], output_csv_path: str) -> None:
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Parameter", "Nilai"])
        for key, value in summary.items():
            writer.writerow([key, value])
    print(f"-> Ringkasan studi kasus OSM disimpan ke '{output_csv_path}'")


def run_scalability_benchmark(
    vertex_sizes: List[int],
    output_csv_path: str,
) -> Dict[str, Dict[str, List[float]]]:
    """
    Menjalankan uji skalabilitas Prim vs Kruskal pada Sparse & Dense Graph,
    menampilkan tabel di terminal, dan menyimpannya ke file CSV.
    """
    print("\n=== 2. BENCHMARK SKALABILITAS (WAKTU & MEMORI) ===")
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    results: Dict[str, Dict[str, List[float]]] = {
        "sparse": {"prim_ms": [], "kruskal_ms": [], "prim_kb": [], "kruskal_kb": []},
        "dense": {"prim_ms": [], "kruskal_ms": [], "prim_kb": [], "kruskal_kb": []},
    }
    csv_rows = []

    for density in ["sparse", "dense"]:
        print(f"\nKategori: {density.upper()} GRAPH")
        print(
            f"{'V':<8} | {'E':<10} | {'Prim (ms)':<12} | {'Kruskal (ms)':<12} "
            f"| {'Prim (KB)':<12} | {'Kruskal (KB)':<12}"
        )
        print("-" * 78)

        for v in vertex_sizes:
            edges, adj_list = generate_connected_graph(v, density_type=density)

            p_metrics = measure_algorithm(prim_mst, v, adj_list)
            k_metrics = measure_algorithm(kruskal_mst, v, edges)

            _, cost_p = p_metrics["result"]
            _, cost_k = k_metrics["result"]
            assert (
                abs(cost_p - cost_k) < 1e-6
            ), "Error: Total bobot Prim & Kruskal berbeda!"

            results[density]["prim_ms"].append(p_metrics["time_ms"])
            results[density]["kruskal_ms"].append(k_metrics["time_ms"])
            results[density]["prim_kb"].append(p_metrics["peak_kb"])
            results[density]["kruskal_kb"].append(k_metrics["peak_kb"])

            print(
                f"{v:<8} | {len(edges):<10} | {p_metrics['time_ms']:<12.4f} | "
                f"{k_metrics['time_ms']:<12.4f} | {p_metrics['peak_kb']:<12.2f} | "
                f"{k_metrics['peak_kb']:<12.2f}"
            )

            csv_rows.append(
                [
                    density,
                    v,
                    len(edges),
                    round(p_metrics["time_ms"], 4),
                    round(k_metrics["time_ms"], 4),
                    round(p_metrics["peak_kb"], 2),
                    round(k_metrics["peak_kb"], 2),
                ]
            )

    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Graph_Type",
                "Vertices_V",
                "Edges_E",
                "Prim_Time_ms",
                "Kruskal_Time_ms",
                "Prim_Memory_KB",
                "Kruskal_Memory_KB",
            ]
        )
        writer.writerows(csv_rows)

    print(f"\n-> Tabel hasil benchmark disimpan ke '{output_csv_path}'")
    return results
