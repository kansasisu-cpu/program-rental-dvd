from prettytable import PrettyTable
import inquirer

from tema import tema_admin
from data import koleksi_dvd, data_transaksi
from utils import clear_terminal, enter, input_teks, input_angka, konfirmasi
from storage import simpan_data

def menu_dvd():
    clear_terminal()
    while True:
        clear_terminal()
        print("=====================================")
        print("              MENU DVD")
        print("=====================================")
        pertanyaan = [inquirer.List("pilihan", 
                                    message="Pilih menu", 
                                    choices=[" Lihat koleksi DVD", " Cari DVD", " Manage DVD", " Kembali"])
                     ]

        jawaban = inquirer.prompt(pertanyaan, theme=tema_admin())

        if jawaban["pilihan"] == " Lihat koleksi DVD":
            clear_terminal()
            print("KOLEKSI DVD 💿")
            tampilkan_koleksi()
            print()
            enter("Tekan Enter untuk kembali ke menu DVD...")

        elif jawaban["pilihan"] == " Cari DVD":
            cari_dvd()

        elif jawaban["pilihan"] == " Manage DVD":
            manage_dvd()
        
        elif jawaban["pilihan"] == " Kembali":
            break
            
def tampilkan_koleksi():
    if len(koleksi_dvd) == 0:
        print("Belum ada koleksi DVD.")
        return

    tabel = PrettyTable()
    tabel.field_names = ["ID", "Judul", "Genre", "Tahun", "Harga Sewa", "Stok"]

    for id_dvd, dvd in koleksi_dvd.items():
        tabel.add_row([
            id_dvd,
            dvd["judul"],
            dvd["genre"],
            dvd["tahun"],
            f"Rp{dvd['harga']}",
            dvd["stok"],
        ])

    tabel.align["Judul"] = "l"
    tabel.align["Genre"] = "l"
    tabel.align["Tahun"] = "l"

    print(tabel)

def cari_dvd():
    while True:
        clear_terminal()
        print("==============================")
        print("           CARI DVD  🔎      ")
        print("==============================")
        
        pertanyaan = [
            inquirer.List(
                "pilihan",
                message="Pilih kategori pencarian",
                choices=[" Cari berdasarkan ID", " Cari berdasarkan Judul", " Cari berdasarkan Genre", " Kembali"]
            )
        ]
        
        jawaban = inquirer.prompt(pertanyaan, theme=tema_admin())
        
        if jawaban["pilihan"] == " Cari berdasarkan ID":
            cari_id()
            clear_terminal()
            
        elif jawaban["pilihan"] == " Cari berdasarkan Judul":
            cari_judul()
            clear_terminal()
            
        elif jawaban["pilihan"] == " Cari berdasarkan Genre":
            cari_genre()
            clear_terminal()

        elif jawaban["pilihan"] == " Kembali":
            break
        
def cari_id():
    clear_terminal()
    print("CARI DVD BERDASARKAN ID 🔎")
    try:
        id_cari = input_teks("Masukkan ID DVD yang dicari: ").upper()
        
        if id_cari not in koleksi_dvd:
            raise KeyError(id_cari)
            
    except ValueError as e:
        print(f"\nGagal mencari DVD, {e}")
    except KeyError:
        print("\nDVD dengan ID tersebut tidak ditemukan!")
    else:
        print()
        tampilkan_tabel_hasil({id_cari: koleksi_dvd[id_cari]})
    finally:
        enter("Tekan Enter untuk kembali ke menu...")

def cari_judul():
    clear_terminal()
    print("CARI DVD BERDASARKAN JUDUL 🔎")
    try:
        mencari = input_teks("Masukkan judul film yang dicari: ").lower()
        
        dvd_cocok = {a: b for a, b in koleksi_dvd.items() if mencari in b["judul"].lower()}

        if len(dvd_cocok) == 0:
            raise KeyError(mencari)
            
    except ValueError as e:
        print(f"\nGagal mencari DVD, {e}")
    except KeyError:
        print("\nDVD dengan judul tersebut tidak ditemukan!")
    else:
        print()
        tampilkan_tabel_hasil(dvd_cocok)
    finally:
        enter("Tekan Enter untuk kembali ke menu...")

def cari_genre():
    clear_terminal()
    print("CARI DVD BERDASARKAN GENRE 🔎")
    try:
        mencari = input_teks("Masukkan genre DVD yang dicari: ").lower()
        
        dvd_cocok = {a: b for a, b in koleksi_dvd.items() if mencari in b["genre"].lower()}

        if len(dvd_cocok) == 0:
            raise KeyError(mencari)
            
    except ValueError as e:
        print(f"\nGagal mencari DVD, {e}")
    except KeyError:
        print("\nDVD dengan genre tersebut tidak ditemukan!")
    else:
        print()
        tampilkan_tabel_hasil(dvd_cocok)
    finally:
        enter("Tekan Enter untuk kembali ke menu...")
        
