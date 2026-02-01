from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict

# ==========================================
# CONTRACT A: Ingestion Output
# ==========================================
class RawDocument(BaseModel):
    """
    Representa un documento crudo ingresado al sistema desde cualquier fuente.
    Este es el contrato entre Ingestion y Preprocessing.
    """
    model_config = ConfigDict(frozen=True)  # Inmutable

    trace_id: UUID = Field(default_factory=uuid4, description="ID único de traza para observabilidad")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_type: str = Field(..., description="Origen del dato: 'jira', 'slack', 'email', 'api'")
    original_id: Optional[str] = Field(None, description="ID en el sistema de origen")
    payload: str = Field(..., description="Contenido de texto crudo a clasificar")
    metadata: Dict = Field(default_factory=dict, description="Contexto extra no utilizado para inferencia")


# ==========================================
# CONTRACT B: Preprocessing Output
# ==========================================
class FeatureSet(BaseModel):
    """
    Representa los datos limpios y transformados listos para el modelo.
    Este es el contrato entre Preprocessing e Inference.
    """
    model_config = ConfigDict(frozen=True)

    trace_id: UUID
    clean_text: str = Field(..., description="Texto normalizado (lowercase, sin punc, etc)")
    tokens: List[str] = Field(default_factory=list)
    embedding: Optional[List[float]] = Field(None, description="Vector pre-calculado si aplica")
    features_version: str = Field(..., description="Versión de la lógica de limpieza")


# ==========================================
# CONTRACT C: Inference Output
# ==========================================
class PredictionResult(BaseModel):
    """
    El resultado final de la clasificación.
    Este es el contrato entre Inference y Storage/Consumers.
    """
    model_config = ConfigDict(frozen=True)

    trace_id: UUID
    model_name: str
    model_version: str
    predicted_class: str = Field(..., description="Clase predicha: 'bug', 'feature', 'debt', etc")
    confidence: float = Field(..., ge=0.0, le=1.0)
    inference_time_ms: int = Field(..., description="Latencia de la inferencia en milisegundos")
