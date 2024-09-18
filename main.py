from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()

# URLs de los archivos CSV en GitHub
url_unido = 'https://raw.githubusercontent.com/HarryGuevara/Proyecto-Individual-PI-SoyHenry/master/df_unido.csv'
url_cleaned = 'https://raw.githubusercontent.com/HarryGuevara/Proyecto-Individual-PI-SoyHenry/master/movie_dataset_cleaned.csv'

# Inicialización de los DataFrames
df_unido = None
df_cleaned = None

def load_dataframes():
    global df_unido, df_cleaned
    try:
        if df_unido is None:
            df_unido = pd.read_csv(url_unido)
        if df_cleaned is None:
            df_cleaned = pd.read_csv(url_cleaned)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar los archivos CSV: {e}")

@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la API de análisis de películas"}

@app.get("/cantidad_filmaciones_mes/{mes}")
async def cantidad_filmaciones_mes(mes: str):
    try:
        load_dataframes()  # Cargar los DataFrames solo cuando sea necesario

        # Convertir la columna 'release_date' a datetime
        df_cleaned['release_date'] = pd.to_datetime(df_cleaned['release_date'], errors='coerce')

        # Convertir el mes a número usando un diccionario
        meses = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
            'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
            'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }
        mes_num = meses.get(mes.lower())
        if mes_num is None:
            return {"error": "Mes inválido. Usa el nombre del mes en español (Ej: enero, febrero)"}

        # Filtrar las películas por mes y contar
        cantidad = df_cleaned[df_cleaned['release_date'].dt.month == mes_num].shape[0]

        return {"mes": mes, "cantidad": cantidad}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la solicitud: {e}")

@app.get("/datos_unido")
async def datos_unido():
    try:
        load_dataframes()  # Cargar los DataFrames solo cuando sea necesario

        # Retornar el primer registro de df_unido como un ejemplo
        if not df_unido.empty:
            return df_unido.head().to_dict(orient='records')
        else:
            return {"message": "No hay datos disponibles en df_unido"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar los datos unidos: {e}")

