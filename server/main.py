import socket
import sys

SEPARATOR = b"<FILENAME_END>"
PORT = 8000
HOST = "0.0.0.0"

def start_server():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        srv.bind((HOST, PORT))
        srv.listen(5)
        print(f"🟢 Server aktif dan mendengarkan di port {PORT}...")
        print("💡 Tekan Ctrl + C untuk menghentikan server.\n")
    except Exception as e:
        print(f"❌ Gagal mengaktifkan server: {e}")
        sys.exit(1)

    try:
        while True:
            print("⏳ Menunggu koneksi masuk...")
            conn, addr = srv.accept()
            print(f"🤝 Terhubung dengan client dari: {addr}")

            raw = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                raw += chunk
            
            conn.close()
            print(f"📦 Data selesai diunduh ({len(raw):,} bytes). Memproses file...")

            # Validasi separator data
            if SEPARATOR not in raw:
                print("❌ Error: Format data tidak valid (separator tidak ditemukan).\n")
                continue

            # Pemisahan nama file dan isi
            filename_bytes, file_data = raw.split(SEPARATOR, 1)
            filename = filename_bytes.decode()

            # Menyimpan file ke direktori saat ini
            with open(filename, "wb") as f:
                f.write(file_data)

            print(f"✅ Sukses: File '{filename}' berhasil disimpan!\n")

    except KeyboardInterrupt:
        print("\n🛑 Server dihentikan oleh pengguna.")
    finally:
        srv.close()

if __name__ == "__main__":
    start_server()