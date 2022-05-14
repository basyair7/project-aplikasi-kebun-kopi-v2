# PROGRAM PROJECT AKHIR PEMROGRAMAN 2
NAMA    = "FATHUL BASYAIR"
NPM     = "1904105010004"
PRODI   = "TEKNIK ELEKTRO"

"""
FILE INI ADALAH TEMPAT PROGRAM UTAMA APLIKASI DATA KEBUN KOPI
WARNING : DILARANG KERAS MENGUBAH ISI FILE INI/ PLAGIARISME
"""

from DatabaseSQLite import *
from BackendProgram import get_data, grafik, all_grafik
from random import uniform
from tkinter import *
from tkinter import filedialog
from threading import Lock, Event, Thread
from time import sleep

# Lock threading
lock = Lock();
exit_get_data = Event();

# Nama Database
nama_db = "kebun_kopi.db";
# Nama Table Lokasi ID Tree
nama_table = "table_loc_sensor";

# buka database
sql = db_connect(nama_db)
# buat database lokal otomatis (jika belum tersedia)
sql.create()

# buat fungsi ambil data
def ambil_data():
    try:
        id_tree = int(id_tree_entry.get())
        #id_tree_entry.configure(state=DISABLED)
        # Search Random location Latitude & Longitude
        loc_lat = uniform(1, 20)
        loc_lon = uniform(1, 360)

        # masukkan data ke dalam database
        sql.insert_loc_sensor(id_tree=id_tree, namatable=nama_table, loc_lat=loc_lat, loc_lon=loc_lon)
        messagebox.showinfo("Informasi", f"ID Pohon {id_tree} berhasil ditambahkan");
        info_box.insert(END, "Informasi");
        info_box.insert(END, f"ID Pohon {id_tree} berhasil ditambahkan")
        info_box.insert(END, " ");

        def program_get_data():
            while True:
                # cek exit_get_data
                # jika client minta perubahan id & keluar dari app, maka program_get_data harus berhenti
                if(id_tree == 0):
                    info_box.insert(END, "Informasi");
                    info_box.insert(END, "ID Pohon 0 Tidak Tersedia!")
                    info_box.insert(END, " ");
                    return messagebox.showerror("Informasi", "ID Pohon 0 Tidak Tersedia!");

                if exit_get_data.is_set():
                    break;
                
                # koneksi aplikasi ke api address
                data = get_data(id_tree).get_data();
                # masukkan data api address ke dalam database
                sql.insert_data(namatable=f"id_tree{id_tree}", date=data['date'], time=data['time'], air_temp=data['air_temp'], air_hum=data['air_hum'], rainfall=data['rainfall'], uv_level=data['uv_level'], soil_temp=data['soil_temp'], soil_hum=data['soil_hum'], soil_ph=data['soil_ph'], n_ph_level=data['n_ph_level'], p_ph_level=data['p_ph_level'], k_ph_level=data['k_ph_level'])
                
                # break setiap 1 menit
                sleep(60)

        # buat dan jalankan multitask Thread
        Thread(target=program_get_data).start()
    
    except ValueError:
        messagebox.showerror("Informasi", "Silahkan isi ID Tree\n*ID Tree Berupa Angka Bulat");
        info_box.insert(END, "Informasi");
        info_box.insert(END, "Silahkan isi ID Tree *ID Tree Berupa Angka Bulat");
        info_box.insert(END, " ");
        
    except IntegrityError:
        messagebox.showwarning("Informasi", f"ID Pohon {id_tree} sudah terisi\nSilahkan Hapus Data terlebih dahulu. ");
        info_box.insert(END, "Informasi");
        info_box.insert(END, f"ID Pohon {id_tree} sudah terisi Silahkan Hapus Data terlebih dahulu.");
        info_box.insert(END, " ");
        
    # clear input box
    id_tree_entry.delete(0, END)

