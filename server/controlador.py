from vista import MenuServer
from modelo import conectar_db

#lanzamiento del servidor

if __name__ == '__main__':
    conectar_db()
    menu = MenuServer()
    menu.Menu()
