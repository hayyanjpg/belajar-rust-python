# Materi 06: OOP - Class, Object, Inheritance, Polymorphism
# Penjelasan: Python mendukung OOP penuh. Class = blueprint, Object = instance.
# Pillars: Encapsulation, Inheritance, Polymorphism, Abstraction.

# ============================================
# 1. CLASS DASAR & __init__
# ============================================
class Mahasiswa:
    """Class representasi mahasiswa (docstring = dokumentasi class)"""

    # Class attribute (shared by all instances)
    universitas = "Universitas Indonesia"
    jumlah_mahasiswa = 0

    def __init__(self, nama: str, nim: str, jurusan: str):
        """Constructor: dipanggil saat object dibuat"""
        # Instance attributes (unique per object)
        self.nama = nama
        self.nim = nim
        self.jurusan = jurusan
        self._ipk = 0.0          # Protected convention (single underscore)
        self.__nilai_rahasia = 0  # Private convention (double underscore = name mangling)
        Mahasiswa.jumlah_mahasiswa += 1

    # Method instance (butuh self)
    def perkenalkan(self) -> str:
        return f"Halo, saya {self.nama} ({self.nim}) dari {self.jurusan}"

    # Property getter/setter untuk controlled access
    @property
    def ipk(self) -> float:
        return self._ipk

    @ipk.setter
    def ipk(self, nilai: float):
        if 0.0 <= nilai <= 4.0:
            self._ipk = nilai
        else:
            raise ValueError("IPK harus 0.0 - 4.0")

    # Method untuk private attribute (name mangling: _ClassName__attr)
    def set_nilai_rahasia(self, nilai: int):
        self.__nilai_rahasia = nilai

    def get_nilai_rahasia(self) -> int:
        return self.__nilai_rahasia

    # Class method (decorator @classmethod) - akses class attribute
    @classmethod
    def dari_string(cls, data: str):
        """Factory method: buat object dari string 'nama|nim|jurusan'"""
        nama, nim, jurusan = data.split("|")
        return cls(nama, nim, jurusan)

    @classmethod
    def total_mahasiswa(cls) -> int:
        return cls.jumlah_mahasiswa

    # Static method (decorator @staticmethod) - tidak butuh self/cls
    @staticmethod
    def validasi_nim(nim: str) -> bool:
        return nim.isdigit() and len(nim) >= 8

    # Magic/dunder methods
    def __str__(self) -> str:
        return f"Mahasiswa({self.nama}, {self.nim})"

    def __repr__(self) -> str:
        return f"Mahasiswa(nama='{self.nama}', nim='{self.nim}', jurusan='{self.jurusan}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Mahasiswa):
            return NotImplemented
        return self.nim == other.nim

    def __lt__(self, other) -> bool:
        if not isinstance(other, Mahasiswa):
            return NotImplemented
        return self._ipk < other._ipk


# ============================================
# 2. INHERITANCE (PEWARISAN)
# ============================================
class MahasiswaSiswa(Mahasiswa):
    """Subclass: pewarisan dari Mahasiswa"""

    def __init__(self, nama: str, nim: str, jurusan: str, angkatan: int):
        super().__init__(nama, nim, jurusan)  # panggil parent __init__
        self.angkatan = angkatan
        self.organisasi = []

    def tambah_organisasi(self, org: str):
        self.organisasi.append(org)

    # Override method parent
    def perkenalkan(self) -> str:
        base = super().perkenalkan()
        return f"{base}, Angkatan {self.angkatan}"

    # Method tambahan subclass
    def info_lengkap(self) -> str:
        org = ", ".join(self.organisasi) if self.organisasi else "Tidak ada"
        return f"{self.perkenalkan()}, Org: {org}"


class Dosen:
    """Class terpisah untuk demo polymorphism"""

    def __init__(self, nama: str, nidn: str, matkul: str):
        self.nama = nama
        self.nidn = nidn
        self.matkul = matkul

    def perkenalkan(self) -> str:
        return f"Halo, saya Dosen {self.nama} (NIDN: {self.nidn}), mengajar {self.matkul}"


# ============================================
# 3. ABSTRACTION & POLYMORPHISM
# ============================================
from abc import ABC, abstractmethod

class Bentuk(ABC):
    """Abstract Base Class - tidak bisa di-instansiasi langsung"""

    @abstractmethod
    def luas(self) -> float:
        pass

    @abstractmethod
    def keliling(self) -> float:
        pass

    def info(self) -> str:
        return f"Luas: {self.luas():.2f}, Keliling: {self.keliling():.2f}"


