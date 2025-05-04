from collections import deque
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class RubikBuilding:
    def __init__(self, size=10):
        # Inisialisasi gedung rubik ukuran 10x10x10 (koordinat 0-9)
        self.size = size
        self.building = np.zeros((size, size, size), dtype=int)
        self.bombs = []  # Simpan koordinat bom
    
    def add_bomb(self, x, y, z):
        """Tambahkan bom pada koordinat tertentu."""
        if 0 <= x < self.size and 0 <= y < self.size and 0 <= z < self.size:
            self.building[x, y, z] = 1  # Tandai sebagai bom
            self.bombs.append((x, y, z))
            return True
        return False
    
    def is_valid_position(self, x, y, z):
        """Cek apakah posisi valid (dalam gedung dan tidak ada bom)."""
        return (0 <= x < self.size and 
                0 <= y < self.size and 
                0 <= z < self.size and 
                self.building[x, y, z] != 1)
    
    def shortest_path(self, start, end):
        """
        Temukan jalur terpendek dari start ke end menggunakan BFS.
        
        Args:
            start: tuple (x, y, z) posisi awal
            end: tuple (x, y, z) posisi akhir
            
        Returns:
            list: Daftar koordinat yang membentuk jalur terpendek,
                 atau None jika tidak ada jalur yang ditemukan
        """
        if not self.is_valid_position(*start) or not self.is_valid_position(*end):
            return None
        
        # Arah pergerakan: (x, y, z) -> atas, bawah, kanan, kiri, depan, belakang
        directions = [
            (1, 0, 0), (-1, 0, 0),  # kanan, kiri
            (0, 1, 0), (0, -1, 0),  # depan, belakang
            (0, 0, 1), (0, 0, -1)   # atas, bawah
        ]
        
        # Inisialisasi queue untuk BFS
        queue = deque([start])
        visited = set([start])
        parent = {start: None}
        
        while queue:
            current = queue.popleft()
            
            # Jika sudah mencapai tujuan
            if current == end:
                # Rekonstruksi jalur
                path = []
                while current:
                    path.append(current)
                    current = parent[current]
                path.reverse()  # Kembalikan jalur dari awal ke akhir
                return path
            
            # Coba semua arah pergerakan yang mungkin
            for dx, dy, dz in directions:
                nx, ny, nz = current[0] + dx, current[1] + dy, current[2] + dz
                next_pos = (nx, ny, nz)
                
                # Cek apakah posisi ini valid dan belum dikunjungi
                if self.is_valid_position(nx, ny, nz) and next_pos not in visited:
                    queue.append(next_pos)
                    visited.add(next_pos)
                    parent[next_pos] = current
        
        # Tidak ada jalur yang ditemukan
        return None
    
    def visualize_path(self, path):
        """Visualisasikan jalur dalam gedung rubik."""
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot gedung
        ax.set_xlim([0, self.size])
        ax.set_ylim([0, self.size])
        ax.set_zlim([0, self.size])
        
        # Plot bom
        bomb_x, bomb_y, bomb_z = [], [], []
        for x, y, z in self.bombs:
            bomb_x.append(x)
            bomb_y.append(y)
            bomb_z.append(z)
        ax.scatter(bomb_x, bomb_y, bomb_z, color='red', marker='o', s=100, label='Bom')
        
        # Plot jalur
        if path:
            path_x, path_y, path_z = [], [], []
            for x, y, z in path:
                path_x.append(x)
                path_y.append(y)
                path_z.append(z)
            ax.plot(path_x, path_y, path_z, 'b-', linewidth=2, label='Jalur')
            
            # Plot titik awal dan akhir
            ax.scatter([path[0][0]], [path[0][1]], [path[0][2]], color='green', marker='^', s=100, label='Awal')
            ax.scatter([path[-1][0]], [path[-1][1]], [path[-1][2]], color='purple', marker='*', s=100, label='Akhir')
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Visualisasi Jalur Robot dalam Gedung Rubik')
        ax.legend()
        plt.tight_layout()
        plt.show()

