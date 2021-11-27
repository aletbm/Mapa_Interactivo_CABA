import socket
from modelo import filtrar_data, wget
import ast
from observador import TemaConcreto, ConcreteObserverA

HOST = "localhost"  # Mi localhost
PORT = 4000  # > 1023
url = "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/oferta-gastronomica/oferta_gastronomica.csv"


def comunicacion(cliente, direccion):
    """
    

    Parameters
    ----------
    cliente : TYPE
        DESCRIPTION.
    direccion : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    tema1 = TemaConcreto()
    ConcreteObserverA(tema1)
    while True:
        try:
            position = cliente.recv(1024)
            position = ast.literal_eval(position.decode("utf-8")) #Verificar comportamiento
            opcion = cliente.recv(1024)  # Espero receibir 1024 bits
            lat = position["lat"]
            lng = position["long"]
            tema1.set_estado(lat, lng, direccion, opcion.decode("utf-8"))
            data = filtrar_data(opcion.decode("utf-8"), position)
            if data is False:
                break
            cliente.sendall(str(str(data).__sizeof__()).encode())  # Envio el tamaño de lo que voy a enviar
            cliente.sendall(str(data).encode())
        except:
            cliente.close()
            break


class Server:
    def __init__(self, host, port):
        """
        

        Parameters
        ----------
        host : TYPE
            DESCRIPTION.
        port : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.s.bind((host, port))
            self.s.listen()
        except OSError as error:
            print(error)
        return

    def accept(self):
        """
        

        Returns
        -------
        cliente : TYPE
            DESCRIPTION.
        direccion : TYPE
            DESCRIPTION.

        """
        cliente, direccion = self.s.accept()
        return cliente, direccion

    def close(self):
        self.s.close()
        return


if __name__ == '__main__':
    wget(url)
    sv = Server(HOST, PORT)
    while True:
        print(f"Escuchando por el puerto {PORT}...")
        cliente, direccion = sv.accept()
        print("Conexion entrante desde", direccion[0])
        comunicacion(cliente, direccion[0])
        print("Conexion cerrada para", direccion[0])
    sv.close()
