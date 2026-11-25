from prettytable import PrettyTable
import re
import inquirer

from tema import tema_admin
from data import data_penyewa, data_transaksi, counter
from utils import clear_terminal, enter, input_teks, konfirmasi
from storage import simpan_data
        
def menu_data_penyewa():
    clear_terminal()
    while True:
        clear_terminal()
        print("=====================================")
        print("           MENU DATA PENYEWA         ")
        print("=====================================")
        pertanyaan = [inquirer.List("pilihan", 
                                    message="Pilih menu", 
                                    choices=[" Lihat data penyewa", " Manage data penyewa", " Kembali"])
                     ]

        jawaban = inquirer.prompt(pertanyaan, theme=tema_admin())

        if jawaban["pilihan"] == " Lihat data penyewa":
            clear_terminal()
            print("DATA PENYEWA 📄")
            tampilkan_penyewa()
            enter("Tekan Enter untuk kembali ke menu data penyewa...")

        elif jawaban["pilihan"] == " Manage data penyewa":
            manage_penyewa()

        elif jawaban["pilihan"] == " Kembali":
            break
        
def tampilkan_penyewa():
    if len(data_penyewa) == 0:
        print("Belum ada penyewa.")
        return
    
    tabel = PrettyTable()
    tabel.field_names = ["ID", "Nama", "Telepon", "Alamat"]

    for id_penyewa, penyewa in data_penyewa.items():
        tabel.add_row([
            id_penyewa,
            penyewa["nama"],
            penyewa["telepon"],
            penyewa["alamat"]
        ])

    print(tabel)

def manage_penyewa():
    clear_terminal()

    if len(data_penyewa) == 0:
        print("DATA PENYEWA 📄")
        print("Belum ada penyewa.")
        enter("Tekan Enter untuk kembali ke menu data penyewa...")
        return
    
    while True:
        print("\n==============================")
        print("      MANAGE DATA PENYEWA     ")
        print("==============================")
        print("DATA PENYEWA 📄")
        tampilkan_penyewa()
        
        pertanyaan = [
            inquirer.List("pilihan", 
            message="Pilih menu", 
            choices=[" Ubah data penyewa", " Hapus data penyewa", " Kembali"]
            )
        ]
        
        jawaban = inquirer.prompt(pertanyaan, theme=tema_admin())
        
        
        if jawaban["pilihan"]  == " Ubah data penyewa":
            ubah_penyewa()
            clear_terminal()
        
        elif jawaban["pilihan"] == " Hapus data penyewa":
            hapus_penyewa()
            clear_terminal()
            
        elif jawaban["pilihan"] == " Kembali":
            break

def ubah_penyewa():
    clear_terminal()
    print("UBAH DATA PENYEWA ♻️")
    tampilkan_penyewa()

    if len(data_penyewa) == 0:
        enter("Tekan Enter untuk kembali ke menu admin...")
        return
    
    try:
        id_penyewa = input_teks("ID penyewa yang ingin diubah: ").upper()
        penyewa = data_penyewa[id_penyewa]
        nama_baru = input("\nNama baru (Enter jika tidak ingin diubah): ").strip()
        telepon_baru = input("Nomor telepon baru (Enter jika tidak ingin diubah): ").strip()
        telepon_baru = re.sub(r"[\s-]", "", telepon_baru)
        if telepon_baru != "" and  not re.fullmatch(r"(08[1-9][0-9]{8,10})", telepon_baru):
            raise ValueError("Nomor telepon tidak valid! Contoh: 081234567890")
        alamat_baru = input("Alamat baru (Enter jika tidak ingin diubah): ").strip()

    except KeyError:
        print("\nData penyewa tidak ditemukan!")

    except ValueError as e:
        print(f"\n{e}")

    else:
        if nama_baru != "":
            penyewa["nama"] = nama_baru

        if telepon_baru != "":
            penyewa["telepon"] = telepon_baru

        if alamat_baru != "":
            penyewa["alamat"] = alamat_baru

        simpan_data()
        print("\nData penyewa berhasil diperbarui!")

    finally:
        enter("Tekan Enter untuk kembali ke menu...")

def hapus_penyewa():
    clear_terminal()
    print("HAPUS DATA PENYEWA 🗑️")
    tampilkan_penyewa()

    if len(data_penyewa) == 0:
        enter("Tekan Enter untuk kembali ke menu admin...")
        return
    
    try:
        id_penyewa = input_teks("ID penyewa yang ingin dihapus: ").upper()
        if id_penyewa not in data_penyewa:
            raise KeyError(id_penyewa)
        for t in data_transaksi.values():
            if t["id_penyewa"] == id_penyewa and t["status"] == "Dipinjam":
                raise ValueError("Penyewa masih memiliki transaksi aktif dan tidak bisa dihapus!")
            
    except KeyError:
        print("Data penyewa tidak ditemukan!")

    except ValueError as e:
        print(f"{e}")

    else:
        if konfirmasi("Yakin hapus data penyewa?"):
            del data_penyewa[id_penyewa]
            simpan_data()
            print("Data penyewa berhasil dihapus!")

        else:
            print("Penghapusan dibatalkan.")

    finally:
        enter("Tekan Enter untuk kembali ke menu...")
    
def buat_id_penyewa():
    nomor = counter["penyewa"]
    id_baru = "Z" + str(nomor)

    if nomor < 10:
        id_baru = "Z00" + str(nomor)

    elif nomor < 100:
        id_baru = "Z0" + str(nomor)

    counter["penyewa"] += 1
    return id_baru