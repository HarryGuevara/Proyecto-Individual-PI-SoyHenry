import pandas as pd
from fastapi import FastAPI
import requests

app = FastAPI()

# URLs de los archivos en el repositorio de GitHub (versión raw)
url_unido = 'https://github.com/HarryGuevara/Proyecto-Individual-PI-SoyHenry/blob/master/df_unido.csv'
url_cleaned = 'https://github.com/HarryGuevara/Proyecto-Individual-PI-SoyHenry/blob/master/movie_dataset_cleaned.csv'

# Descargar y cargar los archivos
df_unido = pd.read_csv(url_unido)
df_cleaned = pd.read_csv(url_cleaned)

# Rutas de la API

@app.get("/cantidad_filmaciones_mes/{mes}")
async def cantidad_filmaciones_mes(mes: str):
    try:
        mes_num = pd.to_datetime(mes, format='%B').month
    except ValueError:
        return {"error": "Mes inválido. Usa el nombre completo en inglés (Ej: January, February)"}
    df_cleaned['release_date'] = pd.to_datetime(df_cleaned['release_date'], errors='coerce')
    cantidad = df_cleaned[df_cleaned['release_date'].dt.month == mes_num].shape[0]
    return {"mes": mes, "cantidad_peliculas": cantidad}

@app.get("/cantidad_filmaciones_dia/{dia}")
async def cantidad_filmaciones_dia(dia: str):
    dias = {
        'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3, 'viernes': 4, 'sábado': 5, 'domingo': 6
    }
    dia_num = dias.get(dia.lower())
    if dia_num is None:
        return {"error": "Día inválido. Usa el nombre del día en español (Ej: lunes, martes)"}
    df_cleaned['release_date'] = pd.to_datetime(df_cleaned['release_date'], errors='coerce')
    cantidad = df_cleaned[df_cleaned['release_date'].dt.dayofweek == dia_num].shape[0]
    return {"dia": dia, "cantidad_peliculas": cantidad}

@app.get("/score_titulo/{titulo_de_la_filmacion}")
async def score_titulo(titulo_de_la_filmacion: str):
    peliculas = df_cleaned[df_cleaned['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]
    if peliculas.empty:
        return {"error": "Título no encontrado"}
    
    resultados = []
    for _, pelicula in peliculas.iterrows():
        resultados.append({
            'titulo': pelicula['title'],
            'año': pelicula['release_year'],
            'score': pelicula['popularity']
        })
    
    return resultados

@app.get("/votos_titulo/{titulo_de_la_filmacion}")
async def votos_titulo(titulo_de_la_filmacion: str):
    pelicula = df_combined[df_combined['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]
    if pelicula.empty:
        return "Título no encontrado"
    votos = pelicula.iloc[0]['vote_count']
    promedio_votos = pelicula.iloc[0]['vote_average']
    if votos < 2000:
        return "La película no cumple con la condición de al menos 2000 valoraciones"
    return f"La película {titulo_de_la_filmacion} fue estrenada en el año {pelicula.iloc[0]['release_year']}. La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio_votos}"

@app.get("/get_actor/{nombre_actor}")
async def get_actor(nombre_actor: str):
    actores = df_unido[df_unido['role'] == 'Actor']  # Filtra solo actores
    actor = actores[actores['name'].str.contains(nombre_actor, case=False, na=False)]
    
    if actor.empty:
        return {"error": "Actor no encontrado"}
    
    cantidad_peliculas = actor.shape[0]
    retorno_total = actor['return'].sum()
    retorno_promedio = actor['return'].mean()
    
    return {
        "actor": nombre_actor,
        "cantidad_peliculas": cantidad_peliculas,
        "retorno_total": retorno_total,
        "retorno_promedio": retorno_promedio
    }

@app.get("/get_director/{nombre_director}")
async def get_director(nombre_director: str):
    directores = df_unido[df_unido['role'] == 'Director']  # Filtra solo directores
    director = directores[directores['name'].str.contains(nombre_director, case=False, na=False)]
    
    if director.empty:
        return {"error": "Director no encontrado"}
    
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
