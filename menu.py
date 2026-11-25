import inquirer

from tema import tema_admin, tema_user
from utils import clear_terminal, enter
from dvd import menu_dvd, tampilkan_koleksi, cari_dvd
from penyewa import menu_data_penyewa
from transaksi import menu_transaksi, pengembalian_dvd, tampilkan_transaksi, sewa_dvd, lihat_total_pendapatan

def menu_admin():
    clear_terminal()
    print("Anda login sebagai admin!")
    enter("Tekan Enter untuk melanjutkan ke menu admin...")

    while True:
        clear_terminal()
        print("=====================================")
        print("              MENU ADMIN")
        print("=====================================")
        pertanyaan = [inquirer.List("pilihan", 
                                    message="Pilih menu", 
                                    choices=[" DVD", " Data penyewa", " Transaksi", " Total pendapatan", " Logout"])
                     ]

        jawaban = inquirer.prompt(pertanyaan, theme=tema_admin())

        if jawaban["pilihan"] == " DVD":
            menu_dvd()
            
        elif jawaban["pilihan"] == " Data penyewa":
            menu_data_penyewa()

            
        elif jawaban["pilihan"] == " Transaksi":
            menu_transaksi()

        elif jawaban["pilihan"] == " Total pendapatan":
            lihat_total_pendapatan()

        elif jawaban["pilihan"] == " Logout":
            clear_terminal()
            print("Logout berhasil.")
            enter("Tekan Enter untuk melanjutkan...")
            break

def menu_pengguna(username):
    while True:
        clear_terminal()
        print("=============================")
        print("        MENU PENGGUNA")
        print("=============================")
        pertanyaan = [inquirer.List("pilihan", 
                                    message="Pilih menu", 
                                    choices=[" Lihat koleksi DVD", " Cari DVD", " Sewa DVD", " Lihat transaksi saya", " Kembalikan DVD", " Logout"])
                    ]

        jawaban = inquirer.prompt(pertanyaan, theme=tema_user())

        if jawaban["pilihan"] == " Lihat koleksi DVD":
            clear_terminal()
            print("KOLEKSI DVD 💿")
            tampilkan_koleksi()
            enter()

        elif jawaban["pilihan"] == " Cari DVD":
            cari_dvd()

        elif jawaban["pilihan"] == " Sewa DVD":
            sewa_dvd(username)

        elif jawaban["pilihan"] == " Lihat transaksi saya":
            clear_terminal()
            print("TRANSAKSI SAYA 👤")
            tampilkan_transaksi(username)
            enter()

        elif jawaban["pilihan"] == " Kembalikan DVD":
            pengembalian_dvd(username)

        elif jawaban["pilihan"] == " Logout":
            clear_terminal()
            print("Logout berhasil.")
            enter("Tekan Enter untuk melanjutkan...")
            break

        else:
            print("\nOpsi tidak valid! Masukkan pilihan 1 sampai 6.")
            enter("Tekan Enter untuk mencoba lagi...")