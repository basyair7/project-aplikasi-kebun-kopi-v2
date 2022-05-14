"""
PROGRAM PROJECT AKHIR PEMROGRAMAN 2
NAMA    : FATHUL BASYAIR
NPM     : 1904105010004
PRODI   : TEKNIK ELEKTRO

FILE INI ADALAH LIBRARY TEMPAT MENGAMBIL DATA MELALUI API ADDRESS
DAN MEMBUAT SEBUAH PLOT GRAFIK DATA SENSOR TANAMAN

WARNING : DILARANG KERAS MENGUBAH API ADDRESS / PLAGIARISME
"""

from urllib.request import urlopen
from tkinter import messagebox
import matplotlib.pyplot as plt
import json
import datetime
from time import sleep


class get_data:
    def __init__(self, id_tree):
        self.id_tree = id_tree
        if self.id_tree == None:
            return messagebox.showerror("Informasi", "ID Pohon Kosong!");
            
    def get_data(self):
        tree = self.id_tree

        def url_api(sensor_type):
            address = f"https://belajar-python-unsyiah.an.r.appspot.com/sensor/read?npm=1904105010004&id_tree={tree}&sensor_type={sensor_type}";
            return address;
        
        def air_temp(self):
            # koneksi ke api
            address = url_api(0);
            
            # buka data api
            url = urlopen(address);
            documents = url.read().decode("utf-8");
            # convert json api
            self.data_1 = json.loads(documents)['value']
            sleep(1)
        
        def air_hum(self):
            # koneksi ke api
            address = url_api(1)
            
            # buka data api
            url = urlopen(address);
            documents = url.read().decode("utf-8");
            # convert json api
            self.data_2 = json.loads(documents)['value']
            sleep(1)
        
        def rainfall(self):
            # koneksi ke api
            address = url_api(2)
            
            # buka data api
            url = urlopen(address);
            documents = url.read().decode("utf-8");
            # convert json api
            self.data_3 = json.loads(documents)['value']
            sleep(1)
        
        def uv_level(self):
            # koneksi ke api
            address = url_api(3)
            
            # buka data api
            url = urlopen(address);
            documents = url.read().decode("utf-8");
            # convert json api
            self.data_4 = json.loads(documents)['value']
            sleep(1)
        
        def soil_temp(self):
            # koneksi ke api
            address = url_api(4)
            
            # buka data api
            url = urlopen(address);
            documents = url.read().decode("utf-8");
            # convert json api
            self.data_5 = json.loads(documents)['value']
            sleep(1)
        
        def soil_hum(self):
            # koneksi ke api
            address = url_api(5)
            
            # buka data api
            url = urlopen(address);
            documents = url.read().decode("utf-8");
            # convert json api
            self.data_6 = json.loads(documents)['value']
            sleep(1)
        
        def soil_ph(self):
            # koneksi ke api
            address = url_api(6)
            
            # buka data api
            url = urlopen(address);
            documents = url.read().decode("utf-8");
            # convert json api
            self.data_7 = json.loads(documents)['value']
            sleep(1)

        def n_level(self):
            # koneksi ke api
            address = url_api(7)
            
            # buka data api
            url = urlopen(address);
            documents = url.read().decode("utf-8");
            # convert json api
            self.data_8 = json.loads(documents)['value']
            sleep(1)
        
        def p_level(self):
            # koneksi ke api
            address = url_api(8)
            
            # buka data api
            url = urlopen(address);
            documents = url.read().decode("utf-8");
            # convert json api
            self.data_9 = json.loads(documents)['value']
            sleep(1)
        
        def k_level(self):
            # koneksi ke api
            address = url_api(9)
            
            # buka data api
            url = urlopen(address);
            documents = url.read().decode("utf-8");
            # convert json api
            self.data_10 = json.loads(documents)['value']
            sleep(1)
        
        # ambil data dari api address
        air_temp(self)
        air_hum(self)
        rainfall(self)
        uv_level(self)
        soil_temp(self)
        soil_hum(self)
        soil_ph(self)
        n_level(self)
        p_level(self)
        k_level(self)

        # Create a real date and time
        now = datetime.datetime.now()
        date = now.day
        month = now.month
        year = now.year
        Time = (now.strftime("%H:%M"))
        date = f"{date}/{month}/{year}"


        # masukkan data ke format json
        return {
            "id_tree": tree, "date": date, "time": Time,
            "air_temp": self.data_1, "air_hum": self.data_2, 
            "rainfall": self.data_3, "uv_level": self.data_4, 
            "soil_temp": self.data_5, "soil_hum": self.data_6,  
            "soil_ph": self.data_7, "n_ph_level": self.data_8, 
            "p_ph_level": self.data_9, "k_ph_level": self.data_10
        }


class grafik:
    def __init__(self, x, y, color, legend, sub="", x_label="", y_label=""):
        self.title = sub
        self.data_x = x
        self.data_y = y
        self.x_label = x_label
        self.y_label = y_label
        self.color = color
        self.legend = legend

    def one_graph(self):
        # masukkan data ke object plot
        plt.plot(self.data_x, self.data_y, self.color)
        # membuat identitas plot
        plt.title(self.title)
        plt.legend([self.legend])
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        # tampilkan grafik
        plt.show()

class all_grafik:
    def __init__(self, id_tree, time, air_temp, air_hum, rainfall, uv_level, soil_temp, soil_hum, soil_ph, n_level, p_level, k_level):
        self.time = time; self.id_tree = id_tree
        self.air_temp = air_temp; self.air_hum = air_hum
        self.rainfall = rainfall; self.uv_level = uv_level
        self.soil_temp = soil_temp; self.soil_hum = soil_hum
        self.soil_ph = soil_ph; self.n_level = n_level
        self.p_level = p_level; self.k_level = k_level

    def main(self):
        # masukkan data ke object plot
        # air temperature
        plt.plot(self.time, self.air_temp, 'g-o')
        # air humidity
        plt.plot(self.time, self.air_hum, 'g-o')
        # rainfall
        plt.plot(self.time, self.rainfall, 'c-o')
        # UV level
        plt.plot(self.time, self.uv_level, 'y-o')
        # soil temperature
        plt.plot(self.time, self.soil_temp, 'k-o')
        # soil humidity
        plt.plot(self.time, self.soil_hum, 'k-o')
        # soil pH
        plt.plot(self.time, self.soil_ph, 'k-o')
        # N level
        plt.plot(self.time, self.n_level, 'm-o')
        # P level
        plt.plot(self.time, self.p_level, 'r-o')
        # K level
        plt.plot(self.time, self.k_level, 'b-o')

        # membuat identitas plot
        plt.title(f"Grafik ID Pohon {self.id_tree}")
        plt.legend(['Suhu udara', 'Kelembaban udara', 'Curah hujan', 'Sinar UV', 'Suhu tanah', 'Kelembaban tanah', 'pH tanah', 'N level', 'P level', 'K level'])
        plt.xlabel("Waktu")
        plt.ylabel("Data")
        
        # tampilkan grafik
        plt.show()
