import os
import json
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_drive_service():
    """Menghubungkan ke Google Drive (Pintar mendeteksi Lokal vs Internet)"""
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/drive.metadata.readonly']
    
    try:
        creds = None
        
        # 1. CEK LOKAL: Cek apakah ada file fisik 'credentials.json' di laptop
        if os.path.exists('credentials.json'):
            creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
        
        # 2. CEK INTERNET: Jika file tidak ada, ambil dari brankas rahasia Streamlit Cloud
        elif "google_drive" in st.secrets:
            google_secrets = st.secrets["google_drive"].to_dict()
            creds = service_account.Credentials.from_service_account_info(google_secrets, scopes=SCOPES)
            
        elif "google_credentials" in st.secrets:
            try:
                creds_dict = json.loads(st.secrets["google_credentials"])
            except:
                creds_dict = st.secrets["google_credentials"].to_dict()
            creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
            
        else:
            st.error("Kunci rahasia Google Drive tidak ditemukan di Streamlit Cloud!")
            return None
            
        service = build('drive', 'v3', credentials=creds)
        return service
    
    except Exception as e:
        st.error(f"Error aslinya: {e}")
        st.error("Gagal terhubung ke Google Drive.")
        return None

def get_folder_id_by_name(service, folder_name):
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        return None
    return items[0]['id']

def get_pdfs_by_folder(service, folder_id):
    query = f"'{folder_id}' in parents and mimeType='application/pdf' and trashed=false"
    pdf_list = []
    page_token = None
    while True:
        results = service.files().list(
            q=query, 
            fields="nextPageToken, files(id, name)",
            pageToken=page_token,
            pageSize=1000
        ).execute()
        
        items = results.get('files', [])
        for item in items:
            pdf_list.append({
                'id': item['id'],
                'name': item['name'],
                'link': f"https://drive.google.com/file/d/{item['id']}/view"
            })
            
        page_token = results.get('nextPageToken')
        if not page_token:
            break
    return pdf_list