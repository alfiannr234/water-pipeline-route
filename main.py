import random

from src.algorithms.kruskal import kruskal_mst
from src.algorithms.prim import prim_mst
from src.data.osm_loader import load_osm_water_graph
from src.evaluation.benchmark import (
    measure_algorithm,
    run_scalability_benchmark,
    save_osm_summary_csv,
)
from src.evaluation.visualizer import plot_benchmark_results, plot_osm_mst


def run_osm_case_study() -> None:
    print("=== 1. STUDI KASUS RIIL: OPTIMASI PIPA AIR BERBASIS OPENSTREETMAP ===")
    # Koordinat contoh kawasan permukiman di Jebres, Surakarta (ubah sesuai target wilayah)
    koordinat_pusat = (-7.5561, 110.8565)
    radius_m = 500
    biaya_per_meter = 45000  # Asumsi pengadaan & instalasi pipa distribusi Rp 45.000/m

    g_clean, idx_to_osm, edges, adj_list = load_osm_water_graph(
        koordinat_pusat, radius_m
    )
    num_v = len(idx_to_osm)
    num_e = len(edges)

    p_metrics = measure_algorithm(prim_mst, num_v, adj_list)
    k_metrics = measure_algorithm(kruskal_mst, num_v, edges)

    mst_prim, total_prim = p_metrics["result"]
    mst_kruskal, total_kruskal = k_metrics["result"]

    assert (
        abs(total_prim - total_kruskal) < 1e-6
    ), "Error: Total panjang Prim & Kruskal berbeda!"

    total_raw = sum(w for _, _, w in edges)
    penghematan_m = total_raw - total_kruskal
    persen_hemat = (penghematan_m / total_raw) * 100.0

    summary = {
        "Koordinat_Pusat": str(koordinat_pusat),
        "Radius_Meter": radius_m,
        "Jumlah_Simpul_V": num_v,
        "Jumlah_Sisi_Kandidat_E": num_e,
        "Jumlah_Sisi_MST": len(mst_kruskal),
        "Panjang_Jalan_Total_m": round(total_raw, 2),
        "Panjang_Pipa_MST_m": round(total_kruskal, 2),
        "Penghematan_Panjang_m": round(penghematan_m, 2),
        "Persentase_Penghematan_%": round(persen_hemat, 2),
        "Estimasi_Biaya_Awal_Rp": round(total_raw * biaya_per_meter),
        "Estimasi_Biaya_MST_Rp": round(total_kruskal * biaya_per_meter),
        "Penghematan_Biaya_Rp": round(penghematan_m * biaya_per_meter),
        "Prim_Time_ms": round(p_metrics["time_ms"], 4),
        "Kruskal_Time_ms": round(k_metrics["time_ms"], 4),
        "Prim_Memory_KB": round(p_metrics["peak_kb"], 2),
        "Kruskal_Memory_KB": round(k_metrics["peak_kb"], 2),
    }

    for key, val in summary.items():
        print(f"  {key:<28}: {val}")

    save_osm_summary_csv(summary, "results/tables/osm_case_study.csv")
    plot_osm_mst(
        g_clean=g_clean,
        idx_to_osm=idx_to_osm,
        all_edges=edges,
        mst_edges=mst_kruskal,
        total_raw=total_raw,
        total_mst=total_kruskal,
        save_path="results/figures/peta_pipa_air_mst.png",
    )


def main() -> None:
    random.seed(42)  # Menjamin hasil pengujian bersifat reproducible

    # Tahap 1: Eksperimen Peta Riil OpenStreetMap
    run_osm_case_study()

    # Tahap 2: Uji Skalabilitas Waktu & Memori (Sparse vs Dense Graph)
    ukuran_simpul = [200, 500, 1000, 1500, 2000]
    benchmark_results = run_scalability_benchmark(
        vertex_sizes=ukuran_simpul,
        output_csv_path="results/tables/benchmark_results.csv",
    )
    plot_benchmark_results(
        results=benchmark_results,
        vertex_sizes=ukuran_simpul,
        save_path="results/figures/benchmark_prim_vs_kruskal.png",
    )


if __name__ == "__main__":
    main()
