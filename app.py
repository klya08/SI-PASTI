import streamlit as st
import pandas as pd
from io import BytesIO
import time 
import base64 
import os 
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

from services.drive_service import get_drive_service, get_folder_id_by_name, get_pdfs_by_folder
from services.matching_service import match_data_row

st.set_page_config(page_title="Digitalisasi Arsip Akta Nikah KUA", page_icon="📖", layout="wide")

img_base64 = ""
if os.path.exists("logo_sipasti.png"):
    with open("logo_sipasti.png", "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

if 'current_step' not in st.session_state:
    st.session_state['current_step'] = 1

try:
    credentials = st.secrets["credentials"].to_dict()
    cookie = st.secrets["cookie"]
    preauthorized = st.secrets["preauthorized"]

    st.markdown(inject_tailwind_and_fonts(), unsafe_allow_html=True)

    authenticator = stauth.Authenticate(
        credentials,
        cookie["name"],
        cookie["key"],
        cookie["expiry_days"],
        preauthorized
    )

    # ==========================================
    # HALAMAN LOGIN
    # ==========================================
    if not st.session_state.get("authentication_status"):
        # KUNCI PERBAIKAN: Mengurung form login di dalam container kosong
        login_container = st.empty()
        with login_container.container():
            col_kiri, col_tengah, col_kanan = st.columns([1, 1.5, 1])
            
            with col_tengah:
                img_tag = f'<img src="data:image/png;base64,{img_base64}" width="125" style="margin-bottom: -30px; position: relative; z-index: 1;">' if img_base64 else ""
                
                st.markdown(f"""<div style='text-align: center; margin-top: 5px; margin-bottom: 12px;'>
{img_tag}
<h2 style='font-weight: 800; font-size: 28px; color: #064e3b; margin-top: 0px; margin-bottom: 2px; letter-spacing: 1.5px; position: relative; z-index: 2;'>SI-PASTI</h2>
<p style='color: #6b7280; font-size: 13px; font-weight: 600; margin-top: 0px; margin-bottom: 0px; letter-spacing: 0.5px;'>Digitalisasi Arsip Akta Nikah KUA</p>
</div>""", unsafe_allow_html=True)
                
                authenticator.login()

                if st.session_state.get("authentication_status") == False:
                    st.error('❌ Username atau password salah! Silakan coba lagi.')
                elif st.session_state.get("authentication_status") == None:
                    st.info('🔒 Silakan masukkan username dan password untuk mengakses Arsip KUA.')
        
        # JIKA status tiba-tiba jadi True karena "Cookie" tanpa memuat ulang halaman,
        # kita hapus kontainer logonya dan paksa halaman untuk merender ulang!
        if st.session_state.get("authentication_status") == True:
            login_container.empty()
            st.rerun()
            
    # ==========================================
    # HALAMAN DASHBOARD UTAMA
    # ==========================================
    if st.session_state.get("authentication_status") == True:
        
        if 'has_logged_in' not in st.session_state:
            loading_html = f"""<style>
.fifa-loader-overlay {{ position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: #050a07; z-index: 999999; display: flex; flex-direction: column; justify-content: center; align-items: center; animation: fadeOutOverlay 0.5s ease-in-out 2.5s forwards; }}
.fifa-logo {{ width: 130px; animation: pulse-glow 1.5s infinite alternate ease-in-out; }}
.fifa-text {{ color: #10b981; margin-top: 35px; font-size: 13px; font-weight: 800; letter-spacing: 4px; animation: pulse-text 1.5s infinite alternate ease-in-out; }}
@keyframes pulse-glow {{ 0% {{ transform: scale(0.9); filter: drop-shadow(0 0 5px #064e3b); opacity: 0.7; }} 100% {{ transform: scale(1.1); filter: drop-shadow(0 0 25px #10b981); opacity: 1; }} }}
@keyframes pulse-text {{ 0% {{ opacity: 0.3; }} 100% {{ opacity: 1; filter: drop-shadow(0 0 5px #10b981); }} }}
@keyframes fadeOutOverlay {{ 0% {{ opacity: 1; visibility: visible; }} 100% {{ opacity: 0; visibility: hidden; pointer-events: none; }} }}
</style>
<div class="fifa-loader-overlay">
<img src="data:image/png;base64,{img_base64}" class="fifa-logo">
<div class="fifa-text">MENGAMANKAN KONEKSI...</div>
</div>"""
            st.markdown(loading_html, unsafe_allow_html=True)
            st.session_state['has_logged_in'] = True

        authenticator.logout(location='sidebar')
        st.sidebar.markdown(render_sidebar_brand(), unsafe_allow_html=True)
        st.sidebar.markdown(render_user_profile(st.session_state["name"]), unsafe_allow_html=True)
        
        st.sidebar.markdown('<p class="kua-sidebar-label">Panel kontrol</p>', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="kua-side-note">Unggah data Excel dan tentukan tahun folder untuk memulai pencarian arsip.</div>', unsafe_allow_html=True)

        st.markdown(render_header(img_base64), unsafe_allow_html=True)
        st.markdown(render_stepper(st.session_state['current_step']), unsafe_allow_html=True)

        # --- LANGKAH 1 ---
        st.markdown("""<div class="section-wrapper">
<div class="section-header">
<h2 class="section-title">
<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
Langkah 1 · Upload Data Excel
</h2>
<p class="section-caption">Siapkan file Excel dan tentukan folder tahun yang akan dicari di Google Drive.</p>
</div>""", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1], gap="large")

        with col1:
            uploaded_file = st.file_uploader("Pilih file Excel", type=["xlsx"], help="Tarik file ke area ini atau pilih dari perangkat.")
        with col2:
            tahun_target = st.text_input("Tahun Target Folder", value="2018", help="Folder Google Drive akan dicari berdasarkan tahun yang dipilih.")
            
        st.markdown('</div>', unsafe_allow_html=True)

        if uploaded_file is not None:
            st.session_state['current_step'] = 2

            try:
                df = pd.read_excel(uploaded_file)
                st.info(f"📊 Ditemukan **{len(df)} baris data** di dalam file Excel yang siap diproses.")
                
                # --- LANGKAH 2 ---
                st.markdown("""<div class="section-wrapper">
<div class="section-header">
<h2 class="section-title">
<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
Langkah 2 · Proses Pencocokan
</h2>
<p class="section-caption">Sistem akan mencocokkan data dengan arsip PDF secara otomatis pada folder yang dipilih.</p>
</div>""", unsafe_allow_html=True)
                
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
                                            
                                            for col in result_df.select_dtypes(include=['datetime64[ns]', 'datetime64']).columns:
                                                result_df[col] = result_df[col].dt.strftime('%d/%m/%Y')
                                                
                                            if 'TGLNIKAHMASEHI' in result_df.columns:
                                                try:
                                                    result_df['TGLNIKAHMASEHI'] = pd.to_datetime(result_df['TGLNIKAHMASEHI']).dt.strftime('%d/%m/%Y')
                                                except:
                                                    pass
                                            
                                            st.session_state['result_df'] = result_df
                                            
                                        st.session_state['current_step'] = 4
                                        st.rerun() 
                                    else:
                                        st.warning(f"Folder '{tahun_target}' ditemukan, tetapi tidak ada file PDF di dalamnya.")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # --- LANGKAH 3 ---
                if 'result_df' in st.session_state:
                    res_df = st.session_state['result_df']
                    
                    st.markdown("""<div class="section-wrapper">
<div class="section-header">
<h2 class="section-title">
<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
Langkah 3 · Review dan Unduh
</h2>
<p class="section-caption">Tinjau hasil pencocokan di bawah, lakukan penyesuaian bila diperlukan, lalu unduh laporannya.</p>
</div>""", unsafe_allow_html=True)
                    
                    tot_data = len(res_df)
                    tot_match = len(res_df[res_df['STATUS_MATCH'] == 'MATCHED'])
                    tot_notfound = len(res_df[res_df['STATUS_MATCH'] == 'NOT FOUND'])
                    tot_ambigu = len(res_df[res_df['STATUS_MATCH'] == 'AMBIGUOUS'])
                    
                    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                    col_m1.metric("Total Data", tot_data)
                    col_m2.metric("Matched", tot_match)
                    col_m3.metric("Not Found", tot_notfound)
                    col_m4.metric("Ambiguous", tot_ambigu)
                    
                    def color_status(val):
                        if val == 'MATCHED': return 'background-color: #ecfdf5; color: #064e3b;'
                        elif val == 'NOT FOUND': return 'background-color: #fef2f2; color: #991b1b;'
                        elif val == 'AMBIGUOUS': return 'background-color: #fffbeb; color: #92400e;'
                        return ''

                    edited_df = st.data_editor(
                        res_df.style.map(color_status, subset=['STATUS_MATCH']),
                        use_container_width=True,
                        height=400,
                    )
                    
                    st.write("<br>", unsafe_allow_html=True) 
                    
                    nama_file_kustom = st.text_input("Nama File Laporan (Tanpa spasi dianjurkan):", value=f"Laporan_Hasil_Pencocokan_{tahun_target}.xlsx")
                    if not nama_file_kustom.endswith(".xlsx"):
                        nama_file_kustom += ".xlsx"
                    
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        edited_df.to_excel(writer, index=False, sheet_name='Laporan_Akta')
                    processed_data = output.getvalue()
                    
                    st.download_button(
                        label=f"📥 Download Laporan Final",
                        data=processed_data,
                        file_name=nama_file_kustom,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        type="primary"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses data: {e}")
        
        else:
            if st.session_state['current_step'] != 1:
                st.session_state['current_step'] = 1
                if 'result_df' in st.session_state:
                    del st.session_state['result_df']
                st.rerun()

except Exception as e:
    st.error(f"Error aslinya adalah: {e}")
    st.exception(e)