from typing import Optional
import logging
from uuid import UUID

from contracts.schemas import RawDocument, FeatureSet, PredictionResult

# Interfaces abstractas (Protocolos) para desacoplar implementaciones reales
# En un futuro, estas podrían moverse a un archivo interfaces.py
class IngestionSource:
    def validate(self, doc: RawDocument) -> bool:
        ...

class Preprocessor:
    def process(self, doc: RawDocument) -> FeatureSet:
        ...

class InferenceModel:
    def predict(self, features: FeatureSet) -> PredictionResult:
        ...

class Storage:
    def save(self, result: PredictionResult) -> None:
        ...

class PipelineOrchestrator:
    """
    Coordinator central del flujo de datos canónico.
    Responsabilidad: Asegurar que el dato pase de A -> B -> C sin violar contratos.
    """
    def __init__(
        self, 
        preprocessor: Preprocessor,
        model: InferenceModel,
        storage: Storage
    ):
        self.preprocessor = preprocessor
        self.model = model
        self.storage = storage
        self.logger = logging.getLogger(__name__)

    def run_sync(self, document: RawDocument) -> Optional[PredictionResult]:
        """
        Ejecución síncrona del pipeline (Blocking).
        Útil para pruebas o endpoints realtime críticos.
        """
        try:
            self.logger.info(f"Starting pipeline for trace_id={document.trace_id}")

            # 1. Preprocessing
            # Transforma RawDocument -> FeatureSet
            features = self.preprocessor.process(document)
            
            # Validación de integridad post-proceso
            if not features.clean_text:
                self.logger.warning(f"Empty text after preprocessing for trace_id={document.trace_id}")
                return None

            # 2. Inference
            # Transforma FeatureSet -> PredictionResult
            prediction = self.model.predict(features)

            # 3. Storage / Action
            self.storage.save(prediction)

            self.logger.info(
                f"Pipeline finished. trace_id={document.trace_id}, "
                f"prediction={prediction.predicted_class}, "
                f"confidence={prediction.confidence:.2f}"
            )
            return prediction

        except Exception as e:
            self.logger.error(f"Pipeline failed for trace_id={document.trace_id}: {str(e)}", exc_info=True)
            # Aquí podríamos implementar lógica de Dead Letter Queue (DLQ)
            raise e
