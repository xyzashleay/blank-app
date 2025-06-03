import streamlit as st
import pandas as pd
import os
from collections import Counter

# --- Configuration ---
FILE_PATH = "alumni_data (1).xlsx"
SHEET_NAME = 'Data ' # Ensure this matches your Excel sheet name

# --- Helper Functions ---
def format_currency(amount):
    """Format currency from number to Rupiah format"""
    if pd.isna(amount) or amount == '':
        return 'Tidak tersedia'
    try:
        if isinstance(amount, str) and amount.startswith('Rp'):
            return amount
        num_amount = int(float(amount))
        return f"Rp{num_amount:,}".replace(',', '.') + ",00"
    except ValueError:
        return str(amount) # Return as string if conversion fails

@st.cache_data
def load_data(file_path, sheet_name):
    """Load alumni data from Excel file or use sample data if not found."""
    try:
        if os.path.exists(file_path):
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            df['NPM'] = df['NPM'].astype(str)
            df['Angkatan'] = df['Angkatan'].astype(str)
            df['Tahun Lulus'] = df['Tahun Lulus'].astype(str)
            # Apply currency formatting. It's better to convert to numeric first if possible.
            df['Rata-rata Gaji'] = df['Rata-rata Gaji'].apply(lambda x: float(str(x).replace('Rp', '').replace('.', '').replace(',', '')) if isinstance(x, str) and x.startswith('Rp') else x)
            df['Rata-rata Gaji'] = df['Rata-rata Gaji'].apply(format_currency)
            return df
        else:
            sample_data = {
                'No': [1, 2, 3],
                'Nama': ['Sari Gita Fitri', 'Natasha Rosaline', 'Fadel Muhammad'],
                'NPM': ['1606829390', '1606889793', '1606824540'],
                'Program Studi': ['Matematika', 'Matematika', 'Matematika'],
                'Angkatan': ['2016', '2016', '2016'],
                'Peminatan': ['Matematika Komputasi', 'Matematika Komputasi', 'Matematika Komputasi'],
                'Judul Skripsi': [
                    'Implementasi Algoritma Kernel K-Means based Co-clustering untuk Memprediksi Penyakit Kanker Paru-paru',
                    'Fuzzy C-Means Clustering dengan Reduksi Dimensi Deep Autoencoders untuk Pendeteksian Topik pada Data Tekstual Twitter',
                    'Prediksi Insiden DBD di DKI Jakarta Menggunakan Radial Basis Function Neural Network'
                ],
                'Tahun Lulus': ['2020', '2020', '2020'],
                'Pekerjaan': ['Data Analyst', 'Senior Analyst Specialist System Infrastructure', 'Data Platform Engineer'],
                'Id Karyawan': ['KI202001', 'BC202049', 'BR202070'],
                'Nama Perusahaan': ['Kimbo', 'PT Bank Central Asia Tbk', 'PT Bank Raya Indonesia'],
                'Alamat Perusahaan': [
                    'Ruko Harco Mangga Dua, Jakarta',
                    'Menara BCA lantai LG. Jl. MH. Thamrin no. 1 Jakarta Pusat 10310',
                    'Jl. Jenderal Sudirman Kav.44-46, Jakarta 10210'
                ],
                'Rata-rata Gaji': [8000000, 15000000, 12000000]
            }
            df = pd.DataFrame(sample_data)
            df['Rata-rata Gaji'] = df['Rata-rata Gaji'].apply(format_currency)
            st.warning("File Excel tidak ditemukan. Menggunakan data contoh.")
            return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame() # Return empty DataFrame on error

# --- Pages ---