# buat fungsi tampilkan data sensor
def option_sensor():
    # buat list data sensor
    data_sensor = []
    def input_data():
        data_sensor.clear()
        id_tree = id_tree_entry.get();
        data_sensor.append(id_tree)
        messagebox.showinfo("Informasi", f"ID Pohon {id_tree} berhasil ditambahkan");
        # clear input box
        id_tree_entry.delete(0, END)

    def result_data():
        try:
            # koneksi ke database lokal
            query = sql.read_data(f"id_tree{data_sensor[0]}")
            list_data = ""
            for row in query:
                list_data += f"ID Pohon\t\t : {data_sensor[0]}\nDate Time\t\t : {row[0]} ({row[1]})\nSuhu Udara\t\t : {row[2]}\nKelembaban Udara : {row[3]}\nCurah Hujan\t\t : {row[4]}\nUV Level\t\t : {row[5]}\nSuhu tanah\t\t : {row[6]}\nKelembaban Tanah\t: {row[7]}\npH Tanah\t\t : {row[8]}\nN Level\t\t : {row[9]}\nP Level\t\t : {row[10]}\nK Level\t\t : {row[11]}\n\n"

            global result_data
            result_data = Tk(); result_data.resizable(False, False)
            result_data.title("Tampilkan data sensor");
            
            # Screen resolution
            width_of_window = 700; height_of_window = 450
            screen_width = result_data.winfo_screenwidth()
            screen_height = result_data.winfo_screenheight()
            x_coordinate = (screen_width/4) - (width_of_window/4)
            y_coordinate = (screen_height/4) - (height_of_window/4)
            result_data.geometry(f"{width_of_window}x{height_of_window}+{int(x_coordinate)}+{int(y_coordinate)}")

            # membuat frame layout text
            frm_text = Frame(result_data, relief=RIDGE, borderwidth=5)
            frm_text.grid(row=0, column=0, padx=(10,0), pady=12)
            
            # Scrollbar
            scrolltxt_y = Scrollbar(frm_text, orient=VERTICAL)
            scrolltxt_y.grid(row=1, column=1, columnspan=1, ipady=170)

            # result box
            result_box = Text(frm_text, yscrollcommand=scrolltxt_y.set)
            result_box.grid(row=1, column=0, ipadx=2, ipady=2)
            scrolltxt_y.config(command=result_box.yview)

            result_box.insert(END, list_data)

            result_data.mainloop()
            
        except OperationalError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");
        except IndexError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");
            
    def air_temp_graph():
        try:
            # koneksi ke database lokal
            query = sql.read_data_spesific(f"id_tree{data_sensor[0]}", "air_temp")
            x = []; y = []
            for row in query:
                x.append(row[0]); y.append(row[1])
                
            grafik(x, y, 'g-o', "Suhu Udara", "Grafik Suhu Udara", "Waktu", "Sensor").one_graph()
            
        except OperationalError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");
        except IndexError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");
    
    def air_hum_graph():
        try:
            # koneksi ke database lokal
            query = sql.read_data_spesific(f"id_tree{data_sensor[0]}", "air_hum")
            x = []; y = []
            for row in query:
                x.append(row[0]); y.append(row[1])
    
            grafik(x, y, 'g-o', "Kelembaban Udara", "Grafik Kelembaban Udara", "Waktu", "Sensor").one_graph()
            
        except OperationalError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");
        except IndexError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");

    def rainfall_graph():
        try:
            # koneksi ke database lokal
            query = sql.read_data_spesific(f"id_tree{data_sensor[0]}", "rainfall")
            x = []; y = []
            for row in query:
                x.append(row[0]); y.append(row[1])
                
            grafik(x, y, 'c-o', "Curah Hujan", "Grafik Curah Hujan", "Waktu", "Sensor").one_graph()
            
        except OperationalError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");
        except IndexError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");

    def uv_level_graph():
        try:
            # koneksi ke database lokal
            query = sql.read_data_spesific(f"id_tree{data_sensor[0]}", "uv_level")
            x = []; y = []
            for row in query:
                x.append(row[0]); y.append(row[1])
                
            grafik(x, y, 'y-o', "Sinar UV", "Grafik Tingkat Sinar UV", "Waktu", "Sensor").one_graph()
            
        except OperationalError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");
        except IndexError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");

    def soil_temp_graph():
        try:
            # koneksi ke database lokal
            query = sql.read_data_spesific(f"id_tree{data_sensor[0]}", "soil_temp")
            x = []; y = []
            for row in query:
                x.append(row[0]); y.append(row[1])
                
            grafik(x, y, 'k-o', "Suhu Tanah", "Grafik Suhu Tanah", "Waktu", "Sensor").one_graph()
            
        except OperationalError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");
        except IndexError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");

    def soil_hum_graph():
        try:
            # koneksi ke database lokal
            query = sql.read_data_spesific(f"id_tree{data_sensor[0]}", "soil_hum")
            x = []; y = []
            for row in query:
                x.append(row[0]); y.append(row[1])
                
            grafik(x, y, 'k-o', "Kelembaban Tanah", "Grafik Kelembaban Tanah", "Waktu", "Sensor").one_graph()
            
        except OperationalError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");
        except IndexError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");

    def soil_ph_graph():
        try:
            # koneksi ke database lokal
            query = sql.read_data_spesific(f"id_tree{data_sensor[0]}", "soil_ph")
            x = []; y = []
            for row in query:
                x.append(row[0]); y.append(row[1])
                
            grafik(x, y, 'k-o', "pH Tanah", "Grafik pH Tanah", "Waktu", "Sensor").one_graph()
            
        except OperationalError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");
        except IndexError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");

    def n_level_graph():
        try:
            # koneksi ke database lokal
            query = sql.read_data_spesific(f"id_tree{data_sensor[0]}", "n_ph_level")
            x = []; y = []
            for row in query:
                x.append(row[0]); y.append(row[1])
                
            grafik(x, y, 'm-o', "N Level", "Grafik Kadar N Tanah", "Waktu", "Sensor").one_graph()
            
        except OperationalError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");
        except IndexError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");

    def p_level_graph():
        try:
            # koneksi ke database lokal
            query = sql.read_data_spesific(f"id_tree{data_sensor[0]}", "p_ph_level")
            x = []; y = []
            for row in query:
                x.append(row[0]); y.append(row[1])
                
            grafik(x, y, 'r-o', "P Level", "Grafik Kadar P Tanah", "Waktu", "Sensor").one_graph()
            
        except OperationalError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");
        except IndexError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");

    def k_level_graph():
        try:
            # koneksi ke database lokal
            query = sql.read_data_spesific(f"id_tree{data_sensor[0]}", "k_ph_level")
            x = []; y = []
            for row in query:
                x.append(row[0]); y.append(row[1])
                
            grafik(x, y, 'b-o', "K Level", "Grafik Kadar K Tanah", "Waktu", "Sensor").one_graph()
            
        except OperationalError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");
        except IndexError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");

    def semua_data_graph():
        try:
            # koneksi ke database lokal
            query = sql.read_data(f"id_tree{data_sensor[0]}")
            time = [] 
            data_1 = []; data_2 = []; data_3 = []; data_4 = []
            data_5 = []; data_6 = []; data_7 = []; data_8 = []
            data_9 = []; data_10 = []
            for row in query:
                time.append(row[1])
                data_1.append(row[2]); data_2.append(row[3]); data_3.append(row[4]); data_4.append(row[5])
                data_5.append(row[6]); data_6.append(row[7]); data_7.append(row[8]); data_8.append(row[9])
                data_9.append(row[10]); data_10.append(row[11])

            all_grafik(id_tree=data_sensor[0], time=time, air_temp=data_1, air_hum=data_2, rainfall=data_3, uv_level=data_4, soil_temp=data_5, soil_hum=data_6, soil_ph=data_7, n_level=data_8, p_level=data_9, k_level=data_10).main()

        except OperationalError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");
        except IndexError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");

    global option_sensor
    option_sensor = Tk(); option_sensor.resizable(False, False);
    option_sensor.title("Sensor Tanaman");
    # Screen resolution
    width_of_window = 395; height_of_window = 450
    screen_width = option_sensor.winfo_screenwidth()
    screen_height = option_sensor.winfo_screenheight()
    x_coordinate = (screen_width/4) - (width_of_window/4)
    y_coordinate = (screen_height/2) - (height_of_window/2)
    option_sensor.geometry(f"{width_of_window}x{height_of_window}+{int(x_coordinate)}+{int(y_coordinate)}");

    # frame layout input id_tree
    frm_id_tree = Frame(option_sensor, relief=RIDGE, borderwidth=5);
    frm_id_tree.grid(row=0, column=0, ipadx=32, ipady=5, padx=10, pady=10)
    # frame layout button application
    frm_btn_app = Frame(option_sensor, relief=RIDGE, borderwidth=5);
    frm_btn_app.grid(row=1, column=0, ipadx=30, padx=10)
    # frame layout textbox informasi
    frm_info = Frame(option_sensor, relief=RIDGE, borderwidth=5)
    frm_info.grid(row=2, column=0, padx=10, pady=10, ipadx=6)

    # membuat teks box label
    id_tree_label = Label(frm_id_tree, text="ID Pohon\t:")
    id_tree_label.grid(row=1, column=1, padx=5, pady=5)

    # membuat teks box
    id_tree_entry = Entry(frm_id_tree, width=20)
    id_tree_entry.grid(row=1, column=2, padx=5, pady=5)

    # membuat tombol aplikasi
    # tambah data
    add_data = Button(frm_id_tree, text="Masukkan ID", command=input_data)
    add_data.grid(row=2, column=1, pady=10, padx=16, ipadx=22)
    # tampilkan data sensor
    show_data = Button(frm_id_tree, text="Tampilkan data sensor", command=result_data)
    show_data.grid(row=2, column=2, padx=5, pady=10, ipadx=2)

    # tombol sensor
    ipadx_size={'air_temp': 20, 'air_hum': 5, 'rainfall': 16, 'uv_lvl':32, 'soil_temp': 20, 'soil_hum': 3, 'soil_ph': 25, 'n_lvl': 32, 'p_lvl': 32, 'k_lvl': 32, 'all_graph': 15}
    # air_temp
    air_temp_btn = Button(frm_btn_app, text="Suhu udara", command=air_temp_graph)
    air_temp_btn.grid(row=0, column=0, pady=10, padx=25, ipadx=ipadx_size['air_temp'])
    # air_hum
    air_hum_btn = Button(frm_btn_app, text="Kelembaban udara", command=air_hum_graph)
    air_hum_btn.grid(row=0, column=1, pady=11, padx=10, ipadx=ipadx_size['air_hum'])
    # rainfall
    rainfall_btn = Button(frm_btn_app, text="Curah Hujan", command=rainfall_graph)
    rainfall_btn.grid(row=1, column=0, pady=11, ipadx=ipadx_size['rainfall'])
    # uv_lvl
    uv_lvl_btn = Button(frm_btn_app, text="UV Level", command=uv_level_graph)
    uv_lvl_btn.grid(row=1, column=1, pady=11, ipadx=ipadx_size['uv_lvl'])
    # soil_temp
    soil_temp_btn = Button(frm_btn_app, text="Suhu Tanah", command=soil_temp_graph)
    soil_temp_btn.grid(row=2, column=0, pady=11, ipadx=ipadx_size['soil_temp'])
    # soil_hum
    soil_hum_btn = Button(frm_btn_app, text="Kelembaban Tanah", command=soil_hum_graph)
    soil_hum_btn.grid(row=2, column=1, pady=11, ipadx=ipadx_size['soil_hum'])
    #soil_ph
    soil_ph_btn = Button(frm_btn_app, text="ph Tanah", command=soil_ph_graph)
    soil_ph_btn.grid(row=3, column=0, pady=11, ipadx=ipadx_size['soil_ph'])
    #n_lvl
    n_lvl_btn = Button(frm_btn_app, text="N Level", command=n_level_graph)
    n_lvl_btn.grid(row=3, column=1, pady=11, ipadx=ipadx_size['n_lvl'])
    # p_lvl
    p_lvl_btn = Button(frm_btn_app, text="P Level", command=p_level_graph)
    p_lvl_btn.grid(row=4, column=0, pady=11, ipadx=ipadx_size['p_lvl'])
    # k_lvl
    k_lvl_btn = Button(frm_btn_app, text="K Level", command=k_level_graph)
    k_lvl_btn.grid(row=4, column=1, pady=11, ipadx=ipadx_size['k_lvl'])
    # semua grafik
    all_graph_btn = Button(frm_btn_app, text="Tampilkan\nSemua Grafik", command=semua_data_graph)
    all_graph_btn.grid(row=5, column=0, pady=11, ipadx=ipadx_size['all_graph'])

    # mainloop
    option_sensor.mainloop();

