import socket, json, time, random

vehicle_id = input("Enter Vehicle ID: ")
server_ip = '127.0.0.1'
port = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_ip, port))

while True:
    data = {
        "id": vehicle_id,
        "speed": random.randint(20, 100),
        "location": [random.randint(0, 100), random.randint(0, 100)],
        "status": "OK"
    }
    sock.sendall(json.dumps(data).encode())
    print("Data sent:", data)
    time.sleep(2)