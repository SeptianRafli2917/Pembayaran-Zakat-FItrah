import mysql.connector
from datetime import datetime

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="zakat_db"
        )
    except mysql.connector.Error as e:
        print(f"Error: Gagal koneksi ke database - {str(e)}")
        exit(1)

def create_beras_table():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS beras (
            id INT AUTO_INCREMENT PRIMARY KEY,
            harga DECIMAL(10,2)
        )
    ''')
    db.commit()

#beras db
def tambah_data_beras():
    db = connect_db()
    cursor = db.cursor()
    try:
        print("\n=== Tambah Data Beras ===")
        harga = float(input("Masukkan harga beras per Liter: Rp "))
        
        cursor.execute('''
            INSERT INTO beras (harga)
            VALUES (%s)
        ''', (harga,))
        db.commit()
        print("\nHarga beras berhasil ditambahkan!")
        
    except ValueError:
        print("Error: Harga harus berupa angka!")
    except Exception as e:
        print(f"Error: {str(e)}")

def tampilkan_data_beras():
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM beras')
        hasil = cursor.fetchall()
        
        if not hasil:
            print("\nBelum ada data harga beras")
            return None
            
        print("\n=== Daftar Harga Beras ===")
        print("-" * 35)
        print(f"{'ID':^4} | {'Harga/Liter':^28}")
        print("-" * 35)
        
        for row in hasil:
            print(f"{row[0]:^4} | Rp {float(row[1]):>24,.2f}")
        print("-" * 35)
        return hasil
    except mysql.connector.Error as e:
        print(f"Error: Gagal mengambil data beras - {str(e)}")
        return None

# #pembayaran db
def create_payment_table(db):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pembayaran (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nama VARCHAR(100),
            jumlah_jiwa INT,
            jenis_zakat VARCHAR(10),
            metode_pembayaran VARCHAR(50),
            total_bayar DECIMAL(10,2),
            nominal_dibayar DECIMAL(10,2),
            kembalian DECIMAL(10,2),
            keterangan TEXT,
            tanggal_bayar DATETIME
        )
    ''')
    db.commit()

def tampilkan_data_pembayaran():
    db = connect_db()
    cursor = db.cursor()
    print("\n=== Data Pembayaran Zakat ===")
    cursor.execute("""
        SELECT nama, jumlah_jiwa, metode_pembayaran, 
               total_bayar, nominal_dibayar, kembalian, 
               tanggal_bayar 
        FROM pembayaran 
        ORDER BY tanggal_bayar DESC
    """)
    hasil = cursor.fetchall()
    
    if not hasil:
        print("Belum ada data pembayaran")
        return
        
    print("-" * 100)
    print(f"{'Nama':^20} | {'Jumlah Jiwa':^10} | {'Metode':^15} | {'Total':^15} | {'Dibayar':^15} | {'Kembalian':^15} | {'Tanggal':^20}")
    print("-" * 100)
    
    for row in hasil:
        print(f"{row[0]:<20} | {row[1]:^10} | {row[2]:^15} | Rp {float(row[3]):>11,.2f} | Rp {float(row[4]):>11,.2f} | Rp {float(row[5]):>11,.2f} | {row[6]}")
    print("-" * 100)

try:
    db = connect_db()
    cursor = db.cursor()
    create_beras_table()
    create_payment_table(db)
except mysql.connector.Error as e:
    print(f"Database connection failed: {e}")
    exit(1)

try:
    while True:
        print("\n=== Menu ===")
        print("1. Tambah Data Beras")
        print("2. Tampilkan Data Beras")
        print("3. Tampilkan Data Pembayaran")
        print("4. Keluar")
        
        pilihan = input("Pilih menu (1-6): ")
        
        if pilihan == '1':
            tambah_data_beras()
        elif pilihan == '2':
            tampilkan_data_beras()
        elif pilihan == '3':
            tampilkan_data_pembayaran()
        elif pilihan == '4':
            print("Program selesai")
            break
        else:
            print("Pilihan tidak valid!")
finally:
    cursor.close()
    db.close()