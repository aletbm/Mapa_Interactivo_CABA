from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import QUrl, Signal, Slot
from PySide2.QtWidgets import QWidget, QHBoxLayout
from PySide2.QtWebEngineWidgets import QWebEngineView
import os
import folium  # pip install folium
from jinja2 import Template


#   'purple', 'lightgray', 'beige', 'orange', 'gray', 'cadetblue', 'red', 'lightgreen', 'darkpurple', 'pink', 'darkgreen', 'black', 'blue', 'white', 'darkred', 'green', 'darkblue', 'lightred', 'lightblue'


class MyApp(QtWidgets.QMainWindow):
    """Clase que muestra el mapa durante la busqueda"""

    update = Signal()

    def __init__(self):
        
        """
        Metodo constructor de la clase

        Returns
        -------
        None.

        """
        
        
        super().__init__()
        self.initWindow()

    def initWindow(self):
        """

        Returns
        -------
        None.

        """
        
        self.setWindowTitle(self.tr("Mapa Interactivo v1.0"))
        self.setWindowIcon(QtGui.QIcon(os.path.abspath("") + "/src/app.png"))
        self.setFixedSize(1500, 800)
        self.browserUI()

    def browserUI(self):
        """    

        Returns
        -------
        None.

        """
        
        self.view = QWebEngineView()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        lay = QHBoxLayout(central_widget)
        lay.addWidget(self.view, stretch=1)

        plot_path = os.path.abspath(os.path.abspath("") + "/src/mapa.html")
        self.plot_url = QUrl.fromLocalFile(plot_path)

        self.view.load(self.plot_url)

        self.update.connect(self.refreshing)

    @Slot()
    def refreshing(self):
        self.view.reload()

    def closeEvent(self, event):
        event.accept()


def add_markers(mapa, df, name, direccion, opcion):
    """
    Añade los marcadores al mapa

    Returns
    -------
    None.

    """
    ## Estilos de iconos y colores
    icon = [
        "glyphicon-cutlery",
        "fa-coffee",
        "fa-beer",
        "fa-birthday-cake",
        "glyphicon-glass",
        "glyphicon-glass",
        "fa-hamburger",
        "fa-biking-mountain",
    ]
    color = [
        "orange",
        "green",
        "cadetblue",
        "lightred",
        "darkpurple",
        "purple",
        "darkblue",
        "darkred",
    ]
    prefix = ["glyphicon", "fa", "fa", "fa", "glyphicon", "glyphicon", "fa", "fa"]
    for i, sitio in df.iterrows():
        folium.Marker(
            [sitio["lat"], sitio["long"]],
            popup=f"<b>{sitio[name]}</b>" + f"\n{sitio[direccion]}",
            icon=folium.Icon(
                color=color[opcion - 1],
                prefix=prefix[opcion - 1],
                icon=icon[opcion - 1],
            ),
        ).add_to(mapa)
    return


def draw_mapa(miposicion, userMap=None, zoom=15):
    """
    
    Parameters
    ----------
    miposicion : dict
        DESCRIPTION: diccionario con la posicion que se de como input
    userMap : TYPE: opcional
        DESCRIPTION. se setea en None.
    zoom : TYPE: opcional
        DESCRIPTION. se setea en 15.

    Returns
    -------
    mapa :
        DESCRIPTION: ddevuelve el mapa con la posicion

    """

    mapa = folium.Map(
        location=[miposicion["lat"], miposicion["long"]],
        zoom_start=zoom,
        control_scale=True,
    )  # tiles='cartodbpositron'

    mrk = folium.Marker(
        location=[miposicion["lat"], miposicion["long"]],
        popup=f'<input type="text" value="{miposicion["lat"]}, {miposicion["long"]}" id="myInput"><button onclick="myFunction()">Copiar ubicacion</button>',
        draggable=True,
        icon=folium.Icon(color="red", icon="glyphicon-map-marker"),
    ).add_to(mapa)

    el = folium.MacroElement().add_to(mapa)
    el._template = Template(
        """
        {% macro script(this, kwargs) %}

        """
        + mrk.get_name()
        + """.on('click', getPosition);

        function myFunction(lat, lng) {
            var input = document.createElement('textarea');
            input.textContent = lat + ',' + lng
            document.body.appendChild(input);
            input.select();
            document.execCommand('copy');
            document.body.removeChild(input);
        }
        function getPosition(e) {
            var lat = e.latlng.lat.toFixed(6);
            var lng = e.latlng.lng.toFixed(6);
            var coord = lat + ',' + lng
            var newContent = `<input type=\"text\" value=${coord} id=\"myInput\"><button onclick=\"myFunction(${lat}, ${lng})\">Copiar ubicacion</button>`;
            e.target.setPopupContent(newContent);
        };
        {% endmacro %}
    """
    )

    if userMap == "user":
        folium.Circle(
            [miposicion["lat"], miposicion["long"]],
            radius=1150,
            fill=True,
            fill_color="lightblue",
            fill_opacity=0.4,
        ).add_to(mapa)

    mapa.save(os.path.abspath("") + "/src/mapa.html")

    return mapa
