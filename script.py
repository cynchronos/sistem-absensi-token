import os
import sys
import time
from prettytable import PrettyTable
import string    
import random

import prettytable

import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    database="UTY"
)

cur = conn.cursor()

def main():
    def clrscr():
        if sys.platform == "windows":
            os.system('cls')
        elif sys.platform == "linux":
            os.system('clear')
        elif sys.platform == "darwin":
            os.system('clear')
        else:
            print("Cannot Clear Screen, Unsupport Platform")
            
    def auth(username,password):
        quser = "SELECT username,password,nama,jabatan from users WHERE username = '%s'" % (username)
        cur.execute(quser)
        userauth = cur.fetchone()
        
        if  userauth :
            if password == userauth[1]:
                pass
            else:
                print('Username/Password Salah')
                main()
        else:
            print('Username/Password Salah')
            main()
        
        if userauth[3] == 'dosen':
            lecmenu()
        else:
            mhsmenu(username)
            
    def lecmenu():
        print('========================')
        print('Selamat Datang Dosen')
        print('========================')
        
        menus = ['Buat Presensi', 'Cari Mahasiswa', 'Keluar']
        
        for i,listmenu in enumerate(menus):
            print(1+i,".",listmenu)
            
        inpmenu = input("Pilih Menu: ")
        
        if inpmenu == '1':
            buatAbsen()
        elif inpmenu == '2':
            cariMhs()
        elif inpmenu == '3':
            print("Terima Kasih")
            exit()
        else:
            print("Salah Input")
            lecmenu()
    def buatAbsen():
        matkul = input("Pilih Mata Kuliah:\n1. Algoritma Pemrograman\n2. Pemrograman Basis Objek\nInput: ")
        if matkul == '1':
            matkul = 'Algoritma Pemrograman'
        elif matkul == '2':
            pass
        else:
            print("Input Salah")
            buatAbsen()
            
        pertemuan = input("Pilih Pertemuan: ")
        
        if pertemuan.isdigit():
            pertemuan = int(pertemuan)
            if pertemuan > 4:
                print("Pertemuan Tidak Ditemukan")
                buatAbsen()
            else: pass
        else:
            print("Salah Input")
            buatAbsen()
            
        S = 10    
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
        qupdate  = "UPDATE matkultoken SET token = '%s' WHERE matkul = '%s' AND pertemuan = %s" %(token,matkul,pertemuan)
        cur.execute(qupdate)
        conn.commit()
        
       
        if cur.rowcount > 0:
            print("Token Presensi: ", token)
            input("Tekan Enter Untuk Kembali Ke Menu")
            clrscr()
            lecmenu() 
        else:
            print("Token Gagal")
            buatAbsen()
       
    def cariMhs():
        choices = input('Cari Berdasarkan:\n1. NPM\n2. Nama Mahasiswa\nPilihan:  ')
        
        while choices != '1' and choices != '2':
            print("Input Salah")
            choices = input('Pilihan:  ')
        
        if choices == '1':
            search = input("Masukkan NPM Mahasiswa: ")
                
            qsearchitem = "SELECT nama,nomorpokok FROM users WHERE nomorpokok = '%s'" %(search)
            cur.execute(qsearchitem)
            result = cur.fetchall()
            
        else:
            
            search = input("Masukkan Nama Mahasiswa: ")
                       
            qsearchitem = "SELECT nama,nomorpokok FROM users WHERE nama LIKE '%" + search + "%'"
    
            cur.execute(qsearchitem)
            result = cur.fetchall()
            
        columns = ['Nama','NPM']
        tbl = PrettyTable()
        tbl.field_names = columns
        
        for row in result:
            print(row)
            tbl.add_row(row)
        
        print(tbl)
        
        input("Tekan Enter Untuk Melanjutkan")
        clrscr()
        lecmenu()
        
    def mhsmenu(username):
        qselect = "SELECT nomorpokok FROM users WHERE username = '%s'" %(username)
        cur.execute(qselect)
        npm = cur.fetchone()
        npm = npm[0]
        
        print('========================')
        print('Menu Mahasiswa')
        print('========================')
        
        menus = ['Cek Kehadiran', 'Lakukan Presensi', 'Keluar']
        
        for i,listmenu in enumerate(menus):
            print(1+i,".",listmenu)
            
        inpmenu = input("Pilih Menu: ")
        
        if inpmenu == '1':
            cekKehadiran(npm)
        elif inpmenu == '2':
            presensi(npm)
        elif inpmenu == '3':
            print("Terima Kasih")
            exit()
        else:
            print("Salah Input")
            clrscr()
            mhsmenu(mhsmenu)
    def cekKehadiran(npm):
        qselect = "SELECT matkul,p1,p2,p3,p4 from abs%s" % (npm)
        cur.execute(qselect)
        result = cur.fetchall()
        
        columns = ['Mata Kuliah','Pertemuan 1','Pertemuan 2','Pertemuan 3','Pertemuan 4']
        tbl = PrettyTable()
        tbl.field_names = columns
        
        for row in result:
            tbl.add_row(row)
        
        print(tbl)
        
        input("Tekan Enter Untuk Melanjutkan")
        clrscr()
        mhsmenu(username)
    
    def presensi(npm):
        npm = npm
        token = input("Masukkan Token: ")
        
        qselectmatkul = "SELECT matkul,pertemuan,token FROM matkultoken WHERE token='%s'" %(token)
        cur.execute(qselectmatkul)
        result = cur.fetchone()
        
        
        if result:
            pass
        else:
            print("Token Yang Anda Masukkan Salah")
            presensi(npm)
            
        matkul = result[0]
        pertemuan = result[1]
        
        # print(result)
        qabsupdate = "UPDATE abs%s SET p%s = 'Hadir' WHERE matkul = '%s'" %(npm,pertemuan,matkul)
        cur.execute(qabsupdate)
        conn.commit()
        if cur.rowcount > 0:
            print("Terima Kasih Telah Melakukan Presensi")
            input("Tekan Enter Untuk Kembali Ke Menu")
            clrscr()
            mhsmenu(username)
        else:
            print("Anda Telah Melakukan Presensi")
            input("Tekan Enter Untuk Kembali Ke Menu")
            clrscr()
            mhsmenu(username)
        
        
          
    print('========================')
    print('SISTEM AKADEMIK')
    print('========================')
    
    username = input('Username: ')
    password = input('Password: ')
    auth(username,password)

main()