// Materi 09: Collections - Vec, String, HashMap, HashSet, BTreeMap
// Penjelasan: Rust punya koleksi di standard library. Yang paling sering dipakai:
// - Vec<T>      : array dinamis (mirip list Python)
// - String      : teks yang bisa tumbuh (mirip str Python)
// - HashMap<K,V>: key-value tanpa urutan (mirip dict Python)
// - HashSet<T>  : kumpulan nilai unik (mirip set Python)
// - BTreeMap<K,V>: key-value yang selalu terurut berdasarkan key

use std::collections::{BTreeMap, HashMap, HashSet};

// ============================================
// 1. VEC<T> - ARRAY DINAMIS
// ============================================
fn demo_vec() {
    println!("\n--- VEC<T> ---");

    // Membuat Vec: Vec::new() atau makro vec![]
    let mut angka: Vec<i32> = Vec::new();
    angka.push(30);
    angka.push(10);
    angka.push(20);
    angka.extend([40, 50]); // tambah banyak sekaligus
    println!("  isi: {:?}", angka);

    // Akses: indexing (panic kalau salah) vs get (mengembalikan Option)
    println!("  angka[0]: {}", angka[0]);
    match angka.get(99) {
        Some(v) => println!("  index 99: {}", v),
        None => println!("  index 99: tidak ada (aman, tidak panic)"),
    }

    // Update & hapus
    angka[1] = 11;
    let terakhir = angka.pop(); // hapus dari belakang
    println!("  setelah update & pop: {:?} (pop = {:?})", angka, terakhir);

    angka.insert(0, 5); // sisipkan di index 0
    let dihapus = angka.remove(2); // hapus index 2, geser sisanya
    println!("  insert(0,5) + remove(2): {:?} (dihapus = {})", angka, dihapus);

    // Filter di tempat
    angka.retain(|&x| x % 2 == 0);
    println!("  retain genap: {:?}", angka);

    // Sort & binary search (data harus terurut dulu)
    angka.sort();
    println!("  sort: {:?}", angka);
    println!("  binary_search(&20): {:?}", angka.binary_search(&20));

    // Iterasi: &vec (borrow), iter_mut (ubah), into_iter (pindah ownership)
    let total: i32 = angka.iter().sum();
    let rata_rata = total as f64 / angka.len() as f64;
    println!("  total: {}, rata-rata: {:.2}", total, rata_rata);

    let mut kuadrat = angka.clone();
    for n in kuadrat.iter_mut() {
        *n *= *n;
    }
    println!("  kuadrat: {:?}", kuadrat);

    // Vec 2 dimensi (matriks)
    let matriks: Vec<Vec<i32>> = vec![vec![1, 2], vec![3, 4]];
    println!("  matriks[1][0]: {}", matriks[1][0]);
}

// ============================================
// 2. STRING - TEKS YANG BISA TUMBUH
// ============================================
fn demo_string() {
    println!("\n--- STRING ---");

    // String = owned, &str = borrow (slice)
    let mut s = String::from("Halo");
    s.push_str(", Rust"); // tambah &str
    s.push('!'); // tambah satu char
    println!("  s: {}", s);
    println!("  len (byte): {}, jumlah char: {}", s.len(), s.chars().count());

    // String tidak bisa di-index dengan s[0] karena UTF-8.
    // Gunakan chars() atau bytes(), atau slice &s[0..4] (harus di batas char).
    println!("  huruf pertama: {:?}", s.chars().next());
    println!("  byte pertama: {}", s.as_bytes()[0]);

    // Method umum
    println!("  uppercase: {}", s.to_uppercase());
    println!("  replace: {}", s.replace("Rust", "Python"));
    println!("  split: {:?}", "apel,jeruk,mangga".split(',').collect::<Vec<_>>());

    // Gabung Vec<String> menjadi satu String
    let buah = vec!["apel".to_string(), "jeruk".to_string(), "mangga".to_string()];
    println!("  join: {}", buah.join(" | "));

    // Parsing string -> angka (mengembalikan Result)
    match "42".parse::<i32>() {
        Ok(n) => println!("  parse '42' -> {}", n),
        Err(e) => println!("  parse gagal: {}", e),
    }

    // Trim & cek isi
    let kotor = "  teks dengan spasi  ";
    println!("  trim: '{}'", kotor.trim());
    println!("  starts_with: {}", s.starts_with("Halo"));
    println!("  contains: {}", s.contains("Rust"));
}

// ============================================
// 3. HASHMAP<K, V> - KEY-VALUE
// ============================================
fn hitung_kata(teks: &str) -> HashMap<String, usize> {
    let mut hasil = HashMap::new();
    for kata in teks.split_whitespace() {
        // entry API: hitung tanpa lookup dua kali
        *hasil.entry(kata.to_lowercase()).or_insert(0) += 1;
    }
    hasil
}