# tampilkan koordinat sensor per id pohon
def koordinat_sensor():
    try:
        def get_data_in_db():
            data = sql.read_data(nama_table)
            # ambil data dan tampilkan ke textbox
            print_records = ""
            for row in data:
                print_records += f"ID Pohon\t: {row[0]} -> Latitude\t: {row[1]}\tLongitude\t: {row[2]}\n"
            
            return print_records;
        
        global options_koordinat
        options_koordinat = Tk(); options_koordinat.resizable(False, False)
        options_koordinat.title("Tampilkan koordinat sensor pohon");
        
        # Screen resolution
        width_of_window = 700; height_of_window = 450
        screen_width = options_koordinat.winfo_screenwidth()
        screen_height = options_koordinat.winfo_screenheight()
        x_coordinate = (screen_width/4) - (width_of_window/4)
        y_coordinate = (screen_height/4) - (height_of_window/4)
        options_koordinat.geometry(f"{width_of_window}x{height_of_window}+{int(x_coordinate)}+{int(y_coordinate)}")

        # membuat frame layout text
        frm_text = Frame(options_koordinat, relief=RIDGE, borderwidth=5)
        frm_text.grid(row=0, column=0, padx=(10,0), pady=12)
        
        # Scrollbar
        scrolltxt_y = Scrollbar(frm_text, orient=VERTICAL)
        scrolltxt_y.grid(row=1, column=1, columnspan=1, ipady=170)

        # result box
        result_box = Text(frm_text, yscrollcommand=scrolltxt_y.set)
        result_box.grid(row=1, column=0, ipadx=2, ipady=2)
        scrolltxt_y.config(command=result_box.yview)

        result_box.insert(END, get_data_in_db())

        options_koordinat.mainloop()

    except OperationalError:
        messagebox.showwarning("Informasi", "Tidak ada data")
        info_box.insert(END, "Informasi");
        info_box.insert(END, f"Tidak ada data pada aplikasi.");
        info_box.insert(END, " ");
        return options_koordinat.destroy()