class Persegi(Bentuk):
    def __init__(self, sisi: float):
        self.sisi = sisi

    def luas(self) -> float:
        return self.sisi ** 2

    def keliling(self) -> float:
        return 4 * self.sisi


class Lingkaran(Bentuk):
    def __init__(self, jari: float):
        self.jari = jari

    def luas(self) -> float:
        import math
        return math.pi * self.jari ** 2

    def keliling(self) -> float:
        import math
        return 2 * math.pi * self.jari


# ============================================
# 4. COMPOSITION (KOMPOSISI) - Alternatif Inheritance
# ============================================
class Alamat:
    def __init__(self, jalan: str, kota: str, provinsi: str, kode_pos: str):
        self.jalan = jalan
        self.kota = kota
        self.provinsi = provinsi
        self.kode_pos = kode_pos

    def __str__(self):
        return f"{self.jalan}, {self.kota}, {self.provinsi} {self.kode_pos}"


class MahasiswaLengkap:
    """Menggunakan composition: Mahasiswa 'punya' Alamat"""

    def __init__(self, nama: str, nim: str, alamat: Alamat):
        self.nama = nama
        self.nim = nim
        self.alamat = alamat  # Composition

    def __str__(self):
        return f"{self.nama} ({self.nim}) - {self.alamat}"


# ============================================
# DEMO / TEST
# ============================================
if __name__ == "__main__":
    print("=" * 50)
    print("DEMO OOP PYTHON")
    print("=" * 50)

    # 1. Basic class & object
    mhs1 = Mahasiswa("Hayyan", "2021001", "Informatika")
    mhs1.ipk = 3.85
    print(f"\n1. Basic Class:")
    print(f"   {mhs1.perkenalkan()}")
    print(f"   IPK: {mhs1.ipk}")
    print(f"   str: {mhs1}")
    print(f"   repr: {repr(mhs1)}")

    # 2. Class method & static method
    mhs2 = Mahasiswa.dari_string("Rina|2021002|Sistem Informasi")
    print(f"\n2. Class Method Factory:")
    print(f"   {mhs2.perkenalkan()}")
    print(f"   Validasi NIM '2021001': {Mahasiswa.validasi_nim('2021001')}")
    print(f"   Total mahasiswa: {Mahasiswa.total_mahasiswa()}")

    # 3. Inheritance
    mhs_siswa = MahasiswaSiswa("Budi", "2021003", "Teknik Informatika", 2021)
    mhs_siswa.tambah_organisasi("HIMATIF")
    mhs_siswa.tambah_organisasi("KMahasiswa")
    print(f"\n3. Inheritance:")
    print(f"   {mhs_siswa.info_lengkap()}")

    # 4. Polymorphism: fungsi menerima interface yang sama
    def sapu_semua(orang_list):
        for orang in orang_list:
            print(f"   {orang.perkenalkan()}")

    dosen1 = Dosen("Dr. Siti", "12345678", "Struktur Data")
    print(f"\n4. Polymorphism:")
    sapu_semua([mhs1, mhs_siswa, dosen1])

    # 5. Abstract class
    print(f"\n5. Abstract Class:")
    bentuk_list = [Persegi(5), Lingkaran(3)]
    for b in bentuk_list:
        print(f"   {type(b).__name__}: {b.info()}")

    # 6. Composition
    print(f"\n6. Composition:")
    alamat = Alamat("Jl. Merdeka No. 10", "Jakarta", "DKI Jakarta", "10110")
    mhs_lengkap = MahasiswaLengkap("Sari", "2021004", alamat)
    print(f"   {mhs_lengkap}")

    # 7. Magic methods: equality & comparison
    print(f"\n7. Magic Methods (__eq__, __lt__):")
    mhs_a = Mahasiswa("A", "001", "IT")
    mhs_a.ipk = 3.5
    mhs_b = Mahasiswa("B", "001", "IT")  # NIM sama
    mhs_b.ipk = 3.8
    print(f"   mhs_a == mhs_b (NIM sama): {mhs_a == mhs_b}")
    print(f"   mhs_a < mhs_b (IPK): {mhs_a < mhs_b}")

    # 8. Private & name mangling demo
    print(f"\n8. Private Attribute (Name Mangling):")
    mhs1.set_nilai_rahasia(95)
    print(f"   Via method: {mhs1.get_nilai_rahasia()}")
    print(f"   Direct access mangled: {mhs1._Mahasiswa__nilai_rahasia}")

    # 9. MRO (Method Resolution Order)
    print(f"\n9. MRO MahasiswaSiswa:")
    for cls in MahasiswaSiswa.__mro__:
        print(f"   {cls}")

print("\n=== SELESAI ===")