import socket
import threading
import tkinter as tk
import json
import math
from datetime import datetime

HOST = '127.0.0.1'
PORT = 9999
COLLISION_DISTANCE = 30
VEHICLE_RADIUS = 10

vehicles = {}
log_file = "collision_log.txt"

class V2VDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("🚦 V2V Unified Dashboard")
        self.root.geometry("650x600")

        self.canvas = tk.Canvas(root, width=600, height=500, bg="white")
        self.canvas.pack(pady=10)

        self.alerts = tk.StringVar()
        tk.Label(root, textvariable=self.alerts, font=("Helvetica", 12), fg="red").pack()

        self.update_gui()

    def update_gui(self):
        self.canvas.delete("all")
        alerts = []

        vehicle_ids = list(vehicles.keys())
        for vid in vehicle_ids:
            v = vehicles[vid]
            x, y = v['location']
            color = "red" if v.get("brake") else "green"

            self.canvas.create_oval(x - VEHICLE_RADIUS, y - VEHICLE_RADIUS,
                                    x + VEHICLE_RADIUS, y + VEHICLE_RADIUS,
                                    fill=color)
            self.canvas.create_text(x, y - 15, text=vid, fill="black")
            self.canvas.create_text(x, y + 15, text=f"{v['speed']} km/h", fill="blue")

        for i in range(len(vehicle_ids)):
            for j in range(i + 1, len(vehicle_ids)):
                v1 = vehicles[vehicle_ids[i]]
                v2 = vehicles[vehicle_ids[j]]
                dist = math.dist(v1["location"], v2["location"])
                if dist < COLLISION_DISTANCE:
                    alert = f"⚠️ COLLISION RISK: {vehicle_ids[i]} & {vehicle_ids[j]}"
                    alerts.append(alert)
                    with open(log_file, "a") as f:
                        f.write(f"{datetime.now()} - {alert}\n")

        for vid in vehicle_ids:
            if vehicles[vid].get("brake"):
                alerts.append(f"🛑 {vid} is braking")

        self.alerts.set("\n".join(alerts) if alerts else "✅ All vehicles safe")
        self.root.after(1000, self.update_gui)

def start_socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"✅ Unified Dashboard Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

def handle_client(conn):
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            vehicle_data = json.loads(data)
            vehicles[vehicle_data["id"]] = {
                "speed": vehicle_data["speed"],
                "location": vehicle_data["location"],
                "brake": vehicle_data.get("brake", False)
            }
        except:
            break
    conn.close()

if __name__ == "__main__":
    threading.Thread(target=start_socket_server, daemon=True).start()
    root = tk.Tk()
    app = V2VDashboard(root)
    root.mainloop()