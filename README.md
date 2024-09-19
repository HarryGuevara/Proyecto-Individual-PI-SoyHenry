
# Proyecto de API de Análisis de Películas

Este proyecto implementa una API utilizando FastAPI para el análisis de datos relacionados con películas. La API permite consultar la cantidad de películas filmadas en un mes específico y obtener datos combinados de una fuente adicional.

## Estructura del Proyecto

- `main.py`: Contiene la implementación de la API utilizando FastAPI.
- `test_main.py`: Contiene las pruebas para la API para asegurar su correcto funcionamiento.

## Instalación

Para instalar y ejecutar este proyecto, sigue estos pasos:

1. **Clonar el Repositorio**

   ```bash
   git clone https://github.com/HarryGuevara/Proyecto-Individual-PI-SoyHenry.git
   cd Proyecto-Individual-PI-SoyHenry
   ```

2. **Crear y Activar un Entorno Virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

3. **Instalar Dependencias**

   ```bash
   pip install fastapi uvicorn pandas
   ```

4. **Ejecutar la Aplicación**

   ```bash
   uvicorn main:app --reload
   ```

   La aplicación estará disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Endpoints

### 1. Obtener un Mensaje de Bienvenida

- **Ruta:** `/`
- **Método:** `GET`
- **Respuesta:**

  ```json
  {
      "message": "Bienvenido a la API de análisis de películas"
  }
  ```

### 2. Consultar la Cantidad de Películas Filmadas en un Mes

- **Ruta:** `/cantidad_filmaciones_mes/{mes}`
- **Método:** `GET`
- **Parámetro:**
  - `mes` (string): Nombre del mes (ej. "January", "February", etc.)
- **Respuesta:**

  ```json
  {
      "mes": "January",
      "cantidad": 25
  }
  ```

- **Error (si el mes no es válido o hay problemas procesando la solicitud):**

  ```json
  {
      "detail": "Error procesando la solicitud: <mensaje de error>"
  }
  ```

### 3. Obtener Datos Combinados

- **Ruta:** `/datos_unido`
- **Método:** `GET`
- **Respuesta:** Devuelve una lista de diccionarios con los primeros registros de los datos combinados.

  ```json
  [
      {
          "column1": "value1",
          "column2": "value2",
          ...
      }
  ]
  ```

- **Error (si no hay datos disponibles):**

  ```json
  {
      "message": "No hay datos disponibles en df_unido"
  }
  ```

## Pruebas

Para ejecutar las pruebas de la API, utiliza `pytest`:

```bash
pytest test_main.py
```

Las pruebas incluyen:

- Verificación del mensaje de bienvenida.
- Consulta de la cantidad de películas filmadas en un mes.
- Obtención de datos combinados.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir al proyecto, por favor realiza un fork del repositorio, realiza tus cambios y envía un pull request.

---

## Documentación sobre Resolución de Conflictos y Gestión de Versiones

### Resolución de Conflictos en Git

Cuando trabajas en un proyecto con Git y varias personas están realizando cambios en el mismo repositorio, pueden ocurrir conflictos durante las operaciones de `merge` o `pull`. A continuación, te mostramos cómo resolver estos conflictos y mantener tu repositorio en buen estado.

#### 1. Identificación de Conflictos

Cuando Git encuentra conflictos durante un `merge` o `pull`, marca los archivos conflictivos con marcas de conflicto en el archivo. Estas marcas son:

```
<<<<<<< HEAD
// Cambios en tu rama local
=======
// Cambios en la rama remota
>>>>>>> nombre-de-la-rama-remota
```

#### 2. Resolución de Conflictos

1. **Abrir el Archivo Conflictivo**:
   - Utiliza un editor que soporte archivos Jupyter Notebook (por ejemplo, Jupyter Notebook, JupyterLab o Visual Studio Code con extensión Jupyter) para abrir el archivo conflictivo.

2. **Editar el Archivo**:
   - Busca las marcas de conflicto (`<<<<<<<`, `=======`, `>>>>>>>`) en el archivo.
   - Decide qué cambios deseas conservar o cómo combinar las diferentes versiones.
   - Elimina las marcas de conflicto y guarda el archivo con los cambios deseados.

3. **Añadir y Confirmar Cambios**:
   - Añade el archivo resuelto a la etapa de preparación (`staging area`):
     ```bash
     git add nombre-del-archivo
     ```
   - Realiza un `commit` para registrar la resolución del conflicto:
     ```bash
     git commit -m "Resuelto conflicto en nombre-del-archivo"
     ```

