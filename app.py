from flask import Flask, render_template, request
from pymongo import MongoClient
import os
from os.path import join, dirname
from dotenv import load_dotenv
from http import client
import psutil
import platform
import socket

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI= os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

def tampilkan_info_hardware():
    ram = psutil.virtual_memory()
    penyimpanan = psutil.disk_usage('/')
    nama_perangkat = platform.node()
    sistem_operasi = platform.system()
    provider_internet = socket.gethostname()

    total_ram = round(ram.total / (1024 ** 3), 2)  # Mengkonversi ke gigabyte
    tersedia_ram = round(ram.available / (1024 ** 3), 2)
    persentase_ram = ram.percent

    total_penyimpanan = round(penyimpanan.total / (1024 ** 3), 2)  # Mengkonversi ke gigabyte
    tersedia_penyimpanan = round(penyimpanan.free / (1024 ** 3), 2)
    persentase_penyimpanan = penyimpanan.percent

    info_hardware = {
        "RAM": total_ram,
        "RAM Tersedia" : tersedia_ram,
        "Persentase RAM" : persentase_ram,
        "Total Penyimpanan" : total_penyimpanan,
        "Penyimpanan Tersedia" : tersedia_penyimpanan, 
        "Persentase Penyimpanan" : persentase_penyimpanan,
        "Nama Perangkat": nama_perangkat,
        "Sistem Operasi": sistem_operasi,
        "Provider Internet": provider_internet
    }
    db.datauser.insert_one(info_hardware)
    return info_hardware

# Kode lainnya tetap sama



@app.route('/')
def tampilkan_halaman():
    return render_template('index.html')

@app.route('/info', methods=['POST'])
def tampilkan_info():
    info_hardware = tampilkan_info_hardware()
    return info_hardware

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
