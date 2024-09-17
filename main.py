from fastapi import FastAPI
import pandas as pd
import requests

app = FastAPI()

# Ruta para verificar si la API está funcionando
@app.get("/")
async def read_root():
    return {"message": "API is running"}

# Ruta para obtener datos desde una URL externa utilizando requests
@app.get("/fetch-data/")
async def fetch_data(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return {"data": response.json()}
    return {"error": "Failed to fetch data"}

# Ruta para cargar un archivo CSV y mostrar las primeras filas utilizando pandas
@app.post("/upload-csv/")
async def upload_csv(file_path: str):
    try:
        data = pd.read_csv(file_path)
        return {"head": data.head().to_dict()}
    except Exception as e:
        return {"error": str(e)}

# Ruta para realizar una operación básica con pandas
@app.get("/data-info/")
async def data_info():
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
        'Age': [24, 27, 22, 32, 29],
        'City': ['New York', 'Paris', 'Berlin', 'London', 'Tokyo']
    }
    df = pd.DataFrame(data)
    return {
        "description": df.describe().to_dict(),
        "columns": df.columns.tolist()
    }

# Ejecutar con Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
