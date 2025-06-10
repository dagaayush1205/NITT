# File: imu_client_plot.py (Run this on your laptop)

import socket
import json
import matplotlib.pyplot as plt
from collections import deque

IP_OF_PI = "192.168.x.x"  # Replace with actual IP of Raspberry Pi
PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP_OF_PI, PORT))

plt.ion()
fig, axs = plt.subplots(2, 1, figsize=(8, 6))
accel_lines = [axs[0].plot([], [], label=axis)[0] for axis in ['Ax', 'Ay', 'Az']]
gyro_lines = [axs[1].plot([], [], label=axis)[0] for axis in ['Gx', 'Gy', 'Gz']]

for ax in axs:
    ax.legend()
    ax.set_xlim(0, 100)
    ax.set_ylim(-20000, 20000)
    ax.grid(True)

max_len = 100
x = deque(range(max_len), maxlen=max_len)
accel_data = [deque([0]*max_len, maxlen=max_len) for _ in range(3)]
gyro_data = [deque([0]*max_len, maxlen=max_len) for _ in range(3)]

try:
    buffer = ""
    while True:
        data = sock.recv(1024).decode()
        buffer += data
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            try:
                d = json.loads(line)
                for q, key in zip(accel_data, ['ax', 'ay', 'az']):
                    q.append(d[key])
                for q, key in zip(gyro_data, ['gx', 'gy', 'gz']):
                    q.append(d[key])

                for line, data in zip(accel_lines, accel_data):
                    line.set_ydata(data)
                    line.set_xdata(x)
                for line, data in zip(gyro_lines, gyro_data):
                    line.set_ydata(data)
                    line.set_xdata(x)

                for ax in axs:
                    ax.relim()
                    ax.autoscale_view()

                plt.draw()
                plt.pause(0.01)
            except json.JSONDecodeError:
                continue
except KeyboardInterrupt:
    print("Client closed.")
    sock.close()
    plt.ioff()
    plt.show()

