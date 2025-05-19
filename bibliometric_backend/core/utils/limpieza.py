import os

import pandas as pd


def procesar_archivo_csv(ruta_archivo):
    """
    Recibe la ruta a un archivo CSV, elimina duplicados y guarda:
    - un archivo limpio con entradas únicas
    - un archivo con los duplicados eliminados
    """
    df = pd.read_csv(ruta_archivo)

    # Normaliza columnas
    df.columns = df.columns.str.strip().str.lower()

    # Claves para detectar duplicados (ajústalo si es necesario)
    claves = ["titulo", "autores"]

    # Elimina duplicados y guarda aparte los repetidos
    df_limpio = df.drop_duplicates(subset=claves, keep="first")
    df_duplicados = df[df.duplicated(subset=claves, keep="first")]

    base = os.path.splitext(ruta_archivo)[0]
    ruta_limpio = base + "_unificado.csv"
    ruta_duplicados = base + "_duplicados.csv"

    df_limpio.to_csv(ruta_limpio, index=False)
    df_duplicados.to_csv(ruta_duplicados, index=False)

    return ruta_limpio, ruta_duplicados
