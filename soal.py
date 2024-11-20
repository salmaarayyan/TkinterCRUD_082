import sqlite3 # Untuk menghubungkan dengan database SQLite
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk # Untuk membuat antarmuka GUI menggunakan Tkinter

# Membuat database dan tabel jika belum ada
def create_database():
    conn = sqlite3.connect('nilai_siswa_.db') # Membuka/terhubung ke database SQLite
    cursor = conn.cursor() # Membuat cursor untuk mengeksekusi perintah SQL
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS nilai_siswa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_siswa TEXT NOT NULL,
        biologi INTEGER,
        fisika INTEGER,
        inggris INTEGER,
        prediksi_fakultas TEXT
        )
    ''')
    conn.commit() # Menyimpan perubahan ke database
    conn.close() # Menutup koneksi database

# Mengambil semua data dari tabel
def fetch_data():
    conn = sqlite3.connect('nilai_siswa_.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nilai_siswa') # Query untuk mengambil semua data
    rows = cursor.fetchall() # Menyimpan semua baris hasil query
    conn.close()
    return rows

# Menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa_.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))  # Menyimpan data siswa
    conn.commit()
    conn.close()

# Memperbarui data dalam database berdasarkan ID
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa_.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id)) # Query update data berdasarkan ID
    conn.commit()
    conn.close()

# Menghapus data dari database berdasarkan ID
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa_.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,)) # Query delete berdasarkan ID
    conn.commit()
    conn.close()

# Menghitung prediksi fakultas berdasarkan nilai tertinggi
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran" # Biologi tertinggi
    elif fisika > biologi and fisika > inggris:
        return "Teknik" # Fisika tertinggi
    elif inggris > biologi and inggris > fisika:
        return "Bahasa" # Bahasa Inggris tertinggi
    else:
        return "Tidak diketahui" # Jika nilai sama atau tidak ada yang lebih tinggi

# Fungsi untuk menambahkan data siswa baru
def submit():
    try:
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.") # Validasi input nama
        
        prediksi = calculate_prediction(biologi, fisika, inggris) # Prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Simpan ke database
        messagebox.showinfo("Sukses", f"Data Berhasil disimpan!\nPrediksi fakultas: {prediksi}")
        clear_inputs() # Kosongkan input setelah data tersimpan
        populate_table() # Refresh tabel untuk menampilkan data baru

    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}") # Tampilkan error jika input salah

# Fungsi untuk memperbarui data siswa yang dipilih
def update():
    try:
        if not selected_record_id.get():
            raise ValueError("Pilih data dari tabel untuk di-update.")

        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")
        
        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)
        messagebox.showinfo("Sukses", "Data Berhasil diperbarui!")
        clear_inputs()
        populate_table()

    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus data siswa yang dipilih
def delete():
    try:
        if not selected_record_id.get():
            raise ValueError("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())
        delete_database(record_id)
        messagebox.showinfo("Sukses", "Data Berhasil dihapus!")
        clear_inputs()
        populate_table()

    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Mengosongkan input pada form
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

# Menampilkan data ke dalam tabel
def populate_table():
    for row in tree.get_children():
        tree.delete(row) # Hapus semua data di tabel
    for row in fetch_data():
        tree.insert('', 'end', values=row) # Masukkan data dari database ke tabel

# Mengisi input berdasarkan data yang dipilih dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']

        selected_record_id.set(selected_row[0]) # ID data yang dipilih
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid")

# Inisialisasi database
create_database()

# Membuat GUI utama
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel untuk menyimpan input
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()

# Form input
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Bahasa Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Tombol aksi
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Tabel untuk menampilkan data
columns = ('id', 'nama_siswa', 'biologi', 'fisika', 'inggris', 'prediksi_fakultas')
tree = ttk.Treeview(root, columns=columns, show='headings')

# Membuat header kolom
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center')

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Event untuk memilih data dari tabel
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

# Menampilkan data awal di tabel
populate_table()

# Menjalankan aplikasi
root.mainloop()