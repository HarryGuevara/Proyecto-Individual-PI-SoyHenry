
```markdown
# Proyecto de API de Análisis de Películas

Este proyecto implementa una API utilizando **FastAPI** para el análisis de datos relacionados con películas. La API permite consultar la cantidad de películas filmadas en un mes específico y obtener datos combinados de una fuente adicional.

## Estructura del Proyecto

- **main.py**: Contiene la implementación de la API utilizando FastAPI.
- **test_main.py**: Contiene las pruebas para la API para asegurar su correcto funcionamiento.
- **Procfile**: Archivo para el despliegue en plataformas como Render.
- **render.yaml**: Configuración para el despliegue en Render.
- **requirements.txt**: Lista de dependencias necesarias para ejecutar el proyecto.

## Instalación

Para instalar y ejecutar este proyecto, sigue estos pasos:

### Clonar el Repositorio

```bash
git clone https://github.com/HarryGuevara/Proyecto-Individual-PI-SoyHenry.git
cd Proyecto-Individual-PI-SoyHenry
```

### Crear y Activar un Entorno Virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
```

### Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar la Aplicación

```bash
uvicorn main:app --reload
```

La aplicación estará disponible en `http://127.0.0.1:8000`.

## Endpoints

### 1. Obtener un Mensaje de Bienvenida

- **Ruta**: `/`
- **Método**: GET
- **Respuesta**:
    ```json
    {
        "message": "Bienvenido a la API de análisis de películas"
    }
    ```

### 2. Consultar la Cantidad de Películas Filmadas en un Mes

- **Ruta**: `/cantidad_filmaciones_mes/{mes}`
- **Método**: GET
- **Parámetro**:
    - `mes` (string): Nombre del mes en español (ej. "enero", "febrero", etc.)
- **Respuesta**:
    ```json
    {
        "mes": "enero",
        "cantidad": 25
    }
    ```
- **Error** (si el mes no es válido o hay problemas procesando la solicitud):
    ```json
    {
        "detail": "Error procesando la solicitud: <mensaje de error>"
    }
    ```

### 3. Obtener Datos Combinados

- **Ruta**: `/datos_unido`
- **Método**: GET
- **Respuesta**: Devuelve una lista de diccionarios con los primeros registros de los datos combinados.
    ```json
    [
        {
            "column1": "value1",
            "column2": "value2",
            ...
        }
    ]
    ```
- **Error** (si no hay datos disponibles):
    ```json
    {
        "message": "No hay datos disponibles en df_unido"
    }
    ```

## Pruebas

Para ejecutar las pruebas de la API, utiliza pytest:

```bash
pytest test_main.py
```

### Las pruebas incluyen:

- Verificación del mensaje de bienvenida.
- Consulta de la cantidad de películas filmadas en un mes.
- Obtención de datos combinados.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir al proyecto, por favor realiza un fork del repositorio, realiza tus cambios y envía un pull request.

## Documentación sobre Resolución de Conflictos y Gestión de Versiones

### Resolución de Conflictos en Git

Cuando trabajas en un proyecto con Git y varias personas están realizando cambios en el mismo repositorio, pueden ocurrir conflictos durante las operaciones de merge o pull. A continuación, te mostramos cómo resolver estos conflictos y mantener tu repositorio en buen estado.

#### 1. Identificación de Conflictos

Cuando Git encuentra conflictos durante un merge o pull, marca los archivos conflictivos con marcas de conflicto en el archivo.

#### 2. Resolución de Conflictos

- **Abrir el Archivo Conflictivo**: Usa un editor que soporte archivos Jupyter Notebook para abrir el archivo conflictivo.
- **Editar el Archivo**: Decide qué cambios deseas conservar o cómo combinar las diferentes versiones.
- **Añadir y Confirmar Cambios**: 
    ```bash
    git add nombre-del-archivo
    git commit -m "Resuelto conflicto en nombre-del-archivo"
    ```

#### 3. Actualización del Repositorio

- **Hacer Pull**: 
    ```bash
    git pull origin nombre-de-la-rama
    ```
- **Hacer Push**: 
    ```bash
    git push origin nombre-de-la-rama
    ```

## Integración de Archivos CSV

Este proyecto incluye un proceso para combinar dos archivos CSV que contienen información sobre películas. La única columna común entre los dos archivos es `id_film`, que se utiliza para alinear la información de ambos conjuntos de datos.

### Procedimiento de Integración

1. **Carga de Archivos CSV**: Los archivos se cargan en dos DataFrames de pandas.
2. **Conversión de Tipo de Datos**: Se asegura que `id_film` sea numérico para la combinación.
3. **Combinación de DataFrames**: Se realiza una combinación outer en los DataFrames usando `id_film` como clave.

