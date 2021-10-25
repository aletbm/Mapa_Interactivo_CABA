import socket

HOST = "127.0.0.1"  # Mi localhost
PORT = 2000  # > 1023

with socket.socket(
    socket.AF_INET, socket.SOCK_STREAM
) as s:  # AF_INET(IPv4), SOCK_STREAM (Indica TCP Socket, espera confirmacion de dato rrecibido) o puede ser SOCK_DGRAM (Indica UDP Socket tranmision de datos estilo Spotify, no espera confirmacion de dato recibido  por ende mayor velocidad de transmision)
    s.bind((HOST, PORT))
    s.listen()
    conexion, direccion = s.accept()
    with conexion:
        print("Conexion desde", direccion[0])
        while True:
            data = conexion.recv(1024)  # Espero receibir 1024 bits
            if not data:
                break
            print(data)
            conexion.sendall(data)  # Envio lo que recibi
