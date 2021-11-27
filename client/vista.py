import socket
import pandas as pd ## tambien pip install openpyxl
import ast
from viewer import add_markers, draw_mapa
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QRunnable
import os
import webbrowser
import re
from modelo import send_email

HOST = "localhost"  # Mi localhost
PORT = 4000  # Mismo puerto que el del servidor


class Menu:
    def __init__(self):
        """
        Metodo constructor de la clase

        Returns
        -------
        None.

        """
        self.miposicion = {"lat": -34.5983, "long": -58.4533}
        self.mail = ""
        self.flag = 0

    def mostrar_menu(self):
        """
        interfaz de usuario 
        muestra las distitnas opciones

        Returns
        -------
        None.

        """
        print("==================================================")
        print("Hola usuario")

        if self.flag == 0:
            while True:
                self.mail = input("Introduzca una direccion de e-mail por favor:")
                if self.verificacion_regex(self.mail) is True:
                    break
                else:
                    print("Verifique el correo ingresado e intentelo nuevamente.")
            while True:
                print("==================================================")
                print("¿Por que metodo quiere buscar?")
                print("Oprima 1 para buscar por sus coordenadas")
                print("Oprima 2 para buscar por barrio")
                print("==================================================")

                opcion_buscar = int(input("Ingrese un numero: "))
                print("==================================================")
                
                if opcion_buscar == 1:
                    print(
                        """Ingrese sus coordenadas [Latitud,Longitud]\nAyuda: Arrastre el marcador, haga click en el y copie las coordenadas"""
                    )
                    miposicion = str(input("Ingrese un numero: "))

                elif opcion_buscar == 2:
                    df = pd.read_excel(os.path.abspath("") + "/src/barrios_caba.xlsx")
                    barrios = df["barrio"].to_dict()

                    for i in barrios:
                        barrio = barrios[i]
                        print(f"{i}-{barrio}")

                    print("elija un barrio")
                    opcion_barrio = int(input("-->"))

                    coordenadas = df.loc[opcion_barrio, "coordenadas"]
                    miposicion = str(coordenadas)
                else:
                    print("Opcion no valida.")
                    continue

                miposicion = miposicion.split(",")
                self.miposicion = {
                    "lat": float(miposicion[0]),
                    "long": float(miposicion[1]),
                }

                self.flag = 1
                break
        print("==================================================")
        print("¿Qué quieres hacer?")
        print(
            "(Ingresa el numero de la opcion deseada para buscar los lugares cercanos)\nATENCION: Procura realizar tu busqueda antes de enviar el mail, sino enviaras un mapa sin informacion."
        )

        print("=========================")
        print("=========================")
        print("=========================")
        print("0 - ENVIARME MAPA POR MAIL ")
        print("1 - IR A UN RESTAURANTE  ")
        print("2 - IR A UN CAFE ")
        print("3 - IR A UN BAR  ")
        print("4 - IR A UN CONFITERIA  ")
        print("5 - IR A UN PUB ")
        print("6 - IR A UNA VINERIA ")
        print("7 - IR A UNA SANDWICHERIA ")
        print("8 - UN TAKE AWAY O DELIVERY ")
        print("9 - SALIR ")
        print("=========================")
        print("=========================")
        print("=========================")

        self.opcion = str(input("Ingrese un numero: "))

        if self.opcion == "0":
            print("Enviando mail...")

        elif self.opcion == "1":
            print("Buscando restaurantes cerca...")

        elif self.opcion == "2":
            print("Buscando cafes cerca...")

        elif self.opcion == "3":
            print("Buscando bar cerca...")

        elif self.opcion == "4":
            print("Buscando confiteria cerca...")

        elif self.opcion == "5":
            print("Buscando pub cerca...")

        elif self.opcion == "6":
            print("Buscando vineria cerca...")

        elif self.opcion == "7":
            print("Buscando sandwicheria cerca...")

        elif self.opcion == "8":
            print("Buscando take away y delivery cerca...")

        elif self.opcion == "9":
            print("Cerrando mapa...")

    def getOpcion(self):
        """
        Tomas la opciones elegida

        """
        return self.opcion

    def getPosicion(self):
        """
        Toma la posicion dada como input


        """
        return self.miposicion

    def getMail(self):
        """
        Toma el mail introducido como input

        """
        return self.mail

    def verificacion_regex(self, email=None):
        """

        Verificacion de regex

        Parameters
        ----------
        email : TYPE, optional
            DESCRIPTION. el valor seteado es None.

        """
        patron = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}\b", re.I)
        if patron.match(email) is not None:
            return True
        return False


def comunicacion(clt, opcion, posicion):
    """
    Establece la comunicacion y envia los parametros al servidor

    Parameters
    ----------
    clt : HOST Y Y PORT.
    opcion : TYPE: string
        DESCRIPTION: La opcion elegida por el usuario
    posicion : TYPE: string
        DESCRIPTION: posicion elegida

    Returns
    -------
    df : retorna el dataframe de la variable df_dict

    """
    try:
        clt.send(str(posicion).encode())
        clt.send(bytearray(opcion, encoding="utf-8"))
        if opcion == "9":
            return
        data = clt.recv(1024)
        df_dict = clt.recv(int(data.decode())).decode()
        df_dict = ast.literal_eval(df_dict.replace("nan", '""'))
        df = pd.DataFrame.from_dict(df_dict)
        return df
    except ConnectionResetError:
        return None


class Cliente:
    def __init__(self, host, port):
        """
        Constructor de la clase

        """
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """
        conexion con el servidor

        Returns
        -------
        None.

        """
        print("Abriendo conexion con el servidor...")
        self.s.connect((self.host, self.port))
        return

    def send(self, data):
        """
        Envia la informacion al servidor

        Parameters
        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.s.sendall(data)

    def recv(self, size):

        return self.s.recv(size)

    def close(self):
        """
        cierre de conexion con el servidor

        Returns
        -------
        None.

        """
        self.s.close()
        return


class Runnable(QRunnable): ## comentar
    def __init__(self, myApp=None, view=None):
        """
        

        Parameters
        ----------
        myApp : TYPE, optional
            DESCRIPTION. The default is None.
        view : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        super(Runnable, self).__init__()
        self.view = view
        if self.view == 'APP':
            self.refresh = myApp.update

    def run(self):
        """
        

        Returns
        -------
        None.

        """
        if self.view == 'APP':
            app = QApplication.instance()
        clt = Cliente(HOST, PORT)

        try:
            clt.connect()
        except ConnectionRefusedError:
            print("ERROR:No se puede establecer conexion con el servidor.")
            exit(1)

        menu = Menu()
        while True:
            menu.mostrar_menu()
            if menu.getOpcion() == "0":
                send_email(menu.getMail())
            else:
                if menu.getOpcion() == "9":
                    if self.view == 'APP':
                        app.quit()
                    print("Cerrando conexion con el servidor....")
                    comunicacion(clt, menu.getOpcion(), menu.getPosicion())
                    clt.close()
                    return
                df = comunicacion(clt, menu.getOpcion(), menu.getPosicion())
                if df is None:
                    if self.view == 'APP':
                        app.quit()
                    print("Servidor no responde, cerrando mapa....")
                    clt.close()
                    return
                mapa = draw_mapa(menu.getPosicion(), "user")
                add_markers(mapa, df, "nombre", "direccion_completa", int(menu.getOpcion()))
                mapa.save(os.path.abspath("") + "/src/mapa.html")
                if self.view == 'APP':
                    self.refresh.emit()
                else:
                    nombreArchivo = os.path.abspath("") + "/src/mapa.html"
                    webbrowser.open_new_tab(nombreArchivo)
