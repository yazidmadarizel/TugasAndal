# Navigasi Robot di Gedung Berbentuk Rubik (3D Grid Pathfinding)

## Gambaran Umum
Proyek ini mengimplementasikan sistem navigasi robot dalam gedung berbentuk kubus Rubik 10x10x10 menggunakan algoritma **Breadth-First Search (BFS)** untuk menemukan jalur terpendek antara dua titik sambil menghindari rintangan (bom).

## Algoritma: Breadth-First Search (BFS)
Implementasi menggunakan BFS karena:

✔ **Menjamin jalur terpendek** pada grid tanpa bobot  
✔ **Eksplorasi level-per-level** memastikan optimalitas  
✔ **Efisien untuk ruang terbatas** (grid 10x10x10)  
✔ **Implementasi sederhana** menggunakan struktur data antrian  

## Fitur Utama
- Pemodelan gedung 3D menggunakan array numpy
- Beberapa skenario pengujian (pabrik, apartemen, mall)
- Visualisasi 3D dengan matplotlib
- Pengecekan validasi posisi
- Penghindaran rintangan (bom)

## Detail Implementasi
### Sistem Pergerakan
Robot dapat bergerak dalam 6 arah dasar:
- Atas/Bawah (sumbu Z)
- Kiri/Kanan (sumbu X)
- Depan/Belakang (sumbu Y)

### Struktur Data
- **Array numpy 3D** untuk representasi gedung
- **Antrian (queue)** untuk implementasi BFS
- **Dictionary** untuk rekonstruksi jalur

## Potensi Pengembangan
1. **Algoritma Alternatif**:
   - A* dengan heuristik jarak Manhattan 3D
   - Dijkstra untuk pergerakan berbobot

2. **Peningkatan Pergerakan**:
   - Gerakan diagonal
   - Biaya pergerakan variabel

3. **Optimasi Memori**:
   - BFS dua arah
   - Priority queue untuk jalur berbobot

## Mengapa BFS Optimal untuk Kasus Ini
| Algoritma | Kelebihan | Kekurangan |
|-----------|----------|------------|
| **BFS** | Jalur terpendek terjamin, implementasi sederhana | Boros memori untuk ruang besar |
| DFS | Hemat memori | Tidak menjamin jalur terpendek |
| Dijkstra | Mendukung bobot edge | Berlebihan untuk grid tanpa bobot |
| A* | Lebih cepat untuk ruang besar | Overhead heuristik untuk grid kecil |

Untuk ruang terbatas 10x10x10 ini, BFS memberikan keseimbangan terbaik antara kesederhanaan dan performa.

## Cara Penggunaan
1. Definisikan layout gedung dan rintangan
2. Tentukan posisi awal dan tujuan
3. Jalankan algoritma BFS
4. Visualisasikan jalur dalam 3D

## Contoh Skenario Uji
1. Gedung dasar
2. Skenario pabrik
3. Kompleks apartemen
4. Layout pusat perbelanjaan

## Kesimpulan
Implementasi ini menyediakan solusi efisien untuk pencarian jalur 3D dalam ruang terbatas menggunakan BFS. Algoritma ini menjamin jalur optimal sambil mempertahankan visualisasi yang jelas dan kemampuan pengujian yang fleksibel.

Untuk ruang pencarian lebih besar atau pergerakan dengan biaya kompleks, pertimbangkan untuk beralih ke algoritma A* atau Dijkstra.
