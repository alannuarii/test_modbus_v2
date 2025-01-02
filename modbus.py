import struct
import time
from pymodbus.client import ModbusTcpClient

def read_modbus_data():
    # Konfigurasi koneksi Modbus
    modbus_host = "192.168.0.250"
    modbus_port = 504

    # Inisialisasi klien Modbus
    client = ModbusTcpClient(modbus_host, port=modbus_port)

    try:
        if not client.connect():
            print("Koneksi gagal ke server Modbus.")
            return

        print("Koneksi berhasil. Memulai pembacaan data...")

        while True:
            # Membaca 2 holding register mulai dari address 3110
            address = 3058
            count = 2
            unit = 9  # Slave ID

            try:
                result = client.read_holding_registers(address, count, slave=unit)
                print(f"Data register: {result.registers}")

                if not result.isError() and result.registers:
                    # Gabungkan kedua register menjadi satu bilangan 32-bit (asumsi little endian)
                    value_32bit = (result.registers[1] << 16) | result.registers[0]

                    # Konversi ke Float32
                    tot_active_pwr = struct.unpack('<f', value_32bit.to_bytes(4, 'little'))[0]

                    # Menampilkan data yang dibaca
                    print(f"Total Active Power: {tot_active_pwr} kW")
                else:
                    print(f"Gagal membaca data dari Modbus: {result}")
            except Exception as e:
                print(f"Exception saat membaca data: {e}")
                break

            # Tunggu selama 5 detik sebelum polling berikutnya
            time.sleep(1)
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        client.close()
        print("Koneksi ditutup.")

if __name__ == "__main__":
    read_modbus_data()
