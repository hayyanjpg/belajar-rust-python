// Materi 21: Async/Await dengan Tokio
//
// Perbedaan penting:
// - Thread OS: paralel, mahal, cocok untuk CPU-bound.
// - Task async: murah, dijalankan runtime, cocok untuk I/O-bound.
// - `await` hanya menyerahkan kontrol ke runtime, BUKAN membuat thread baru.
//
// Jalankan: cargo run
// Jalankan tes: cargo test
//
// Fitur yang dipakai di Cargo.toml:
// - macros        : #[tokio::main], #[tokio::test]
// - rt-multi-thread: thread pool tempat task dijalankan
// - time          : sleep, timeout
// - sync          : channel mpsc

use std::time::{Duration, Instant};

use tokio::sync::mpsc;
use tokio::time::sleep;

/// Fungsi async yang menyimulasikan pekerjaan I/O (misalnya request HTTP).
async fn tugas(id: u32, ms: u64) -> (u32, u64) {
    println!("  [tugas {id}] mulai ({} ms)", ms);
    sleep(Duration::from_millis(ms)).await;
    println!("  [tugas {id}] selesai");
    (id, ms * 2)
}

/// Produser mengirim beberapa nilai lewat channel async.
async fn produser(tx: mpsc::Sender<u32>) {
    for nilai in 1..=3 {
        tx.send(nilai)
            .await
            .expect("penerima sudah drop sebelum pengiriman selesai");
        sleep(Duration::from_millis(10)).await;
    }
}

#[tokio::main]
async fn main() {
    println!("{}", "=".repeat(50));
    println!("DEMO ASYNC DENGAN TOKIO");
    println!("{}", "=".repeat(50));

    println!("\n--- 1. BERURUTAN (sequential) ---");
    let mulai = Instant::now();
    let a = tugas(1, 60).await;
    let b = tugas(2, 60).await;
    println!("  hasil: {a:?}, {b:?}");
    println!("  total waktu: {:?} (~120 ms karena berurutan)", mulai.elapsed());

    println!("\n--- 2. join! (konkuren dalam satu task) ---");
    let mulai = Instant::now();
    let (c, d) = tokio::join!(tugas(3, 60), tugas(4, 60));
    println!("  hasil: {c:?}, {d:?}");
    println!("  total waktu: {:?} (~60 ms karena bersamaan)", mulai.elapsed());

    println!("\n--- 3. tokio::spawn (task baru) ---");
    let mulai = Instant::now();
    let handle = tokio::spawn(tugas(5, 40));
    let hasil_spawn = handle.await.expect("task panic");
    println!("  hasil dari task: {hasil_spawn:?}");
    println!("  total waktu: {:?}", mulai.elapsed());

    println!("\n--- 4. CHANNEL mpsc ---");
    let (tx, mut rx) = mpsc::channel::<u32>(8);
    tokio::spawn(produser(tx));
    let mut diterima = Vec::new();
    while let Some(nilai) = rx.recv().await {
        println!("  diterima: {nilai}");
        diterima.push(nilai);
    }
    println!("  semua pesan: {diterima:?}");

    println!("\n--- 5. TIMEOUT ---");
    match tokio::time::timeout(Duration::from_millis(30), tugas(6, 200)).await {
        Ok(hasil) => println!("  selesai sebelum timeout: {hasil:?}"),
        Err(_) => println!("  timeout! tugas 6 melebihi 30 ms"),
    }

    println!("\n--- 6. Send + Sync ---");
    println!("  tokio::spawn mensyaratkan future: Send + 'static.");
    println!("  Rc<...> tidak Send; pakai Arc<...> jika dipakai lintas task.");

    println!("\n=== SELESAI ===");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn tugas_mengembalikan_hasil() {
        assert_eq!(tugas(7, 0).await, (7, 0));
        assert_eq!(tugas(8, 5).await, (8, 10));
    }

    #[tokio::test]
    async fn join_menjalankan_berdua() {
        let mulai = Instant::now();
        let (a, b) = tokio::join!(tugas(1, 20), tugas(2, 20));
        assert_eq!((a, b), ((1, 40), (2, 40)));
        assert!(mulai.elapsed() < Duration::from_millis(100));
    }

    #[tokio::test]
    async fn channel_mengirim_tiga_pesan() {
        let (tx, mut rx) = mpsc::channel::<u32>(4);
        tokio::spawn(produser(tx));

        let mut hasil = Vec::new();
        while let Some(nilai) = rx.recv().await {
            hasil.push(nilai);
        }
        assert_eq!(hasil, vec![1, 2, 3]);
    }

    #[tokio::test]
    async fn timeout_mendeteksi_tugas_lambat() {
        let hasil = tokio::time::timeout(Duration::from_millis(5), tugas(9, 100)).await;
        assert!(hasil.is_err());
    }
}
