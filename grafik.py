import inquirer
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from data import koleksi_dvd, data_transaksi
from tema import tema_admin
from utils import enter, total_harga

def grafik_pendapatan():
    baris = []
    for transaksi in data_transaksi.values():
        id_dvd = transaksi["id_dvd"]
        judul = koleksi_dvd.get(id_dvd, {}).get("judul", id_dvd)
        nilai = total_harga(transaksi["harga"], transaksi["jumlah"], transaksi["durasi"])
        baris.append({"DVD": judul, "Pendapatan": nilai})

    if len(baris) == 0:
        print("Belum ada transaksi, tidak dapat menampilkan grafik.")
        enter()
        return

    df = pd.DataFrame(baris)
    per_dvd = df.groupby("DVD")["Pendapatan"].sum().sort_values(ascending=False)

    warna = [plt.cm.tab20(i % 20) for i in range(len(per_dvd))]

    plt.figure(figsize=(10, 6))
    plt.bar(per_dvd.index, per_dvd.values, color=warna)

    plt.title("Total Pendapatan per DVD")
    plt.xlabel("Judul DVD")
    plt.ylabel("Pendapatan (Rp)")

    plt.gca().yaxis.set_major_formatter(
        FuncFormatter(lambda x, _: f"Rp{int(x):,}".replace(",", "."))
    )

    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()