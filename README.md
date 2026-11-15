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