# Contoh penggunaan
if __name__ == "__main__":
    # Inisialisasi gedung rubik 10x10x10
    building = RubikBuilding(size=10)
    
    # Tambahkan beberapa bom
    # Lantai 1 (z=0)
    building.add_bomb(2, 2, 0)
    building.add_bomb(2, 3, 0)
    building.add_bomb(3, 2, 0)
    
    # Lantai 2 (z=1)
    building.add_bomb(5, 5, 1)
    building.add_bomb(6, 5, 1)
    building.add_bomb(5, 6, 1)
    
    # Lantai 3 (z=2)
    building.add_bomb(7, 7, 2)
    building.add_bomb(8, 7, 2)
    building.add_bomb(7, 8, 2)
    
    # Lantai 4-6 memiliki dinding pemisah
    for z in range(3, 6):
        for x in range(4):
            for y in range(6, 10):
                building.add_bomb(x, y, z)
    
    # Lantai 7-9 memiliki pola bom tertentu
    for z in range(6, 9):
        if z % 2 == 0:  # Lantai genap
            for x in range(3, 7):
                for y in range(3, 7):
                    building.add_bomb(x, y, z)
        else:  # Lantai ganjil
            for x in range(2, 8, 5):  # 2 dan 7
                for y in range(2, 8):
                    building.add_bomb(x, y, z)
    
    # Tentukan posisi awal dan akhir
    start_pos = (0, 0, 0)  # Pojok kiri bawah
    end_pos = (9, 9, 9)    # Pojok kanan atas
    
    # Temukan jalur terpendek
    path = building.shortest_path(start_pos, end_pos)
    
    if path:
        print(f"Jalur terpendek ditemukan dengan {len(path)} langkah:")
        for i, (x, y, z) in enumerate(path):
            print(f"Langkah {i+1}: ({x}, {y}, {z})")
        
        # Visualisasi jalur
        building.visualize_path(path)
    else:
        print("Tidak ada jalur yang ditemukan dari posisi awal ke posisi akhir.")

# Membuat kasus uji lain
def test_case_pabrik():
    """
    Skenario: Robot di pabrik berlantai banyak dengan mesin berbahaya
    Robot harus bernavigasi dari pos pengisian daya ke titik inspeksi
    """
    print("\n--- Kasus Uji: Pabrik Berlantai Banyak ---")
    factory = RubikBuilding(size=10)
    
    # Tambahkan mesin berbahaya di berbagai lokasi
    # Lantai produksi (z=0,1,2)
    for z in range(3):
        # Mesin di tengah ruangan
        for x in range(3, 7):
            for y in range(3, 7):
                if not (x == 5 and y == 5):  # Biarkan jalur di tengah
                    factory.add_bomb(x, y, z)
    
    # Lantai penyimpanan (z=3,4)
    for z in range(3, 5):
        # Rak-rak penyimpanan
        for x in range(0, 10, 2):  # Rak di posisi genap
            for y in range(10):
                if y % 3 != 0:  # Biarkan jalur untuk lewat
                    factory.add_bomb(x, y, z)
    
    # Lantai kantor (z=5,6)
    # Ruangan kantor dengan lorong
    for z in range(5, 7):
        for x in range(10):
            for y in range(10):
                if (x % 3 == 0 or y % 3 == 0):  # Lorong
                    continue
                factory.add_bomb(x, y, z)
    
    # Lantai atap (z=7,8,9)
    # Beberapa area tertutup untuk peralatan
    for z in range(7, 10):
        for x in range(2, 5):
            for y in range(7, 10):
                factory.add_bomb(x, y, z)
        for x in range(7, 10):
            for y in range(2, 5):
                factory.add_bomb(x, y, z)
    
    # Tentukan posisi awal (pos pengisian daya) dan akhir (titik inspeksi)
    start_pos = (0, 0, 0)
    end_pos = (9, 9, 9)
    
    # Temukan jalur terbaik
    path = factory.shortest_path(start_pos, end_pos)
    
    if path:
        print(f"Jalur terpendek ditemukan dengan {len(path)} langkah")
        print(f"Dari {start_pos} ke {end_pos}")
        
        # Tampilkan jumlah belokan
        turns = 0
        for i in range(1, len(path)-1):
            # Hitung perubahan arah
            prev_dir = (path[i][0] - path[i-1][0], path[i][1] - path[i-1][1], path[i][2] - path[i-1][2])
            next_dir = (path[i+1][0] - path[i][0], path[i+1][1] - path[i][1], path[i+1][2] - path[i][2])
            if prev_dir != next_dir:
                turns += 1
        
        print(f"Jumlah belokan: {turns}")
        
        # Visualisasi
        factory.visualize_path(path)
    else:
        print("Tidak ada jalur yang ditemukan dari pos pengisian daya ke titik inspeksi.")

