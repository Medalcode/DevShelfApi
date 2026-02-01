# Skema Implementation Backlog

## 📋 Prioridad 0: Cimientos y Gobernanza (Bloqueante)

### [ARCH-001] Scaffold de "Screaming Architecture" y Entorno Docker

- **Descripción:** Reestructurar el repositorio separando claramente `cmd/` (entrypoints), `internal/` (lógica privada) y `contracts/` (schemas). Configurar `docker-compose` base.
- **Motivación Técnica:** Evitar que el código de infraestructura se mezcle con el dominio desde el día 1. Garantizar entornos reproducibles.
- **Criterios de Aceptación:**
  - [ ] Estructura de carpetas creada: `cmd/api`, `internal/ingestion`, `internal/pipeline`, `contracts`.
  - [ ] `docker-compose.yml` levanta servicios de API (Python) y Redis.
  - [ ] `make run` levanta el stack localmente sin errores.

### [ARCH-002] Definición de Contratos de Datos Inmutables (DTOs)

- **Descripción:** Implementar en `contracts/schemas.py` los modelos Pydantic: `RawDocument`, `FeatureSet` y `PredictionResult`.
- **Motivación Técnica:** Desacoplamiento total. Ingesta e Inferencia no deben compartir lógica, solo estos contratos. Permite desarrollo paralelo.
- **Criterios de Aceptación:**
  - [ ] Modelos definidos con tipado estricto (UUID, float, datetime).
  - [ ] Tests unitarios que validen fallos ante payloads incompletos.
  - [ ] Los modelos son serializables a JSON.

## 🟠 Prioridad 1: Pipeline Core (Lógica de Negocio)

### [PIPE-001] Orquestador del Pipeline Canónico

- **Descripción:** Crear `PipelineOrchestrator` en `internal/pipeline/`. Debe coordinar el flujo: Ingesta → Preprocesamiento → Inferencia → Storage.
- **Motivación Técnica:** Centralizar el control de flujo y manejo de errores. Evitar llamadas directas entre capas hermanas ("Spaghetti code").
- **Criterios de Aceptación:**
  - [ ] El orquestador maneja excepciones y detiene el flujo ordenadamente.
  - [ ] Soporta inyección de dependencias para los componentes del pipeline.

### [PIPE-002] Estrategia de Inferencia Intercambiable

- **Descripción:** Implementar patrón Strategy en `internal/inference`. Interfaz base `ModelStrategy`.
- **Motivación Técnica:** Permitir cambios de modelo (ej. de Random Forest a BERT) sin tocar el orquestador ni la API.
- **Criterios de Aceptación:**
  - [ ] Interfaz `predict(FeatureSet) -> PredictionResult` definida.
  - [ ] Implementación `DummyStrategy` funcional para desarrollo local.

## 🟡 Prioridad 2: Interfaces y Observabilidad

### [API-001] API Gateway "Dumb" (Adaptador)

- **Descripción:** Endpoint `POST /ingest` que solo valide contratos y delegue al pipeline.
- **Motivación Técnica:** Mantener la API libre de lógica de negocio para facilitar migración futura a Workers asíncronos.
- **Criterios de Aceptación:**
  - [ ] Validación estricta de input (422 si falla).
  - [ ] Generación o propagación de `trace_id`.
  - [ ] Respuesta estandarizada.

### [OBS-001] Logging Estructurado con Trace Context

- **Descripción:** Configurar logger para emitir JSON e inyectar `trace_id` en cada paso del pipeline.
- **Motivación Técnica:** Imposible depurar sistemas distribuidos/asíncronos sin trazabilidad unificada.
- **Criterios de Aceptación:**
  - [ ] Logs en formato JSON `{"level": "info", "trace_id": "...", "msg": "..."}`.
  - [ ] Traza visible desde API hasta Storage.
