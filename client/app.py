import streamlit as st
import socket

# Menggunakan separator yang sama dengan server
SEPARATOR = b"<FILENAME_END>"

st.set_page_config(page_title="TCP File Sender", layout="centered")
st.title("📤 TCP File Transfer - Client")

# Input konfigurasi jaringan
host = st.text_input("IP Address Server Target", value="127.0.0.1")
port = st.number_input("Port Server Target", value=8000, step=1)
uploaded_file = st.file_uploader("Pilih file yang ingin dikirim")

if st.button("Kirim File", type="primary"):
    if uploaded_file is None:
        st.warning("Silakan pilih file terlebih dahulu.")
    else:
        try:
            filename = uploaded_file.name
            file_data = uploaded_file.read()

            # Inisialisasi socket TCP
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, int(port)))
            
            # Format paket data: nama_file + SEPARATOR + isi_file
            payload = filename.encode() + SEPARATOR + file_data
            s.sendall(payload)
            s.close()

            st.success(f"✅ File '{filename}' ({len(file_data):,} bytes) berhasil dikirim ke {host}:{int(port)}")
        except Exception as e:
            st.error(f"❌ Gagal mengirim file: {e}")