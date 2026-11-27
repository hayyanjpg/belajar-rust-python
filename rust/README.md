# rust

Folder latihan dan catatan belajar bahasa pemrograman Rust.

## Roadmap Rust

### Tahap 1 — Fondasi
- [x] Instalasi toolchain (`rustup`, `cargo`, `rustc`)
- [x] Struktur proyek dan perintah dasar Cargo (`new`, `build`, `run`, `check`, `fmt`, `clippy`)
- [x] Sintaks dasar: variabel, mutabilitas, konstanta, tipe data skalar & kompilasi
- [x] Tipe data majemuk: tuple, array, slice
- [x] Percabangan (`if`, `else`) dan perulangan (`loop`, `while`, `for`) — materi 18
- [x] Fungsi, parameter, nilai balik, dan ekspresi

### Tahap 2 — Konsep Inti
- [x] Ownership (kepemilikan) dan aturan borrow checker
- [x] Borrowing: immutable (`&T`) dan mutable (`&mut T`)
- [x] Lifetimes dasar
- [x] Struct, method, dan `impl`
- [x] Enum dan pattern matching (`match`, `if let`)
- [x] Module system, `use`, dan visibilitas (`pub`)
- [x] `Option<T>` dan `Result<T>` untuk penanganan error
- [x] Error handling: `?` operator, custom error, `panic!`

### Tahap 3 — Koleksi & Iterasi
- [x] `Vec<T>`, `String`, `HashMap`, `HashSet`
- [x] Iterator, closure, dan adaptor (`map`, `filter`, `collect`, `fold`)
- [x] Generic types, trait, dan trait bound
- [x] Deriving trait (`Debug`, `Clone`, `PartialEq`, dll.)

### Tahap 4 — Konkurensi & OOP Fungsional
- [x] Smart pointer: `Box<T>`, `Rc<T>`, `RefCell<T>`, `Arc<T>`
- [x] Concurrency: `thread::spawn`, `move` closure, `channel`
- [x] `Send` dan `Sync` trait (dasar, lewat `Arc`/`Mutex`)
- [x] Async dasar: `async`/`await`, runtime `tokio` — materi 21
- [x] Unsafe Rust: kapan dan mengapa dihindari — materi 19

### Tahap 5 — Proyek Nyata
- [x] CLI tool dengan `clap` — contoh `16_cli_clap.rs`
- [x] Web API dengan `axum` — contoh `17_web_axum.rs`
- [x] Manajemen dependensi: `Cargo.toml`, workspace (`workspace/`), feature flag
- [x] Testing: 20 unit test + 9 integration test di `12_module_cargo`, 4 test async, 3 test + 1 doctest di crate publish
- [x] Benchmark performa dan optimasi memori — materi 20
- [x] Publish crate ke crates.io — panduan `dry-run` di `22_publish_crate/README.md`

### Tahap 6 — Materi Tambahan (2026-11-26)
- [x] 18_percabangan_perulangan.rs — `if`/`else`, `loop`, `while`, `for`, labeled loop
- [x] 19_unsafe_dasar.rs — raw pointer, `MaybeUninit`, `unsafe impl`, FFI
- [x] 20_benchmark_optimasi.rs — `Instant`, `black_box`, `size_of`, capacity
- [x] 21_async_tokio/ — `async`/`await`, `spawn`, `join!`, channel, timeout
- [x] 22_publish_crate/ — contoh crate + alur `cargo publish`

### Tahap 7 — Trait Object & Generic (2026-11-28)
- [x] 23_trait_object_dan_generic.rs — `dyn Trait`, generic bound, 3 unit test
  - `rustc --edition 2021 --test 23_trait_object_dan_generic.rs -o materi23_test`

Catatan: `16_cli_clap.rs` dan `17_web_axum.rs` adalah contoh yang memakai crate
eksternal, jadi belum dikompilasi sebagai file standalone oleh CI.

## Sumber Belajar
- The Rust Programming Language (Rust Book) — https://doc.rust-lang.org/book/
- Rustlings — latihan interaktif
- Rust by Example — https://doc.rust-lang.org/rust-by-example/