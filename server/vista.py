import os
import subprocess
import sys
import threading

proceso = ""


class MenuServer:
    def __init__(self):
        """
        constructor

        """
        self.ruta_server = os.path.abspath("") + '/server.py'

    def lanzar_servidor(self):
        """
    
       Lanzamiento del servidor

        """
        global proceso
        proceso = subprocess.Popen([sys.executable, self.ruta_server])
        proceso.communicate()

    def Menu(self):
        """
        Menu del servidor

        """
        print("Iniciando servidor...")
        if proceso != "":
            proceso.kill()
            threading.Thread(target=self.lanzar_servidor, daemon=True).start()
        else:
            threading.Thread(target=self.lanzar_servidor, daemon=True).start()
        while True:
            close = str(input("---Presione 'S' para cerrar el servidor---\n"))
            if close == 'S':
                print('Cerrando servidor...')
                proceso.kill()
                break
