import struct
import time
from pymodbus.client import ModbusTcpClient

def read_modbus_data():
    # Konfigurasi koneksi Modbus
    modbus_host = "192.168.0.250"
    modbus_port = 504

    # Inisialisasi klien Modbus
    client = ModbusTcpClient(modbus_host, port=modbus_port)

    while True:
        # Coba koneksi ke server Modbus
        connection = client.connect()
        if connection:
            pass
        else:
            print("Koneksi gagal")
            break

        # Membaca 2 input register mulai dari address 24
        address = 3110
        count = 2  # Dibubah menjadi 2 untuk membaca dua register
        try:
            result = client.read_input_registers(address, count, slave=9)
            if not result.isError():
                # Gabungkan kedua register menjadi satu bilangan 32-bit (asumsi little endian)
                value_32bit = (result.registers[1] << 16) | result.registers[0]

                # Konversi ke Float32
                frequency = struct.unpack('<f', value_32bit.to_bytes(4, 'little'))[0]

                # Menampilkan data yang dibaca
                print(f"Frekuensi: {frequency} Hz")
            else:
                print(f"Gagal membaca data dari Modbus: {result}")
        except Exception as e:
            print(f"Exception: {e}")

        # Tutup koneksi
        client.close()

        # Tunggu selama 5 detik sebelum polling berikutnya
        time.sleep(5)

if __name__ == "__main__":
    read_modbus_data()