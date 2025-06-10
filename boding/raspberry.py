
import socket
import smbus2
import time
import math
import json

# MPU6050 setup
MPU_ADDR = 0x68
bus = smbus2.SMBus(1)
bus.write_byte_data(MPU_ADDR, 0x6B, 0)  # Wake up MPU6050

def read_word(reg):
    high = bus.read_byte_data(MPU_ADDR, reg)
    low = bus.read_byte_data(MPU_ADDR, reg + 1)
    val = (high << 8) + low
    return val - 65536 if val > 32767 else val

def get_accel():
    ax = read_word(0x3B) / 16384.0
    ay = read_word(0x3D) / 16384.0
    az = read_word(0x3F) / 16384.0
    return ax, ay, az

def get_gyro():
    gx = read_word(0x43) / 131.0
    gy = read_word(0x45) / 131.0
    gz = read_word(0x47) / 131.0
    return gx, gy, gz

# Complementary filter
alpha = 0.98
dt = 0.01
pitch, roll = 0.0, 0.0

# TCP server
HOST = '0.0.0.0'
PORT = 5005
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print(f"[INFO] Waiting for connection on {HOST}:{PORT}...")
conn, addr = s.accept()
print(f"[INFO] Connected by {addr}")

try:
    while True:
        ax, ay, az = get_accel()
        gx, gy, gz = get_gyro()

        accel_roll = math.atan2(ay, az) * 180 / math.pi
        accel_pitch = math.atan2(-ax, math.sqrt(ay*ay + az*az)) * 180 / math.pi

        roll = alpha * (roll + gx * dt) + (1 - alpha) * accel_roll
        pitch = alpha * (pitch + gy * dt) + (1 - alpha) * accel_pitch

        msg = json.dumps({"roll": roll, "pitch": pitch}) + "\n"
        conn.sendall(msg.encode())
        time.sleep(dt)

except KeyboardInterrupt:
    print("Stopping server...")

finally:
    conn.close()
    s.close()

