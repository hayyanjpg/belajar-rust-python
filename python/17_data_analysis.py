"""
17_data_analysis.py - Data Analysis dengan NumPy dan Pandas

Tahap 5: Spesialisasi - Data Analysis
Materi: numpy, pandas, data manipulation, exploratory data analysis
"""

import numpy as np
import pandas as pd

# ============================================================================
# 1. NUMPY - Array numerik
# ============================================================================

def demo_numpy():
    print("=== DEMO NUMPY ===")

    # Membuat array
    arr1d = np.array([1, 2, 3, 4, 5])
    arr2d = np.array([[1, 2, 3], [4, 5, 6]])
    arr_zeros = np.zeros((3, 3))
    arr_ones = np.ones((2, 4))
    arr_range = np.arange(0, 10, 2)
    arr_linspace = np.linspace(0, 1, 5)

    print(f"1D array: {arr1d}")
    print(f"2D array:\n{arr2d}")
    print(f"Zeros 3x3:\n{arr_zeros}")
    print(f"Ones 2x4:\n{arr_ones}")
    print(f"Range 0-10 step 2: {arr_range}")
    print(f"Linspace 0-1 (5 titik): {arr_linspace}")

    # Operasi array (vektorisasi)
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    print(f"\na + b = {a + b}")
    print(f"a * b = {a * b}")
    print(f"a ** 2 = {a ** 2}")
    print(f"sin(a) = {np.sin(a)}")

    # Statistik
    data = np.array([10, 20, 30, 40, 50])
    print(f"\nMean: {np.mean(data)}")
    print(f"Median: {np.median(data)}")
    print(f"Std: {np.std(data)}")
    print(f"Min: {np.min(data)}, Max: {np.max(data)}")
    print(f"Sum: {np.sum(data)}")

    # Indexing dan slicing
    matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(f"\nMatrix:\n{matrix}")
    print(f"Baris 0: {matrix[0]}")
    print(f"Kolom 1: {matrix[:, 1]}")
    print(f"Elemen [1,2]: {matrix[1, 2]}")
    print(f"Slice [0:2, 0:2]:\n{matrix[0:2, 0:2]}")

    # Boolean indexing
    filter_data = data > 25
    print(f"\nData > 25: {data[filter_data]}")


# ============================================================================
# 2. PANDAS - Data manipulation
# ============================================================================

def demo_pandas():
    print("\n=== DEMO PANDAS ===")

    # Membuat Series dan DataFrame
    series = pd.Series([10, 20, 30, 40, 50], index=['a', 'b', 'c', 'd', 'e'])
    print(f"Series:\n{series}")

    data_dict = {
        'nama': ['Budi', 'Siti', 'Joko', 'Ani'],
        'umur': [25, 30, 35, 28],
        'kota': ['Jakarta', 'Bandung', 'Surabaya', 'Yogyakarta'],
        'gaji': [7000000, 9000000, 12000000, 8000000]
    }
    df = pd.DataFrame(data_dict)
    print(f"\nDataFrame:\n{df}")

    # Inspeksi DataFrame
    print(f"\nShape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nInfo:\n{df.info()}")
    print(f"\nDescribe:\n{df.describe()}")

    # Selection
    print(f"\nKolom 'nama':\n{df['nama']}")
    print(f"\nBaris 0-1:\n{df.iloc[0:2]}")
    print(f"\nFilter umur > 30:\n{df[df['umur'] > 30]}")
    print(f"\nFilter kota Jakarta:\n{df[df['kota'] == 'Jakarta']}")

    # Manipulasi data
    df['tahun_lahir'] = 2026 - df['umur']
    print(f"\nSetelah menambah kolom tahun_lahir:\n{df}")

    df['gaji_juta'] = df['gaji'] / 1000000
    print(f"\nSetelah menambah kolom gaji_juta:\n{df}")

    # GroupBy
    print(f"\nRata-rata gaji per kota:\n{df.groupby('kota')['gaji'].mean()}")

    # Sorting
    print(f"\nUrutkan berdasarkan gaji (desc):\n{df.sort_values('gaji', ascending=False)}")

    # Missing data
    df_with_nan = df.copy()
    df_with_nan.loc[1, 'gaji'] = np.nan
    print(f"\nData dengan NaN:\n{df_with_nan}")
    print(f"\nDrop NaN:\n{df_with_nan.dropna()}")
    print(f"\nFill NaN dengan mean:\n{df_with_nan.fillna(df_with_nan['gaji'].mean())}")

    # Export/Import CSV
    df.to_csv('data_latihan/pegawai.csv', index=False)
    print("\nData diekspor ke data_latihan/pegawai.csv")

    df_imported = pd.read_csv('data_latihan/pegawai.csv')
    print(f"Data diimpor:\n{df_imported}")


def latihan_numpy():
    print("\n=== LATIHAN NUMPY ===")
    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(f"Array: {arr}")
    print(f"Array dikalikan 2: {arr * 2}")
    print(f"Array yang genap: {arr[arr % 2 == 0]}")
    print(f"Array lebih dari 5: {arr[arr > 5]}")
    print(f"Jumlah semua elemen: {np.sum(arr)}")


def latihan_pandas():
    print("\n=== LATIHAN PANDAS ===")
    data = pd.DataFrame({
        'produk': ['Laptop', 'Mouse', 'Keyboard', 'Monitor'],
        'harga': [10000000, 200000, 500000, 3000000],
        'stok': [10, 50, 30, 15]
    })
    print(f"DataFrame produk:\n{data}")
    data['total_nilai'] = data['harga'] * data['stok']
    print(f"\nSetelah kolom total_nilai:\n{data}")
    print(f"\nProduk dengan stok < 20:\n{data[data['stok'] < 20]}")


if __name__ == '__main__':
    import os
    os.makedirs('data_latihan', exist_ok=True)

    demo_numpy()
    demo_pandas()
    latihan_numpy()
    latihan_pandas()
