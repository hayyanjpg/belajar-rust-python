//! Module `util`: kumpulan helper.
//!
//! Karena berupa folder, module ini butuh `mod.rs` sebagai pintu masuk.

pub mod teks;

// Re-export: item `teks::kapitalisasi` bisa dipanggil lewat `util::kapitalisasi`.
pub use teks::kapitalisasi;
