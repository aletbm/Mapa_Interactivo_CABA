import folium  # pip install folium
from folium.plugins import MousePosition


def add_markers(mapa, df, name, direccion, icon, color):
    for i, sitio in df.iterrows():
        folium.Marker(
            [sitio["lat"], sitio["long"]],
            popup=f"<b>{sitio[name]}</b>" + f"\n{sitio[direccion]}",
            icon=folium.Icon(color=color, icon=icon),
        ).add_to(mapa)
    return


def draw_mapa(miposicion, userMap=None, zoom=16):
    mapa = folium.Map(
        location=[miposicion["lat"], miposicion["long"]],
        zoom_start=zoom,
        control_scale=True,
    )  # tiles='cartodbpositron'
    if userMap == 'user':
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

    mapa.save("./mapa.html")

    return mapa