# Simpan data ke dalam file
def simpan_data():
    # buat list data sensor
    data_sensor = []
    def input_data():
        data_sensor.clear()
        id_tree = id_tree_entry.get();
        data_sensor.append(id_tree)
        messagebox.showinfo("Informasi", f"ID Pohon {id_tree} berhasil ditambahkan");
        # clear input box
        id_tree_entry.delete(0, END)

    def get_data_in_db():
        data = sql.read_data_loc(nama_table, data_sensor[0])
        # ambil data dan tampilkan ke textbox
        print_records = ""
        for row in data:
            print_records += f"ID Pohon\t\t : {data_sensor[0]} -> Latitude\t: {row[1]}\tLongitude\t: {row[2]}\n\n"
        
        return print_records;
            
    def get_all_data_sensor():
        # koneksi ke database lokal
        query = sql.read_data(f"id_tree{data_sensor[0]}")
        list_data = ""
        for row in query:
            list_data += f"Date Time\t\t : {row[0]} ({row[1]})\nSuhu Udara\t\t : {row[2]}\nKelembaban Udara : {row[3]}\nCurah Hujan\t\t : {row[4]}\nUV Level\t\t : {row[5]}\nSuhu tanah\t\t : {row[6]}\nKelembaban Tanah\t: {row[7]}\npH Tanah\t\t : {row[8]}\nN Level\t\t : {row[9]}\nP Level\t\t : {row[10]}\nK Level\t\t : {row[11]}\n\n";

        return list_data;
    
    def run():
        try:
            # Save data in txt
            merge_data = f"\t\t\t\t\t\tData Sensor Kebun Kopi (ID Pohon {data_sensor[0]})\t\t\t\t\t\t\n\n\n" + get_data_in_db() + get_all_data_sensor()

            # Create name for txt
            f = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
            if f is None:
                return

            f.write(merge_data)
            f.close()

            # Show information
            messagebox.showinfo('Informasi', 'Data sudah disimpan')
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Data telah disimpan dalam file.");
            info_box.insert(END, " ");

        except IndexError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");

        except OperationalError:
            messagebox.showwarning("Informasi", "Tidak ada data")
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"Tidak ada data pada aplikasi.");
            info_box.insert(END, " ");

    global option_save
    option_save = Tk(); option_save.title("Simpan data ke file"); 
    option_save.resizable(False, False)
    # Screen resolution
    width_of_window = 320; height_of_window = 150
    screen_width = option_save.winfo_screenwidth()
    screen_height = option_save.winfo_screenheight()
    x_coordinate = (screen_width/4) + (width_of_window/4)
    y_coordinate = (screen_height/2) - (height_of_window/2)
    option_save.geometry(f"{width_of_window}x{height_of_window}+{int(x_coordinate)}+{int(y_coordinate)}")

    # frame layout input id_tree
    frm_id_tree = Frame(option_save, relief=RIDGE, borderwidth=5);
    frm_id_tree.grid(row=0, column=0, ipadx=20, ipady=5, padx=5, pady=10)
    # frame layout button application
    frm_btn_app = Frame(option_save, relief=RIDGE, borderwidth=5);
    frm_btn_app.grid(row=1, column=0, ipadx=8, padx=5)

    # membuat teks box label
    id_tree_label = Label(frm_id_tree, text="Select ID Pohon\t:")
    id_tree_label.grid(row=1, column=1, padx=5, pady=5)

    # membuat teks box
    id_tree_entry = Entry(frm_id_tree, width=20)
    id_tree_entry.grid(row=1, column=2, padx=5, pady=5)

    # membuat tombol aplikasi
    # tambah data
    add_data = Button(frm_btn_app, text=f"Masukkan ID", command=input_data)
    add_data.grid(row=3, column=0, pady=10, padx=10, ipadx=22)
    # tombol sensor
    save_btn = Button(frm_btn_app, text="Simpan Data", command=run)
    save_btn.grid(row=3, column=1, pady=10, padx=5, ipadx=22)

    option_save.mainloop()

