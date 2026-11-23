"""
18_visualisasi.py - Visualisasi Data dengan Matplotlib dan Seaborn

Tahap 5: Spesialisasi - Visualisasi Data
Materi: matplotlib, seaborn, plot grafik, histogram, scatter, bar chart
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Set style seaborn
sns.set_style("whitegrid")


def demo_matplotlib():
    print("=== DEMO MATPLOTLIB ===")

    # Data contoh
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    categories = ['A', 'B', 'C', 'D']
    values = [23, 45, 56, 78]

    # Figure 1: Line plot
    plt.figure(figsize=(10, 6))
    plt.plot(x, y1, label='sin(x)', color='blue', linewidth=2)
    plt.plot(x, y2, label='cos(x)', color='red', linewidth=2, linestyle='--')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Grafik Sinus dan Cosinus')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('data_latihan/line_plot.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("Line plot disimpan ke data_latihan/line_plot.png")

    # Figure 2: Bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(categories, values, color=['skyblue', 'lightgreen', 'lightcoral', 'gold'])
    plt.xlabel('Kategori')
    plt.ylabel('Nilai')
    plt.title('Bar Chart Nilai per Kategori')
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('data_latihan/bar_chart.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("Bar chart disimpan ke data_latihan/bar_chart.png")

    # Figure 3: Scatter plot
    np.random.seed(42)
    x_scatter = np.random.randn(100)
    y_scatter = 2 * x_scatter + np.random.randn(100) * 0.5
    plt.figure(figsize=(8, 6))
    plt.scatter(x_scatter, y_scatter, alpha=0.6, c='purple', s=50)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Scatter Plot dengan Noise')
    plt.grid(True, alpha=0.3)
    plt.savefig('data_latihan/scatter_plot.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("Scatter plot disimpan ke data_latihan/scatter_plot.png")

    # Figure 4: Histogram
    data_hist = np.random.normal(0, 1, 1000)
    plt.figure(figsize=(8, 6))
    plt.hist(data_hist, bins=30, color='teal', alpha=0.7, edgecolor='black')
    plt.xlabel('Nilai')
    plt.ylabel('Frekuensi')
    plt.title('Histogram Distribusi Normal')
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('data_latihan/histogram.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("Histogram disimpan ke data_latihan/histogram.png")


def demo_seaborn():
    print("\n=== DEMO SEABORN ===")

    # Load dataset bawaan seaborn
    tips = sns.load_dataset('tips')
    print(f"Dataset tips (5 baris pertama):\n{tips.head()}")

    # Figure 5: Boxplot
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=tips, x='day', y='total_bill', palette='Set2')
    plt.title('Total Bill per Hari (Boxplot)')
    plt.savefig('data_latihan/seaborn_boxplot.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("Seaborn boxplot disimpan ke data_latihan/seaborn_boxplot.png")

    # Figure 6: Histogram dengan KDE (distplot replacement)
    plt.figure(figsize=(8, 6))
    sns.histplot(data=tips, x='total_bill', kde=True, color='green', alpha=0.6)
    plt.title('Distribusi Total Bill (Histogram + KDE)')
    plt.savefig('data_latihan/seaborn_histplot.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("Seaborn histplot disimpan ke data_latihan/seaborn_histplot.png")

    # Figure 7: Scatter plot dengan hue
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=tips, x='total_bill', y='tip', hue='sex', style='time', s=80)
    plt.title('Total Bill vs Tip (berdasarkan Sex dan Time)')
    plt.savefig('data_latihan/seaborn_scatter.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("Seaborn scatter disimpan ke data_latihan/seaborn_scatter.png")

    # Figure 8: Heatmap korelasi
    plt.figure(figsize=(8, 6))
    corr = tips[['total_bill', 'tip', 'size']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, fmt='.2f')
    plt.title('Heatmap Korelasi Dataset Tips')
    plt.savefig('data_latihan/seaborn_heatmap.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("Seaborn heatmap disimpan ke data_latihan/seaborn_heatmap.png")


def latihan_matplotlib():
    print("\n=== LATIHAN MATPLOTLIB ===")
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    plt.figure(figsize=(6, 4))
    plt.plot(x, y, marker='o', color='green')
    plt.title('Latihan: Grafik Garis Sederhana')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.savefig('data_latihan/latihan_line.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("Latihan line plot disimpan ke data_latihan/latihan_line.png")


def latihan_seaborn():
    print("\n=== LATIHAN SEABORN ===")
    iris = sns.load_dataset('iris')
    plt.figure(figsize=(8, 6))
    sns.pairplot(iris, hue='species', diag_kind='kde', plot_kws={'alpha': 0.6})
    plt.savefig('data_latihan/seaborn_pairplot.png', dpi=100, bbox_inches='tight')
    plt.close()
    print("Seaborn pairplot disimpan ke data_latihan/seaborn_pairplot.png")


if __name__ == '__main__':
    import os
    os.makedirs('data_latihan', exist_ok=True)

    demo_matplotlib()
    demo_seaborn()
    latihan_matplotlib()
    latihan_seaborn()
    print("\nSemua plot disimpan di folder data_latihan/")
