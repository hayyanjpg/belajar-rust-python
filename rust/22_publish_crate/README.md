# belajar-publish-contoh

Contoh crate Rust kecil untuk mempelajari alur publish ke [crates.io](https://crates.io).

> Perhatian: crate ini **hanya contoh latihan**. Jangan publish paket latihan
> ke registry publik tanpa mengganti nama menjadi nama yang unik.

## Isi crate

- `sapaan(nama)` — contoh fungsi dengan doctest.
- `kuadrat(n)` — contoh fungsi dengan unit test.
- `rata_rata(data)` — contoh fungsi yang mengembalikan `Option<f64>`.

## Menjalankan test

```bash
cargo test
```

Termasuk doctest dari komentar `///` pada `sapaan`.

## Alur publish (untuk dipelajari)

1. Pastikan `Cargo.toml` lengkap: `name`, `version`, `description`,
   `license`, `repository`, `readme`, `keywords`, `categories`.
2. Cek kualitas paket:

   ```bash
   cargo fmt --check
   cargo clippy -- -D warnings
   cargo test
   ```

3. Simulasi packaging tanpa mengirim apa pun:

   ```bash
   cargo publish --dry-run
   ```

   Perintah ini akan membangun crate dan menunjukkan isi paket (`.crate`).

4. Login ke crates.io (token dari https://crates.io/settings/tokens):

   ```bash
   cargo login
   # atau: cargo login <token>
   ```

5. Publish versi baru (nama harus unik dan versi belum pernah dipakai):

   ```bash
   cargo publish
   ```

6. Setelah publish, versi tidak bisa dihapus. Untuk perbaikan, naikkan
   versi, misalnya `0.1.0` → `0.1.1`, lalu `cargo publish` lagi.

## Catatan penting

- `Cargo.lock` biasanya **tidak** dipakai saat publish library; ini berbeda
  dengan binary/application yang sebaiknya meng-commit lockfile.
- Gunakan `cargo package --list` untuk melihat file mana saja yang ikut masuk.
- Semver: `0.1.0` → `0.2.0` untuk perubahan yang tidak kompatibel,
  `0.1.1` untuk perbaikan kecil, `0.1.2` untuk patch.

## Sumber

- https://doc.rust-lang.org/cargo/reference/publishing.html
- https://crates.io/
