# Imagen base con Python
FROM python:3.11-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app
RUN pip install kaggle pymongo pandas
# Copiar los archivos del proyecto
COPY etl.py .
COPY requirements.txt .

# Instalar dependencias
RUN pip install -r requirements.txt

# Ejecutar el script ETL al iniciar el contenedor
CMD ["python", "etl.py"]
