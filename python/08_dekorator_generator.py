# Materi 08: Dekorator & Generator - Advanced Python
# Penjelasan: Dekorator = fungsi yang memodifikasi fungsi lain (higher-order function).
# Generator = fungsi yang menghasilkan iterator lazy (menggunakan yield).

import time
import functools
from typing import Callable, Any, Generator, Iterator
from contextlib import contextmanager

# ============================================
# 1. DEKORATOR DASAR
# ============================================
def dekorator_sederhana(func: Callable) -> Callable:
    """Dekorator paling dasar: wrap fungsi tanpa argumen"""
    def wrapper(*args, **kwargs):
        print(f"[DEKORATOR] Sebelum memanggil {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[DEKORATOR] Sesudah memanggil {func.__name__}")
        return result
    return wrapper


@dekorator_sederhana
def halo(nama: str) -> str:
    return f"Halo, {nama}!"


# ============================================
# 2. DEKORATOR DENGAN ARGUMEN (Decorator Factory)
# ============================================
def repeat(times: int) -> Callable:
    """Decorator factory: menerima argumen, return decorator"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)  # Preserve metadata (__name__, __doc__, dll.)
        def wrapper(*args, **kwargs):
            results = []
            for i in range(times):
                print(f"  [Repeat {i+1}/{times}]")
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator


@repeat(3)
def sapu(nama: str) -> str:
    return f"Sapu: {nama}"


# ============================================
# 3. DEKORATOR CLASS-BASED
# ============================================
class CountCalls:
    """Class-based decorator: track jumlah pemanggilan"""

    def __init__(self, func: Callable):
        self.func = func
        self.count = 0
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"[CountCalls] {self.func.__name__} dipanggil ke-{self.count}")
        return self.func(*args, **kwargs)


@CountCalls
def hitung(a: int, b: int) -> int:
    return a + b


# ============================================
# 4. DEKORATOR BUILT-IN: @property, @classmethod, @staticmethod
# ============================================
class Mahasiswa:
    def __init__(self, nama: str, nilai: list):
        self.nama = nama
        self._nilai = nilai

    @property
    def rata_rata(self) -> float:
        """Read-only property"""
        return sum(self._nilai) / len(self._nilai) if self._nilai else 0.0

    @property
    def nilai(self) -> list:
        return self._nilai

    @nilai.setter
    def nilai(self, nilai_baru: list):
        if all(isinstance(n, (int, float)) for n in nilai_baru):
            self._nilai = nilai_baru
        else:
            raise ValueError("Nilai harus angka")


# ============================================
# 5. DEKORATOR FUNGSI UTILITAS: @functools.lru_cache (Memoization)
# ============================================
@functools.lru_cache(maxsize=128)
def fibonacci_cached(n: int) -> int:
    """Fibonacci dengan caching otomatis (O(n) dari O(2^n))"""
    if n < 2:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)


@functools.lru_cache(maxsize=None)
def faktorial_cached(n: int) -> int:
    if n <= 1:
        return 1
    return n * faktorial_cached(n - 1)


# ============================================
# 6. DEKORATOR TIMING & LOGGING
# ============================================
def timer(func: Callable) -> Callable:
    """Dekorator untuk mengukur waktu eksekusi"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[TIMER] {func.__name__} took {(end-start)*1000:.4f} ms")
        return result
    return wrapper


