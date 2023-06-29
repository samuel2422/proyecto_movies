import pandas as pd


df = pd.read_csv("movies_credits.csv")  # Reemplaza "movies_credits.csv" con la ruta de tu archivo CSV


def obtener_coincidencias(mes: str):
        coincidencias = 0
    for index, row in df.iterrows():
        release_month = row["release_month"]
        if release_month.lower() == mes.lower():
            coincidencias = coincidencias+1

    return coincidencias

obtener_coincidencias("enero")