
import socket
import json
import matplotlib.pyplot as plt
from collections import deque

PI_IP = "192.168.x.x"  # 🛑 Replace with your Raspberry Pi IP
PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((PI_IP, PORT))
print("[INFO] Connected to Raspberry Pi")

plt.ion()
fig, ax = plt.subplots()
line_roll, = ax.plot([], [], label='Roll (°)')
line_pitch, = ax.plot([], [], label='Pitch (°)')
ax.set_xlim(0, 100)
ax.set_ylim(-90, 90)
ax.legend()
ax.grid(True)

x_vals = deque(maxlen=100)
roll_vals = deque(maxlen=100)
pitch_vals = deque(maxlen=100)
index = 0
buffer = ""

try:
    while True:
        data = sock.recv(1024).decode()
        buffer += data
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            try:
                angles = json.loads(line)
                roll_vals.append(angles['roll'])
                pitch_vals.append(angles['pitch'])
                x_vals.append(index)
                index += 1

                line_roll.set_data(x_vals, roll_vals)
                line_pitch.set_data(x_vals, pitch_vals)
                ax.set_xlim(max(0, index - 100), index)

                plt.draw()
                plt.pause(0.01)

            except json.JSONDecodeError:
                continue

except KeyboardInterrupt:
    print("Exiting client.")
    sock.close()
    plt.ioff()
    plt.show()