# hapus database
def delete():
    def delete_id():
        try:
            id_tree = id_tree_entry.get()
            ask = messagebox.askquestion(f"Hapus Data ID {id_tree}", f"Yakin anda menghapus data id tree {id_tree} dari aplikasi?")
            if ask == 'yes':
                exit_get_data.set()
                sleep(2)
                exit_get_data.clear()
                sql.remove_table(del_id=id_tree, del_table=nama_table)
                messagebox.showinfo(f"Hapus Data ID {id_tree}", f"Data id tree {id_tree} telah dihapus")
                info_box.insert(END, "Hapus Data ID");
                info_box.insert(END, f"Data id tree {id_tree} telah dihapus");
                info_box.insert(END, " ");
        
        except ValueError:
            messagebox.showerror("Informasi", "Silahkan isi ID Tree\n*ID Tree Berupa Angka Bulat");
            info_box.insert(END, "Informasi");
            info_box.insert(END, "Silahkan isi ID Tree *ID Tree Berupa Angka Bulat");
            info_box.insert(END, " ");
            
        except OperationalError:
            messagebox.showerror("Informasi", f"ID Tree {id_tree} tidak ditemukan");
            info_box.insert(END, "Informasi");
            info_box.insert(END, f"ID Tree {id_tree} tidak ditemukan dalam database");
            info_box.insert(END, " ");

        option_delete.destroy()

    def delete_db():
        ask = messagebox.askquestion("Hapus Semua Data", "Yakin anda menghapus semua data dari aplikasi?")
        if ask == 'yes':
            try:
                exit_get_data.set()
                sleep(2)
                exit_get_data.clear()
                sql.remove_db()
                messagebox.showinfo("Hapus Semua Data", "Semua data sensor telah dihapus")
                info_box.insert(END, "Hapus Semua Data");
                info_box.insert(END, "Semua data sensor telah dihapus");
                info_box.insert(END, " ");

                sql.create()

            except:
                messagebox.showerror("Informasi", "File database tidak dapat dihapus");
                info_box.insert(END, "Informasi");
                info_box.insert(END, "File database tidak dapat dihapus")
                info_box.insert(END, " ");
            option_delete.destroy()
    
    global option_delete
    option_delete = Tk(); option_delete.title("Hapus data"); 
    option_delete.resizable(False, False)
    # Screen resolution
    width_of_window = 350; height_of_window = 150
    screen_width = option_delete.winfo_screenwidth()
    screen_height = option_delete.winfo_screenheight()
    x_coordinate = (screen_width/4) + (width_of_window/4)
    y_coordinate = (screen_height/2) - (height_of_window/2)
    option_delete.geometry(f"{width_of_window}x{height_of_window}+{int(x_coordinate)}+{int(y_coordinate)}")

    # frame layout input id_tree
    frm_id_tree = Frame(option_delete, relief=RIDGE, borderwidth=5);
    frm_id_tree.grid(row=0, column=0, ipadx=38, ipady=5, padx=5, pady=10)
    # frame layout button application
    frm_btn_app = Frame(option_delete, relief=RIDGE, borderwidth=5);
    frm_btn_app.grid(row=1, column=0, ipadx=5, padx=5)

    # membuat teks box label
    id_tree_label = Label(frm_id_tree, text="Select ID Pohon\t:")
    id_tree_label.grid(row=1, column=1, padx=5, pady=5)

    # membuat teks box
    id_tree_entry = Entry(frm_id_tree, width=20)
    id_tree_entry.grid(row=1, column=2, padx=5, pady=5)

    # membuat tombol aplikasi
    # tambah data
    add_data = Button(frm_btn_app, text=f"Hapus Data ID", command=delete_id)
    add_data.grid(row=3, column=0, pady=10, padx=10, ipadx=22)

    # tombol sensor
    sensor_btn = Button(frm_btn_app, text="Hapus Semua Data", command=delete_db)
    sensor_btn.grid(row=3, column=1, pady=10, padx=5, ipadx=22)

    option_delete.mainloop()

