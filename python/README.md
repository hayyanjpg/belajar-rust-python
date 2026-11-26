# python

Folder latihan dan catatan belajar bahasa pemrograman Python.

## Roadmap Python

### Tahap 1 — Fondasi
- [x] Instalasi Python dan setup virtual environment (`venv`, `pip`)
- [x] Sintaks dasar: variabel, tipe data, casting
- [x] Operator aritmatika, perbandingan, logika
- [x] Input/output dan string formatting (f-string)
- [x] Struktur kontrol: `if`/`elif`/`else`, `for`, `while`
- [x] Fungsi: parameter, default value, `*args`, `**kwargs`, return

### Tahap 2 — Struktur Data
- [x] List dan operasinya (indexing, slicing, method)
- [x] Tuple dan perbedaannya dengan list (materi 05 & 23)
- [x] Dictionary dan set (materi 05 & 23)
- [x] List/dict/set comprehension
- [x] Unpacking, `*` operator, `enumerate`, `zip(strict=True)` (materi 23)

### Tahap 3 — Pilar OOP & Modularisasi
- [x] Class, object, atribut, method, `__init__`
- [x] Inheritance, encapsulation, polymorphism
- [x] Magic/dunder methods (`__str__`, `__repr__`, `__eq__`, `__len__`)
- [x] Module, package, dan `import`
- [x] Exception handling (`try`, `except`, `finally`, `raise`)
- [x] File handling dan `with` statement (context manager)

### Tahap 4 — Standar Library & Populer
- [x] `datetime`, `math`, `random`, `os`, `pathlib`, `json`
- [x] `collections`, `itertools`, `functools`
- [x] Regex dengan `re`
- [x] Virtual environment lanjutan: `pip freeze`, `requirements.txt`
- [x] Testing dengan `unittest` dan `pytest`

### Tahap 5 — Spesialisasi
- [x] Data analysis: `numpy`, `pandas` (17_data_analysis.py)
- [x] Visualisasi data: `matplotlib`, `seaborn` (18_visualisasi.py)
- [x] Web development: `flask`, `fastapi` (19_web_dev.py)
- [x] Automation & scripting: `requests`, `beautifulsoup4` (20_automasi.py)
- [x] Database: `sqlite3`, SQLAlchemy (21_database.py)
- [x] Async programming: `asyncio`, `aiohttp` (22_async_tooling.py)
- [x] Type hints + tooling: `mypy`, `black`, `ruff` dipakai di CI

### Tahap 6 — Lanjutan (2026-11-26)
- [x] 23_tuple_set_unpacking.py — tuple, set, unpacking bintang, `enumerate`, `zip`
- [x] 24_algoritma_struktur_data.py — stack, queue, linked list, sorting, binary search
- [x] 25_fungsional_lanjutan.py — `functools`, `itertools`, closure
- [x] 26_dataclass_enum_serialisasi.py — `dataclass`, `Enum`, JSON
- [x] 27_logging_argparse.py — `logging` dan CLI `argparse`
- [x] 28_mini_project_todo.py — Todo CLI (JSON, exception, dataclass)

### Mini Project
- [x] 16_mini_project_kasir.py — Kasir CLI (OOP, exception, JSON, type hints)
  - `python 16_mini_project_kasir.py` untuk demo
  - `python 16_mini_project_kasir.py --interactive` untuk mode interaktif
- [x] 28_mini_project_todo.py — Todo CLI
  - `python 28_mini_project_todo.py` untuk demo (memakai folder sementara)
  - `python 28_mini_project_todo.py --berkas todo.json tambah "Belajar Rust"` untuk CLI

### Testing Otomatis
- `test_23_tuple_set_unpacking.py` — 6 test pytest untuk materi 23
- Jalankan: `pytest 11_testing.py test_23_tuple_set_unpacking.py -v`

## Sumber Belajar
- Python Official Tutorial — https://docs.python.org/3/tutorial/
- Real Python — https://realpython.com/
- Automate the Boring Stuff with Python — https://automatetheboringstuff.com/