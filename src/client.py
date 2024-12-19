import json
import socket

HEADER = 64
HOST = '0.0.0.0'
PORT = 8080
FORMAT = 'utf-8'

# ฟังก์ชันส่งข้อมูล
def send(client, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

graph = {
    'node': ['1'],  
    'weight': 0,  
    'graph': {
        '1': {'2': 3, '3': 2, '4': 5},  
        '2': {'1': 3, '3': 1, '4': 5},  
        '3': {'1': 2, '2': 4, '4': 1},  
        '4': {'1': 5, '2': 3, '3': 4}   
    }
}

# ส่งข้อมูลไปยังแต่ละพอร์ตของ Node
for i in range(4):
    try:
        # เชื่อมต่อกับพอร์ตของ Node แต่ละตัว
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT + i))

        # กำหนด Node เริ่มต้น
        graph["node"] = [str(i + 1)]  # เปลี่ยน Node เริ่มต้นตามพอร์ต
        graph["weight"] = 0  # รีเซ็ตน้ำหนัก

        # ส่งข้อมูล
        send(client, json.dumps(graph))
    except Exception as e:
        print(f"Error connecting to Node {i+1}: {e}")
    finally:
        client.close()  
