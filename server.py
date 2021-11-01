import socket
from ubicaciones_s import filtrar_data

HOST = "127.0.0.1"  # Mi localhost
PORT = 2000  # > 1023


def comunicacion(cliente):
    data = cliente.recv(1024)  # Espero receibir 1024 bits
    data = filtrar_data(data.decode("utf-8"))
    cliente.sendall(
        str(str(data).__sizeof__()).encode()
    )  # Envio el tamaño de lo que voy a enviar
    cliente.sendall(str(data).encode())


class Server:
    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.s.bind((host, port))
            self.s.listen()
            print(f"Escuchando por el puerto {PORT}...")
        except OSError as error:
            print(error)
        return

    def accept(self):
        cliente, direccion = self.s.accept()
        return cliente, direccion

    def close(self):
        self.s.close()
        return


sv = Server(HOST, PORT)
cliente, direccion = sv.accept()
print("Conexion entrante desde", direccion[0])
while True:
    comunicacion(cliente)
sv.close()
