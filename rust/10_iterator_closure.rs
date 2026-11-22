// Materi 10: Iterator & Closure
// Penjelasan: Iterator menghasilkan elemen satu per satu (lazy), closure adalah
// fungsi anonim yang bisa menangkap variabel di sekitarnya.
// Kombinasi keduanya membuat operasi koleksi jadi ringkas tanpa loop manual.

// ============================================
// 1. CLOSURE DASAR
// ============================================
fn demo_closure() {
    println!("\n--- CLOSURE DASAR ---");

    // Closure: |parameter| ekspresi
    let tambah = |a: i32, b: i32| a + b;
    println!("  tambah(2, 3) = {}", tambah(2, 3));

    // Closure tanpa parameter
    let sapa = || "Halo dari closure";
    println!("  {}", sapa());

    // Closure dengan block dan tipe return eksplisit
    let pangkat = |x: i32, n: u32| -> i32 {
        let mut hasil = 1;
        for _ in 0..n {
            hasil *= x;
        }
        hasil
    };
    println!("  pangkat(2, 10) = {}", pangkat(2, 10));

    // Closure menangkap environment
    let batas = 5;
    let melebihi_batas = |n: i32| n > batas; // menangkap `batas` by reference
    println!("  7 > {}? {}", batas, melebihi_batas(7));

    // move: memindahkan ownership ke closure
    let nama = String::from("Hayyan");
    let tampilkan = move || format!("Nama: {}", nama);
    println!("  {}", tampilkan());
    // `nama` sudah dipindah ke closure, tidak bisa dipakai lagi di sini.

    // FnMut: closure yang mengubah state
    let mut hitungan = 0;
    let mut naikkan = || {
        hitungan += 1;
        hitungan
    };
    println!("  naikkan: {}, {}, {}", naikkan(), naikkan(), naikkan());

    // Closure sebagai argumen fungsi
    fn terapkan<F: Fn(i32) -> i32>(nilai: i32, f: F) -> i32 {
        f(nilai)
    }
    println!("  terapkan(5, |x| x * 3) = {}", terapkan(5, |x| x * 3));
}

// ============================================
// 2. ITERATOR DASAR
// ============================================
fn demo_iterator_dasar() {
    println!("\n--- ITERATOR DASAR ---");

    let angka = vec![10, 20, 30, 40, 50];

    // iter() -> &T, iter_mut() -> &mut T, into_iter() -> T (ownership pindah)
    let mut iter = angka.iter();
    println!("  next: {:?}", iter.next());
    println!("  next: {:?}", iter.next());
    println!("  sisa: {:?}", iter.collect::<Vec<_>>());

    // Iterator itu lazy: belum dieksekusi sebelum dikonsumsi
    let malas = angka.iter().map(|n| {
        println!("    [map dijalankan untuk {}]", n);
        n * 2
    });
    println!("  map dibuat, belum ada output di atas.");
    println!("  setelah collect: {:?}", malas.collect::<Vec<_>>());

    // for loop memakai IntoIterator secara otomatis
    let total = {
        let mut t = 0;
        for n in &angka {
            t += n;
        }
        t
    };
    println!("  total lewat for: {}", total);
}

