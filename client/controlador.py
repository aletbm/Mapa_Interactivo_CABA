from vista import Runnable
from viewer import MyApp, draw_mapa
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QThreadPool
import sys
import webbrowser
import os

options = ["APP", "BROWSER"]
VIEW = options[0]

# Lanzamiento de la aplicación

if __name__ == "__main__":
    print("Abriendo mapa...")
    centro_mapa = {"lat": -34.5983, "long": -58.4533}
    draw_mapa(centro_mapa, "root", zoom=13)
    if QApplication.instance() is None and VIEW == "APP":
        app = QApplication(sys.argv)
        myApp = MyApp()
        myApp.show()
        runnable = Runnable(myApp, VIEW)
        QThreadPool.globalInstance().start(runnable)
        sys.exit(app.exec_())
    else:
        nombreArchivo = os.path.abspath("") + "/src/mapa.html"
        webbrowser.open_new_tab(nombreArchivo)
        runnable = Runnable(view=VIEW)
        runnable.run()
