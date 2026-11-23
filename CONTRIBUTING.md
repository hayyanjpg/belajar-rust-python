# Kontribusi

Terima kasih atas minat Anda berkontribusi pada repository `belajar-rust-python`!
Repository ini adalah tempat pembelajaran bahasa pemrograman Rust dan Python.

## Cara Berkontribusi

1. **Fork** repository ini ke akun GitHub Anda.
2. **Clone** fork Anda ke lokal:
   ```bash
   git clone https://github.com/<username-anda>/belajar-rust-python.git
   cd belajar-rust-python
   ```
3. Buat **branch baru** untuk fitur atau perbaikan:
   ```bash
   git checkout -b fitur/nama-fitur
   ```
4. Lakukan perubahan dan **commit**:
   ```bash
   git add .
   git commit -m "feat: deskripsi perubahan"
   ```
5. **Push** ke branch Anda:
   ```bash
   git push origin fitur/nama-fitur
   ```
6. Buka **Pull Request** dari branch Anda ke branch `main` repository asli.

## Panduan Commit

Gunakan format conventional commits:

- `feat:` - fitur baru atau materi baru
- `fix:` - perbaikan bug atau kesalahan
- `docs:` - perubahan dokumentasi
- `style:` - formatting kode, tidak mengubah logika
- `refactor:` - refaktor kode
- `test:` - menambahkan atau memperbarui test
- `chore:` - tugas pemeliharaan

Contoh:
```
feat(python): tambah materi Tahap 5 data analysis
fix(rust): perbaiki error kompilasi pada file 15_concurrency.rs
```

## Struktur Repository

```
belajar-rust-python/
├── python/       # Materi belajar Python
├── rust/         # Materi belajar Rust
├── .github/      # CI/CD workflow
├── LICENSE       # Lisensi MIT
├── README.md     # Dokumentasi utama
└── .gitignore    # File yang diabaikan git
```

## Standar Kode

### Python
- Gunakan type hints untuk fungsi publik
- Ikuti PEP 8 untuk formatting
- Sertakan docstring pada setiap fungsi dan kelas
- Tulis komentar dalam bahasa Indonesia

### Rust
- Gunakan `cargo fmt` untuk formatting
- Jalankan `cargo clippy` untuk linting
- Sertakan komentar dalam bahasa Indonesia
- Tulis unit test untuk logika penting

## Laporan Bug dan Fitur

Buka **Issue** di tab Issues untuk melaporkan bug atau meminta fitur baru. Berikan informasi yang cukup lengkap untuk memudahkan penanganan.

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).