# keluar dari aplikasi    
def keluar():
    ask = messagebox.askquestion("Keluar", "Anda yakin keluar dari Aplikasi?")
    if ask == 'yes':
        exit_get_data.set()
        return exit()

# about me
def about_me():
    messagebox._show("About Me", 
        f"Aplikasi Data Kebun Kopi\n\nVersion\t: v1.0\n\nDibuat Oleh \n\nNama\t: {NAMA}\nNPM\t: {NPM}\nProdi\t: {PRODI}\n\nPROJECT AKHIR PEMROGRAMAN 2"
    )


# membuat home tk
home = Tk(); home.resizable(False, False);
home.title("Aplikasi Data Kebun Kopi");
#home.overrideredirect(1)

# Screen resolution
width_of_window = 350; height_of_window = 480
screen_width = home.winfo_screenwidth()
screen_height = home.winfo_screenheight()
x_coordinate = (screen_width/2) - (width_of_window/2)
y_coordinate = (screen_height/2) - (height_of_window/2)
home.geometry(f"{width_of_window}x{height_of_window}+{int(x_coordinate)}+{int(y_coordinate)}")

# membuat frame layout
# frame layout input id_tree
frm_id_tree = Frame(home, relief=RIDGE, borderwidth=5);
frm_id_tree.grid(row=0, column=0, ipadx=38, ipady=5, padx=5, pady=10)
# frame layout button application
frm_btn_app = Frame(home, relief=RIDGE, borderwidth=5);
frm_btn_app.grid(row=1, column=0, ipadx=5, padx=5)
# frame layout textbox informasi
frm_info = Frame(home, relief=RIDGE, borderwidth=5)
frm_info.grid(row=2, column=0, padx=10, pady=10, ipadx=6)

