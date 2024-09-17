import pandas as pd
from fastapi import FastAPI
import requests

app = FastAPI()

# URLs de los archivos en el repositorio de GitHub (versión raw)
url_unido = 'https://raw.githubusercontent.com/HarryGuevara/Proyecto-Individual-PI-SoyHenry/main/df_unido.csv'
url_cleaned = 'https://raw.githubusercontent.com/HarryGuevara/Proyecto-Individual-PI-SoyHenry/main/movie_dataset_cleaned.csv'

# Descargar y cargar los archivos
df_unido = pd.read_csv(url_unido)
df_cleaned = pd.read_csv(url_cleaned)

# Rutas de la API

@app.get("/cantidad_filmaciones_mes/{mes}")
async def cantidad_filmaciones_mes(mes: str):
    df_cleaned['release_date'] = pd.to_datetime(df_cleaned['release_date'], errors='coerce')
    mes_num = pd.to_datetime(mes, format='%B').month
    cantidad = df_cleaned[df_cleaned['release_date'].dt.month == mes_num].shape[0]
    return f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes}"

@app.get("/cantidad_filmaciones_dia/{dia}")
async def cantidad_filmaciones_dia(dia: str):
    dias = {
        'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3, 'viernes': 4, 'sábado': 5, 'domingo': 6
    }
    dia_num = dias.get(dia.lower())
    if dia_num is None:
        return "Día inválido"
    df_cleaned['release_date'] = pd.to_datetime(df_cleaned['release_date'], errors='coerce')
    cantidad = df_cleaned[df_cleaned['release_date'].dt.dayofweek == dia_num].shape[0]
    return f"{cantidad} cantidad de películas fueron estrenadas en los días {dia}"

@app.get("/score_titulo/{titulo_de_la_filmacion}")
async def score_titulo(titulo_de_la_filmacion: str):
    pelicula = df_cleaned[df_cleaned['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]
    if pelicula.empty:
        return "Título no encontrado"
    score = pelicula.iloc[0]['popularity']
    año = pelicula.iloc[0]['release_year']
    return f"La película {titulo_de_la_filmacion} fue estrenada en el año {año} con un score/popularidad de {score}"

@app.get("/votos_titulo/{titulo_de_la_filmacion}")
async def votos_titulo(titulo_de_la_filmacion: str):
    pelicula = df_cleaned[df_cleaned['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]
    if pelicula.empty:
        return "Título no encontrado"
    votos = pelicula.iloc[0]['vote_count']
    promedio_votos = pelicula.iloc[0]['vote_average']
    if votos < 2000:
        return "La película no cumple con la condición de al menos 2000 valoraciones"
    return f"La película {titulo_de_la_filmacion} fue estrenada en el año {pelicula.iloc[0]['release_year']}. La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio_votos}"

@app.get("/get_actor/{nombre_actor}")
async def get_actor(nombre_actor: str):
    actor = df_unido[df_unido['name'].str.contains(nombre_actor, case=False, na=False)]
    if actor.empty:
        return "Actor no encontrado"
    cantidad_peliculas = actor.shape[0]
    retorno_promedio = actor['return'].mean()
    retorno_total = actor['return'].sum()
    return f"El actor {nombre_actor} ha participado de {cantidad_peliculas} cantidad de filmaciones, el mismo ha conseguido un retorno de {retorno_total} con un promedio de {retorno_promedio} por filmación"

@app.get("/get_director/{nombre_director}")
async def get_director(nombre_director: str):
    director = df_unido[df_unido['name'].str.contains(nombre_director, case=False, na=False)]
    if director.empty:
        return "Director no encontrado"
    resultados = []
    for _, row in director.iterrows():
        resultados.append({
            'titulo': row['title'],
            'fecha_lanzamiento': row['release_date'],
            'retorno': row['return'],
            'costo': row['budget'],
            'ganancia': row['revenue']
        })
    return resultados
