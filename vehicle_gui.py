import tkinter as tk
import socket
import threading
import time
import random
import json
from datetime import datetime

VEHICLE_ID = "Vehicle X"  # Change in each instance
SERVER_HOST = 'localhost'
SERVER_PORT = 9999

class VehicleClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{VEHICLE_ID} - V2V Client")
        self.root.geometry("300x250")
        self.root.config(bg="#eef2ff")

        self.speed = tk.StringVar()
        self.location = tk.StringVar()
        self.alert = tk.StringVar()

        tk.Label(root, text="🚗 V2V Vehicle Dashboard", font=("Helvetica", 14, "bold"), bg="#eef2ff").pack(pady=10)
        tk.Label(root, text=f"Vehicle ID: {VEHICLE_ID}", font=("Helvetica", 12), bg="#eef2ff").pack(pady=5)
        tk.Label(root, textvariable=self.speed, font=("Helvetica", 11), bg="#eef2ff").pack()
        tk.Label(root, textvariable=self.location, font=("Helvetica", 11), bg="#eef2ff").pack()
        tk.Label(root, textvariable=self.alert, font=("Helvetica", 12, "bold"), fg="red", bg="#eef2ff").pack(pady=10)

        threading.Thread(target=self.networking_thread, daemon=True).start()

    def networking_thread(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((SERVER_HOST, SERVER_PORT))
            print("✅ Connected to server!")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return

        while True:
            spd = random.randint(30, 120)
            x = random.randint(100, 500)
            y = random.randint(100, 500)
            timestamp = datetime.now().isoformat()

            self.speed.set(f"Speed: {spd} km/h")
            self.location.set(f"Location: ({x}, {y})")
            self.alert.set("⚠️ Over-speeding!" if spd > 100 else "")

            data = {
                "id": VEHICLE_ID,
                "speed": spd,
                "location": [x, y],
                "timestamp": timestamp
            }
            try:
                client.sendall(json.dumps(data).encode())
            except:
                print("❌ Lost connection to server")
                break
            time.sleep(2)

if __name__ == "__main__":
    root = tk.Tk()
    app = VehicleClientGUI(root)
    root.mainloop()