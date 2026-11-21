import csv
import gc
import json
import os
import platform
import random
import statistics
import sys
import time
import tracemalloc
from typing import Any, Callable, Dict, List

from src.algorithms.kruskal import kruskal_mst
from src.algorithms.prim import prim_mst
from src.algorithms.prim_array import prim_array_mst
from src.data.graph_gen import generate_connected_graph
from src.evaluation.instrument import kruskal_scan_count, prim_heap_counts

# Nama algoritma -> (fungsi, jenis masukan: "adj" atau "edges")
ALGORITHMS: Dict[str, tuple] = {
    "prim_heap": (prim_mst, "adj"),
    "prim_array": (prim_array_mst, "adj"),
    "kruskal": (kruskal_mst, "edges"),
}


def collect_environment() -> Dict[str, Any]:
    """Mencatat spesifikasi perangkat agar hasil benchmark dapat dilaporkan."""
    ram_gb = "unknown"
    try:
        ram_gb = round(
            os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1024**3, 1
        )
    except (ValueError, OSError, AttributeError):
        try:
            import psutil  # opsional, dipakai jika tersedia (mis. di Windows)

            ram_gb = round(psutil.virtual_memory().total / 1024**3, 1)
        except ImportError:
            pass
    return {
        "platform": platform.platform(),
        "processor": platform.processor() or platform.machine(),
        "cpu_count_logical": os.cpu_count(),
        "ram_gb": ram_gb,
        "python_version": sys.version.split()[0],
        "python_implementation": platform.python_implementation(),
    }


def measure_time_ms(func: Callable, *args) -> tuple:
    gc.collect()
    t0 = time.perf_counter()
    result = func(*args)
    return result, (time.perf_counter() - t0) * 1000.0


def measure_peak_kb(func: Callable, *args) -> float:
    gc.collect()
    tracemalloc.start()
    func(*args)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak / 1024.0


def measure_algorithm(func: Callable, *args, repeats: int = 5) -> Dict[str, Any]:
    """
    Dipakai pada studi kasus OSM: 1 putaran pemanasan, lalu `repeats` putaran
    pengukuran waktu (dilaporkan median/min/maks), lalu 1 putaran memori
    terpisah agar overhead tracemalloc tidak memengaruhi waktu.
    """
    func(*args)  # warm-up
    times = []
    result = None
    for _ in range(repeats):
        result, t = measure_time_ms(func, *args)
        times.append(t)
    return {
        "result": result,
        "time_ms": statistics.median(times),
        "time_min_ms": min(times),
        "time_max_ms": max(times),
        "peak_kb": measure_peak_kb(func, *args),
    }


def save_osm_summary_csv(rows: List[Dict[str, Any]], output_csv_path: str) -> None:
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"-> Ringkasan studi kasus OSM disimpan ke '{output_csv_path}'")


def save_environment(env: Dict[str, Any], path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(env, f, indent=2)
    print(f"-> Spesifikasi perangkat disimpan ke '{path}'")


def run_scalability_benchmark(
    vertex_sizes: List[int],
    output_csv_path: str,
    repeats: int = 5,
    order_seed: int = 2026,
) -> Dict[str, Dict[str, Dict[str, List[float]]]]:
    """
    Uji skalabilitas Prim (heap), Prim (larik), dan Kruskal pada Sparse & Dense Graph.
    - Graf dibangkitkan dengan modul `random` global (seed diatur di main.py).
    - Setiap graf: 1 putaran pemanasan per algoritma, lalu `repeats` putaran
      waktu dengan URUTAN ALGORITMA DIACAK tiap putaran (RNG terpisah agar
      pembangkitan graf tetap reproducible), lalu 1 putaran memori per algoritma.
    - Dilaporkan median, minimum, dan maksimum waktu.
    """
    print(
        f"\n=== 2. BENCHMARK SKALABILITAS ({repeats} pengulangan, median [min-maks]) ==="
    )
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    order_rng = random.Random(order_seed)

    results: Dict[str, Dict[str, Dict[str, List[float]]]] = {
        d: {a: {"med": [], "min": [], "max": [], "kb": []} for a in ALGORITHMS}
        for d in ["sparse", "dense"]
    }
    csv_rows = []

    for density in ["sparse", "dense"]:
        print(f"\nKategori: {density.upper()} GRAPH")
        for v in vertex_sizes:
            edges, adj_list = generate_connected_graph(v, density_type=density)
            inputs = {"adj": (v, adj_list), "edges": (v, edges)}

            times = {a: [] for a in ALGORITHMS}
            totals = {}
            for name, (func, kind) in ALGORITHMS.items():  # warm-up
                func(*inputs[kind])
            for _ in range(repeats):
                order = list(ALGORITHMS)
                order_rng.shuffle(order)
                for name in order:
                    func, kind = ALGORITHMS[name]
                    (_, total), t = measure_time_ms(func, *inputs[kind])
                    times[name].append(t)
                    totals[name] = total
            ref_total = totals["kruskal"]
            for name, total in totals.items():
                assert (
                    abs(total - ref_total) < 1e-6
                ), f"Total bobot {name} berbeda dari Kruskal!"

            row = {
                "Graph_Type": density,
                "Vertices_V": v,
                "Edges_E": len(edges),
                "Repeats": repeats,
            }
            for name, (func, kind) in ALGORITHMS.items():
                med, lo, hi = (
                    statistics.median(times[name]),
                    min(times[name]),
                    max(times[name]),
                )
                kb = measure_peak_kb(func, *inputs[kind])
                for key, val in (("med", med), ("min", lo), ("max", hi), ("kb", kb)):
                    results[density][name][key].append(val)
                row[f"{name}_ms_median"] = round(med, 4)
                row[f"{name}_ms_min"] = round(lo, 4)
                row[f"{name}_ms_max"] = round(hi, 4)
                row[f"{name}_peak_kb"] = round(kb, 2)
            row.update(prim_heap_counts(v, adj_list))
            row.update(kruskal_scan_count(v, edges))
            csv_rows.append(row)

            print(
                f"V={v:<5} E={len(edges):<7} | "
                + " | ".join(
                    f"{n}: {row[f'{n}_ms_median']:.3f} ms ({row[f'{n}_peak_kb']:.0f} KB)"
                    for n in ALGORITHMS
                )
            )

    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"\n-> Tabel hasil benchmark disimpan ke '{output_csv_path}'")
    return results