#### 3. Actualización del Repositorio

1. **Hacer Pull**:
   - Asegúrate de integrar los últimos cambios del repositorio remoto antes de realizar un `push`:
     ```bash
     git pull origin nombre-de-la-rama
     ```

   - Si hay más conflictos, repite el proceso de resolución como se describe anteriormente.

2. **Hacer Push**:
   - Una vez resueltos todos los conflictos y confirmados los cambios, sube tus cambios al repositorio remoto:
     ```bash
     git push origin nombre-de-la-rama
     ```

### Notas Adicionales

- **Conflictos de Merge**: Los conflictos pueden ocurrir cuando dos o más ramas modifican la misma parte de un archivo. Es importante revisar cuidadosamente los conflictos y decidir cómo combinarlos para mantener la integridad del código.

- **Archivos No Rastreables**: Si tienes nuevos archivos que no están siendo rastreados por Git, añádelos a la etapa de preparación y confirma los cambios como se describe en los pasos anteriores.

- **Abortar un Merge**: Si el proceso de `merge` se vuelve demasiado complejo o si decides que no deseas realizar el `merge`, puedes abortar el proceso con el siguiente comando:
  ```bash
  git merge --abort
  ```

Esta documentación te ayudará a gestionar los conflictos y mantener un flujo de trabajo eficiente en tu proyecto. Si encuentras problemas específicos o necesitas ayuda adicional, consulta la [documentación oficial de Git](https://git-scm.com/doc) o busca asistencia en la comunidad.

---

## Integración de Archivos CSV

Este proyecto incluye un proceso para combinar dos archivos CSV que contienen información sobre películas. A continuación, se describe el procedimiento utilizado para integrar estos archivos y asegurar que la información sea completa y precisa.

### Descripción del Proyecto

El propósito de este proceso es consolidar datos de dos fuentes diferentes en un solo archivo CSV. La única columna común entre los dos archivos es `id_film`, que se utiliza para alinear la información de ambos conjuntos de datos. El resultado es un archivo unificado que conserva todos los datos de ambos archivos originales.

### Archivos de Entrada

- **`movie_dataset_cleaned.csv`**: Primer archivo CSV que contiene datos sobre películas, incluyendo columnas como `budget`, `revenue`, y `runtime`.
- **`df_unido.csv`**: Segundo archivo CSV que contiene información adicional sobre las películas, pero puede tener columnas diferentes.

### Procedimiento de Integración

1. **Carga de Archivos CSV**:
   Los archivos CSV se cargan en dos DataFrames de pandas.

2. **Conversión de Tipo de Datos**:
   La columna `id_film` en ambos DataFrames se convierte a tipo numérico (`int`) para asegurar que la combinación de datos sea precisa. Los valores no numéricos se manejan como `NaN` y luego se rellenan con 0.

3. **Combinación de DataFrames**:
   Se realiza una combinación `outer` en los DataFrames usando la columna `id_film` como clave. Esto asegura que todas las filas de ambos DataFrames se conserven en el DataFrame resultante.

4. **Manejo de Columnas Duplicadas y Datos Faltantes**:
   La combinación `outer` puede resultar en columnas duplicadas y valores `NaN` en las columnas que no están presentes en ambos archivos. Es posible que se requiera una revisión adicional para manejar estos aspectos.

5. **Guardado del Archivo Unificado**:
   El DataFrame resultante se guarda en un nuevo archivo CSV llamado `combined_dataset.csv`.

### Código Utilizado

A continuación se muestra el código utilizado para realizar la integración de los archivos:

```python
import pandas as pd
import os

# Cargar los dos archivos CSV
file_path_1 = "D:/SOYHENRY_PI_1/fastapi_project/movie_dataset_cleaned.csv"
file_path_2 = "D:/SOYHENRY_PI_1/fastapi_project/df_unido.csv"

df1 = pd.read_csv(file_path_1)
df2 = pd.read_csv(file_path_2)

# Verificar las columnas en ambos DataFrames
print("Columnas en df1:", df1.columns)
print("Columnas en df2:", df2.columns)

# Convertir 'id_film' a tipo numérico en ambos DataFrames
df1['id_film'] = pd.to_numeric(df1['id_film'], errors='coerce').fillna(0).