// ============================================
// 3. ADAPTOR ITERATOR (map, filter, flat_map, ...)
// ============================================
fn demo_adaptor() {
    println!("\n--- ADAPTOR ITERATOR ---");

    let angka: Vec<i32> = (1..=10).collect();
    println!("  data: {:?}", angka);

    let kuadrat_genap: Vec<i32> = angka
        .iter()
        .filter(|&&n| n % 2 == 0)
        .map(|&n| n * n)
        .collect();
    println!("  kuadrat genap: {:?}", kuadrat_genap);

    // enumerate: index + nilai
    for (i, n) in ["apel", "jeruk", "mangga"].iter().enumerate() {
        println!("  {}: {}", i + 1, n);
    }

    // zip: gabungkan dua iterator (berhenti di yang terpendek)
    let nama = ["Hayyan", "Rina", "Budi"];
    let nilai = [90, 85, 88];
    let pasangan: Vec<(&str, i32)> = nama.iter().copied().zip(nilai).collect();
    println!("  zip: {:?}", pasangan);

    // chain: sambung dua iterator
    let gabung: Vec<i32> = (1..=3).chain(10..=12).collect();
    println!("  chain: {:?}", gabung);

    // flat_map: map lalu ratakan (flatten) satu level
    let kata = ["halo dunia", "belajar rust"];
    let semua_kata: Vec<&str> = kata.iter().flat_map(|s| s.split_whitespace()).collect();
    println!("  flat_map: {:?}", semua_kata);

    // filter_map: filter + map sekaligus (buang None)
    let teks = ["10", "abc", "20", "30"];
    let valid: Vec<i32> = teks.iter().filter_map(|s| s.parse::<i32>().ok()).collect();
    println!("  filter_map parse: {:?}", valid);

    // take, skip, take_while, skip_while
    println!("  take(3): {:?}", angka.iter().take(3).collect::<Vec<_>>());
    println!("  skip(7): {:?}", angka.iter().skip(7).collect::<Vec<_>>());
    println!(
        "  take_while(<5): {:?}",
        angka.iter().take_while(|&&n| n < 5).collect::<Vec<_>>()
    );
    println!(
        "  skip_while(<5): {:?}",
        angka.iter().skip_while(|&&n| n < 5).collect::<Vec<_>>()
    );

    // rev: membalik urutan
    println!("  rev: {:?}", angka.iter().rev().take(3).collect::<Vec<_>>());
}

// ============================================
// 4. KONSUMEN ITERATOR (collect, fold, any, ...)
// ============================================
fn demo_konsumen() {
    println!("\n--- KONSUMEN ITERATOR ---");

    let angka = vec![3, 7, 2, 9, 4, 8];

    println!("  sum: {}", angka.iter().sum::<i32>());
    println!("  product: {}", angka.iter().product::<i32>());
    println!("  count: {}", angka.iter().count());
    println!("  max: {:?}", angka.iter().max());
    println!("  min: {:?}", angka.iter().min());

    println!("  any(>8): {}", angka.iter().any(|&n| n > 8));
    println!("  all(>0): {}", angka.iter().all(|&n| n > 0));
    println!("  find(genap): {:?}", angka.iter().find(|&&n| n % 2 == 0));
    println!("  position(9): {:?}", angka.iter().position(|&n| n == 9));

    // fold: akumulasi dengan nilai awal
    let total = angka.iter().fold(0, |acc, &n| acc + n);
    println!("  fold total: {}", total);

    // reduce: seperti fold tapi tanpa nilai awal (return Option)
    let maks = angka.iter().copied().reduce(|a, b| a.max(b));
    println!("  reduce max: {:?}", maks);

    // max_by_key / min_by_key: pilih berdasarkan kriteria
    let kata = ["rust", "python", "c", "javascript"];
    println!(
        "  kata terpanjang: {:?}",
        kata.iter().max_by_key(|k| k.len())
    );

    // for_each: konsumsi dengan efek samping
    print!("  for_each: ");
    angka.iter().take(3).for_each(|n| print!("{} ", n));
    println!();

    // partition: pisahkan jadi dua Vec
    let (genap, ganjil): (Vec<i32>, Vec<i32>) = angka.iter().partition(|&&n| n % 2 == 0);
    println!("  partition genap: {:?}", genap);
    println!("  partition ganjil: {:?}", ganjil);
}

// ============================================
// 5. CUSTOM ITERATOR
// ============================================
struct Counter {
    batas: u32,
    saat_ini: u32,
}

impl Counter {
    fn new(batas: u32) -> Self {
        Counter { batas, saat_ini: 0 }
    }
}

impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
        if self.saat_ini < self.batas {
            self.saat_ini += 1;
            Some(self.saat_ini)
        } else {
            None
        }
    }
}

fn demo_custom_iterator() {
    println!("\n--- CUSTOM ITERATOR ---");

    let counter = Counter::new(5);
    let isi: Vec<u32> = counter.collect();
    println!("  Counter(5): {:?}", isi);

    // Semua method iterator otomatis tersedia untuk custom iterator
    let jumlah_kuadrat: u32 = Counter::new(5).map(|n| n * n).sum();
    println!("  jumlah kuadrat 1..=5: {}", jumlah_kuadrat);

    let genap: Vec<u32> = Counter::new(10).filter(|n| n % 2 == 0).collect();
    println!("  genap 1..=10: {:?}", genap);
}