def test_case_gedung_apartemen():
    """
    Skenario: Robot pengantar makanan di gedung apartemen
    Robot harus mengantar makanan dari lobi ke berbagai unit
    """
    print("\n--- Kasus Uji: Gedung Apartemen ---")
    apartment = RubikBuilding(size=10)
    
    # Inisialisasi seluruh gedung sebagai ruang kosong (semua 0)
    # Secara default semua ruangan bisa diakses
    
    # Tambahkan dinding luar dan struktur internal gedung
    for z in range(10):
        for x in range(10):
            for y in range(10):
                # Buat koridor dan ruangan yang bisa diakses
                # Koridor horizontal utama di tengah
                if y == 5:
                    apartment.building[x, y, z] = 0
                # Koridor vertikal utama di tengah
                elif x == 5:
                    apartment.building[x, y, z] = 0
                # Koridor dari tangga menuju koridor utama (lantai dasar)
                elif (x <= 5 and y == 1) or (x == 1 and y <= 5):
                    apartment.building[x, y, z] = 0
                # Koridor dari koridor utama ke pojok kanan atas
                elif (x >= 5 and y == 8) or (x == 8 and y >= 5):
                    apartment.building[x, y, z] = 0
                # Tangga/lift di sudut
                elif x == 1 and y == 1:
                    apartment.building[x, y, z] = 0
                # Unit apartemen di pojok kanan atas
                elif x == 8 and y == 8:
                    apartment.building[x, y, z] = 0
                else:
                    # Tandai ruangan lain sebagai tidak dapat diakses
                    apartment.building[x, y, z] = 1
                    apartment.bombs.append((x, y, z))
    
    # Hapus hambatan di jalur kritis
    # Pastikan ada jalur yang menghubungkan mulai dari tangga di lantai atas
    # menuju unit apartemen target
    for z in range(10):
        # Pastikan tangga tidak terhalang
        apartment.building[1, 1, z] = 0
        
        # Pastikan ada jalur yang menghubungkan tangga ke unit target
        # Koridor dari tangga ke koridor utama
        for x in range(1, 6):
            apartment.building[x, 1, z] = 0
        for y in range(1, 6):
            apartment.building[1, y, z] = 0
            
        # Koridor dari koridor utama ke unit target
        for x in range(5, 9):
            apartment.building[x, 8, z] = 0
        for y in range(5, 9):
            apartment.building[8, y, z] = 0
            
        # Koridor utama
        for x in range(10):
            apartment.building[x, 5, z] = 0
        for y in range(10):
            apartment.building[5, y, z] = 0
    
    # Rekonstruksi daftar bom berdasarkan building matrix
    apartment.bombs = []
    for x in range(10):
        for y in range(10):
            for z in range(10):
                if apartment.building[x, y, z] == 1:
                    apartment.bombs.append((x, y, z))
    
    # Visualisasi struktur lantai teratas untuk verifikasi
    print(f"Struktur Lantai 9 (lantai unit target):")
    for y in range(10):
        for x in range(10):
            print(f"{apartment.building[x, y, 9]}", end=" ")
        print()
    
    # Tentukan posisi awal (lobi) dan akhir (unit apartemen)
    start_pos = (1, 1, 0)  # Lobi
    end_pos = (8, 8, 9)    # Unit apartemen di lantai teratas
    
    # Temukan jalur terbaik
    path = apartment.shortest_path(start_pos, end_pos)
    
    if path:
        print(f"Jalur terpendek ditemukan dengan {len(path)} langkah")
        print(f"Dari {start_pos} ke {end_pos}")
        
        # Visualisasi
        apartment.visualize_path(path)
    else:
        print("Tidak ada jalur yang ditemukan dari lobi ke unit apartemen.")
        
        # Debug: cek konektivitas
        print("Memeriksa konektivitas...")
        # Cek apakah start_pos valid
        if not apartment.is_valid_position(*start_pos):
            print(f"Posisi awal {start_pos} tidak valid!")
        
        # Cek apakah end_pos valid
        if not apartment.is_valid_position(*end_pos):
            print(f"Posisi akhir {end_pos} tidak valid!")
            
        # Cek apakah ada jalur dari lobi ke tangga lantai atas
        path_to_top_stairs = apartment.shortest_path(start_pos, (1, 1, 9))
        if path_to_top_stairs:
            print(f"Ada jalur ke tangga lantai atas: {len(path_to_top_stairs)} langkah")
        else:
            print("Tidak ada jalur ke tangga lantai atas")
        
        # Cek apakah ada jalur dari tangga lantai atas ke tujuan
        path_from_top_stairs = apartment.shortest_path((1, 1, 9), end_pos)
        if path_from_top_stairs:
            print(f"Ada jalur dari tangga lantai atas ke tujuan: {len(path_from_top_stairs)} langkah")
        else:
            print("Tidak ada jalur dari tangga lantai atas ke tujuan")

# Tambahkan fungsi untuk menampilkan struktur gedung
def display_building_structure(building):
    """Menampilkan struktur gedung untuk debugging"""
    print("\nStruktur Gedung (0=jalur, 1=bom/dinding):")
    for z in range(building.size):
        print(f"\nLantai {z}:")
        for y in range(building.size):
            for x in range(building.size):
                print(f"{building.building[x, y, z]}", end=" ")
            print()  # Baris baru