def welcome_page():
    """Displays the welcome page."""
    st.markdown(
        """
        <style>
        .stApp {
    background: linear-gradient(90deg, #ad0000, #441f1f);
    color: white;
        }
        .stButton button {
            background-color: white;
            color: #000000;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #e0e7ff;
        }
        .feature-card {
            background-color: #cc7676;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            height: 150px; /* Fixed height for cards */
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .feature-card h3 {
            color: #530808;
            margin-bottom: 10px;
        }
        .feature-card p {
            color: white;
            font-size: 14px;
            line-height: 1.5;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1 style='text-align: center; color: white; font-size: 50px;'>DATABASE ALUMNI S1<br>DEPARTEMEN MATEMATIKA FMIPA UI</h1>", unsafe_allow_html=True)
    st.markdown(
    """
    <p style='text-align: center; color: white; font-size: 25px; line-height: 1.25;'>
    Sistem informasi terintegrasi untuk mengelola data alumni S1<br>Matematika, Statistika, dan Ilmu Aktuaria FMIPA UI
    </p>
    """,
    unsafe_allow_html=True
    )

    st.markdown("---") # Horizontal line for separation

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <h3>📊 Data Alumni</h3>
                <p>Pencarian dan pengelolaan<br>data lengkap alumni</p>
            </div>
            """, unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <h3>🏢 Perusahaan</h3>
                <p>Analisis distribusi alumni<br>di berbagai perusahaan</p>
            </div>
            """, unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <h3>📈 Statistik</h3>
                <p>Laporan dan analisis<br>data karir alumni</p>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("---") # Horizontal line for separation
    st.write("") # Add some space

    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("Mulai Eksplorasi Data", key="start_button"):
        st.session_state.current_page = 'search'
        st.rerun() # Rerun to switch page
    st.markdown("</div>", unsafe_allow_html=True)


def search_page(alumni_data):
    """Displays the search and data page."""
    st.title("Database Alumni Matematika FMIPA UI")

    # Navigation buttons in the sidebar
    with st.sidebar:
        st.header("Navigasi")
        if st.button("🏠 Beranda", key="nav_home"):
            st.session_state.current_page = 'welcome'
            st.rerun()
        if st.button("📊 Statistik", key="nav_stats"):
            st.session_state.current_page = 'statistics'
            st.rerun()
        if st.button("➕ Tambah Data", key="nav_add"):
            st.session_state.current_page = 'add'
            st.rerun()

    st.subheader("🔍 Pencarian Alumni")

    # Search filters using Streamlit widgets
    col1, col2, col3 = st.columns(3)
    with col1:
        nama_filter = st.text_input("Nama:", key="nama_filter")
    with col2:
        program_studi_filter = st.selectbox("Program Studi:", ['', 'Matematika', 'Statistika', 'Ilmu Aktuaria'], key="program_studi_filter")
    with col3:
        npm_filter = st.text_input("NPM:", key="npm_filter")

    col4, col5, col6 = st.columns(3)
    with col4:
        pekerjaan_filter = st.text_input("Pekerjaan:", key="pekerjaan_filter")
    with col5:
        perusahaan_filter = st.text_input("Perusahaan:", key="perusahaan_filter")
    with col6:
        gaji_filter = st.text_input("Gaji:", help="Masukkan sebagian angka gaji (contoh: 8000000)", key="gaji_filter")

    if st.button("Hapus Semua Filter", key="clear_filters_button"):
        # Reset text inputs by clearing session state
        st.session_state.nama_filter = ""
        st.session_state.program_studi_filter = ""
        st.session_state.npm_filter = ""
        st.session_state.pekerjaan_filter = ""
        st.session_state.perusahaan_filter = ""
        st.session_state.gaji_filter = ""
        st.rerun() # Rerun to apply cleared filters

    filtered_data = alumni_data.copy()

    # Apply filters
    if nama_filter:
        filtered_data = filtered_data[filtered_data['Nama'].str.contains(nama_filter, case=False, na=False)]
    if program_studi_filter:
        filtered_data = filtered_data[filtered_data['Program Studi'].str.contains(program_studi_filter, case=False, na=False)]
    if npm_filter:
        filtered_data = filtered_data[filtered_data['NPM'].str.contains(npm_filter, na=False)]
    if pekerjaan_filter:
        filtered_data = filtered_data[filtered_data['Pekerjaan'].str.contains(pekerjaan_filter, case=False, na=False)]
    if perusahaan_filter:
        filtered_data = filtered_data[filtered_data['Nama Perusahaan'].str.contains(perusahaan_filter, case=False, na=False)]
    if gaji_filter:
        filtered_data = filtered_data[filtered_data['Rata-rata Gaji'].str.contains(gaji_filter, case=False, na=False)]

    st.subheader(f"Hasil Pencarian ({len(filtered_data)} alumni)")

    if not filtered_data.empty:
        # Display DataFrame
        st.dataframe(filtered_data[['Nama', 'NPM', 'Program Studi', 'Pekerjaan', 'Nama Perusahaan', 'Rata-rata Gaji']],
                     use_container_width=True,
                     hide_index=True)

        # Allow user to select a row for details
        selected_row_index = st.session_state.get('selected_row_index', None)
        selected_row_nama = st.session_state.get('selected_row_nama', None)

        # Create a dropdown for selecting an alumni
        alumni_names = filtered_data['Nama'].tolist()
        selected_name = st.selectbox("Pilih alumni untuk melihat detail:", [""] + alumni_names)

        if selected_name and selected_name != "":
            selected_alumni = filtered_data[filtered_data['Nama'] == selected_name].iloc[0]
            st.session_state.selected_alumni = selected_alumni
            st.session_state.selected_row_index = selected_alumni.name # Store index if needed
            st.session_state.selected_row_nama = selected_name
            st.session_state.current_page = 'detail'
            st.rerun()
    else:
        st.info("Tidak ada data alumni yang cocok dengan filter.")


def alumni_detail_page(alumni_data):
    """Displays detailed information for a selected alumni."""
    if 'selected_alumni' not in st.session_state or st.session_state.selected_alumni is None:
        st.warning("Tidak ada alumni yang dipilih. Silakan kembali ke halaman pencarian.")
        if st.button("← Kembali ke Pencarian"):
            st.session_state.current_page = 'search'
            st.rerun()
        return

    alumni = st.session_state.selected_alumni
    st.title(f"Detail Alumni - {alumni['Nama']}")

    # Navigation in the sidebar
    with st.sidebar:
        st.header("Navigasi")
        if st.button("← Kembali ke Pencarian", key="back_to_search"):
            st.session_state.current_page = 'search'
            st.rerun()

    st.subheader("👤 Informasi Alumni")
    st.write(f"**Nama:** {alumni['Nama']}")
    st.write(f"**NPM:** {alumni['NPM']}")

    st.subheader("📚 Riwayat Pendidikan")
    st.write(f"**Program Studi:** {alumni['Program Studi']}")
    st.write(f"**Peminatan:** {alumni['Peminatan']}")
    st.write(f"**Angkatan:** {alumni['Angkatan']}")
    st.write(f"**Tahun Lulus:** {alumni['Tahun Lulus']}")
    st.write(f"**Judul Skripsi:** {alumni['Judul Skripsi']}")

    st.subheader("💼 Informasi Karir")
    st.write(f"**Pekerjaan:** {alumni['Pekerjaan']}")
    st.write(f"**Perusahaan:** {alumni['Nama Perusahaan']}")
    st.write(f"**ID Karyawan:** {alumni['Id Karyawan']}")
    st.write(f"**Alamat Perusahaan:** {alumni['Alamat Perusahaan']}")
    st.write(f"**Rata-rata Gaji:** {alumni['Rata-rata Gaji']}")


def statistics_page(alumni_data):
    """Displays statistics page."""
    st.title("Statistik Alumni")

    # Navigation in the sidebar
    with st.sidebar:
        st.header("Navigasi")
        if st.button("← Kembali ke Pencarian", key="back_to_search_stats"):
            st.session_state.current_page = 'search'
            st.rerun()

    st.subheader("Ringkasan Data")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Total Alumni", value=len(alumni_data))
    with col2:
        unique_programs = alumni_data['Program Studi'].nunique()
        st.metric(label="Program Studi Unik", value=unique_programs)
    with col3:
        unique_companies = alumni_data['Nama Perusahaan'].nunique()
        st.metric(label="Perusahaan Unik", value=unique_companies)

    st.markdown("---")

    st.subheader("🏆 Top 3 Perusahaan Paling Populer")
    if not alumni_data.empty:
        company_counts = Counter(alumni_data['Nama Perusahaan'].dropna())
        top_companies = company_counts.most_common(3)

        medals = ['🥇', '🥈', '🥉']
        colors = ['#fbbf24', '#9ca3af', '#f97316']

        for i, (company, count) in enumerate(top_companies):
            col_icon, col_info, col_percent = st.columns([0.1, 0.6, 0.3])
            with col_icon:
                st.markdown(f"<h1 style='text-align: center; color: {colors[i]};'>{medals[i]}</h1>", unsafe_allow_html=True)
            with col_info:
                st.markdown(f"**{company}**")
                st.write(f"{count} alumni bekerja di sini")
            with col_percent:
                percentage = (count / len(alumni_data)) * 100
                st.markdown(f"<div style='background-color: {colors[i]}; color: white; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold;'>{percentage:.1f}%</div>", unsafe_allow_html=True)
    else:
        st.info("Tidak ada data alumni untuk menampilkan statistik perusahaan.")


def add_alumni_page():
    """Displays the form to add new alumni data."""
    st.title("Tambah Data Alumni Baru")

    # Navigation in the sidebar
    with st.sidebar:
        st.header("Navigasi")
        if st.button("← Kembali ke Pencarian", key="back_from_add"):
            st.session_state.current_page = 'search'
            st.rerun()

    # Form fields using Streamlit widgets
    with st.form("add_alumni_form"):
        st.subheader("Informasi Pribadi")
        nama = st.text_input("Nama:", key="form_nama")
        npm = st.text_input("NPM:", key="form_npm")
        program_studi = st.selectbox("Program Studi:", ['Matematika', 'Statistika', 'Ilmu Aktuaria'], key="form_program_studi")
        angkatan = st.text_input("Angkatan:", key="form_angkatan")
        peminatan = st.text_input("Peminatan:", key="form_peminatan")
        judul_skripsi = st.text_area("Judul Skripsi:", key="form_judul_skripsi")
        tahun_lulus = st.text_input("Tahun Lulus:", key="form_tahun_lulus")

        st.subheader("Informasi Karir")
        pekerjaan = st.text_input("Pekerjaan:", key="form_pekerjaan")
        id_karyawan = st.text_input("Id Karyawan:", key="form_id_karyawan")
        nama_perusahaan = st.text_input("Nama Perusahaan:", key="form_nama_perusahaan")
        alamat_perusahaan = st.text_area("Alamat Perusahaan:", key="form_alamat_perusahaan")
        rata_rata_gaji = st.text_input("Rata-rata Gaji (contoh: 8000000):", help="Masukkan angka saja, contoh: 8000000", key="form_rata_rata_gaji")

        submitted = st.form_submit_button("Simpan Data")

        if submitted:
            # Validate required fields
            required_fields = {'Nama': nama, 'NPM': npm, 'Program Studi': program_studi}
            for field_name, field_value in required_fields.items():
                if not field_value.strip():
                    st.error(f"Field **{field_name}** harus diisi!")
                    return

            # Format salary
            formatted_gaji = ""
            if rata_rata_gaji:
                try:
                    gaji_num = int(rata_rata_gaji.replace('.', '').replace(',', ''))
                    formatted_gaji = format_currency(gaji_num)
                except ValueError:
                    if not rata_rata_gaji.startswith('Rp'):
                        st.error("Format gaji tidak valid! Masukkan angka saja.")
                        return
                    formatted_gaji = rata_rata_gaji # If already in Rp format, keep it

            new_alumni = {
                'No': len(st.session_state.alumni_data) + 1,
                'Nama': nama,
                'NPM': npm,
                'Program Studi': program_studi,
                'Angkatan': angkatan,
                'Peminatan': peminatan,
                'Judul Skripsi': judul_skripsi,
                'Tahun Lulus': tahun_lulus,
                'Pekerjaan': pekerjaan,
                'Id Karyawan': id_karyawan,
                'Nama Perusahaan': nama_perusahaan,
                'Alamat Perusahaan': alamat_perusahaan,
                'Rata-rata Gaji': formatted_gaji
            }

            # Add to dataframe (using session state to persist data)
            new_row_df = pd.DataFrame([new_alumni])
            st.session_state.alumni_data = pd.concat([st.session_state.alumni_data, new_row_df], ignore_index=True)

            st.success("Data alumni berhasil ditambahkan!")
            st.session_state.current_page = 'search'
            st.rerun() # Rerun to show updated search page

# --- Main Application Logic ---
def main():
    st.set_page_config(layout="wide", page_title="Database Alumni Matematika FMIPA UI")

    # Initialize session state for data and current page if not already set
    if 'alumni_data' not in st.session_state:
        st.session_state.alumni_data = load_data(FILE_PATH, SHEET_NAME)

    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'welcome'

    # Route based on current page
    if st.session_state.current_page == 'welcome':
        welcome_page()
    elif st.session_state.current_page == 'search':
        search_page(st.session_state.alumni_data)
    elif st.session_state.current_page == 'detail':
        alumni_detail_page(st.session_state.alumni_data)
    elif st.session_state.current_page == 'statistics':
        statistics_page(st.session_state.alumni_data)
    elif st.session_state.current_page == 'add':
        add_alumni_page()

if __name__ == "__main__":
    main()
