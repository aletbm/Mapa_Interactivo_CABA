import pandas as pd
import folium  # pip install folium
from viewer import MyApp
from PyQt5.QtWidgets import QApplication
import sys
from folium.plugins import MousePosition


def add_markers(mapa, df, name, direccion, icon, color):
    for i, sitio in df.iterrows():
        folium.Marker(
            [sitio["lat"], sitio["long"]],
            popup=f"<b>{sitio[name]}</b>" + f"\n{sitio[direccion]}",
            icon=folium.Icon(color=color, icon=icon),
        ).add_to(mapa)
    return


def radius_scan(df, lat, longi, miposicion, radio):
    x = df[lat].astype(float) - miposicion["lat"]
    y = df[longi].astype(float) - miposicion["long"]
    df_r = df[((x ** 2) + ((y * 0.82) ** 2)) <= radio ** 2]
    return df_r


miposicion = {"lat": -34.601614, "long": -58.409270}
radio = 0.009

gastro = pd.read_csv("./Data/oferta_gastronomica.csv")
gastro_cat = gastro["categoria"].value_counts().index.tolist()
gastro_r = radius_scan(gastro, "lat", "long", miposicion, radio)

alojamientos = pd.read_csv("./Data/alojamientos-turisticos.csv")
alojamientos = alojamientos.rename(columns={"Lat": "lat", "Long": "long"})
aloja_cat = alojamientos["tipo"].value_counts().index.tolist()
aloja = alojamientos[(alojamientos["direccion"].notna())]
aloja = radius_scan(aloja, "lat", "long", miposicion, radio)

hospitales = pd.read_csv("./Data/hospitales.csv")
hospitales.insert(1, "long", 0, allow_duplicates=False)
hospitales.insert(2, "lat", 0, allow_duplicates=False)
for i, x in enumerate(hospitales["WKT"]):
    x = x.split("-")
    hospitales.iloc[i, 1] = -float(x[1])
    hospitales.iloc[i, 2] = -float(x[2][:-2])
hospital = radius_scan(hospitales, "lat", "long", miposicion, radio)

cent_salud = pd.read_csv("./Data/centros-de-salud-privados.csv")
cent_salud.insert(2, "direccion", 0, allow_duplicates=False)
for i in range(0, len(cent_salud)):
    cent_salud.iloc[i, 2] = f"{cent_salud['calle'][i]} {str(cent_salud['altura'][i])}"
cent_salud_r = radius_scan(cent_salud, "lat", "long", miposicion, radio)


# esp_culturales = pd.read_csv("./Data/espacios-culturales.csv")
# print(esp_culturales["FUNCION_PRINCIPAL"].value_counts())

# culto = pd.read_csv("./Data/lugares-de-culto.csv")
# print(culto["grupo"].value_counts())

# est_subte = pd.read_csv("./Data/bocas-de-subte.csv")
# print(est_subte["linea"].value_counts())


# mapa = folium.Map(location=[-34.595355, -58.446799], zoom_start=12)
# while True:
#     lat = input("Latitud:")
#     long = input("Longitud:")
    # if len(lat) != 0 and len(long) != 0:
mapa = folium.Map(
    location=[miposicion["lat"], miposicion["long"]], zoom_start=16, control_scale=True
)  # tiles='cartodbpositron'
folium.Marker(
    [miposicion["lat"], miposicion["long"]],
    popup="Mi Ubicacion",
    icon=folium.Icon(color="red", icon="glyphicon-map-marker"),
).add_to(mapa)
folium.Circle(
    [miposicion["lat"], miposicion["long"]],
    radius=1000,
    fill=True,
    fill_color="lightblue",
    fill_opacity=0.4,
).add_to(mapa)

formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"

MousePosition(
    position="topright",
    separator=" | ",
    empty_string="NaN",
    lng_first=True,
    num_digits=20,
    prefix="Coordinates:",
    lat_formatter=formatter,
    lng_formatter=formatter,
).add_to(mapa)

mapa.add_child(folium.LatLngPopup())

gastro_R = gastro_r[gastro_r["categoria"] == "RESTAURANTE"]
add_markers(
    mapa, gastro_R, "nombre", "direccion_completa", "glyphicon-cutlery", "orange"
)
gastro_B = gastro_r[gastro_r["categoria"] == "BAR"]
add_markers(mapa, gastro_B, "nombre", "direccion_completa", "glyphicon-glass", "green")
gastro_C = gastro_r[gastro_r["categoria"] == "CONFITERIA"]
add_markers(mapa, gastro_C, "nombre", "direccion_completa", "glyphicon-apple", "pink")

add_markers(mapa, aloja, "nombre", "direccion", "glyphicon-home", "blue")
add_markers(mapa, hospital, "NOMBRE", "DOM_NORMA", "glyphicon-header", "red")
add_markers(mapa, cent_salud_r, "nombre", "direccion", "glyphicon-header", "red")
mapa.save("./mapa.html")

if QApplication.instance() is None:   
    app = QApplication(sys.argv)
    myApp = MyApp(mapa)
    myApp.show()
try:
    sys.exit(app.exec_())
except SystemExit:
    print("Cerrando Ventana...")