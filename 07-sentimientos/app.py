from contextlib import asynccontextmanager
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_NAME = "Juanillaberia/spanish-fake-news-classifier"
ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    model.eval()
    ml_models["tokenizer"] = tokenizer
    ml_models["model"] = model
    yield
    ml_models.clear()

app = FastAPI(
    title="API Detector de Noticias Falsas",
    description="Clasificador de noticias en español (Real vs. Fake) usando BETO.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

class NewsRequest(BaseModel):
    text: str = Field(..., min_length=20, description="Cuerpo completo o párrafos de la noticia a evaluar.")
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "El Banco Central anunció este martes que mantendrá la tasa de interés de referencia sin cambios..."
            }
        }
    )

class PredictionResponse(BaseModel):
    label: str
    confidence: float
    is_fake: bool

@app.get("/health", tags=["Sistema"])
def health_check():
    return {"status": "ok", "model_loaded": "model" in ml_models}

@app.post("/predict", response_model=PredictionResponse, tags=["Clasificación"])
def predict_news(request: NewsRequest):
    if "model" not in ml_models:
        raise HTTPException(status_code=503, detail="El modelo aún no está listo.")
    
    tokenizer, model = ml_models["tokenizer"], ml_models["model"]
    inputs = tokenizer(request.text, truncation=True, max_length=512, padding="max_length", return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)
        # probabilities, se selecciona el primer elemento [0]
        probabilities = torch.softmax(outputs.logits, dim=-1)[0]
        predicted_id = torch.argmax(probabilities).item()
        confidence = probabilities[predicted_id].item()
    
    is_fake = (predicted_id == 0)
    return PredictionResponse(
        label="Fake" if is_fake else "Real",
        confidence=round(confidence, 4),
        is_fake=is_fake
    )
