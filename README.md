# Optimasi Rute Pipa Distribusi Air Bersih Berbasis Data OpenStreetMap Menggunakan Algoritma Prim dan Kruskal

Repository ini berisi implementasi *source code* Final Project mata kuliah **Desain dan Analisis Algoritma**. Program mengimplementasikan algoritma *Greedy* **Prim** (*Binary Min-Heap*, $O(E \log V)$) dan **Kruskal** (*Disjoint Set Union*, $O(E \log E)$) secara manual untuk mencari *Minimum Spanning Tree* (MST) pada peta jalan asli dari OpenStreetMap, sekaligus melakukan pengujian skalabilitas waktu eksekusi pada *Sparse Graph* dan *Dense Graph*.

## Anggota Kelompok
1. [Nama Lengkap Anggota 1] – [NIM]
2. [Nama Lengkap Anggota 2] – [NIM]
3. [Nama Lengkap Anggota 3] – [NIM]

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
   git clone [https://github.com/](https://github.com/)[username-kalian]/[nama-repository].git
   cd [nama-repository]
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
   python optimasi_pipa_air_osmnx.py
   ```

### Opsi 2: Menjalankan di Google Colab

1. Unggah file `optimasi_pipa_air_osmnx.py` (atau salin isinya ke sel kode baru di Google Colab).
2. Jalankan perintah instalasi berikut pada sel pertama:
   ```python
   !pip install osmnx networkx matplotlib
   ```
3. Jalankan skrip pada sel berikutnya:
   ```python
   !python optimasi_pipa_air_osmnx.py
   ```

---

## Mengubah Lokasi Studi Kasus
Untuk mengganti area perumahan yang diuji, ubah variabel `koordinat_surakarta` (format `(latitude, longitude)`) dan `radius_m` di dalam fungsi `jalankan_studi_kasus_pipa_air()` pada file `optimasi_pipa_air_osmnx.py`:

```python
koordinat_surakarta = (-7.5561, 110.8565)  # Ganti dengan koordinat lokasi pilihan
radius_m = 500                             # Radius area peta dalam meter
```

---

## Keluaran Program
Setelah eksekusi selesai, program akan menghasilkan:
1. **Ringkasan Terminal:** Jumlah simpul ($V$), jumlah ruas jalan ($E$), total panjang pipa sebelum dan sesudah optimasi MST, persentase penghematan biaya, serta tabel waktu eksekusi *benchmark* (dalam milidetik).
2. **`peta_pipa_air_mst.png`:** Visualisasi perbandingan peta jaringan jalan asli OpenStreetMap dengan rute pipa air optimal hasil MST.
3. **`benchmark_pipa_air.png`:** Grafik perbandingan waktu eksekusi empiris algoritma Prim dan Kruskal pada *Sparse Graph* dan *Dense Graph*.

---

## Daftar Pustaka

[1] T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, *Introduction to Algorithms*, 4th ed. Cambridge, MA, USA: MIT Press, 2022.

[2] J. Kleinberg and É. Tardos, *Algorithm Design*. Boston, MA, USA: Pearson Education, 2006.

[3] S. Dasgupta, C. H. Papadimitriou, and U. V. Vazirani, *Algorithms*. New York, NY, USA: McGraw-Hill, 2008.

[4] R. C. Prim, "Shortest connection networks and some generalizations," *The Bell System Technical Journal*, vol. 36, no. 6, pp. 1389–1401, Nov. 1957.

[5] J. B. Kruskal, "On the shortest spanning subtree of a graph and the traveling salesman problem," *Proceedings of the American Mathematical Society*, vol. 7, no. 1, pp. 48–50, Feb. 1956.

[6] G. Boeing, "OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks," *Computers, Environment and Urban Systems*, vol. 65, pp. 126–139, Sep. 2017.

[7] A. A. Hagberg, D. A. Schult, and P. J. Swart, "Exploring network structure, dynamics, and function using NetworkX," in *Proc. 7th Python in Science Conf. (SciPy 2008)*, Pasadena, CA, USA, 2008, pp. 11–15.