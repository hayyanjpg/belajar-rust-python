// Materi 04: Fungsi dan Nilai Balik

fn sapa(nama: &str) {
    println!("Halo, {}!", nama);
}

fn tambah(a: i32, b: i32) -> i32 {
    a + b
}

fn bagi(a: f64, b: f64) -> f64 {
    a / b
}

fn faktorial(n: u64) -> u64 {
    if n <= 1 {
        1
    } else {
        n * faktorial(n - 1)
    }
}

fn fibonacci(n: u32) -> u64 {
    if n == 0 {
        0
    } else if n == 1 {
        1
    } else {
        fibonacci(n - 1) + fibonacci(n - 2)
    }
}

fn max_dari(a: i32, b: i32) -> i32 {
    if a > b {
        a
    } else {
        b
    }
}

fn minmax(angka: &[i32]) -> (i32, i32) {
    let mut min = angka[0];
    let mut max = angka[0];
    for &n in angka {
        if n < min {
            min = n;
        }
        if n > max {
            max = n;
        }
    }
    (min, max)
}

fn jumlahkan(s: &str) -> usize {
    s.len()
}

fn main() {
    sapa("Hayyan");
    sapa("Rust");

    println!("tambah(10, 5)     = {}", tambah(10, 5));
    println!("bagi(10.0, 4.0)   = {:.2}", bagi(10.0, 4.0));
    println!("faktorial(5)      = {}", faktorial(5));
    println!("fibonacci(10)     = {}", fibonacci(10));
    println!("max_dari(7, 12)   = {}", max_dari(7, 12));

    let (min, max) = minmax(&[4, 8, 15, 16, 23, 42]);
    println!("minmax            = min {}, max {}", min, max);

    let panjang = jumlahkan("Hello Rust");
    println!("jumlahkan()       = {}", panjang);

    let hasil = tambah(tambah(1, 2), tambah(3, 4));
    println!("Nested call       = {}", hasil);

    let tanpa_return = {
        let x = 10;
        x * 2
    };
    println!("Blok ekspresi     = {}", tanpa_return);

    for i in 0..5 {
        println!("fib({}) = {}", i, fibonacci(i));
    }
}