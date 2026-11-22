# rust

Folder latihan dan catatan belajar bahasa pemrograman Rust.

## Roadmap Rust

### Tahap 1 — Fondasi
- [ ] Instalasi toolchain (`rustup`, `cargo`, `rustc`)
- [ ] Struktur proyek dan perintah dasar Cargo (`new`, `build`, `run`, `check`, `fmt`, `clippy`)
- [x] Sintaks dasar: variabel, mutabilitas, konstanta, tipe data skalar & kompilasi
- [x] Tipe data majemuk: tuple, array, slice
- [ ] Percabangan (`if`, `else`) dan perulangan (`loop`, `while`, `for`)
- [x] Fungsi, parameter, nilai balik, dan ekspresi

### Tahap 2 — Konsep Inti
- [x] Ownership (kepemilikan) dan aturan borrow checker
- [x] Borrowing: immutable (`&T`) dan mutable (`&mut T`)
- [ ] Lifetimes dasar
- [x] Struct, method, dan `impl`
- [x] Enum dan pattern matching (`match`, `if let`)
- [ ] Module system, `use`, dan visibilitas (`pub`)
- [x] `Option<T>` dan `Result<T>` untuk penanganan error
- [x] Error handling: `?` operator, custom error, `panic!`

### Tahap 3 — Koleksi & Iterasi
- [x] `Vec<T>`, `String`, `HashMap`, `HashSet`
- [x] Iterator, closure, dan adaptor (`map`, `filter`, `collect`, `fold`)
- [x] Generic types, trait, dan trait bound
- [x] Deriving trait (`Debug`, `Clone`, `PartialEq`, dll.)

### Tahap 4 — Konkurensi & OOP Fungsional
- [ ] Smart pointer: `Box<T>`, `Rc<T>`, `RefCell<T>`, `Arc<T>`
- [ ] Concurrency: `thread::spawn`, `move` closure, `channel`
- [ ] `Send` dan `Sync` trait
- [ ] Async dasar: `async`/`await`, runtime `tokio`
- [ ] Unsafe Rust: kapan dan mengapa dihindari

### Tahap 5 — Proyek Nyata
- [ ] CLI tool dengan `clap`
- [ ] Web API dengan `axum` atau `actix-web`
- [ ] Manajemen dependensi: `Cargo.toml`, workspace, feature flag
- [ ] Testing: unit test, integration test, benchmark
- [ ] Benchmark performa dan optimasi memori
- [ ] Publish crate ke crates.io

## Sumber Belajar
- The Rust Programming Language (Rust Book) — https://doc.rust-lang.org/book/
- Rustlings — latihan interaktif
- Rust by Example — https://doc.rust-lang.org/rust-by-example/