// Materi 14: Smart Pointer - Box, Rc, RefCell, Arc, Weak
// Penjelasan: Smart pointer adalah tipe yang memiliki data di heap sekaligus
// menyimpan metadata kepemilikan. Ringkasan:
//
//   Box<T>          : 1 pemilik, data di heap
//   Rc<T>           : banyak pemilik, hanya untuk single-thread
//   Arc<T>          : banyak pemilik, aman antar-thread (atomic)
//   RefCell<T>      : interior mutability, aturan borrow dicek saat runtime
//   Weak<T>         : reference tanpa kepemilikan, mencegah reference cycle
//
// Catatan: Rc/RefCell BUKAN untuk multi-thread. Untuk itu pakai Arc/Mutex.

use std::cell::RefCell;
use std::rc::{Rc, Weak};
use std::sync::Arc;
use std::thread;

// ============================================
// 1. BOX<T> - DATA DI HEAP
// ============================================
// Enum rekursif wajib memakai Box agar ukurannya diketahui compiler.
#[derive(Debug)]
enum List {
    Kosong,
    Node(i32, Box<List>),
}

impl List {
    fn panjang(&self) -> usize {
        match self {
            List::Kosong => 0,
            List::Node(_, sisa) => 1 + sisa.panjang(),
        }
    }

    fn jumlah(&self) -> i32 {
        match self {
            List::Kosong => 0,
            List::Node(nilai, sisa) => nilai + sisa.jumlah(),
        }
    }
}

// Trait object juga sering dibungkus Box.
trait Suara {
    fn suara(&self) -> &'static str;
}

struct Kucing;
struct Anjing;

impl Suara for Kucing {
    fn suara(&self) -> &'static str {
        "meong"
    }
}

impl Suara for Anjing {
    fn suara(&self) -> &'static str {
        "guk guk"
    }
}

fn demo_box() {
    println!("\n--- BOX<T> ---");

    // Angka biasa ada di stack; Box memindahkannya ke heap.
    let di_heap = Box::new(42);
    println!("  Box<i32>: {}", di_heap);
    println!("  deref   : {}", *di_heap);

    // List rekursif
    let list = List::Node(
        1,
        Box::new(List::Node(2, Box::new(List::Node(3, Box::new(List::Kosong))))),
    );
    println!("  list   : {:?}", list);
    println!("  panjang: {}", list.panjang());
    println!("  jumlah : {}", list.jumlah());

    // Box<dyn Trait>: polymorphism dengan data di heap
    let hewan: Vec<Box<dyn Suara>> = vec![Box::new(Kucing), Box::new(Anjing)];
    for h in &hewan {
        println!("  suara: {}", h.suara());
    }
}

// ============================================
// 2. RC<T> - SHARED OWNERSHIP (SINGLE THREAD)
// ============================================
fn demo_rc() {
    println!("\n--- RC<T> ---");

    let data = Rc::new(vec![1, 2, 3, 4]);
    println!("  awal strong_count: {}", Rc::strong_count(&data));

    {
        let a = Rc::clone(&data); // clone Rc = menambah pemilik, BUKAN meng-copy data
        let b = Rc::clone(&data);
        println!("  setelah 2 clone   : {}", Rc::strong_count(&data));
        println!("  a = {:?}, b = {:?}", a, b);
        println!("  alamat sama? {}", Rc::ptr_eq(&data, &a));
    } // a dan b drop di sini

    println!("  setelah scope     : {}", Rc::strong_count(&data));
    println!("  isi data          : {:?}", data);

    // Rc tidak bisa diubah isinya (immutable). Untuk mutable, lihat RefCell.
}

// ============================================
// 3. REFCELL<T> - INTERIOR MUTABILITY
// ============================================
fn demo_refcell() {
    println!("\n--- REFCELL<T> ---");

    let nilai = RefCell::new(10);

    // borrow_mut() memberi RefMut, aturan borrow dicek saat runtime.
    *nilai.borrow_mut() += 5;
    println!("  setelah +5: {}", nilai.borrow());

    // Banyak immutable borrow boleh bersamaan.
    {
        let b1 = nilai.borrow();
        let b2 = nilai.borrow();
        println!("  dua borrow: {} dan {}", b1, b2);
    }

    // Kalau aturan dilanggar, RefCell mengembalikan error (tidak panic).
    let b1 = nilai.borrow();
    match nilai.try_borrow_mut() {
        Ok(_) => println!("  borrow_mut berhasil"),
        Err(e) => println!("  borrow_mut ditolak (runtime): {}", e),
    }
    drop(b1);

    *nilai.borrow_mut() += 1;
    println!("  setelah b1 drop: {}", nilai.borrow());
}

// ============================================
// 4. RC<REFCELL<T>> - SHARED + MUTABLE
// ============================================
#[derive(Debug)]
struct Catatan {
    baris: Vec<String>,
}

fn demo_rc_refcell() {
    println!("\n--- RC<REFCELL<T>> ---");

    let catatan = Rc::new(RefCell::new(Catatan { baris: Vec::new() }));

    let pemilik_lain = Rc::clone(&catatan);
    pemilik_lain
        .borrow_mut()
        .baris
        .push("dibuat oleh pemilik_lain".to_string());

    catatan
        .borrow_mut()
        .baris
        .push("dibuat oleh pemilik utama".to_string());

    println!("  strong_count: {}", Rc::strong_count(&catatan));
    println!("  isi: {:?}", catatan.borrow().baris);

    // Shared counter
    let counter = Rc::new(RefCell::new(0));
    let clones: Vec<Rc<RefCell<i32>>> = (0..3).map(|_| Rc::clone(&counter)).collect();
    for c in &clones {
        *c.borrow_mut() += 1;
    }
    println!("  counter: {}", counter.borrow());
}

