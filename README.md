# belajar-rust

Repository untuk pembelajaran bahasa pemrograman **Rust** dan **Python**.

## Struktur Folder

```
belajar-rust/
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

## Progress Checklist (Updated: 2026-11-18)

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
- [x] 10_module_package.py - Module, package, import, __init__.py, __name__ (+ 5 latihan)
- [x] 11_testing.py - unittest, pytest, fixture, mocking, parameterize (+ 5 latihan)

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

### Selanjutnya (Planned)
- [ ] Rust: Collections (Vec, HashMap), Iterator, Generics, Trait
- [ ] Rust: Smart Pointer, Concurrency, Async
- [ ] Python: Stdlib (datetime, regex, collections), Type hints

## Cara Mulai

```bash
# Clone repository
git clone <url-repo>

# Rust
cd rust
cargo new hello-rust
cd hello-rust
cargo run

# Python
cd python
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```
