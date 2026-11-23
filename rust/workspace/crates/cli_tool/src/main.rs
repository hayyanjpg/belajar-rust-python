use clap::{Parser, Subcommand};

#[derive(Parser, Debug)]
#[command(author, version, about)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Ucapkan selamat
    Greet {
        /// Nama orang
        name: String,
    },
    /// Hitung fibonacci
    Fib {
        /// Posisi fibonacci
        n: u32,
    },
}

fn fibonacci(n: u32) -> u64 {
    match n {
        0 => 0,
        1 => 1,
        _ => {
            let mut a = 0;
            let mut b = 1;
            for _ in 2..=n {
                let c = a + b;
                a = b;
                b = c;
            }
            b
        }
    }
}

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Commands::Greet { name } => {
            println!("Halo, {}! Selamat belajar Rust!", name);
        }
        Commands::Fib { n } => {
            println!("Fibonacci({}) = {}", n, fibonacci(n));
        }
    }
}
