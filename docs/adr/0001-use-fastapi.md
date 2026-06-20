# ADR 0001: FastAPI como Framework Backend

**Fecha:** 2026-06-20\
**Estado:** Aceptado

## Contexto
El backend de GESTKRUN requiere un framework web moderno que soporte programación asíncrona, validación robusta de datos, generación automática de documentación OpenAPI, y tipado fuerte. Las alternativas consideradas fueron Django REST Framework, Flask y FastAPI.

## Decisión
Se adopta **FastAPI 0.110+** como framework backend por las siguientes razones:
- Soporte nativo de async/await para operaciones I/O bound (DB, cache, workers).
- Validación integrada con Pydantic v2 (tipado en requests/responses).
- Generación automática de OpenAPI 3.1 + interfaz Swagger/Redoc.
- Sistema de inyección de dependencias nativo.
- Rendimiento ASGI con Uvicorn/Gunicorn.
- Tipado fuerte con soporte Python 3.12+.

## Consecuencias
- No se puede usar Django ORM (se usa SQLAlchemy 2.0 async).
- La inyección de dependencias de FastAPI reemplaza a DI containers externos.
- Middleware y exception handlers deben implementarse como dependencias ASGI.
- La comunidad de FastAPI ofrece menos paquetes third-party que Django, pero los necesarios están disponibles.

## Alternativas Consideradas
- **Django REST Framework:** maduro, pero su ORM no tiene soporte async nativo completo; más pesado para un diseño Clean Architecture.
- **Flask:** demasiado minimalista, requiere ensamblar muchos componentes externos (validación, DI, docs) que FastAPI provee nativamente.
