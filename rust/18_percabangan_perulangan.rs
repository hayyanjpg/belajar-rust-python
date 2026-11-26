// Materi 18: Percabangan dan Perulangan
// Penjelasan: Rust tidak punya `switch`; ada `if`/`else if`/`else` dan `match`.
// Empat bentuk perulangan: loop, while, while let, dan for.
//
// Kompilasi: rustc --edition 2021 18_percabangan_perulangan.rs -o percabangan
// Jalankan tes: rustc --edition 2021 --test 18_percabangan_perulangan.rs -o tes && ./tes

fn demo_if() {
    println!("\n--- IF / ELSE IF / ELSE ---");

    let nilai = 82;
    if nilai >= 90 {
        println!("  nilai {nilai}: A");
    } else if nilai >= 75 {
        println!("  nilai {nilai}: B");
    } else if nilai >= 60 {
        println!("  nilai {nilai}: C");
    } else {
        println!("  nilai {nilai}: D");
    }

    // if adalah expression: tiap cabang harus menghasilkan tipe yang sama.
    let status = if nilai >= 75 { "LULUS" } else { "GAGAL" };
    println!("  status: {status}");

    // Kondisi harus benar-benar bool (tidak seperti di Python/C).
    let aktif = true;
    if aktif && nilai > 50 {
        println!("  aktif dan nilai > 50");
    }

    // `let else` (Rust 1.65+) untuk early return saat pola tidak cocok.
    let teks: Option<&str> = Some("123");
    let Some(angka) = teks else {
        println!("  teks bukan Some, berhenti di sini");
        return;
    };
    println!("  let else -> {angka}");
}

fn demo_loop() {
    println!("\n--- LOOP ---");

    // `loop` berjalan sampai `break`; break bisa mengembalikan nilai.
    let mut hitung = 0;
    let hasil = loop {
        hitung += 1;
        if hitung == 4 {
            break hitung * 10;
        }
    };
    println!("  break dengan nilai: {hasil} (setelah {hitung} putaran)");

    // Label berguna untuk menghentikan perulangan luar dari dalam.
    'luar: for i in 1..=3 {
        for j in 1..=3 {
            if i * j > 4 {
                println!("  break 'luar pada i={i}, j={j}");
                break 'luar;
            }
        }
    }

    // continue melompat ke putaran berikutnya.
    let mut genap = Vec::new();
    for n in 1..=8 {
        if n % 2 != 0 {
            continue;
        }
        genap.push(n);
    }
    println!("  genap: {genap:?}");
}

fn demo_while() {
    println!("\n--- WHILE / WHILE LET ---");

    let mut sisa = 3;
    while sisa > 0 {
        println!("  mundur: {sisa}");
        sisa -= 1;
    }

    let mut iterator = ["a", "b", "c"].iter();
    while let Some(huruf) = iterator.next() {
        println!("  while let -> {huruf}");
    }
}

fn demo_for() {
    println!("\n--- FOR ---");

    print!("  rentang 1..=5: ");
    for i in 1..=5 {
        print!("{i} ");
    }
    println!();

    let buah = ["apel", "mangga", "pisang"];
    for (index, nama) in buah.iter().enumerate() {
        println!("  buah[{index}] = {nama}");
    }

    print!("  step_by(2): ");
    for i in (0..10).step_by(2) {
        print!("{i} ");
    }
    println!();

    print!("  rev(): ");
    for i in (1..4).rev() {
        print!("{i} ");
    }
    println!();

    // for pada &str memecah per karakter (char), byte-nya bukan ASCII semua.
    for (pos, ch) in "Rust🦀".char_indices() {
        println!("  char pada byte {pos}: {ch}");
    }
}

fn fizzbuzz(n: u32) -> String {
    match (n % 3, n % 5) {
        (0, 0) => "FizzBuzz".to_string(),
        (0, _) => "Fizz".to_string(),
        (_, 0) => "Buzz".to_string(),
        _ => n.to_string(),
    }
}

fn jumlah_genap(data: &[i32]) -> i32 {
    data.iter().filter(|n| **n % 2 == 0).sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn fizzbuzz_benar() {
        assert_eq!(fizzbuzz(3), "Fizz");
        assert_eq!(fizzbuzz(5), "Buzz");
        assert_eq!(fizzbuzz(15), "FizzBuzz");
        assert_eq!(fizzbuzz(7), "7");
    }

    #[test]
    fn jumlah_genap_benar() {
        assert_eq!(jumlah_genap(&[1, 2, 3, 4, 5]), 6);
        assert_eq!(jumlah_genap(&[]), 0);
    }
}

fn main() {
    println!("{}", "=".repeat(50));
    println!("DEMO PERCABANGAN & PERULANGAN");
    println!("{}", "=".repeat(50));

    demo_if();
    demo_loop();
    demo_while();
    demo_for();

    println!("\n--- LATIHAN: FIZZBUZZ 1..=15 ---");
    for n in 1..=15 {
        print!("{} ", fizzbuzz(n));
    }
    println!("\nJumlah genap 1..=10: {}", jumlah_genap(&(1..=10).collect::<Vec<_>>()));

    println!("\n=== SELESAI ===");
}
