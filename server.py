import socket
import threading
import json

clients = []

def handle_client(conn, addr):
    print(f"🚗 New connection from {addr}")
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            try:
                vehicle_data = json.loads(data)
                print(f"[{vehicle_data['id']}] Speed: {vehicle_data['speed']} | Location: {vehicle_data['location']} | Status: {vehicle_data.get('status', 'N/A')}")
            except json.JSONDecodeError:
                print(f"❌ Received malformed data: {data}")
        except Exception as e:
            print(f"❌ Lost connection to {addr}: {e}")
            break

    clients.remove(conn)
    conn.close()

def start_server():
    host = '127.0.0.1'
    port = 9999
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"✅ Server is running on {host}:{port} (TCP)")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()

if __name__ == "__main__":
    start_server()