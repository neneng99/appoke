import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Path to data files
STOK_BARANG_FILE = "stok_barang.csv"
PENJUALAN_FILE = "penjualan.csv"
SUPPLIER_FILE = "supplier.csv"

# CSS styles for a professional look
st.markdown("""
    <style>
    .header-image {
        width: 100%;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        padding-top: 20px;
    }
    .sidebar .sidebar-content h2 {
        font-family: 'Arial', sans-serif;
        color: #333;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content .radio {
        margin-top: 10px;
    }
    .main-content {
        padding: 20px;
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    }
    .stButton > button {
        background-color: #28a745;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Display the header image
image_path = "/mnt/data/A_professional_dashboard_design_for_a_cashier_appl.png"
if os.path.exists(image_path):
    st.image(image_path, use_column_width=True, class_="header-image")
else:
    st.error("Gambar tidak ditemukan!")

# Load data from CSV files
def load_data():
    if os.path.exists(STOK_BARANG_FILE):
        st.session_state.stok_barang = pd.read_csv(STOK_BARANG_FILE, parse_dates=["Waktu Input"])
    else:
        st.session_state.stok_barang = pd.DataFrame(columns=[
            "ID", "Nama Barang", "Merk", "Ukuran/Kemasan", "Harga", "Stok", "Persentase Keuntungan", "Waktu Input"
        ])

    if os.path.exists(PENJUALAN_FILE):
        st.session_state.penjualan = pd.read_csv(PENJUALAN_FILE, parse_dates=["Waktu"])
    else:
        st.session_state.penjualan = pd.DataFrame(columns=[
            "ID", "Nama Pelanggan", "Nomor Telepon", "Alamat", "Nama Barang", "Ukuran/Kemasan", "Merk", "Jumlah", "Total Harga", "Keuntungan", "Waktu"
        ])

    if os.path.exists(SUPPLIER_FILE):
        st.session_state.supplier = pd.read_csv(SUPPLIER_FILE, parse_dates=["Waktu"])
    else:
        st.session_state.supplier = pd.DataFrame(columns=[
            "ID", "Nama Barang", "Merk", "Ukuran/Kemasan", "Jumlah Barang", "Nama Supplier", "Tagihan", "Waktu"
        ])

# Save data to CSV files
def save_data():
    st.session_state.stok_barang.to_csv(STOK_BARANG_FILE, index=False)
    st.session_state.penjualan.to_csv(PENJUALAN_FILE, index=False)
    st.session_state.supplier.to_csv(SUPPLIER_FILE, index=False)

# Initialize data
if 'stok_barang' not in st.session_state:
    load_data()

# Sidebar menu
menu = st.sidebar.radio("Pilih Menu", ["Stock Barang", "Penjualan", "Supplier", "Owner"])

# Main content area
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Fungsi untuk halaman Stock Barang
def halaman_stock_barang():
    st.header("Stock Barang")
    
    # Form input barang baru
    with st.form("input_barang"):
        nama_barang = st.text_input("Nama Barang")
        merk = st.text_input("Merk")
        ukuran = st.text_input("Ukuran/Kemasan")
        harga = st.number_input("Harga", min_value=0)
        stok = st.number_input("Stok Barang", min_value=0)
        submit = st.form_submit_button("Tambah Barang")
        
        if submit:
            new_id = st.session_state.stok_barang["ID"].max() + 1 if not st.session_state.stok_barang.empty else 1
            new_data = pd.DataFrame({
                "ID": [new_id],
                "Nama Barang": [nama_barang],
                "Merk": [merk],
                "Ukuran/Kemasan": [ukuran],
                "Harga": [harga],
                "Stok": [stok],
                "Persentase Keuntungan": [20],  # Nilai default (tidak ditampilkan di form)
                "Waktu Input": [datetime.now()]  # Menambahkan waktu input barang
            })
            st.session_state.stok_barang = pd.concat([st.session_state.stok_barang, new_data], ignore_index=True)
            st.success("Barang berhasil ditambahkan!")
            save_data()  # Save data after adding new item

    # Tabel stok barang
    st.subheader("Daftar Stok Barang")
    df_stok_barang = st.session_state.stok_barang.copy()
    if "Persentase Keuntungan" in df_stok_barang.columns:
        df_stok_barang = df_stok_barang.drop(columns=["Persentase Keuntungan"])  # Menghapus kolom Persentase Keuntungan jika ada
    st.dataframe(df_stok_barang)

# Fungsi untuk halaman Penjualan
def halaman_penjualan():
    st.header("Penjualan")
    
    with st.form("input_penjualan"):
        nama_pelanggan = st.text_input("Nama Pelanggan")
        nomor_telpon = st.text_input("Nomor Telepon")
        alamat = st.text_area("Alamat")
        nama_barang = st.selectbox("Pilih Barang", st.session_state.stok_barang["Nama Barang"])
        ukuran = st.selectbox("Ukuran/Kemasan", st.session_state.stok_barang["Ukuran/Kemasan"])
        merk = st.selectbox("Merk", st.session_state.stok_barang["Merk"])
        jumlah = st.number_input("Jumlah Orderan", min_value=1)
        submit = st.form_submit_button("Simpan Penjualan")
        
        if submit:
            harga_barang = st.session_state.stok_barang[st.session_state.stok_barang["Nama Barang"] == nama_barang]["Harga"].values[0]
            persentase_keuntungan = st.session_state.stok_barang[st.session_state.stok_barang["Nama Barang"] == nama_barang]["Persentase Keuntungan"].values[0]
            total_harga = harga_barang * jumlah
            keuntungan = total_harga * (persentase_keuntungan / 100)
            waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Mendapatkan waktu saat ini
            
            new_penjualan = pd.DataFrame({
                "ID": [st.session_state.penjualan["ID"].max() + 1 if not st.session_state.penjualan.empty else 1],
                "Nama Pelanggan": [nama_pelanggan],
                "Nomor Telepon": [nomor_telpon],
                "Alamat": [alamat],
                "Nama Barang": [nama_barang],
                "Ukuran/Kemasan": [ukuran],
                "Merk": [merk],
                "Jumlah": [jumlah],
                "Total Harga": [total_harga],
                "Keuntungan": [keuntungan],  # Menyimpan keuntungan
                "Waktu": [waktu]  # Menyimpan waktu penjualan
            })
            st.session_state.penjualan = pd.concat([st.session_state.penjualan, new_penjualan], ignore_index=True)
            
            # Update stok barang
            st.session_state.stok_barang.loc[
                (st.session_state.stok_barang["Nama Barang"] == nama_barang) &
                (st.session_state.stok_barang["Ukuran/Kemasan"] == ukuran),
                "Stok"
            ] -= jumlah
            
            st.success(f"Penjualan untuk {nama_pelanggan} berhasil disimpan!")
            save_data()  # Save data after sale

    # Tabel stok barang terupdate
    st.subheader("Stok Barang Terupdate")
    df_stok_barang = st.session_state.stok_barang.copy()
    if "Persentase Keuntungan" in df_stok_barang.columns:
        df_stok_barang = df_stok_barang.drop(columns=["Persentase Keuntungan"])  # Menghapus kolom Persentase Keuntungan jika ada
    st.dataframe(df_stok_barang)

    # Tombol pencarian stok barang
    search_barang = st.text_input("Cari Barang")
    if search_barang:
        hasil_pencarian = st.session_state.stok_barang[st.session_state.stok_barang["Nama Barang"].str.contains(search_barang, case=False)]
        st.write("Hasil Pencarian:")
        if "Persentase Keuntungan" in hasil_pencarian.columns:
            hasil_pencarian = hasil_pencarian.drop(columns=["Persentase Keuntungan"])  # Menghapus kolom Persentase Keuntungan jika ada
        st.dataframe(hasil_pencarian)

    # Tombol untuk mendownload laporan penjualan
    if st.button("Download Laporan Penjualan (CSV)"):
        csv = st.session_state.penjualan.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv, file_name="laporan_penjualan.csv", mime="text/csv")

    # Tombol untuk print struk
    if st.button("Print Struk Terakhir"):
        from io import StringIO
        struk = StringIO()
        struk.write("=== STRUK PENJUALAN ===\n")
        for idx, row in st.session_state.penjualan.tail(1).iterrows():
            struk.write(f"Nama Pelanggan: {row['Nama Pelanggan']}\n")
            struk.write(f"Nomor Telepon: {row['Nomor Telepon']}\n")
            struk.write(f"Alamat: {row['Alamat']}\n")
            struk.write(f"Nama Barang: {row['Nama Barang']}\n")
            struk.write(f"Ukuran/Kemasan: {row['Ukuran/Kemasan']}\n")
            struk.write(f"Merk: {row['Merk']}\n")
            struk.write(f"Jumlah: {row['Jumlah']}\n")
            struk.write(f"Total Harga: {row['Total Harga']}\n")
            struk.write(f"Waktu: {row['Waktu']}\n")
        struk.write("=========================\n")
        
        # Tulis ke file dan simpan untuk print
        with open('struk_pembelian.txt', 'w') as f:
            f.write(struk.getvalue())
        
        st.success("Struk berhasil dicetak!")

# Fungsi untuk halaman Supplier
def halaman_supplier():
    st.header("Data Supplier")
    
    with st.form("input_supplier"):
        nama_barang = st.text_input("Nama Barang")
        merk = st.text_input("Merk")
        ukuran = st.text_input("Ukuran/Kemasan")
        jumlah_barang = st.number_input("Jumlah Barang", min_value=0)
        nama_supplier = st.text_input("Nama Supplier")
        tagihan = st.number_input("Tagihan", min_value=0)
        submit = st.form_submit_button("Tambah Data Supplier")
        
        if submit:
            new_id = st.session_state.supplier["ID"].max() + 1 if not st.session_state.supplier.empty else 1
            new_data = pd.DataFrame({
                "ID": [new_id],
                "Nama Barang": [nama_barang],
                "Merk": [merk],
                "Ukuran/Kemasan": [ukuran],
                "Jumlah Barang": [jumlah_barang],
                "Nama Supplier": [nama_supplier],
                "Tagihan": [tagihan],
                "Waktu": [datetime.now()]  # Menambahkan waktu input data supplier
            })
            st.session_state.supplier = pd.concat([st.session_state.supplier, new_data], ignore_index=True)
            st.success("Data supplier berhasil ditambahkan!")
            save_data()  # Save data after adding supplier data

    # Tabel data supplier
    st.subheader("Daftar Data Supplier")
    st.dataframe(st.session_state.supplier)

# Fungsi untuk halaman Owner dengan pengaman password
def halaman_owner():
    st.header("Halaman Owner - Analisa Keuangan")

    # Login form
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        with st.form("login_form"):
            password = st.text_input("Masukkan Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit and password == "password123":  # Ganti dengan password yang Anda inginkan
                st.session_state.authenticated = True
                st.success("Login berhasil!")
            elif submit:
                st.error("Password salah!")
        return

    # Tabel stok barang dengan fitur edit dan hapus
    st.subheader("Stok Barang")
    st.dataframe(st.session_state.stok_barang)
    selected_row = st.selectbox("Pilih ID Barang untuk Diedit", st.session_state.stok_barang["ID"])
    
    with st.form("edit_barang"):
        barang_dipilih = st.session_state.stok_barang[st.session_state.stok_barang["ID"] == selected_row]
        nama_barang = st.text_input("Nama Barang", value=barang_dipilih["Nama Barang"].values[0])
        merk = st.text_input("Merk", value=barang_dipilih["Merk"].values[0])
        ukuran = st.text_input("Ukuran/Kemasan", value=barang_dipilih["Ukuran/Kemasan"].values[0])
        harga = st.number_input("Harga", min_value=0, value=int(barang_dipilih["Harga"].values[0]))
        stok = st.number_input("Stok Barang", min_value=0, value=int(barang_dipilih["Stok"].values[0]))
        persentase_keuntungan = st.number_input("Persentase Keuntungan (%)", min_value=0, max_value=100, value=int(barang_dipilih["Persentase Keuntungan"].values[0]))
        submit = st.form_submit_button("Update Barang")
        
        if submit:
            st.session_state.stok_barang.loc[st.session_state.stok_barang["ID"] == selected_row, ["Nama Barang", "Merk", "Ukuran/Kemasan", "Harga", "Stok", "Persentase Keuntungan"]] = [nama_barang, merk, ukuran, harga, stok, persentase_keuntungan]
            st.success("Barang berhasil diupdate!")
            save_data()  # Save data after updating item
    
    # Tombol untuk hapus barang
    if st.button("Hapus Barang"):
        st.session_state.stok_barang = st.session_state.stok_barang[st.session_state.stok_barang["ID"] != selected_row]
        st.success("Barang berhasil dihapus!")
        save_data()  # Save data after deleting item
    
    # Laporan penjualan
    st.subheader("Laporan Penjualan")
    st.dataframe(st.session_state.penjualan)
    
    # Analisa keuangan dengan grafik pemasaran
    st.subheader("Analisa Keuangan")
    
    # Perhitungan total penjualan
    total_penjualan = st.session_state.penjualan["Total Harga"].sum()
    st.write(f"Total Penjualan: Rp {total_penjualan}")
    
    # Perhitungan tagihan supplier bulanan
    current_month = datetime.now().strftime("%Y-%m")
    st.session_state.supplier['Waktu'] = pd.to_datetime(st.session_state.supplier['Waktu'])
    monthly_supplier_bills = st.session_state.supplier[st.session_state.supplier["Waktu"].dt.strftime("%Y-%m") == current_month]["Tagihan"].sum()
    st.write(f"Total Tagihan Supplier Bulan Ini: Rp {monthly_supplier_bills}")
    
    # Perbandingan antara total penjualan dan tagihan supplier
    st.write(f"Selisih antara Total Penjualan dan Tagihan Supplier: Rp {total_penjualan - monthly_supplier_bills}")
    
    # Grafik keuntungan penjualan per barang
    st.subheader("Grafik Pemasaran")
    plt.figure(figsize=(10, 6))
    keuntungan_per_barang = st.session_state.penjualan.groupby("Nama Barang")["Keuntungan"].sum()
    keuntungan_per_barang.plot(kind="bar")
    plt.title("Keuntungan per Barang")
    plt.xlabel("Nama Barang")
    plt.ylabel("Keuntungan")
    st.pyplot(plt)

# Menampilkan halaman berdasarkan menu yang dipilih
if menu == "Stock Barang":
    halaman_stock_barang()
elif menu == "Penjualan":
    halaman_penjualan()
elif menu == "Supplier":
    halaman_supplier()
elif menu == "Owner":
    halaman_owner()

st.markdown('</div>', unsafe_allow_html=True)

# Save data when the app is closed or the menu is changed
save_data()
