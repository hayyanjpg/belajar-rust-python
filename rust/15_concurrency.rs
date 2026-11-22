// Materi 15: Concurrency - Thread, Channel, Mutex, Arc, RwLock
// Penjelasan: Rust memaksa kita memikirkan data sharing sejak compile time.
// Aturan utamanya: data yang dipakai bersama antar-thread harus aman (Send + Sync).
//
// Alat utama di standard library:
// - thread::spawn / thread::scope : membuat thread
// - mpsc::channel                : kirim pesan antar-thread
// - Arc<T>                       : shared ownership antar-thread
// - Mutex<T> / RwLock<T>         : akses eksklusif ke data bersama
// - Atomic*                      : operasi angka tanpa lock

use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::{mpsc, Arc, Mutex, RwLock};
use std::thread;
use std::time::Duration;

// ============================================
// 1. THREAD DASAR
// ============================================
fn demo_thread() {
    println!("\n--- THREAD DASAR ---");

    let handle = thread::spawn(|| {
        for i in 1..=3 {
            println!("  [thread anak] langkah {}", i);
            thread::sleep(Duration::from_millis(10));
        }
        6 * 7
    });

    // Main thread tetap berjalan sementara thread anak bekerja.
    println!("  [main] tetap jalan tanpa menunggu");

    // join() menunggu thread selesai dan mengambil return value.
    let hasil = handle.join().expect("thread anak panic");
    println!("  [main] hasil thread anak: {}", hasil);

    // Thread bisa diberi nama untuk debugging.
    let bernama = thread::Builder::new()
        .name("pekerja-1".to_string())
        .spawn(|| format!("dijalankan oleh {:?}", thread::current().name()))
        .expect("gagal membuat thread");
    println!("  {}", bernama.join().unwrap());
}

// ============================================
// 2. MOVE CLOSURE
// ============================================
fn demo_move() {
    println!("\n--- MOVE CLOSURE ---");

    let data = vec![1, 2, 3, 4, 5];

    // `move` memindahkan ownership `data` ke thread.
    let handle = thread::spawn(move || {
        let total: i32 = data.iter().sum();
        (total, data.len())
    });

    // data sudah dipindah, jadi tidak bisa dipakai di sini:
    // println!("{:?}", data); // ERROR: borrow of moved value

    let (total, jumlah) = handle.join().unwrap();
    println!("  total: {}, jumlah: {}", total, jumlah);
}

// ============================================
// 3. SHARED STATE: ARC<MUTEX<T>>
// ============================================
fn demo_mutex() {
    println!("\n--- ARC<MUTEX<T>> ---");

    let counter = Arc::new(Mutex::new(0));
    let mut handles = Vec::new();

    for id in 0..5 {
        let counter = Arc::clone(&counter);
        handles.push(thread::spawn(move || {
            let mut nilai = counter.lock().expect("mutex poisoned");
            *nilai += 1;
            println!("  thread {} menambah, nilai = {}", id, *nilai);
        }));
    }

    for h in handles {
        h.join().unwrap();
    }

    println!("  hasil akhir: {}", *counter.lock().unwrap());

    // lock() mengembalikan guard. Guard otomatis dilepas saat keluar scope.
    {
        let mut guard = counter.lock().unwrap();
        *guard += 100;
    } // lock dilepas di sini
    println!("  setelah +100: {}", *counter.lock().unwrap());
}

// ============================================
// 4. CHANNEL (MPSC)
// ============================================
fn demo_channel() {
    println!("\n--- CHANNEL (MPSC) ---");

    // mpsc = multi-producer, single-consumer
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        for i in 1..=5 {
            tx.send(i * 10).expect("receiver sudah drop");
        }
    });

    // rx bisa diiterasi sampai semua sender drop.
    let diterima: Vec<i32> = rx.iter().collect();
    println!("  diterima: {:?}", diterima);

    // Banyak producer
    let (tx, rx) = mpsc::channel();
    for id in 0..3 {
        let tx = tx.clone();
        thread::spawn(move || {
            for i in 0..2 {
                tx.send(format!("worker-{}:{}", id, i)).unwrap();
            }
        });
    }
    drop(tx); // drop sender utama agar rx.iter() berhenti

    let mut pesan: Vec<String> = rx.iter().collect();
    pesan.sort();
    println!("  dari banyak producer: {:?}", pesan);
}

// ============================================
// 5. RWLOCK - BANYAK PEMBACA, SATU PENULIS
// ============================================
fn demo_rwlock() {
    println!("\n--- RWLOCK ---");

    let data = Arc::new(RwLock::new(vec![1, 2, 3]));

    let mut pembaca = Vec::new();
    for id in 0..3 {
        let data = Arc::clone(&data);
        pembaca.push(thread::spawn(move || {
            let isi = data.read().unwrap();
            println!("  pembaca {}: {:?}", id, *isi);
        }));
    }

    {
        let mut isi = data.write().unwrap();
        isi.push(4);
        println!("  penulis menambah 4");
    } // write lock dilepas

    for h in pembaca {
        h.join().unwrap();
    }
    println!("  hasil akhir: {:?}", *data.read().unwrap());
}

