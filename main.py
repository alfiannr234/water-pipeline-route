import argparse
import random

from src.algorithms.kruskal import kruskal_mst
from src.algorithms.prim import prim_mst
from src.algorithms.prim_array import prim_array_mst
from src.evaluation.benchmark import (
    collect_environment,
    measure_algorithm,
    run_scalability_benchmark,
    save_aligned_table,
    save_environment,
    save_osm_summary_csv,
)
from src.evaluation.visualizer import plot_benchmark_results, plot_osm_mst

# Titik pusat kawasan permukiman di Kecamatan Jebres, Surakarta
KOORDINAT_PUSAT = (-7.5561, 110.8565)

# Lokasi simpul sumber (pipa induk / reservoir). Jika lokasi sebenarnya diketahui,
# ganti dengan koordinat tersebut. Panjang MST TIDAK bergantung pada simpul awal;
# pilihan ini hanya memengaruhi titik mulai penelusuran Prim dan penanda di peta.
KOORDINAT_SUMBER = KOORDINAT_PUSAT

# Skenario studi kasus: (radius meter, network_type OSMnx)
SKENARIO_OSM = [(300, "all"), (500, "all"), (1000, "all"), (500, "drive")]
SKENARIO_PETA = (500, "all")  # skenario yang divisualisasikan sebagai Gambar 1

# Harga satuan ILUSTRATIF (bukan harga resmi), Rp per meter pipa terpasang
BIAYA_PER_METER = 45000


def run_osm_case_study(repeats: int) -> None:
    from src.data.osm_loader import load_osm_water_graph, nearest_node_index

    print("=== 1. STUDI KASUS: TATA LETAK PIPA MINIMUM BERBASIS OPENSTREETMAP ===")
    rows = []
    for radius_m, net_type in SKENARIO_OSM:
        g_clean, idx_to_osm, edges, adj_list = load_osm_water_graph(
            KOORDINAT_PUSAT, radius_m, net_type
        )
        num_v, num_e = len(idx_to_osm), len(edges)
        src = nearest_node_index(g_clean, idx_to_osm, *KOORDINAT_SUMBER)

        metrics = {
            "prim_heap": measure_algorithm(
                prim_mst, num_v, adj_list, src, repeats=repeats
            ),
            "prim_array": measure_algorithm(
                prim_array_mst, num_v, adj_list, src, repeats=repeats
            ),
            "kruskal": measure_algorithm(kruskal_mst, num_v, edges, repeats=repeats),
        }
        mst_kruskal, total_mst = metrics["kruskal"]["result"]
        for name, m in metrics.items():
            assert abs(m["result"][1] - total_mst) < 1e-6, f"Total {name} berbeda!"

        total_raw = sum(w for _, _, w in edges)
        selisih = total_raw - total_mst
        row = {
            "Skenario": f"{radius_m}m ({net_type})",
            "V": num_v,
            "E": num_e,
            "E/V": round(num_e / num_v, 2),
            "Loop_Dibuang": num_e - (num_v - 1),
            "Total_Ruas_m": round(total_raw, 2),
            "MST_m": round(total_mst, 2),
            "Selisih_persen": round(selisih / total_raw * 100.0, 2),
            "Biaya_MST_Rp": f"{round(total_mst * BIAYA_PER_METER):,}",
        }
        for name, m in metrics.items():
            row[f"{name}_ms"] = round(m["time_ms"], 2)
            row[f"{name}_kb"] = round(m["peak_kb"], 2)
        rows.append(row)
        print("  " + ", ".join(f"{k}={v}" for k, v in row.items()))

        if (radius_m, net_type) == SKENARIO_PETA:
            plot_osm_mst(
                g_clean=g_clean,
                idx_to_osm=idx_to_osm,
                all_edges=edges,
                mst_edges=mst_kruskal,
                total_raw=total_raw,
                total_mst=total_mst,
                save_path="results/figures/peta_pipa_air_mst.png",
                source_idx=src,
            )

    save_osm_summary_csv(rows, "results/tables/osm_case_study.csv")
    save_aligned_table(rows, "results/tables/osm_case_study_rapi.txt")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Optimasi rute pipa air: Prim vs Kruskal"
    )
    parser.add_argument(
        "--repeats", type=int, default=5, help="jumlah pengulangan pengukuran waktu"
    )
    parser.add_argument(
        "--skip-osm",
        action="store_true",
        help="lewati studi kasus OSM (tanpa internet)",
    )
    args = parser.parse_args()

    env = collect_environment()
    print("Perangkat uji:", env)
    save_environment(env, "results/tables/environment.json")

    random.seed(42)  # Menjamin graf sintetis bersifat reproducible

    if not args.skip_osm:
        run_osm_case_study(args.repeats)

    ukuran_simpul = [200, 500, 1000, 1500, 2000]
    benchmark_results = run_scalability_benchmark(
        vertex_sizes=ukuran_simpul,
        output_csv_path="results/tables/benchmark_results.csv",
        repeats=args.repeats,
    )
    plot_benchmark_results(
        results=benchmark_results,
        vertex_sizes=ukuran_simpul,
        save_path="results/figures/benchmark_prim_vs_kruskal.png",
    )


if __name__ == "__main__":
    main()
