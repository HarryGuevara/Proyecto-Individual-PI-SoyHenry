import pandas as pd  
from fastapi import FastAPI  

app = FastAPI()  

# Mantener las URLs de los archivos  
url_unido = 'https://raw.githubusercontent.com/HarryGuevara/Proyecto-Individual-PI-SoyHenry/master/df_unido.csv'  
url_cleaned = 'https://raw.githubusercontent.com/HarryGuevara/Proyecto-Individual-PI-SoyHenry/master/movie_dataset_cleaned.csv'  

# Inicialización de los DataFrames  
df_unido = None  
df_cleaned = None  

@app.get("/")
async def root():
    return {"message": "API está funcionando"}

# Función para cargar los DataFrames  
def load_dataframes():  
    global df_unido, df_cleaned  
    if df_unido is None:  
        df_unido = pd.read_csv(url_unido)  
    if df_cleaned is None:  
        df_cleaned = pd.read_csv(url_cleaned)  

# Endpoint para obtener cantidad de películas por mes  
@app.get("/cantidad_filmaciones_mes/{mes}")  
async def cantidad_filmaciones_mes(mes: str):  
    load_dataframes()  
    meses = {  
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,  
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,  
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12  
    }  
    mes_num = meses.get(mes.lower())  
    if mes_num is None:  
        return {"error": "Mes inválido. Usa el nombre del mes en español (Ej: enero, febrero)"}  
    
    df_cleaned['release_date'] = pd.to_datetime(df_cleaned['release_date'], errors='coerce')  
    cantidad = df_cleaned[df_cleaned['release_date'].dt.month == mes_num].shape[0]  
    return {"mes": mes, "cantidad_peliculas": cantidad}  

# Endpoint para obtener cantidad de películas por día de la semana  
@app.get("/cantidad_filmaciones_dia/{dia}")  
async def cantidad_filmaciones_dia(dia: str):  
    load_dataframes()  
    dias = {  
        'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3, 'viernes': 4, 'sábado': 5, 'domingo': 6  
    }  
    dia_num = dias.get(dia.lower())  
    if dia_num is None:  
        return {"error": "Día inválido. Usa el nombre del día en español (Ej: lunes, martes)"}  
    
    df_cleaned['release_date'] = pd.to_datetime(df_cleaned['release_date'], errors='coerce')  
    cantidad = df_cleaned[df_cleaned['release_date'].dt.dayofweek == dia_num].shape[0]  
    return {"dia": dia, "cantidad_peliculas": cantidad}  

# Endpoint para obtener el score de una película por título  
@app.get("/score_titulo/{titulo_de_la_filmacion}")  
async def score_titulo(titulo_de_la_filmacion: str):  
    load_dataframes()  
    peliculas = df_cleaned[df_cleaned['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]  
    if peliculas.empty:  
        return {"error": "Título no encontrado"}  

    resultados = [{"titulo": pelicula['title'], "año": pelicula['release_year'], "score": pelicula['popularity']} for _, pelicula in peliculas.iterrows()]  
    return resultados  

# Endpoint para obtener votos y promedio de votos por título  
@app.get("/votos_titulo/{titulo_de_la_filmacion}")  
async def votos_titulo(titulo_de_la_filmacion: str):  
    load_dataframes()  
    pelicula = df_cleaned[df_cleaned['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]  

    if pelicula.empty:  
        return {"error": "Título no encontrado"}  

    peli_info = pelicula.iloc[0]  
    votos = peli_info['vote_count']  
    promedio_votos = peli_info['vote_average']  

    if votos < 2000:  
        return {"message": "La película no cumple con la condición de al menos 2000 valoraciones"}  

    return {  
        "titulo": peli_info['title'],  
        "año": peli_info['release_year'],  
        "total_votos": votos,  
        "promedio_votos": promedio_votos  
    }  

# Endpoint para obtener información de un actor  
@app.get("/get_actor/{nombre_actor}")  
async def get_actor(nombre_actor: str):  
    load_dataframes()  
    actores = df_unido[df_unido['role'] == 'Actor']  
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

# Endpoint para obtener información de un director  
@app.get("/get_director/{nombre_director}")  
async def get_director(nombre_director: str):  
    load_dataframes()  
    directores = df_unido[df_unido['role'] == 'Director']  
    director = directores[directores['name'].str.contains(nombre_director, case=False, na=False)]  

    if director.empty:  
        return {"error": "Director no encontrado"}  

    resultados = [{"titulo": row['title'], "fecha_lanzamiento": row['release_date'],  
                   "retorno": row['return'], "costo": row['budget'], "ganancia": row['revenue']} for _, row in director.iterrows()]  
    
    return resultados