// ============================================
// 6. ATOMIC - COUNTER TANPA LOCK
// ============================================
fn demo_atomic() {
    println!("\n--- ATOMIC ---");

    let counter = Arc::new(AtomicUsize::new(0));
    let mut handles = Vec::new();

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        handles.push(thread::spawn(move || {
            counter.fetch_add(1, Ordering::SeqCst);
        }));
    }

    for h in handles {
        h.join().unwrap();
    }

    println!("  counter: {}", counter.load(Ordering::SeqCst));
}

// ============================================
// 7. SCOPED THREADS - BORROW TANPA ARC
// ============================================
fn demo_scope() {
    println!("\n--- THREAD::SCOPE ---");

    let data = vec![1, 2, 3, 4, 5];
    let total = AtomicUsize::new(0);

    // thread::scope menjamin semua thread selesai sebelum scope berakhir,
    // jadi boleh meminjam data lokal tanpa Arc.
    thread::scope(|s| {
        for chunk in data.chunks(2) {
            let total = &total;
            s.spawn(move || {
                let jumlah: usize = chunk.iter().sum::<i32>() as usize;
                total.fetch_add(jumlah, Ordering::SeqCst);
            });
        }
    });

    println!("  total lewat scope: {}", total.load(Ordering::SeqCst));

    // Borrow mutable juga aman karena scope menunggu semua thread.
    let mut angka = vec![1, 2, 3];
    thread::scope(|s| {
        s.spawn(|| {
            angka.push(4);
        });
    });
    println!("  setelah push di thread: {:?}", angka);
}

// ============================================
// 8. LATIHAN
// ============================================
fn jumlah_paralel(data: &[i32], jumlah_thread: usize) -> i32 {
    let chunk_size = (data.len() + jumlah_thread - 1) / jumlah_thread;
    let data = Arc::new(data.to_vec());
    let mut handles = Vec::new();

    for i in 0..jumlah_thread {
        let data = Arc::clone(&data);
        handles.push(thread::spawn(move || {
            let mulai = i * chunk_size;
            let selesai = (mulai + chunk_size).min(data.len());
            data[mulai..selesai].iter().sum::<i32>()
        }));
    }

    handles.into_iter().map(|h| h.join().unwrap()).sum()
}

fn latihan() {
    println!("\n--- LATIHAN ---");

    // Latihan 1: jumlah paralel
    let data: Vec<i32> = (1..=100).collect();
    println!("  1. jumlah paralel: {}", jumlah_paralel(&data, 4));

    // Latihan 2: worker pool sederhana lewat channel
    let (tx_tugas, rx_tugas) = mpsc::channel::<i32>();
    let (tx_hasil, rx_hasil) = mpsc::channel::<i32>();
    let rx_tugas = Arc::new(Mutex::new(rx_tugas));
    let mut workers = Vec::new();

    for _ in 0..3 {
        let rx_tugas = Arc::clone(&rx_tugas);
        let tx_hasil = tx_hasil.clone();
        workers.push(thread::spawn(move || loop {
            let tugas = rx_tugas.lock().unwrap().recv();
            match tugas {
                Ok(n) => {
                    tx_hasil.send(n * n).unwrap();
                }
                Err(_) => break,
            }
        }));
    }
    drop(tx_hasil);

    for n in 1..=6 {
        tx_tugas.send(n).unwrap();
    }
    drop(tx_tugas);

    for w in workers {
        w.join().unwrap();
    }

    let mut hasil: Vec<i32> = rx_hasil.iter().collect();
    hasil.sort();
    println!("  2. kuadrat dari worker: {:?}", hasil);

    // Latihan 3: log bersama dari banyak thread
    let log = Arc::new(Mutex::new(Vec::new()));
    let mut handles = Vec::new();
    for id in 0..4 {
        let log = Arc::clone(&log);
        handles.push(thread::spawn(move || {
            log.lock().unwrap().push(format!("thread-{}", id));
        }));
    }
    for h in handles {
        h.join().unwrap();
    }
    let mut isi_log = log.lock().unwrap().clone();
    isi_log.sort();
    println!("  3. log: {:?}", isi_log);

    // Latihan 4: atomic sebagai penghitung error
    let error = Arc::new(AtomicUsize::new(0));
    let mut handles = Vec::new();
    for i in 0..6 {
        let error = Arc::clone(&error);
        handles.push(thread::spawn(move || {
            if i % 2 == 0 {
                error.fetch_add(1, Ordering::Relaxed);
            }
        }));
    }
    for h in handles {
        h.join().unwrap();
    }
    println!("  4. jumlah error: {}", error.load(Ordering::Relaxed));

    // Latihan 5: scoped thread menjumlahkan slice tanpa Arc
    let nilai = vec![10, 20, 30, 40];
    let hasil = AtomicUsize::new(0);
    thread::scope(|s| {
        for n in &nilai {
            let hasil = &hasil;
            s.spawn(move || {
                hasil.fetch_add(*n as usize, Ordering::SeqCst);
            });
        }
    });
    println!("  5. total scope: {}", hasil.load(Ordering::SeqCst));
}

// ============================================
// MAIN DEMO
// ============================================
fn main() {
    println!("{}", "=".repeat(50));
    println!("DEMO CONCURRENCY RUST");
    println!("{}", "=".repeat(50));

    demo_thread();
    demo_move();
    demo_mutex();
    demo_channel();
    demo_rwlock();
    demo_atomic();
    demo_scope();
    latihan();

    println!("\n=== SELESAI ===");
}