def logger(func: Callable) -> Callable:
    """Dekorator untuk logging input/output"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Call: {func.__name__}(args={args}, kwargs={kwargs})")
        result = func(*args, **kwargs)
        print(f"[LOG] Return: {result}")
        return result
    return wrapper


@timer
@logger  # Stacking decorator: @timer @logger def func() -> timer(logger(func()))
def proses_data(data: list) -> list:
    time.sleep(0.01)  # Simulasi kerja
    return [x * 2 for x in data]


# ============================================
# 7. GENERATOR DASAR (yield)
# ============================================
def generator_sederhana() -> Generator[int, None, None]:
    """Generator: menghasilkan nilai satu per satu (lazy evaluation)"""
    yield 1
    yield 2
    yield 3
    print("Generator selesai")


def countdown(n: int) -> Generator[int, None, None]:
    """Generator countdown"""
    while n > 0:
        yield n
        n -= 1


def fibonacci_gen(limit: int) -> Generator[int, None, None]:
    """Generator Fibonacci hingga limit"""
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b


# ============================================
# 8. GENERATOR EXPRESSION (Generator Comprehension)
# ============================================
# List comprehension: eager (langsung hitung semua)
kuadrat_list = [x * x for x in range(10)]

# Generator expression: lazy (hitung saat dibutuhkan)
kuadrat_gen = (x * x for x in range(10))


# ============================================
# 9. ADVANCED GENERATOR: send(), throw(), close()
# ============================================
def generator_interaktif() -> Generator[str, str, None]:
    """Generator yang bisa menerima data via send()"""
    pesan = yield "Siap terima pesan"
    while True:
        pesan = yield f"Diterima: {pesan}"


def coroutine_contoh():
    """Demo coroutine dengan generator"""
    gen = generator_interaktif()
    print(next(gen))  # Start generator -> "Siap terima pesan"
    print(gen.send("Halo"))   # Kirim "Halo" -> "Diterima: Halo"
    print(gen.send("Dunia"))  # Kirim "Dunia" -> "Diterima: Dunia"
    gen.close()  # Tutup generator


# ============================================
# 10. GENERATOR DELEGATION: yield from
# ============================================
def sub_generator() -> Generator[int, None, str]:
    yield 1
    yield 2
    return "Selesai sub"


def main_generator() -> Generator[int, None, str]:
    yield 0
    result = yield from sub_generator()  # Delegasi ke sub-generator
    yield 3
    return f"Main: {result}"


# ============================================
# 11. ITERTOOLS & GENERATOR PIPELINE
# ============================================
import itertools

def pipeline_contoh():
    """Pipeline data dengan generator + itertools"""
    data = range(1, 21)

    # Pipeline: filter genap -> map kuadrat -> take 5
    gen = (x for x in data)
    gen = filter(lambda x: x % 2 == 0, gen)      # Filter genap
    gen = map(lambda x: x * x, gen)              # Map kuadrat
    gen = itertools.islice(gen, 5)               # Ambil 5 pertama

    print("Pipeline result:", list(gen))

    # itertools chaining
    print("Chain:", list(itertools.chain([1,2], [3,4], [5])))
    print("Cycle:", list(itertools.islice(itertools.cycle('ABC'), 7)))
    print("Accumulate:", list(itertools.accumulate([1,2,3,4,5])))


# ============================================
# 12. CONTEXTLIB: @contextmanager (Generator-based Context Manager)
# ============================================
@contextmanager
def buka_file(nama: str, mode: str = "r"):
    """Context manager dengan generator (lebih sederhana dari class)"""
    print(f"[CM] Membuka {nama}")
    f = open(nama, mode, encoding="utf-8")
    try:
        yield f
    finally:
        print(f"[CM] Menutup {nama}")
        f.close()


@contextmanager
def timer_cm(nama: str):
    """Context manager untuk timing block kode"""
    start = time.perf_counter()
    print(f"[CM-Timer] {nama} mulai")
    try:
        yield
    finally:
        end = time.perf_counter()
        print(f"[CM-Timer] {nama} selesai: {(end-start)*1000:.2f} ms")


# ============================================
# MAIN DEMO
# ============================================
if __name__ == "__main__":
    print("=" * 60)
    print("DEMO DEKORATOR & GENERATOR PYTHON")
    print("=" * 60)

    # 1. Dekorator sederhana
    print("\n--- DEKORATOR SEDERHANA ---")
    print(halo("Hayyan"))

    # 2. Dekorator dengan argumen
    print("\n--- DEKORATOR DENGAN ARGUMEN ---")
    print(sapu("Rust"))

    # 3. Class-based decorator
    print("\n--- CLASS-BASED DEKORATOR ---")
    print(hitung(1, 2))
    print(hitung(3, 4))
    print(hitung(5, 6))
    print(f"Total pemanggilan: {hitung.count}")

    # 4. Property decorator
    print("\n--- @PROPERTY ---")
    mhs = Mahasiswa("Hayyan", [80, 90, 85])
    print(f"Rata-rata: {mhs.rata_rata}")
    mhs.nilai = [95, 85, 90]
    print(f"Rata-rata baru: {mhs.rata_rata}")

    # 5. LRU Cache
    print("\n--- @LRU_CACHE ---")
    import time
    start = time.perf_counter()
    print(f"fibonacci_cached(30) = {fibonacci_cached(30)}")
    print(f"Waktu pertama: {(time.perf_counter()-start)*1000:.2f} ms")

    start = time.perf_counter()
    print(f"fibonacci_cached(30) = {fibonacci_cached(30)}")
    print(f"Waktu cached: {(time.perf_counter()-start)*1000:.2f} ms")
    print(f"Cache info: {fibonacci_cached.cache_info()}")

    # 6. Timer & Logger stacking
    print("\n--- DEKORATOR STACKING ---")
    print(proses_data([1, 2, 3, 4, 5]))

    # 7. Generator dasar
    print("\n--- GENERATOR DASAR ---")
    gen = generator_sederhana()
    print(f"Type: {type(gen)}")
    print(f"Next: {next(gen)}")
    print(f"Next: {next(gen)}")
    print(f"Next: {next(gen)}")
    # next(gen)  # StopIteration

    print("\nCountdown:")
    for n in countdown(5):
        print(f"  {n}")

    print("\nFibonacci < 50:")
    for n in fibonacci_gen(50):
        print(f"  {n}")

    # 8. Generator expression
    print("\n--- GENERATOR EXPRESSION ---")
    print(f"List (eager): {kuadrat_list}")
    print(f"Gen (lazy): {kuadrat_gen}")
    print(f"Next dari gen: {next(kuadrat_gen)}")
    print(f"Next dari gen: {next(kuadrat_gen)}")

    # 9. Generator interaktif (coroutine)
    print("\n--- GENERATOR INTERAKTIF ---")
    coroutine_contoh()

    # 10. yield from
    print("\n--- YIELD FROM ---")
    for val in main_generator():
        print(f"  {val}")

    # 11. Pipeline
    print("\n--- PIPELINE ITERTOOLS ---")
    pipeline_contoh()

    # 12. Context manager
    print("\n--- CONTEXTLIB @contextmanager ---")
    with buka_file("test_cm.txt", "w") as f:
        f.write("Test context manager\nBaris kedua")

    with buka_file("test_cm.txt", "r") as f:
        print(f"Isi: {f.read()}")

    with timer_cm("Operasi berat"):
        time.sleep(0.05)
        sum(range(1000000))

    print("\n=== SELESAI ===")