# membuat teks box label
id_tree_label = Label(frm_id_tree, text="ID Pohon\t:")
id_tree_label.grid(row=1, column=1, padx=5, pady=5)

# membuat teks box
id_tree_entry = Entry(frm_id_tree, width=20)
id_tree_entry.grid(row=1, column=2, padx=5, pady=5)

# membuat tombol aplikasi
# tambah data
add_data = Button(frm_btn_app, text="Tambahkan Data", command=ambil_data)
add_data.grid(row=3, column=0, pady=10, padx=10, ipadx=22)

# tombol sensor
sensor_btn = Button(frm_btn_app, text="Sensor Tamanan", command=option_sensor)
sensor_btn.grid(row=3, column=1, pady=10, padx=11, ipadx=15)

# tombol koordinat sensor
result_btn = Button(frm_btn_app, text="Tampilkan\nKoordinat", command=koordinat_sensor)
result_btn.grid(row=4, column=0, pady=5, ipadx=40)

# Save data to text file
save_btn = Button(frm_btn_app, text="Simpan data\nkedalam file", command=simpan_data)
save_btn.grid(row=4, column=1, pady=5, ipadx=25)

# tombol hapus data
delete_btn = Button(frm_btn_app, text="Hapus Data", command=delete)
delete_btn.grid(row=5, column=0, pady=10, ipadx=38)

# tombol keluar
exit_btn = Button(frm_btn_app, text="Keluar", command=keluar)
exit_btn.grid(row=5, column=1, pady=10, ipadx=40)

# membuat textbox informasi
# Scroll Bar
scroll_y = Scrollbar(frm_info, orient=VERTICAL)
scroll_y.grid(row=0, column=1, ipady=57)
scroll_x = Scrollbar(frm_info, orient=HORIZONTAL)
scroll_x.grid(row=1, column=0, ipadx=100)
# Listbox
info_box = Listbox(frm_info, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
info_box.grid(row=0, column=0, columnspan=1, ipadx=85)
scroll_x.config(command=info_box.xview)
scroll_y.config(command=info_box.yview)

# Button about program
btn_about = Button(home, text='About Me', command=about_me)
btn_about.grid(row=3, column=0, padx=10, pady=8, ipadx=15)

# mainloop
home.mainloop()