# Jalankan test case tambahan
test_case_pabrik()
test_case_gedung_apartemen()

# Tambahkan test case untuk mall
def test_case_mall():
    """
    Skenario: Robot keamanan di mall
    Robot harus berpatroli dari pos keamanan ke berbagai lokasi
    """
    print("\n--- Kasus Uji: Mall ---")
    mall = RubikBuilding(size=10)
    
    # Inisialisasi seluruh gedung sebagai ruang kosong (semua 0)
    # Ini memastikan semua nilai awal adalah 0 sebelum kita mulai menandai ruangan
    
    # Struktur dasar mall - tandai area yang TIDAK bisa diakses (nilai 1)
    for z in range(10):
        for x in range(10):
            for y in range(10):
                # Kita hanya menandai ruangan yang TIDAK bisa diakses
                # Lorong utama berbentuk plus di setiap lantai tetap 0
                if x != 5 and y != 5:  # Bukan bagian dari koridor plus
                    mall.building[x, y, z] = 1
                    mall.bombs.append((x, y, z))
    
    # Tambahkan beberapa area terbuka (set nilai ke 0)
    
    # Food court di lantai 3
    for x in range(3, 8):
        for y in range(3, 8):
            mall.building[x, y, 3] = 0
    
    # Bioskop di lantai 5
    for x in range(7, 10):
        for y in range(7, 10):
            mall.building[x, y, 5] = 0
    
    # Area parkir di lantai bawah
    for z in range(2):
        for x in range(10):
            for y in range(10):
                if (x+y) % 3 != 0:  # Pola selang-seling untuk parkir
                    mall.building[x, y, z] = 0
    
    # Tambahkan jalur dari koridor ke bioskop di lantai 5
    # Pastikan ada jalur yang terhubung dari lift ke bioskop
    for x in range(5, 10):
        mall.building[x, 7, 5] = 0  # Koridor horizontal menuju bioskop
    for y in range(5, 10):
        mall.building[7, y, 5] = 0  # Koridor vertikal menuju bioskop
    
    # Rekonstruksi daftar bom berdasarkan building matrix
    mall.bombs = []
    for x in range(10):
        for y in range(10):
            for z in range(10):
                if mall.building[x, y, z] == 1:
                    mall.bombs.append((x, y, z))
    
    # Tentukan posisi awal dan akhir
    start_pos = (5, 5, 0)  # Pos keamanan di lantai dasar (lift)
    end_pos = (9, 9, 5)    # Bioskop di lantai 5
    
    # Tampilkan struktur lantai bioskop untuk verifikasi sebelum pencarian jalur
    print("\nStruktur Lantai 5 (lantai bioskop) - 0=bisa dilewati, 1=dinding:")
    for y in range(10):
        for x in range(10):
            print(f"{mall.building[x, y, 5]}", end=" ")
        print()
        
    # Verifikasi posisi awal dan akhir
    print(f"\nStatus posisi awal: {start_pos} = {mall.is_valid_position(*start_pos)}")
    print(f"Status posisi akhir: {end_pos} = {mall.is_valid_position(*end_pos)}")
    
    # Temukan jalur terbaik
    path = mall.shortest_path(start_pos, end_pos)
    
    if path:
        print(f"Jalur terpendek ditemukan dengan {len(path)} langkah")
        print(f"Dari {start_pos} ke {end_pos}")
        
        # Cetak beberapa langkah pertama dan terakhir untuk verifikasi
        print("Beberapa langkah pertama:")
        for i in range(min(5, len(path))):
            print(f"  Langkah {i+1}: {path[i]}")
            
        print("Beberapa langkah terakhir:")
        for i in range(max(len(path)-5, 0), len(path)):
            print(f"  Langkah {i+1}: {path[i]}")
        
        # Visualisasi
        mall.visualize_path(path)
    else:
        print("Tidak ada jalur yang ditemukan.")
        
        # Debug: cek konektivitas
        print("Memeriksa konektivitas...")
        # Cek apakah ada jalur dari awal ke lantai 5
        path_to_lvl5 = mall.shortest_path(start_pos, (5, 5, 5))
        if path_to_lvl5:
            print(f"Ada jalur ke lantai 5 (lift): {len(path_to_lvl5)} langkah")
        else:
            print("Tidak ada jalur ke lantai 5 (lift)")
        
        # Cek apakah ada jalur dari lift lantai 5 ke bioskop
        path_from_lift = mall.shortest_path((5, 5, 5), end_pos)
        if path_from_lift:
            print(f"Ada jalur dari lift lantai 5 ke bioskop: {len(path_from_lift)} langkah")
        else:
            print("Tidak ada jalur dari lift lantai 5 ke bioskop")

# Jalankan test case mall
test_case_mall()