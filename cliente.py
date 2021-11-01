import socket
import pandas as pd
import ast
from ubicaciones_c import add_markers, draw_mapa
from viewer import MyApp
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRunnable, QThreadPool
import sys

HOST = "127.0.0.1"  # Mi localhost
PORT = 2000  # Mismo puerto que el del servidor


def comunicacion(clt, opcion):
    clt.send(bytearray(opcion, encoding="utf-8"))
    data = clt.recv(1024)  # 1024 son la cantidad de bits que espero recibir
    df_dict = clt.recv(int(data.decode())).decode()
    df_dict = ast.literal_eval(df_dict.replace("nan", '""'))
    df = pd.DataFrame.from_dict(df_dict)
    return df


class Cliente:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.s.connect((self.host, self.port))
        return

    def send(self, data):
        self.s.sendall(data)

    def recv(self, size):
        return self.s.recv(size)

    def close(self):
        self.s.close()
        return


class Menu:
    def __init__(self):
        self.miposicion = {"lat": -34.601614, "long": -58.409270}
        lista = [
            "RESTAURANTE",
            "CAFE",
            "BAR",
            "CONFITERIA",
            "PUB",
            "VINERIA",
            "SANDWICHERIA",
            "DELIVERY & TAKE AWAY",
        ]
        print("Buscar establecimiento gastronomico")
        print("")
        for i, cat in enumerate(lista):
            print(f"{i+1} - {cat}")
        # print("9 - SALIR")
        print("")
        self.opcion = str(input("Ingrese una opcion--> "))


class Runnable(QRunnable):
    def __init__(self, mapa, myApp):
        super(Runnable, self).__init__()
        self.mapa = mapa
        self.refresh = myApp.update

    def run(self):
        app = QApplication.instance()
        clt = Cliente(HOST, PORT)
        clt.connect()
        while True:
            menu = Menu()
            df = comunicacion(clt, menu.opcion)
            self.mapa = draw_mapa(menu.miposicion, "user")
            add_markers(
                self.mapa,
                df,
                "nombre",
                "direccion_completa",
                "glyphicon-cutlery",
                "orange",
            )
            self.mapa.save("./mapa.html")
            self.refresh.emit()
        # app.quit()


centro_mapa = {"lat": -34.5983, "long": -58.4533}
mapa = draw_mapa(centro_mapa, zoom=13)
if QApplication.instance() is None:
    app = QApplication(sys.argv)
    myApp = MyApp(mapa)
    myApp.show()
    runnable = Runnable(mapa, myApp)
    QThreadPool.globalInstance().start(runnable)
    app.exec_()
