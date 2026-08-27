import streamlit as st
import pandas as pd
from io import BytesIO
import streamlit_authenticator as stauth
from ui import (
    inject_tailwind_and_fonts,
    render_header,
    render_divider,
    render_metrics,
    render_sidebar_brand,
    render_stepper,
    render_user_profile,
)

# Memanggil fungsi layanan kita
from services.drive_service import get_drive_service, get_folder_id_by_name, get_pdfs_by_folder
from services.matching_service import match_data_row

# WAJIB DI PALING ATAS: Pengaturan halaman
st.set_page_config(page_title="Digitalisasi Arsip Akta Nikah KUA", page_icon="📖", layout="wide")

# ==========================================
# INISIALISASI STATE PELACAK PROGRESS
# ==========================================
# Ini harus diinisialisasi sebelum digunakan oleh UI
if 'current_step' not in st.session_state:
    st.session_state['current_step'] = 1

# ==========================================
# BAGIAN 1: LOGIKA KEAMANAN & LOGIN
# ==========================================
try:
    # Menggunakan metode bawaan Streamlit untuk mengubah data menjadi dictionary biasa
    # agar aman saat library mencoba mengubah status logout
    credentials = st.secrets["credentials"].to_dict()
    cookie = st.secrets["cookie"]
    preauthorized = st.secrets["preauthorized"]

    st.markdown(inject_tailwind_and_fonts(), unsafe_allow_html=True)

    # Mengaktifkan sistem login
    authenticator = stauth.Authenticate(
        credentials,
        cookie["name"],
        cookie["key"],
        cookie["expiry_days"],
        preauthorized
    )

    # Menampilkan form login (Versi terbaru 0.4.2 tidak mengembalikan variabel)
    authenticator.login()

    if st.session_state.get("authentication_status") == False:
        st.error('❌ Username atau password salah! Silakan coba lagi.')
    elif st.session_state.get("authentication_status") == None:
        st.info('🔒 Silakan masukkan username dan password untuk mengakses Arsip KUA.')
        
    # Jika Login Berhasil, tampilkan aplikasi utama:
    elif st.session_state.get("authentication_status") == True:
        
        # ==========================================
        # BAGIAN 2: APLIKASI UTAMA (Hanya tampil jika login)
        # ==========================================
        
        # Menambahkan tombol Logout di sidebar beserta sapaan
        authenticator.logout(location='sidebar')
        st.sidebar.markdown(render_sidebar_brand(), unsafe_allow_html=True)
        st.sidebar.markdown(render_user_profile(st.session_state["name"]), unsafe_allow_html=True)

        st.markdown(render_header(), unsafe_allow_html=True)

        st.sidebar.markdown('<p class="kua-sidebar-label">Panel kontrol</p>', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="kua-side-note">Unggah data Excel dan tentukan tahun folder untuk memulai pencarian arsip.</div>', unsafe_allow_html=True)

        # Menampilkan Stepper Dinamis dengan mengirimkan current_step
        st.markdown(render_stepper(st.session_state['current_step']), unsafe_allow_html=True)

        # Langkah 1: Upload dan Input Tahun
        st.markdown('<p class="kua-section-title">Langkah 1 · Upload data dan tentukan tahun</p><p class="kua-section-caption">Siapkan file Excel dan folder tahun yang akan dicari di Google Drive.</p>', unsafe_allow_html=True)
        st.markdown('<div class="kua-panel">', unsafe_allow_html=True)
        st.markdown('<div class="kua-panel-head"><div class="kua-step-badge">01</div><div><p class="kua-panel-title">Upload Data Excel</p><p class="kua-panel-copy">Gunakan file .xlsx berisi data akta nikah yang akan diproses.</p></div></div>', unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1], gap="large")

        with col1:
            uploaded_file = st.file_uploader("Upload File Excel", type=["xlsx"], help="Tarik file ke area ini atau pilih dari perangkat.")
        with col2:
            tahun_target = st.text_input("Tahun Target Folder", value="2018", help="Folder Google Drive akan dicari berdasarkan tahun yang dipilih.")
        st.markdown('</div>', unsafe_allow_html=True)

        if uploaded_file is not None:
            # Pemicu Langkah 2: Saat file berhasil masuk, state berubah ke Langkah 2
            st.session_state['current_step'] = 2

            try:
                df = pd.read_excel(uploaded_file)
                
                st.info(f"📊 Ditemukan **{len(df)} baris data** di dalam file Excel yang siap diproses.")
                
                st.markdown(render_divider(), unsafe_allow_html=True)
                
                # Langkah 2: Proses Pencocokan
                st.markdown('<p class="kua-section-title">Langkah 2 · Proses pencocokan otomatis</p><p class="kua-section-caption">Sistem akan mencocokkan data dengan arsip PDF pada folder Google Drive.</p>', unsafe_allow_html=True)
                
                if st.button("🚀 Mulai Proses Pencocokan", type="primary"):
                    if not tahun_target:
                        st.warning("Harap isi Tahun Target terlebih dahulu!")
                    else:
                        with st.spinner(f"Mencari folder '{tahun_target}' di Google Drive KUA..."):
                            service = get_drive_service()
                            if not service:
                                st.error("Gagal terhubung ke Google Drive. Periksa 'credentials.json'.")
                            else:
                                target_folder_id = get_folder_id_by_name(service, tahun_target)
                                
                                if not target_folder_id:
                                    st.error(f"❌ Folder '{tahun_target}' TIDAK DITEMUKAN di Google Drive KUA.")
                                else:
                                    st.success(f"✅ Folder '{tahun_target}' ditemukan secara otomatis!")
                                    
                                    with st.spinner(f"Memindai seluruh isi PDF di dalam folder {tahun_target}..."):
                                        pdf_list = get_pdfs_by_folder(service, target_folder_id)
                                    
                                    if len(pdf_list) > 0:
                                        st.info(f"📁 Berhasil mengumpulkan **{len(pdf_list)} file PDF** dari Google Drive.")
                                        
                                        with st.spinner("Sedang mencocokkan data..."):
                                            results_data = []
                                            
                                            for index, row in df.iterrows():
                                                match_res = match_data_row(row, pdf_list)
                                                
                                                row_dict = row.to_dict()
                                                row_dict['STATUS_MATCH'] = match_res['status']
                                                row_dict['FILE_PDF_DRIVE'] = match_res['pdf_name']
                                                row_dict['LINK_AKTA_GDRIVE'] = match_res['pdf_link']
                                                
                                                results_data.append(row_dict)
                                            
                                            result_df = pd.DataFrame(results_data)
                                            
                                            # Menggunakan garis miring DD/MM/YYYY
                                            for col in result_df.select_dtypes(include=['datetime64[ns]', 'datetime64']).columns:
                                                result_df[col] = result_df[col].dt.strftime('%d/%m/%Y')
                                                
                                            if 'TGLNIKAHMASEHI' in result_df.columns:
                                                try:
                                                    result_df['TGLNIKAHMASEHI'] = pd.to_datetime(result_df['TGLNIKAHMASEHI']).dt.strftime('%d/%m/%Y')
                                                except:
                                                    pass
                                            
                                            st.session_state['result_df'] = result_df
                                            
                                        # Pemicu Langkah 4: Saat semua proses berhasil dan tabel dirender
                                        st.session_state['current_step'] = 4
                                        # Paksa Streamlit untuk refresh halaman agar stepper ter-update seketika
                                        st.rerun() 

                                    else:
                                        st.warning(f"Folder '{tahun_target}' ditemukan, tetapi tidak ada file PDF di dalamnya.")
                
                # Langkah 3: Preview Hasil dan Download
                if 'result_df' in st.session_state:
                    res_df = st.session_state['result_df']
                    
                    st.markdown(render_divider(), unsafe_allow_html=True)
                    st.markdown('<p class="kua-section-title">Langkah 3 · Preview dan unduh</p><p class="kua-section-caption">Tinjau hasil pencocokan, lakukan penyesuaian bila diperlukan, lalu unduh laporan.</p>', unsafe_allow_html=True)
                    
                    # 1. Hitung angka dari dataframe res_df
                    tot_data = len(res_df)
                    tot_match = len(res_df[res_df['STATUS_MATCH'] == 'MATCHED'])
                    tot_notfound = len(res_df[res_df['STATUS_MATCH'] == 'NOT FOUND'])
                    tot_ambigu = len(res_df[res_df['STATUS_MATCH'] == 'AMBIGUOUS'])
                    
                    # 2. Kirim angkanya ke dalam fungsi desain Card di ui.py
                    st.markdown(render_metrics(tot_data, tot_match, tot_notfound, tot_ambigu), unsafe_allow_html=True)
                    
                    def color_status(val):
                        if val == 'MATCHED': return 'background-color: #d4edda; color: #155724;'
                        elif val == 'NOT FOUND': return 'background-color: #f8d7da; color: #721c24;'
                        elif val == 'AMBIGUOUS': return 'background-color: #fff3cd; color: #856404;'
                        return ''

                    edited_df = st.data_editor(
                        res_df.style.map(color_status, subset=['STATUS_MATCH']),
                        use_container_width=True,
                        height=400,
                    )
                    
                    st.write("<br>", unsafe_allow_html=True) 
                    
                    nama_file_kustom = st.text_input("📝 Jika hasil pratinjau sudah sesuai, beri nama file untuk menyimpannya:", value=f"Laporan_Hasil_Pencocokan_{tahun_target}.xlsx")
                    
                    if not nama_file_kustom.endswith(".xlsx"):
                        nama_file_kustom += ".xlsx"
                    
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        edited_df.to_excel(writer, index=False, sheet_name='Laporan_Akta')
                    processed_data = output.getvalue()
                    
                    st.download_button(
                        label=f"📥 Download Data Sekarang",
                        data=processed_data,
                        file_name=nama_file_kustom,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        type="primary"
                    )
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses data: {e}")
        
        else:
            # RESET Pemicu: Jika file dihapus dari uploader, kembalikan ke Langkah 1 
            # dan bersihkan data pencocokan yang tersimpan
            if st.session_state['current_step'] != 1:
                st.session_state['current_step'] = 1
                if 'result_df' in st.session_state:
                    del st.session_state['result_df']
                st.rerun()

except Exception as e:
    st.error(f"Error aslinya adalah: {e}")
    st.exception(e)