# Materi 24: Algoritma & Struktur Data Dasar
"""Implementasi kecil stack, queue, linked list, sorting, dan binary search.

Tujuannya memahami ide di balik struktur data yang sudah disediakan Python.
Jalankan dengan: python 24_algoritma_struktur_data.py
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass


class Stack:
    """LIFO (last in, first out). Analogi: tumpukan piring."""

    def __init__(self) -> None:
        self._data: list[int] = []

    def push(self, nilai: int) -> None:
        self._data.append(nilai)

    def pop(self) -> int:
        if not self._data:
            raise IndexError("stack kosong")
        return self._data.pop()

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Stack({self._data})"


class Queue:
    """FIFO (first in, first out). `deque` lebih cepat daripada list.pop(0)."""

    def __init__(self) -> None:
        self._data: deque[int] = deque()

    def enqueue(self, nilai: int) -> None:
        self._data.append(nilai)

    def dequeue(self) -> int:
        if not self._data:
            raise IndexError("queue kosong")
        return self._data.popleft()

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Queue({list(self._data)})"


@dataclass
class Node:
    """Simpul linked list: menyimpan nilai + penunjuk ke simpul berikutnya."""

    nilai: int
    berikutnya: Node | None = None


class LinkedList:
    """Linked list sederhana dengan operasi tambah di depan (O(1))."""

    def __init__(self) -> None:
        self.kepala: Node | None = None

    def tambah_depan(self, nilai: int) -> None:
        self.kepala = Node(nilai, self.kepala)

    def ke_list(self) -> list[int]:
        hasil: list[int] = []
        saat_ini = self.kepala
        while saat_ini is not None:
            hasil.append(saat_ini.nilai)
            saat_ini = saat_ini.berikutnya
        return hasil


def cari_biner(data: list[int], target: int) -> int:
    """Cari index target pada data terurut; kembalikan -1 jika tidak ada.

    Kompleksitas O(log n), jauh lebih cepat daripada linear search O(n)
    untuk data besar yang sudah terurut.
    """
    kiri, kanan = 0, len(data) - 1
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        if data[tengah] == target:
            return tengah
        if data[tengah] < target:
            kiri = tengah + 1
        else:
            kanan = tengah - 1
    return -1


def urutkan_gelembung(data: list[int]) -> list[int]:
    """Bubble sort: O(n^2). Dipakai untuk belajar, bukan untuk data besar."""
    hasil = data.copy()
    for i in range(len(hasil)):
        for j in range(len(hasil) - i - 1):
            if hasil[j] > hasil[j + 1]:
                hasil[j], hasil[j + 1] = hasil[j + 1], hasil[j]
    return hasil


def gabung(kiri: list[int], kanan: list[int]) -> list[int]:
    """Gabungkan dua list terurut menjadi satu list terurut."""
    hasil: list[int] = []
    i = j = 0
    while i < len(kiri) and j < len(kanan):
        if kiri[i] <= kanan[j]:
            hasil.append(kiri[i])
            i += 1
        else:
            hasil.append(kanan[j])
            j += 1
    hasil.extend(kiri[i:])
    hasil.extend(kanan[j:])
    return hasil


def urutkan_cepat(data: list[int]) -> list[int]:
    """Merge sort: O(n log n), stabil, tapi butuh memori tambahan O(n)."""
    if len(data) <= 1:
        return data.copy()
    tengah = len(data) // 2
    return gabung(urutkan_cepat(data[:tengah]), urutkan_cepat(data[tengah:]))


def demo() -> None:
    print("=== STACK (LIFO) ===")
    tumpukan = Stack()
    for n in [1, 2, 3]:
        tumpukan.push(n)
    print("Stack:", tumpukan, "panjang:", len(tumpukan))
    print("Pop:", tumpukan.pop(), "sisa:", tumpukan)

    print("\n=== QUEUE (FIFO) ===")
    antrian = Queue()
    for n in [1, 2, 3]:
        antrian.enqueue(n)
    print("Queue:", antrian)
    print("Dequeue:", antrian.dequeue(), "sisa:", antrian)

    print("\n=== LINKED LIST ===")
    linked = LinkedList()
    for n in [10, 20, 30]:
        linked.tambah_depan(n)
    print("Urutan (tambah depan):", linked.ke_list())
    print("Node kepala:", linked.kepala)

    print("\n=== BINARY SEARCH ===")
    data = [2, 5, 8, 12, 16, 23, 38]
    print("Data:", data)
    for target in [8, 23, 7]:
        print(f"  cari {target} -> index {cari_biner(data, target)}")

    print("\n=== SORTING ===")
    acak = [5, 1, 4, 2, 8, 3]
    print("Bubble sort:", urutkan_gelembung(acak))
    print("Merge sort :", urutkan_cepat(acak))
    print("Data asli tidak berubah:", acak)


def latihan() -> None:
    assert cari_biner([1, 3, 5, 7, 9], 7) == 3
    assert cari_biner([1, 3, 5], 2) == -1
    assert cari_biner([], 1) == -1

    assert urutkan_gelembung([3, 2, 1]) == [1, 2, 3]
    assert urutkan_cepat([4, 1, 3, 1, 2]) == [1, 1, 2, 3, 4]

    tumpukan = Stack()
    tumpukan.push(1)
    tumpukan.push(2)
    assert tumpukan.pop() == 2
    assert len(tumpukan) == 1

    antrian = Queue()
    antrian.enqueue(1)
    antrian.enqueue(2)
    assert antrian.dequeue() == 1

    linked = LinkedList()
    linked.tambah_depan(1)
    linked.tambah_depan(2)
    assert linked.ke_list() == [2, 1]

    print("Latihan materi 24: semua assert lolos.")


if __name__ == "__main__":
    demo()
    latihan()
