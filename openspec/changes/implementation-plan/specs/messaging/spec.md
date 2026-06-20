# Spec: Messaging

## Description
Mensajería asíncrona textual a nivel de proyecto y tarea, con WebSockets para tiempo real e historial paginado.

## Requirements

### RMS-01: Message scopes
- Mensajes a nivel de proyecto: chat general del equipo
- Mensajes a nivel de tarea: discusión específica de una tarjeta

### RMS-02: REST endpoints
- GET /projects/{id}/messages — historial paginado (cursor-based)
- POST /projects/{id}/messages — enviar mensaje
- GET /tasks/{id}/messages — historial paginado
- POST /tasks/{id}/messages — enviar mensaje

### RMS-03: WebSocket
- Conexión WebSocket por proyecto
- Eventos: new_message, message_read
- Notificaciones en tiempo real

### RMS-04: Pagination
- Cursor-based (por fecha de envío)
- 50 mensajes por página
- Scroll infinito en frontend

### RMS-05: Frontend
- Chat panel: lista de mensajes + input
- Scroll automático a nuevo mensaje
- Indicador de "escribiendo"
- Timestamps relativos
- Avatar + nombre del remitente