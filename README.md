# Optimasi Rute Pipa Distribusi Air Bersih Berbasis Data OpenStreetMap Menggunakan Algoritma Prim dan Kruskal

<<<<<<< HEAD
Repository ini berisi implementasi *source code* Final Project mata kuliah **Desain dan Analisis Algoritma**. Program mengimplementasikan algoritma *Greedy* **Prim** versi *Binary Min-Heap* (O(E log V)), **Prim** versi larik (O(V²)), dan **Kruskal** (*Disjoint Set Union*, O(E log E)) secara manual untuk mencari *Minimum Spanning Tree* (MST) pada peta jalan asli dari OpenStreetMap, sekaligus melakukan pengujian skalabilitas waktu eksekusi pada *Sparse Graph* dan *Dense Graph*.

## Anggota Kelompok
1.  Rasyid Yusuf Sugiyono   – L0125028
2.  Miftahul Habibi         – L0125084
3.  Alffian Naufal Rabbani  – L0125125 
=======
Repository ini berisi implementasi *source code* Final Project mata kuliah **Desain dan Analisis Algoritma**. Program mengimplementasikan algoritma *Greedy* **Prim** (*Binary Min-Heap*, O(E \log V)) dan **Kruskal** (*Disjoint Set Union*, O(E \log E)) secara manual untuk mencari *Minimum Spanning Tree* (MST) pada peta jalan asli dari OpenStreetMap, sekaligus melakukan pengujian skalabilitas waktu eksekusi pada *Sparse Graph* dan *Dense Graph*.

## Anggota Kelompok
1.  Rasyid Yusuf Sugiyono   – L0125028
2.  Miftahul Habibi 		    – L0125084
3. [Nama Lengkap Anggota 3] – [NIM] 
>>>>>>> 55047fa77362a19638e95a364840cb5360463229

---

## Prasyarat Sistem
* **Python 3.8** atau versi lebih baru.
* **Koneksi internet aktif** (diperlukan saat pertama kali mengunduh data jaringan jalan dari server OpenStreetMap).
* Pustaka Python: `osmnx`, `networkx`, dan `matplotlib`.

---

## Cara Menjalankan Program

### Opsi 1: Menjalankan di Komputer Lokal (VS Code / Terminal)

1. **Clone atau unduh repository ini:**
   ```bash
   git clone https://github.com/alfiannr234/water-pipeline-route.git
   cd water-pipeline-route
   ```

2. **(Opsional) Buat dan aktifkan *virtual environment*:**
   ```bash
   python -m venv venv
   # Untuk Windows:
   venv\Scripts\activate
   # Untuk macOS/Linux:
   source venv/bin/activate
   ```

3. **Instal pustaka yang dibutuhkan:**
   ```bash
   pip install osmnx networkx matplotlib
   ```

4. **Jalankan skrip utama:**
   ```bash
   python main.py              # studi kasus OSM + benchmark (5 pengulangan)
   python main.py --repeats 10 # jumlah pengulangan lain
   python main.py --skip-osm   # benchmark saja, tanpa internet
   ```

### Opsi 2: Menjalankan di Google Colab

1. Clone repository ini di sel pertama: `!git clone https://github.com/alfiannr234/water-pipeline-route.git` lalu `%cd water-pipeline-route`.
2. Jalankan perintah instalasi berikut pada sel pertama:
   ```python
   !pip install osmnx networkx matplotlib
   ```
3. Jalankan skrip pada sel berikutnya:
   ```python
   !python main.py              # studi kasus OSM + benchmark (5 pengulangan)
   python main.py --repeats 10 # jumlah pengulangan lain
   python main.py --skip-osm   # benchmark saja, tanpa internet
   ```

---

## Mengubah Lokasi Studi Kasus
Semua pengaturan ada di bagian atas `main.py`:

```python
KOORDINAT_PUSAT = (-7.5561, 110.8565)   # titik pusat area (latitude, longitude)
KOORDINAT_SUMBER = KOORDINAT_PUSAT      # ganti dengan lokasi pipa induk/reservoir jika diketahui
SKENARIO_OSM = [(300, "all"), (500, "all"), (1000, "all"), (500, "drive")]  # (radius m, network_type)
BIAYA_PER_METER = 45000                 # harga satuan ILUSTRATIF, bukan harga resmi
```

Panjang MST tidak bergantung pada simpul sumber; simpul sumber hanya menentukan titik mulai Prim dan penanda di peta.

---

## Keluaran Program
Setelah eksekusi selesai, program menghasilkan:
1. **`results/tables/environment.json`** — spesifikasi perangkat uji (prosesor, RAM, OS, versi Python). Wajib dicantumkan di makalah.
2. **`results/tables/osm_case_study.csv`** — satu baris per skenario OSM: V, E, jumlah sisi penutup loop yang dibuang MST (E − V + 1), panjang semua ruas vs panjang MST, serta waktu dan memori ketiga algoritma.
3. **`results/tables/benchmark_results.csv`** — untuk setiap graf sintetis: median, minimum, dan maksimum waktu dari N pengulangan (urutan algoritma diacak tiap putaran, didahului pemanasan), memori puncak, dan penghitung struktural (jumlah *push* dan ukuran maksimum *heap* Prim, jumlah sisi yang diperiksa Kruskal).
4. **`results/figures/peta_pipa_air_mst.png`** — peta jaringan jalan OSM vs tata letak pipa MST (skenario radius 500 m, `all`).
5. **`results/figures/benchmark_prim_vs_kruskal.png`** — grafik waktu (median dengan batang galat min–maks) dan memori ketiga algoritma pada graf *sparse* dan *dense*.

---

## Daftar Pustaka

[1] T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, *Introduction to Algorithms*, 4th ed. Cambridge, MA, USA: MIT Press, 2022.

[2] J. Kleinberg and É. Tardos, *Algorithm Design*. Boston, MA, USA: Pearson Education, 2006.

[3] S. Dasgupta, C. H. Papadimitriou, and U. V. Vazirani, *Algorithms*. New York, NY, USA: McGraw-Hill, 2008.

[4] R. C. Prim, "Shortest connection networks and some generalizations," *The Bell System Technical Journal*, vol. 36, no. 6, pp. 1389–1401, Nov. 1957.

[5] J. B. Kruskal, "On the shortest spanning subtree of a graph and the traveling salesman problem," *Proceedings of the American Mathematical Society*, vol. 7, no. 1, pp. 48–50, Feb. 1956.

[6] G. Boeing, "OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks," *Computers, Environment and Urban Systems*, vol. 65, pp. 126–139, Sep. 2017.

[7] A. A. Hagberg, D. A. Schult, and P. J. Swart, "Exploring network structure, dynamics, and function using NetworkX," in *Proc. 7th Python in Science Conf. (SciPy 2008)*, Pasadena, CA, USA, 2008, pp. 11–15.
