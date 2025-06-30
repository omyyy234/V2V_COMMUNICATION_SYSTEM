# 🚦 V2V Communication System (Corrected Version)

This project simulates a Vehicle-to-Vehicle (V2V) communication system using TCP sockets and real-time visualization with Tkinter.

## 🗂 Contents

- `server.py`: Main TCP server that receives data from all vehicle clients.
- `vehicle_client.py`: CLI-based vehicle simulator that sends random speed and location data.
- `vehicle_gui.py`: GUI-based client showing speed, location, and alerts.
- `README.md`: Instructions to run the project.

## 🚀 How to Run

### 1. Start the Server

```bash
python server.py
```

### 2. Launch Vehicle Clients

#### CLI Version:

```bash
python vehicle_client.py
```

> Enter a unique Vehicle ID when prompted.

#### GUI Version:

```bash
python vehicle_gui.py
```

> Change the `VEHICLE_ID` value in the file to simulate multiple vehicles.

### 3. Monitor the Console

- The server logs incoming vehicle data.
- GUI clients show local vehicle status.

## 📌 Notes

- All components run locally using `127.0.0.1:9999`.
- JSON format is used for data exchange.
- GUI sends alert if speed > 100 km/h.

---

Built with ❤️ for V2V simulation!