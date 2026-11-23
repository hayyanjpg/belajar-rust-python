"""
16_cli_clap.rs - CLI Tool dengan Clap

Tahap 5: Proyek Nyata - Rust
Materi: clap, command line interface, argument parsing, subcommand
"""

use clap::{Parser, Subcommand, Args};
use std::fs;
use std::path::PathBuf;

/// Belajar Rust CLI - Aplikasi command line sederhana
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,

    /// Tingkatkan verbosity (bisa digunakan berkali-kali: -v, -vv, -vvv)
    #[arg(short, long, action = clap::ArgAction::Count)]
    verbose: u8,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Mengelola catatan (notes)
    Note(NoteArgs),

    /// Mengonversi suhu
    Convert {
        /// Nilai suhu
        value: f64,

        /// Dari satuan (c, f, k)
        #[arg(short, long)]
        from: String,

        /// Ke satuan (c, f, k)
        #[arg(short, long)]
        to: String,
    },

    /// Menampilkan informasi sistem
    Info,

    /// Mengenkripsi/dekripsi teks dengan Caesar cipher
    Cipher(CipherArgs),
}

#[derive(Args, Debug)]
struct NoteArgs {
    /// Aksi: tambah, lihat, hapus
    #[arg(short, long)]
    action: String,

    /// Judul catatan
    #[arg(short, long)]
    title: Option<String>,

    /// Konten catatan
    #[arg(short, long)]
    content: Option<String>,

    /// File penyimpanan catatan
    #[arg(short, long, default_value = "notes.json")]
    file: PathBuf,
}

#[derive(Args, Debug)]
struct CipherArgs {
    /// Teks yang akan diproses
    text: String,

    /// Pergeseran (shift)
    #[arg(short, long, default_value = "3")]
    shift: i32,

    /// Mode: encrypt atau decrypt
    #[arg(short, long, default_value = "encrypt")]
    mode: String,
}

fn convert_suhu(value: f64, from: &str, to: &str) -> f64 {
    let from = from.to_lowercase();
    let to = to.to_lowercase();

    // Konversi ke Celsius terlebih dahulu
    let celsius = match from.as_str() {
        "c" => value,
        "f" => (value - 32.0) * 5.0 / 9.0,
        "k" => value - 273.15,
        _ => panic!("Satuan asal tidak dikenal: {}", from),
    };

    // Dari Celsius ke tujuan
    match to.as_str() {
        "c" => celsius,
        "f" => celsius * 9.0 / 5.0 + 32.0,
        "k" => celsius + 273.15,
        _ => panic!("Satuan tujuan tidak dikenal: {}", to),
    }
}

fn caesar_cipher(text: &str, shift: i32, mode: &str) -> String {
    let shift = if mode == "decrypt" { -shift } else { shift };
    let shift = shift.rem_euclid(26);

    text.chars()
        .map(|c| {
            if c.is_ascii_uppercase() {
                let base = 'A' as u8;
                ((c as u8 - base + shift as u8) % 26 + base) as char
            } else if c.is_ascii_lowercase() {
                let base = 'a' as u8;
                ((c as u8 - base + shift as u8) % 26 + base) as char
            } else {
                c
            }
        })
        .collect()
}

fn manage_notes(args: &NoteArgs) {
    let notes_dir = "data_latihan";
    fs::create_dir_all(notes_dir).ok();
    let file_path = PathBuf::from(notes_dir).join(&args.file);

    match args.action.as_str() {
        "tambah" => {
            let title = args.title.as_deref().unwrap_or("Tanpa Judul");
            let content = args.content.as_deref().unwrap_or("");
            let entry = format!("{}::{}::\n", title, content);

            // Baca catatan yang sudah ada
            let existing = fs::read_to_string(&file_path).unwrap_or_default();
            let new_content = format!("{}{}", existing, entry);

            fs::write(&file_path, new_content).expect("Gagal menulis catatan");
            println!("Catatan '{}' ditambahkan ke {}", title, file_path.display());
        }
        "lihat" => {
            let content = fs::read_to_string(&file_path).unwrap_or_default();
            if content.is_empty() {
                println("Belum ada catatan.");
            } else {
                println!("=== Daftar Catatan ===");
                for line in content.lines() {
                    if !line.is_empty() {
                        let parts: Vec<&str> = line.splitn(2, "::").collect();
                        if parts.len() == 2 {
                            println!("- {}: {}", parts[0], parts[1]);
                        }
                    }
                }
            }
        }
        "hapus" => {
            if file_path.exists() {
                fs::remove_file(&file_path).expect("Gagal menghapus file catatan");
                println!("Semua catatan dihapus.");
            } else {
                println!("File catatan tidak ditemukan.");
            }
        }
        _ => println!("Aksi tidak dikenal. Gunakan: tambah, lihat, atau hapus"),
    }
}

fn main() {
    let cli = Cli::parse();

    if cli.verbose > 0 {
        eprintln!("Verbose level: {}", cli.verbose);
    }

    match &cli.command {
        Commands::Note(args) => manage_notes(args),
        Commands::Convert { value, from, to } => {
            let result = convert_suhu(*value, from, to);
            println!("{} {} = {:.2} {}", value, from.to_uppercase(), result, to.to_uppercase());
        }
        Commands::Info => {
            println!("=== Informasi Sistem ===");
            println!("OS: {}", std::env::consts::OS);
            println!("Arsitektur: {}", std::env::consts::ARCH);
            println!("Famili: {}", std::env::consts::FAMILY);
            println!("Versi Rust CLI: 1.0.0");
        }
        Commands::Cipher(args) => {
            let result = caesar_cipher(&args.text, args.shift, &args.mode);
            println!("Hasil ({}): {}", args.mode, result);
        }
    }
}