// ============================================
// 5. ARC<T> - SHARED OWNERSHIP ANTAR-THREAD
// ============================================
fn demo_arc() {
    println!("\n--- ARC<T> ---");

    let data = Arc::new(vec![1, 2, 3, 4, 5]);
    println!("  strong_count awal: {}", Arc::strong_count(&data));

    let mut handles = Vec::new();
    for id in 0..3 {
        let data = Arc::clone(&data); // clone murah: hanya menambah counter
        handles.push(thread::spawn(move || {
            let total: i32 = data.iter().sum();
            println!("  thread {}: total {}", id, total);
            total
        }));
    }

    let total_semua: i32 = handles
        .into_iter()
        .map(|h| h.join().expect("thread panic"))
        .sum();
    println!("  hasil join semua thread: {}", total_semua);
    println!("  strong_count akhir: {}", Arc::strong_count(&data));
}

// ============================================
// 6. WEAK<T> - MENCEGAH REFERENCE CYCLE
// ============================================
// Kalau parent menyimpan Rc<Node> ke child dan child menyimpan Rc<Node> ke parent,
// strong_count tidak pernah 0 -> memori bocor. Solusinya: satu arah pakai Weak.
struct Node {
    nama: &'static str,
    anak: RefCell<Vec<Rc<Node>>>,
    induk: RefCell<Weak<Node>>,
}

impl Node {
    fn new(nama: &'static str) -> Rc<Node> {
        Rc::new(Node {
            nama,
            anak: RefCell::new(Vec::new()),
            induk: RefCell::new(Weak::new()),
        })
    }
}

fn demo_weak() {
    println!("\n--- WEAK<T> ---");

    let induk = Node::new("induk");
    let anak = Node::new("anak");

    // Hubungan dua arah: induk -> anak (Rc), anak -> induk (Weak)
    induk.anak.borrow_mut().push(Rc::clone(&anak));
    *anak.induk.borrow_mut() = Rc::downgrade(&induk);

    println!("  strong induk: {}", Rc::strong_count(&induk));
    println!("  strong anak : {}", Rc::strong_count(&anak));
    println!("  weak induk  : {}", Rc::weak_count(&induk));

    // Naik dari anak ke induk lewat upgrade()
    match anak.induk.borrow().upgrade() {
        Some(p) => println!("  induk dari anak: {}", p.nama),
        None => println!("  induk sudah dibebaskan"),
    }

    // Turun dari induk ke anak
    for a in induk.anak.borrow().iter() {
        println!("  anak dari induk: {}", a.nama);
    }

    drop(anak); // strong_count anak turun, tapi induk tetap hidup
    println!("  setelah anak di-drop, strong induk: {}", Rc::strong_count(&induk));
}

// ============================================
// 7. LATIHAN
// ============================================
fn latihan() {
    println!("\n--- LATIHAN ---");

    // Latihan 1: evaluasi ekspresi rekursif dengan Box
    enum Ekspresi {
        Angka(i32),
        Tambah(Box<Ekspresi>, Box<Ekspresi>),
        Kali(Box<Ekspresi>, Box<Ekspresi>),
    }

    impl Ekspresi {
        fn evaluasi(&self) -> i32 {
            match self {
                Ekspresi::Angka(n) => *n,
                Ekspresi::Tambah(a, b) => a.evaluasi() + b.evaluasi(),
                Ekspresi::Kali(a, b) => a.evaluasi() * b.evaluasi(),
            }
        }
    }

    // (2 + 3) * 4 = 20
    let ekspresi = Ekspresi::Kali(
        Box::new(Ekspresi::Tambah(
            Box::new(Ekspresi::Angka(2)),
            Box::new(Ekspresi::Angka(3)),
        )),
        Box::new(Ekspresi::Angka(4)),
    );
    println!("  1. (2 + 3) * 4 = {}", ekspresi.evaluasi());

    // Latihan 2: Rc sebagai shared config
    let konfigurasi = Rc::new(vec!["debug", "verbose"]);
    let fitur = Rc::clone(&konfigurasi);
    println!("  2. fitur: {:?}, pemilik: {}", fitur, Rc::strong_count(&konfigurasi));

    // Latihan 3: RefCell sebagai antrean sederhana
    let antrean = RefCell::new(Vec::new());
    antrean.borrow_mut().push("tugas-1");
    antrean.borrow_mut().push("tugas-2");
    println!("  3. antrean: {:?}", antrean.borrow());

    // Latihan 4: Rc<RefCell> sebagai penghitung bersama
    let skor = Rc::new(RefCell::new(0));
    let pemain = vec![Rc::clone(&skor), Rc::clone(&skor)];
    for s in &pemain {
        *s.borrow_mut() += 10;
    }
    println!("  4. skor akhir: {}", skor.borrow());

    // Latihan 5: Arc dipakai dua thread
    let angka = Arc::new(100);
    let mut handles = Vec::new();
    for _ in 0..2 {
        let angka = Arc::clone(&angka);
        handles.push(thread::spawn(move || *angka + 1));
    }
    let hasil: Vec<i32> = handles.into_iter().map(|h| h.join().unwrap()).collect();
    println!("  5. hasil thread: {:?}", hasil);
}

// ============================================
// MAIN DEMO
// ============================================
fn main() {
    println!("{}", "=".repeat(50));
    println!("DEMO SMART POINTER RUST");
    println!("{}", "=".repeat(50));

    demo_box();
    demo_rc();
    demo_refcell();
    demo_rc_refcell();
    demo_arc();
    demo_weak();
    latihan();

    println!("\n=== SELESAI ===");
}
