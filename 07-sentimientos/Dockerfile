FROM python:3.11-slim

# Evitar archivos .pyc y habilitar logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/app/hf_cache

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-descargar el modelo durante el build para evitar descargas al iniciar
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
    AutoTokenizer.from_pretrained('Juanillaberia/spanish-fake-news-classifier'); \
    AutoModelForSequenceClassification.from_pretrained('Juanillaberia/spanish-fake-news-classifier')"

# Copiar el código de la aplicación
COPY app.py .

EXPOSE 8000

# Ejecutar con 1 worker (ideal para modelos pesados en RAM; escalar horizontalmente con más contenedores)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
