# rust

Folder latihan dan catatan belajar bahasa pemrograman Rust.

## Roadmap Rust

### Tahap 1 — Fondasi
- [ ] Instalasi toolchain (`rustup`, `cargo`, `rustc`)
- [ ] Struktur proyek dan perintah dasar Cargo (`new`, `build`, `run`, `check`, `fmt`, `clippy`)
- [ ] Sintaks dasar: variabel, mutabilitas, konstanta, tipe data skalar & kompilasi
- [ ] Tipe data majemuk: tuple, array, slice
- [ ] Percabangan (`if`, `else`) dan perulangan (`loop`, `while`, `for`)
- [ ] Fungsi, parameter, nilai balik, dan ekspresi

### Tahap 2 — Konsep Inti
- [ ] Ownership (kepemilikan) dan aturan borrow checker
- [ ] Borrowing: immutable (`&T`) dan mutable (`&mut T`)
- [ ] Lifetimes dasar
- [ ] Struct, method, dan `impl`
- [ ] Enum dan pattern matching (`match`, `if let`)
- [ ] Module system, `use`, dan visibilitas (`pub`)
- [ ] `Option<T>` dan `Result<T>` untuk penanganan error
- [ ] Error handling: `?` operator, custom error, `panic!`

### Tahap 3 — Koleksi & Iterasi
- [ ] `Vec<T>`, `String`, `HashMap`, `HashSet`
- [ ] Iterator, closure, dan adaptor (`map`, `filter`, `collect`, `fold`)
- [ ] Generic types, trait, dan trait bound
- [ ] Deriving trait (`Debug`, `Clone`, `PartialEq`, dll.)

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