def tampilkan_tabel_hasil(data_dvd):
    tabel = PrettyTable()
    tabel.field_names = ["ID", "Judul", "Genre", "Tahun", "Harga Sewa", "Stok"]

    for id_dvd, dvd in data_dvd.items():
        tabel.add_row([
            id_dvd,
            dvd["judul"],
            dvd["genre"],
            dvd["tahun"],
            f"Rp{dvd['harga']}",
            dvd["stok"],
        ])

    tabel.align["Judul"] = "l"
    tabel.align["Genre"] = "l"
    tabel.align["Tahun"] = "l"

    print(tabel)

def manage_dvd():
    clear_terminal()  
    while True:
        print("\n==============================")
        print("           MANAGE DVD         ")
        print("==============================")
        pertanyaan = [
            inquirer.List("pilihan", 
            message="Pilih menu", 
            choices=[" Tambah DVD", " Ubah data DVD", " Hapus DVD", " Kembali"]
            )
        ]
        
        jawaban = inquirer.prompt(pertanyaan, theme=tema_admin())
        
        
        if jawaban["pilihan"]  == " Tambah DVD":
            tambah_dvd()
            clear_terminal()
            
        elif jawaban["pilihan"] == " Ubah data DVD":
            ubah_dvd()
            clear_terminal()
        
        elif jawaban["pilihan"] == " Hapus DVD":
            hapus_dvd()
            clear_terminal()
        
        elif jawaban["pilihan"] == " Kembali":
            break
                    
def tambah_dvd():
    clear_terminal()
    print("==========================================")
    print("                TAMBAH DVD                ")
    print("==========================================")

    try:
        id_dvd = input_teks("ID DVD: ").upper()

        if id_dvd in koleksi_dvd:
            raise ValueError("ID DVD sudah digunakan!")
        
        judul = input_teks("Judul film: ")
        genre = input_teks("Genre: ")
        tahun = input_angka("Tahun rilis: ", 1888)
        harga = input_angka("Harga sewa (angka): Rp", 0)
        stok = input_angka("Stok (angka): ", 0)

    except ValueError as e:
        print(f"\nGagal menambah DVD, {e}")

    else:
        koleksi_dvd[id_dvd] = {"judul": judul, "genre": genre, "tahun": tahun, "harga": harga, "stok": stok}
        simpan_data()
        print("\nDVD berhasil ditambahkan!")

    finally:
        enter("Tekan Enter untuk kembali ke menu...")
    

def ubah_dvd():
    clear_terminal()
    print("UBAH DATA DVD ♻️")
    tampilkan_koleksi()
    
    if len(koleksi_dvd) == 0:
        enter("Tekan Enter untuk kembali ke menu...")
        return

    try:
        id_dvd = input_teks("Masukkan ID DVD yang ingin diubah: ").upper()
        dvd = koleksi_dvd[id_dvd]
        
        print(f"\nJudul: {dvd['judul']} | Harga saat ini: Rp {dvd['harga']} | Stok saat ini: {dvd['stok']}")

        harga_baru = input_angka("\nHarga baru (Enter jika tidak ingin diubah): ", 0, True)
        stok_baru = input_angka("Stok baru (Enter jika tidak ingin diubah): ", 0, True)

    except KeyError:
        print("\nDVD tidak ditemukan!")

    except ValueError as e:
        print(f"\nGagal mengubah DVD, {e}")

    else:
        if harga_baru is not None:
            dvd["harga"] = harga_baru
        if stok_baru is not None:
            dvd["stok"] = stok_baru
        simpan_data()
        print("\nData DVD berhasil diperbarui!")

    finally:
        enter("Tekan Enter untuk kembali ke menu...")

def hapus_dvd():
    clear_terminal()

    print("HAPUS DVD 🗑️")
    tampilkan_koleksi()

    if len(koleksi_dvd) == 0:
        enter("Tekan Enter untuk kembali ke menu...")
        return

    try:
        id_dvd = input_teks("ID DVD yang ingin dihapus: ").upper()

        if id_dvd not in koleksi_dvd:
            raise KeyError(id_dvd)
        
        for t in data_transaksi.values():
            if t["id_dvd"] == id_dvd and t["status"] == "Dipinjam":
                raise ValueError("DVD tidak bisa dihapus karena masih dipinjam!")
            
    except KeyError:
        print("DVD tidak ditemukan!")

    except ValueError as e:
        print(f"{e}")

    else:
        if konfirmasi("Yakin hapus DVD ini?"):
            del koleksi_dvd[id_dvd]
            simpan_data()
            print("DVD berhasil dihapus!")

        else:
            print("Penghapusan dibatalkan.")

    finally:
        enter("Tekan Enter untuk kembali ke menu...")