// ============================================
// 6. STUDI KASUS: PIPELINE DATA
// ============================================
#[derive(Debug)]
struct Produk {
    nama: &'static str,
    harga: u32,
    stok: u32,
}

fn demo_pipeline() {
    println!("\n--- STUDI KASUS: PIPELINE DATA ---");

    let produk = vec![
        Produk { nama: "Keyboard", harga: 350_000, stok: 5 },
        Produk { nama: "Mouse", harga: 150_000, stok: 0 },
        Produk { nama: "Monitor", harga: 1_500_000, stok: 2 },
        Produk { nama: "Flashdisk", harga: 90_000, stok: 10 },
        Produk { nama: "Headset", harga: 450_000, stok: 3 },
    ];

    // 1. Produk tersedia, urut dari yang termurah
    let mut tersedia: Vec<&Produk> = produk.iter().filter(|p| p.stok > 0).collect();
    tersedia.sort_by_key(|p| p.harga);
    println!("  tersedia (termurah dulu):");
    for p in &tersedia {
        println!("    {:<10} Rp{:<9} stok {}", p.nama, p.harga, p.stok);
    }

    // 2. Total nilai inventaris
    let nilai_inventaris: u32 = produk.iter().map(|p| p.harga * p.stok).sum();
    println!("  total nilai inventaris: Rp{}", nilai_inventaris);

    // 3. Rata-rata harga produk yang ada stoknya
    let rata_rata = tersedia.iter().map(|p| p.harga).sum::<u32>() as f64 / tersedia.len() as f64;
    println!("  rata-rata harga (tersedia): Rp{:.0}", rata_rata);

    // 4. Nama produk yang harganya di atas 100 ribu, digabung jadi satu string
    let mahal: String = produk
        .iter()
        .filter(|p| p.harga > 100_000)
        .map(|p| p.nama)
        .collect::<Vec<_>>()
        .join(", ");
    println!("  harga > 100rb: {}", mahal);

    // 5. Cari produk pertama yang stoknya habis
    match produk.iter().find(|p| p.stok == 0) {
        Some(p) => println!("  stok habis: {}", p.nama),
        None => println!("  semua stok tersedia"),
    }
}

// ============================================
// LATIHAN
// ============================================
fn latihan() {
    println!("\n--- LATIHAN ---");

    // Latihan 1: jumlahkan angka ganjil 1..=20
    let total: i32 = (1..=20).filter(|n| n % 2 != 0).sum();
    println!("  1. total ganjil 1..=20: {}", total);

    // Latihan 2: ubah daftar kata menjadi huruf kapital
    let kata = vec!["rust", "python", "go"];
    let kapital: Vec<String> = kata.iter().map(|k| k.to_uppercase()).collect();
    println!("  2. kapital: {:?}", kapital);

    // Latihan 3: ambil 3 kata terpanjang
    let kalimat = "belajar rust dan python itu menyenangkan";
    let mut kata_unik: Vec<&str> = kalimat.split_whitespace().collect();
    kata_unik.sort_by_key(|k| std::cmp::Reverse(k.len()));
    kata_unik.dedup();
    println!("  3. 3 terpanjang: {:?}", &kata_unik[..3]);

    // Latihan 4: faktorial dengan fold
    let n = 6;
    let faktorial: u64 = (1..=n).fold(1, |acc, x| acc * x);
    println!("  4. {}! = {}", n, faktorial);

    // Latihan 5: rata-rata dengan closure dan iterator
    let nilai = vec![80, 90, 75, 85, 95];
    let rata = |data: &[i32]| -> f64 {
        data.iter().sum::<i32>() as f64 / data.len() as f64
    };
    println!("  5. rata-rata: {:.2}", rata(&nilai));
}

// ============================================
// MAIN DEMO
// ============================================
fn main() {
    println!("{}", "=".repeat(50));
    println!("DEMO ITERATOR & CLOSURE RUST");
    println!("{}", "=".repeat(50));

    demo_closure();
    demo_iterator_dasar();
    demo_adaptor();
    demo_konsumen();
    demo_custom_iterator();
    demo_pipeline();
    latihan();

    println!("\n=== SELESAI ===");
}
