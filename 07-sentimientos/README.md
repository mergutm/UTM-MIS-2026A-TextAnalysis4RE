# API Detector de Noticias Falsas en Español

Servicio contenedorizado basado en FastAPI y el modelo `Juanillaberia/spanish-fake-news-classifier` para clasificar noticias en español como reales (`Real`) o falsas (`Fake`).

---

## a) Gestión del Contenedor (Encendido y Apagado)

### Construir e iniciar el servicio
Ejecutar el siguiente comando en la raíz del proyecto para construir la imagen e iniciar el contenedor en segundo plano:
```bash
docker compose up -d --build
```

### Detener y eliminar el contenedor
Para detener el servicio y liberar los recursos de red y memoria:
```bash
docker compose down
```

### Verificar estado y registros (logs)
```bash
docker compose logs -f
```

---

## b) FastAPI y Swagger UI

### FastAPI
Es un framework web de alto rendimiento para construir APIs con Python. 
* **Funcionamiento:** Utiliza tipado estándar de Python (mediante Pydantic) para validar automáticamente los datos de entrada y salida, serializar respuestas en formato JSON y gestionar el ciclo de vida del modelo de inteligencia artificial en memoria RAM.

### Swagger UI
Es una interfaz gráfica e interactiva integrada automáticamente por FastAPI.
* **Funcionamiento:** Lee los esquemas y rutas definidos en el código Python para generar una página web accesible en `http://localhost:8000/docs`. Permite visualizar los parámetros requeridos, revisar ejemplos y ejecutar peticiones HTTP reales directamente desde el navegador sin herramientas externas.

---

## c) Generación de Peticiones (`@app.get` y `@app.post`)

En FastAPI, los decoradores `@app.get` y `@app.post` vinculan rutas URL específicas con funciones de Python según el método HTTP.

### Peticiones GET (`@app.get`)
Se utilizan para consultar información o verificar el estado del sistema sin enviar datos en el cuerpo de la petición.

* **Definición en código:**
  ```python
  @app.get("/health")
  def health_check():
      return {"status": "ok"}
  ```
* **Consumo mediante terminal (`curl`):**
  ```bash
  curl -X GET "http://localhost:8000/health"
  ```

### Peticiones POST (`@app.post`)
Se utilizan para enviar datos estructurados (en formato JSON) hacia el servidor para que sean procesados por el modelo.

* **Definición en código:**
  ```python
  @app.post("/predict")
  def predict_news(request: NewsRequest):
      # Procesamiento del texto recibido en request.text
      return {"label": "Real", "confidence": 0.95, "is_fake": False}
  ```
* **Consumo mediante terminal (`curl`):**
  ```bash
  curl -X POST "http://localhost:8000/predict" \
       -H "Content-Type: application/json" \
       -d '{"text": "Texto completo de la noticia a evaluar..."}'
  ```
