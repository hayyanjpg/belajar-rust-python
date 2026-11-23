# belajar-rust-python

Repository untuk pembelajaran bahasa pemrograman **Rust** dan **Python**.

## Struktur Folder

```
belajar-rust-python/
├── rust/       # Latihan dan catatan belajar Rust
├── python/     # Latihan dan catatan belajar Python
└── README.md   # Roadmap belajar
```

## Roadmap

- [Roadmap Rust](rust/README.md)
- [Roadmap Python](python/README.md)

## Ringkasan Target

### Rust
1. Fondasi: sintaks, Cargo, ownership, borrowing, lifetimes
2. Konsep inti: struct, enum, pattern matching, error handling
3. Koleksi & generik: `Vec`, `HashMap`, iterator, trait
4. Konkurensi: thread, channel, async/await
5. Proyek nyata: CLI, web API, testing, publish crate

### Python
1. Fondasi: sintaks, struktur kontrol, fungsi
2. Struktur data: list, tuple, dict, set, comprehension
3. OOP & modularisasi: class, inheritance, module, exception
4. Standard library & tooling: venv, pip, pytest
5. Spesialisasi: data analysis, web dev, automation, database

## Progress Checklist (Updated: 2026-11-24)

### Python - Tahap 1 & 2 (Fondasi & Struktur Data)
- [x] 01_variabel.py - Variabel, tipe data, casting, konstanta (+ 5 latihan)
- [x] 02_percabangan.py - if/elif/else, ternary, match-case (+ 6 latihan)
- [x] 03_perulangan.py - for/while, enumerate, break/continue, nested
- [x] 04_fungsi.py - Fungsi, *args, **kwargs, default, rekursif
- [x] 05_list_dict.py - List, dict, comprehension, nested dict

### Python - Tahap 3 (OOP & Modularisasi)
- [x] 06_oop_class.py - Class, inheritance, polymorphism, ABC, composition, magic methods
- [x] 07_file_handling.py - JSON, CSV, text, binary, pathlib, context manager
- [x] 08_dekorator_generator.py - Decorator, generator, coroutine, itertools, contextlib
- [x] 09_exception_handling.py - Exception handling, try/except, raise, custom error (+ 5 latihan)
- [x] 10_module_package.py - Module, package, import, `__init__.py`, `__name__` (+ 5 latihan)
- [x] 11_testing.py - unittest, pytest, fixture, mocking, parameterize (+ 5 latihan)

### Python - Tahap 4 (Standard Library & Type Hints)
- [x] 12_stdlib_datetime.py - `datetime`, `date`, `time`, `timedelta`, `timezone`, `calendar`
- [x] 13_stdlib_regex.py - `re`: match, search, findall, sub, group, flag
- [x] 14_stdlib_collections.py - `Counter`, `defaultdict`, `deque`, `namedtuple`, `OrderedDict`
- [x] 15_type_hints.py - `typing`: `List`, `Dict`, `Optional`, `Union`, `Protocol`, `Generic`

### Python - Mini Project
- [x] 16_mini_project_kasir.py - Kasir CLI: OOP, exception, JSON, type hints, format rupiah

### Rust - Tahap 1 (Fondasi)
- [x] 01_hello_world.rs - Print, format, debug (+ 6 latihan format)
- [x] 02_variabel_mutability.rs - Mutability, shadowing, const, borrowing (+ 6 latihan)
- [x] 03_tipe_data.rs - Scalar, compound, string, casting, operator
- [x] 04_fungsi_return.rs - Function, return, expression, recursion
- [x] 05_ownership.rs - Ownership, move, clone, borrow, slice

### Rust - Tahap 2 (Konsep Inti)
- [x] 06_struct_method.rs - Struct, impl, method, builder pattern, trait impl
- [x] 07_enum_match.rs - Enum, match, guard, @binding, if let, recursive enum
- [x] 08_error_handling.rs - Result, Option, ?, custom error, combinators

### Rust - Tahap 3 (Koleksi, Iterasi, Generic)
- [x] 09_collections.rs - `Vec`, `String`, `HashMap`, `HashSet`, `BTreeMap`
- [x] 10_iterator_closure.rs - Closure, adaptor, consumer, custom `Iterator`
- [x] 11_generic_trait.rs - Generic function/struct, trait, bound, `dyn Trait`, operator overloading

### Rust - Module, Lifetime & Cargo
- [x] 12_module_cargo/ - Module system (`mod`, `use`, `pub`), nested module, Cargo project, unit test
- [x] 13_lifetime.rs - Lifetime eksplisit, elision, struct ber-lifetime, `'static`, lifetime bound

### Rust - Tahap 4 (Smart Pointer & Concurrency)
- [x] 14_smart_pointer.rs - `Box`, `Rc`, `RefCell`, `Arc`, `Weak`
- [x] 15_concurrency.rs - `thread`, `move` closure, `mpsc`, `Mutex`, `RwLock`, `Atomic`, `thread::scope`

### Rust - Testing
- [x] `12_module_cargo/src/tests_lanjutan.rs` - 13 unit test tambahan (aritmetika, geometri, teks unicode, metadata crate)
- [x] Total unit test Cargo: 20 test (7 bawaan + 13 tambahan), dijalankan lewat `cargo test`

### Selanjutnya (Planned)
- [ ] Rust: Async/await (`tokio`) dan pembahasan `Send`/`Sync` lebih dalam
- [ ] Rust: Cargo workspace, feature flag, publish crate
- [ ] Rust: CLI (`clap`) atau web API (`axum`)
- [ ] Python: Tuple, set, dan unpacking lanjutan

## Cara Mulai

```bash
# Clone repository
git clone https://github.com/hayyanjpg/belajar-rust-python.git
cd belajar-rust-python

# Python: siapkan virtual environment
cd python
python -m venv .venv
.\.venv\Scripts\activate        # Windows
# source .venv/bin/activate     # Linux/macOS
pip install -r requirements.txt

# Menjalankan materi Python
python 01_variabel.py

# Menjalankan test
pytest 11_testing.py -v
```

### Rust (file latihan standalone)

Folder `rust/` berisi file `.rs` tunggal (belum berupa project Cargo), jadi bisa
langsung dikompilasi dengan `rustc`:

```bash
cd rust

# Kompilasi + jalankan satu file
rustc --edition 2021 09_collections.rs -o collections
./collections            # Windows: .\collections.exe

# Cek semua file standalone (PowerShell)
Get-ChildItem *.rs | ForEach-Object {
    rustc --edition 2021 $_.FullName -o "$env:TEMP\$($_.BaseName).exe"
}

# Materi 12 adalah project Cargo (bukan file tunggal)
cd 12_module_cargo
cargo run
cargo test
```

## Catatan

- Semua materi ditulis dengan komentar berbahasa Indonesia dan dilengkapi latihan.
- File yang dibuat saat latihan (`data_latihan/`, file sementara) sudah diabaikan
  lewat `.gitignore`.
- Materi Python 12–16 dan Rust 09–15 adalah lanjutan setelah tahap dasar.
- `rust/12_module_cargo/` adalah project Cargo; materi Rust lainnya adalah file
  `.rs` tunggal yang bisa dikompilasi dengan `rustc`.
