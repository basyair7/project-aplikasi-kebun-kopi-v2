"""
PROGRAM PROJECT AKHIR PEMROGRAMAN 2
NAMA    : MUHAMMAD AL-WAFI
NPM     : 1904105010051
PRODI   : TEKNIK ELEKTRO

FILE INI ADALAH LIBRARY TEMPAT MENYIMPAN DATA KE DALAM DATABASE LOKAL

WARNING : DILARANG KERAS MENGUBAH PROGRAM INI / PLAGIARISME
"""

from sqlite3 import connect;
from sqlite3 import IntegrityError, OperationalError;
from tkinter import messagebox;
import os

class db_connect:
    # buat inisialisasi object class db_connect
    def __init__ (self, namadb=""):
        # ambil nama database dan nama table 
        self.namadb = namadb;

    def create(self):
        # buat file baru database lokal (sqlite3)
        if(self.namadb == ""):
            messagebox.showwarning("Informasi", "Silahkan isi nama database!");
            return exit();

        conn = connect(self.namadb);

        # commit
        conn.commit();
        # tutup database
        conn.close();

    # buat fungsi insert data dalam object db_connect
    def insert_data (self, namatable, date, time, air_temp, air_hum, rainfall, uv_level, soil_temp, soil_hum, soil_ph, n_ph_level, p_ph_level, k_ph_level):
        # ambil data sensor
        self.date = date; self.time = time; self.air_temp = air_temp; self.air_hum = air_hum; 
        self.rainfall = rainfall; self.uv_level = uv_level; self.soil_temp = soil_temp; self.soil_hum = soil_hum; 
        self.soil_ph = soil_ph; self.n_ph_level = n_ph_level; self.p_ph_level = p_ph_level; self.k_ph_level = k_ph_level; 
        self.namatable_id_tree = namatable

        if(self.namadb == ""):
            messagebox.showwarning("Informasi", "Silahkan isi nama database!");
            return exit();
            
        if(self.namatable_id_tree == ""):
            messagebox.showwarning("Informasi", "Silahkan isi nama table!");
            return exit();
        
        # buka database lokal
        conn = connect(self.namadb);
        c = conn.cursor();

        # buat table database jika tidak tersedia
        c.execute(f"CREATE TABLE IF NOT EXISTS {self.namatable_id_tree} (date TEXT, time TEXT, air_temp REAL, air_hum REAL, rainfall REAL, uv_level REAL, soil_temp REAL, soil_hum REAL, soil_ph REAL, n_ph_level REAL, p_ph_level REAL, k_ph_level REAL);");

        # commit
        conn.commit();

        # isi data ke dalam database lokal (sqlite3)
        c.execute(f"INSERT INTO {self.namatable_id_tree} VALUES (:date, :time, :air_temp, :air_hum, :rainfall, :uv_level, :soil_temp, :soil_hum, :soil_ph, :n_ph_level, :p_ph_level, :k_ph_level)",{
            'date': self.date, 'time': self.time, 'air_temp': self.air_temp,
            'air_hum': self.air_hum, 'rainfall': self.rainfall, 'uv_level': self.uv_level, 
            'soil_temp': self.soil_temp, 'soil_hum': self.soil_hum, 'soil_ph': self.soil_ph, 
            'n_ph_level': self.n_ph_level, 'p_ph_level': self.p_ph_level, 'k_ph_level': self.k_ph_level
        });

        # commit
        conn.commit();
        # tutup database
        conn.close();

    def insert_loc_sensor(self, id_tree, namatable, loc_lat, loc_lon):
        self.namatable_loc = namatable; self.id_tree_loc = id_tree;
        self.loc_lat = float(loc_lat); self.loc_lon = float(loc_lon);

        if(self.namadb == ""):
            messagebox.showwarning("Informasi", "Silahkan isi nama database!");
            return exit();

        if(self.namatable_loc == ""):
            messagebox.showwarning("Informasi", "Silahkan isi nama table!");
            return exit();
        
        # Buka database lokal
        conn = connect(self.namadb);
        c = conn.cursor();

        # buat table database jika tidak tersedia
        c.execute(f"CREATE TABLE IF NOT EXISTS {self.namatable_loc}(id_tree INTEGER PRIMARY KEY, loc_lat REAL, loc_lon REAL);");

        # commit
        conn.commit();

        # isi data ke dalam database lokal (sqlite3)
        c.execute(f"INSERT INTO {self.namatable_loc} VALUES (:id_tree, :loc_lat, :loc_lon)",{
            'id_tree': self.id_tree_loc,
            'loc_lat': self.loc_lat,
            'loc_lon': self.loc_lon
        })

        # commit
        conn.commit()
        # tutup database
        conn.close();
                    
    
    #buat fungsi read data dalam object db_connect
    def read_data(self, namatable):
        # buka file database lokal (sqlite3)
        if(self.namadb == ""):
            messagebox.showwarning("Informasi", "Silahkan isi nama database!");
            return exit();
        
        conn = connect(self.namadb);
        c = conn.cursor();
        
        # Menampilkan data database
        if(namatable == ""):
            messagebox.showwarning("Informasi", "Silahkan isi nama table!");
            return exit();
        
        c.execute(f"SELECT * FROM {namatable}");
        data = c.fetchall()

        conn.commit()
        conn.close()
        
        return data;
    
    def read_data_loc(self, namatable, id_tree):
        # buka file database lokal (sqlite3)
        if(self.namadb == ""):
            messagebox.showwarning("Informasi", "Silahkan isi nama database!");
            return exit();

        if(namatable == "" or namatable == None):
            messagebox.showwarning("Informasi", "Silahkan isi nama table!");
            return exit();
        
        if(id_tree == "" or id_tree == None):
            messagebox.showwarning("Informasi", "Silahkan isi ID Pohon!");
            return exit();

        conn = connect(self.namadb);
        c = conn.cursor();

        # mengambil data lokasi id tree
        c.execute(f"SELECT * FROM {namatable} WHERE id_tree={id_tree}")
        data = c.fetchall()

        conn.commit()
        conn.close()
        
        return data;


    def read_data_spesific(self, namatable, namaitem):
        # buka file database lokal (sqlite3)
        if(self.namadb == ""):
            messagebox.showwarning("Informasi", "Silahkan isi nama database!");
            return exit();
        
        conn = connect(self.namadb);
        c = conn.cursor();
        
        # Menampilkan data table
        if(namatable == "" or namatable == None):
            messagebox.showwarning("Informasi", "Silahkan isi nama table!");
            return exit();
        
        if(namaitem == "" or namaitem == None):
            messagebox.showwarning("Informasi", "Silahkan isi nama item!");
            return exit();
        
        c.execute(f"SELECT time, {namaitem}, oid FROM {namatable}");
        data = c.fetchall()

        conn.commit()
        conn.close()
        
        return data;
    
    def remove_db(self):
        # buka file database lokal (sqlite3)
        if(self.namadb == ""):
            messagebox.showwarning("Informasi", "Silahkan isi nama database!")
            return exit();

        os.remove(f"{self.namadb}")

    #buat fungsi remove table dalam object db_connect
    def remove_table(self, del_id, del_table):
        
        if(del_table == ""):
            messagebox.showwarning("Informasi", "Silahkan isi nama table!");
            return exit();
        # buka file database lokal (sqlite3)
        if(self.namadb == ""):
            messagebox.showwarning("Informasi", "Silahkan isi nama database!")
            return exit();

        conn = connect(self.namadb);
        c = conn.cursor();

        # hapus semua data table id_tree
        c.execute(f"DROP TABLE IF EXISTS {del_id};")
        # commit
        conn.commit();
        
        # hapus semua data lokasi id_tree
        c.execute(f"DELETE FROM {del_table} WHERE oid = {del_id};")
        # commit
        conn.commit();

        # tutup database
        conn.close();

    def update_data(self, id_tree, loc_lat, loc_lon, date_time, air_temp, air_hum, rainfall, uv_level, soil_temp, soil_hum, soil_ph, n_ph_level, p_ph_level, k_ph_level):

        # ambil data sensor
        self.id_tree = int(id_tree); self.loc_lat = float(loc_lat); self.loc_lon = float(loc_lon); 
        self.date_time = date_time; self.air_temp = air_temp; self.air_hum = air_hum; self.rainfall = rainfall; 
        self.uv_level = uv_level; self.soil_temp = soil_temp; self.soil_hum = soil_hum; self.soil_ph = soil_ph; 
        self.n_ph_level = n_ph_level; self.p_ph_level = p_ph_level; self.k_ph_level = k_ph_level;  
        
        if(self.namatable == ""):
            messagebox.showwarning("Informasi", "Silahkan isi nama table!");
            return exit();

        # buka file database lokal (sqlite3)
        if(self.namadb == ""):
            messagebox.showwarning("Informasi", "Silahkan isi nama database!")
            return exit();
        
        conn = connect(self.namadb);
        c = conn.cursor();

        # update data table jika ada terbaru
        c.execute(f"UPDATE {self.namatable} SET loc_lat = :loc_lat, loc_lon = :loc_lon, date_time = :date_time, air_temp = :air_temp, air_hum = :air_hum, rainfall = :rainfall, uv_level = :uv_level, soil_temp = :soil_temp, soil_hum = :soil_hum, soil_ph = :soil_ph, n_ph_level = :n_ph_level, p_ph_level = :p_ph_level, k_ph_level = :k_ph_level WHERE id_tree = :id_tree",{
            'loc_lat': self.loc_lat,
            'loc_lon': self.loc_lon, 'date_time': self.date_time, 'air_temp': self.air_temp,
            'air_hum': self.air_hum, 'rainfall': self.rainfall, 'uv_level': self.uv_level, 
            'soil_temp': self.soil_temp, 'soil_hum': self.soil_hum, 'soil_ph': self.soil_ph, 
            'n_ph_level': self.n_ph_level, 'p_ph_level': self.p_ph_level, 'k_ph_level': self.k_ph_level, 'id_tree': self.id_tree
        });

        # commit
        conn.commit();
        # tutup database
        conn.close()
        