import socket
import sqlite3
from datetime import datetime
import threading

# إنشاء قاعدة بيانات لحفظ الهجمات (للمناقشة: لشرح كيف نحلل البيانات لاحقاً)
def init_db():
    conn = sqlite3.connect('attacks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS incidents 
                 (id INTEGER PRIMARY KEY, ip TEXT, port INTEGER, time TEXT)''')
    conn.commit()
    conn.close()

def log_attack(ip, port):
    conn = sqlite3.connect('attacks.db')
    c = conn.cursor()
    c.execute("INSERT INTO incidents (ip, port, time) VALUES (?, ?, ?)",
              (ip, port, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def start_trap(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('0.0.0.0', port))
        server.listen(5)
        print(f"[*] Trap Active on Port: {port}")
        while True:
            client, addr = server.accept()
            log_attack(addr[0], port) # رصد الـ IP والمنفذ
            client.send(b"Access Denied. System Restricted.\n")
            client.close()
    except Exception as e:
        print(f"Error on port {port}: {e}")

if __name__ == "__main__":
    init_db()
    # مراقبة المنافذ الحساسة: 22 (SSH)، 80 (HTTP)، 23 (Telnet)
    for p in [22, 80, 23]:
        threading.Thread(target=start_trap, args=(p,)).start()
