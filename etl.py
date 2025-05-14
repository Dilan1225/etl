# -*- coding: utf-8 -*-
"""ETL Script for COVID-19 Indonesia Dataset

Original file is located at
    https://colab.research.google.com/drive/10Nsc7LY6Ee322LBBWecXLRoMO0crMsJs
"""

import os
import subprocess
import pandas as pd
from pymongo import MongoClient

# Descargar el dataset utilizando subprocess (si no está previamente descargado)
def descargar_dataset():
    if not os.path.exists('covid19-indonesia-time-series-data.zip'):
        print("Descargando el dataset...")
        subprocess.run(["kaggle", "datasets", "download", "-d", "meirnizamani/covid19-indonesia-time-series-data"], check=True)
    else:
        print("El dataset ya está descargado.")
    
    # Descomprimir el archivo ZIP
    if not os.path.exists('Data_COVID19_Indonesia.csv'):
        print("Descomprimiendo el archivo...")
        subprocess.run(["unzip", "covid19-indonesia-time-series-data.zip"], check=True)
    else:
        print("El archivo ya está descomprimido.")

# Conexión a MongoDB Atlas
URI = "mongodb+srv://dilan_291:1012449412Denis$@cluster0.hrhf9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(URI)
db = client["ETL"]
collection = db["KAGGLE"]

# Función para transformar los datos
def transformar_datos(nombre_archivo='/content/Data_COVID19_Indonesia.csv'):
    df = pd.read_csv(nombre_archivo)

    # Transformaciones simples
    df = df.dropna(axis=1, how='all')  # Quitar columnas vacías
    df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]  # Estilo MongoDB

    return df.to_dict(orient='records')

# Función para cargar los datos a MongoDB
def cargar_datos_mongo(datos):
    try:
        collection.insert_many(datos)
        print("✅ Datos cargados correctamente en MongoDB Atlas.")
    except Exception as e:
        print(f"❌ Error al cargar los datos: {e}")

# Ejecutar proceso ETL
def ejecutar_etl():
    print("=== INICIANDO ETL DESDE ARCHIVO LOCAL ===")

    print("[1/3] Descargando el dataset...")
    descargar_dataset()

    print("[2/3] Transformando datos...")
    datos_transformados = transformar_datos()

    print("[3/3] Cargando datos a MongoDB...")
    cargar_datos_mongo(datos_transformados)

    print("=== ETL FINALIZADO ===")

if __name__ == "__main__":
    ejecutar_etl()
