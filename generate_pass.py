import streamlit_authenticator as stauth

# 1. Kita harus membuat dictionary kosong dulu yang struktur kuncinya mirip dengan isi secrets.toml nanti
credentials = {
    'usernames': {
        'admin_kua': {
            'email': 'admin@kua.com',
            'name': 'Petugas KUA',
            'password': 'rahasia123' # <-- GANTI DENGAN PASSWORD ASLI DI SINI
        }
    }
}

# 2. Fungsi Hasher yang baru akan otomatis membaca dictionary tersebut, 
# menghash passwordnya, dan memasukkan hasil hash-nya ke dictionary yang sama.
stauth.Hasher.hash_passwords(credentials)

print("$2b$12$30aC.WZlwscH1OF7H8TFHOIzgk/WzdXeqP6dR8c2/V0q76q7IMhq2:")
# 3. Kita ambil password yang sudah di-hash dari dalam dictionary
print(credentials['usernames']['admin_kua']['password'])