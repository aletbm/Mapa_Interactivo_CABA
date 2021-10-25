import socket

HOST = "127.0.0.1"  # Mi localhost
PORT = 2000  # Mismo puerto que el del servidor

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hola Mundo!")
    data = s.recv(1024)  # 1024 son la cantidad de bits que espero recibir

print("Recibido", repr(data))
