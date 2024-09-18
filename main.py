from fastapi import FastAPI, HTTPException
import pandas as pd
from typing import Optional

app = FastAPI()

# URLs de los archivos CSV en GitHub
url_unido = 'https://raw.githubusercontent.com/HarryGuevara/Proyecto-Individual-PI-SoyHenry/master/df_unido.csv'
url_cleaned = 'https://raw.githubusercontent.com/HarryGuevara/Proyecto-Individual-PI-SoyHenry/master/movie_dataset_cleaned.csv'

# Descargar y cargar los archivos CSV
try:
    df_cleaned = pd.read_csv(url_cleaned)
    df_unido = pd.read_csv(url_unido)
except Exception as e:
    df_cleaned = pd.DataFrame()
    df_unido = pd.DataFrame()
    print(f"Error al cargar los archivos CSV: {e}")

@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la API de análisis de películas"}

@app.get("/cantidad_filmaciones_mes/{mes}")
async def cantidad_filmaciones_mes(mes: str):
    try:
        # Convertir la columna 'release_date' a datetime
        df_cleaned['release_date'] = pd.to_datetime(df_cleaned['release_date'], errors='coerce')

        # Convertir el mes a número
        mes_num = pd.to_datetime(mes, format='%B').month

        # Filtrar las películas por mes y contar
        cantidad = df_cleaned[df_cleaned['release_date'].dt.month == mes_num].shape[0]
        
        return {"mes": mes, "cantidad": cantidad}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la solicitud: {e}")

@app.get("/datos_unido")
async def datos_unido():
    try:
        # Retornar el primer registro de df_unido como un ejemplo
        if not df_unido.empty:
            return df_unido.head().to_dict(orient='records')
        else:
            return {"message": "No hay datos disponibles en df_unido"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar los datos unidos: {e}")
