import pandas as pd
import requests
import os
from peewee import Model, SqliteDatabase, CharField, DateTimeField, FloatField
import datetime


def wget(url): #comentar
    """


    """
    if (
        os.path.exists(os.path.abspath("") + "/src/" + url[url.rfind("/") + 1 : :])
        is False
    ):
        r = requests.get(url, allow_redirects=True)
        with open(os.path.abspath("") + "/src/" + url[url.rfind("/") + 1 : :], "wb") as f:
            f.write(r.content)


def radius_scan(df, lat, longi, miposicion, radio):
    """
    La funcion utiliza la formula de una circunferencia
    para dibujar un radio con la posicion como centro

    """
    x = df[lat].astype(float) - miposicion["lat"]
    y = df[longi].astype(float) - miposicion["long"]
    df_r = df[((x ** 2) + ((y * 0.82) ** 2)) <= radio ** 2]
    return df_r


def filtrar_data(opcion, miposicion):
    """
    Recibe la opcion elegida y la posicion. 
    en funcion de ellos busca lo solicitado

    """
    radio = 0.010

    gastro = pd.read_csv(os.path.abspath("") + "/src/oferta_gastronomica.csv")
    # gastro_cat = gastro["categoria"].value_counts().index.tolist()
    gastro_r = radius_scan(gastro, "lat", "long", miposicion, radio)

    if opcion == "1":
        gastro_R = gastro_r[gastro_r["categoria"] == "RESTAURANTE"].to_dict()

    elif opcion == "2":
        gastro_R = gastro_r[gastro_r["categoria"] == "CAFE"].to_dict()

    elif opcion == "3":
        gastro_R = gastro_r[gastro_r["categoria"] == "BAR"].to_dict()

    elif opcion == "4":
        gastro_R = gastro_r[gastro_r["categoria"] == "CONFITERIA"].to_dict()

    elif opcion == "5":
        gastro_R = gastro_r[gastro_r["categoria"] == "PUB"].to_dict()

    elif opcion == "6":
        gastro_R = gastro_r[gastro_r["categoria"] == "VINERIA"].to_dict()

    elif opcion == "7":
        gastro_R = gastro_r[gastro_r["categoria"] == "SANDWICHERIA"].to_dict()

    elif opcion == "8":
        gastro_R = gastro_r[gastro_r["categoria"] == "DELIVERY & TAKE AWAY"].to_dict()
    else:
        gastro_R = False

    return gastro_R


db = SqliteDatabase("base.db")


class BaseModel(Model):

    """
    Clase de la base de datos con ORM
    """

    class Meta:
        database = db


class log(BaseModel):
    direccion = CharField(unique=False)
    longitud = FloatField(unique = False)
    latitud = FloatField(unique = False)
    busqueda = CharField(unique=False)
    fecha = DateTimeField(default=datetime.datetime.now)


def conectar_db():
    """
    crear la conexion a la base 

    """
    db.connect()
    db.create_tables([log])
    return
