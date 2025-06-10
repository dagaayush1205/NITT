# File: imu_server.py (Run this on Raspberry Pi)

import socket
import smbus2
import time
import json

# MPU6050 setup
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

bus = smbus2.SMBus(1)
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

def read_word(reg):
    high = bus.read_byte_data(MPU6050_ADDR, reg)
    low = bus.read_byte_data(MPU6050_ADDR, reg + 1)
    val = (high << 8) + low
    return val - 65536 if val > 32767 else val

# TCP server
HOST = '0.0.0.0'
PORT = 5005
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"[INFO] Waiting for connection on {HOST}:{PORT}...")

conn, addr = server_socket.accept()
print(f"[INFO] Connected by {addr}")

try:
    while True:
        data = {
            'ax': read_word(ACCEL_XOUT_H),
            'ay': read_word(ACCEL_XOUT_H + 2),
            'az': read_word(ACCEL_XOUT_H + 4),
            'gx': read_word(GYRO_XOUT_H),
            'gy': read_word(GYRO_XOUT_H + 2),
            'gz': read_word(GYRO_XOUT_H + 4)
        }
        conn.sendall((json.dumps(data) + "\n").encode())
        time.sleep(0.05)  # ~20 Hz
except KeyboardInterrupt:
    print("Stopping server...")
finally:
    conn.close()
    server_socket.close()