fn demo_hashmap() {
    println!("\n--- HASHMAP<K, V> ---");

    let mut stok: HashMap<String, u32> = HashMap::new();
    stok.insert("apel".to_string(), 10);
    stok.insert("jeruk".to_string(), 5);

    // entry(): insert kalau belum ada, update kalau sudah ada
    *stok.entry("apel".to_string()).or_insert(0) += 3;
    *stok.entry("mangga".to_string()).or_insert(0) += 7;
    println!("  stok: {:?}", stok);

    // Akses aman dengan get
    match stok.get("jeruk") {
        Some(jumlah) => println!("  jeruk: {}", jumlah),
        None => println!("  jeruk tidak ada"),
    }
    println!("  get('durian').unwrap_or(0): {}", stok.get("durian").unwrap_or(&0));

    // Iterasi HashMap urutannya acak; sort dulu kalau butuh output stabil
    let mut items: Vec<_> = stok.iter().collect();
    items.sort_by_key(|(nama, _)| (*nama).clone());
    for (nama, jumlah) in items {
        println!("  - {}: {}", nama, jumlah);
    }

    // Hapus
    stok.remove("jeruk");
    println!("  setelah remove jeruk: {} item", stok.len());
    println!("  contains_key('apel'): {}", stok.contains_key("apel"));

    // Studi kasus: hitung frekuensi kata
    let teks = "rust itu cepat rust itu aman python itu mudah";
    let frekuensi = hitung_kata(teks);
    let mut urut: Vec<_> = frekuensi.iter().collect();
    urut.sort_by(|a, b| b.1.cmp(a.1).then(a.0.cmp(b.0)));
    println!("  frekuensi kata:");
    for (kata, jumlah) in urut {
        println!("    {}: {}", kata, jumlah);
    }
}

// ============================================
// 4. HASHSET<T> - NILAI UNIK
// ============================================
fn demo_hashset() {
    println!("\n--- HASHSET<T> ---");

    let mut unik: HashSet<i32> = HashSet::new();
    for n in [3, 1, 3, 2, 1, 4] {
        let baru = unik.insert(n);
        println!("  insert({}) -> {}", n, if baru { "baru" } else { "duplikat" });
    }
    println!("  isi unik: {:?}", unik);
    println!("  contains(2): {}", unik.contains(&2));

    // Operasi himpunan
    let a: HashSet<i32> = [1, 2, 3, 4].into_iter().collect();
    let b: HashSet<i32> = [3, 4, 5, 6].into_iter().collect();

    let irisan: HashSet<_> = a.intersection(&b).copied().collect();
    let gabungan: HashSet<_> = a.union(&b).copied().collect();
    let selisih: HashSet<_> = a.difference(&b).copied().collect();

    println!("  a: {:?}", a);
    println!("  b: {:?}", b);
    println!("  irisan: {:?}", irisan);
    println!("  gabungan: {:?}", gabungan);
    println!("  a - b: {:?}", selisih);

    // Deduplikasi Vec sambil menjaga urutan
    let data = vec![3, 1, 3, 2, 1, 4];
    let mut terlihat = HashSet::new();
    let tanpa_duplikat: Vec<i32> = data
        .into_iter()
        .filter(|n| terlihat.insert(*n))
        .collect();
    println!("  dedup: {:?}", tanpa_duplikat);
}

// ============================================
// 5. BTREEMAP<K, V> - KEY-VALUE TERURUT
// ============================================
fn demo_btreemap() {
    println!("\n--- BTREEMAP<K, V> ---");

    // BTreeMap selalu terurut berdasarkan key (butuh Ord)
    let mut peringkat: BTreeMap<u32, String> = BTreeMap::new();
    peringkat.insert(3, "Budi".to_string());
    peringkat.insert(1, "Hayyan".to_string());
    peringkat.insert(2, "Rina".to_string());
    peringkat.insert(4, "Sari".to_string());

    for (posisi, nama) in &peringkat {
        println!("  {}: {}", posisi, nama);
    }

    // range() memakai urutan key
    println!("  range 2..=3:");
    for (posisi, nama) in peringkat.range(2..=3) {
        println!("    {}: {}", posisi, nama);
    }

    println!("  first_key_value: {:?}", peringkat.first_key_value());
    println!("  last_key_value: {:?}", peringkat.last_key_value());
}

// ============================================
// LATIHAN
// ============================================
fn latihan() {
    println!("\n--- LATIHAN ---");

    // Latihan 1: jumlahkan semua angka genap di Vec
    let angka = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    let total_genap: i32 = angka.iter().filter(|&&n| n % 2 == 0).sum();
    println!("  1. total genap: {}", total_genap);

    // Latihan 2: cari nilai terbesar & terkecil
    let maks = angka.iter().max().unwrap();
    let min = angka.iter().min().unwrap();
    println!("  2. min: {}, max: {}", min, maks);

    // Latihan 3: kelompokkan angka berdasarkan ganjil/genap
    let mut kelompok: HashMap<&str, Vec<i32>> = HashMap::new();
    for n in &angka {
        let kunci = if n % 2 == 0 { "genap" } else { "ganjil" };
        kelompok.entry(kunci).or_default().push(*n);
    }
    let mut kunci: Vec<_> = kelompok.keys().copied().collect();
    kunci.sort();
    for k in kunci {
        println!("  3. {}: {:?}", k, kelompok[k]);
    }

    // Latihan 4: cek apakah dua Vec punya elemen yang sama
    let a = vec![1, 2, 3];
    let b = vec![3, 4, 5];
    let set_a: HashSet<_> = a.iter().collect();
    let ada_irisan = b.iter().any(|n| set_a.contains(n));
    println!("  4. punya irisan: {}", ada_irisan);

    // Latihan 5: hitung total harga belanja
    let belanja = vec![("apel", 3, 5_000), ("jeruk", 2, 8_000), ("mangga", 1, 12_000)];
    let total: u32 = belanja.iter().map(|(_, jumlah, harga)| jumlah * harga).sum();
    println!("  5. total belanja: Rp{}", total);
}

// ============================================
// MAIN DEMO
// ============================================
fn main() {
    println!("{}", "=".repeat(50));
    println!("DEMO COLLECTIONS RUST");
    println!("{}", "=".repeat(50));

    demo_vec();
    demo_string();
    demo_hashmap();
    demo_hashset();
    demo_btreemap();
    latihan();

    println!("\n=== SELESAI ===");
}
