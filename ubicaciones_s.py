import pandas as pd


def radius_scan(df, lat, longi, miposicion, radio):
    x = df[lat].astype(float) - miposicion["lat"]
    y = df[longi].astype(float) - miposicion["long"]
    df_r = df[((x ** 2) + ((y * 0.82) ** 2)) <= radio ** 2]
    return df_r


def filtrar_data(opcion):
    miposicion = {"lat": -34.601614, "long": -58.409270}
    radio = 0.009

    gastro = pd.read_csv("./Data/oferta_gastronomica.csv")
    # gastro_cat = gastro["categoria"].value_counts().index.tolist()
    gastro_r = radius_scan(gastro, "lat", "long", miposicion, radio)

    if opcion == "1":
        gastro_R = gastro_r[gastro_r["categoria"] == "RESTAURANTE"]
    return gastro_R.to_dict()