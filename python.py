import mysql.connector
import pandas as pd
from datetime import datetime

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="zakat_fitrah"
        )
    except mysql.connector.Error as e:
        print(f"Error: Gagal koneksi ke database - {str(e)}")
        exit(1)

