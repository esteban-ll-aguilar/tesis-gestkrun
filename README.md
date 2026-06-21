# GESTKRUN

Sistema de gestión de proyectos Scrum con tablero Kanban, backlog, sprints, métricas y artefactos.

## Stack

- **Backend**: Python 3.14, FastAPI, SQLAlchemy, PostgreSQL, Redis
- **Frontend**: React 19, TypeScript 6, Vite 8, Tailwind 4, Recharts
- **Infra**: Docker, Docker Compose, Nginx, PgBouncer

## Requisitos

- Docker + Docker Compose
- Node.js 22+ (desarrollo local frontend)
- Python 3.14 (desarrollo local backend)

## Inicio rápido

```bash
# Clonar e iniciar todo el stack
git clone <repo>
cd tesis-gestkrun
make up

# Ejecutar migraciones
make migrate

# Ver logs
make logs

# Ejecutar tests
make test

# Detener
make down
```

## Desarrollo local

### Backend

```bash
cd tesis-gestkrun-api
cp .env.example .env
poetry install
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload
```

### Frontend

```bash
cd tesis-gestkrun-web
cp .env.example .env
npm install --legacy-peer-deps
npm run dev
```

## Tests

```bash
# Backend (unitarios + integración)
make test

# Backend con cobertura
make test-coverage

# Frontend (si vitest configurado)
cd tesis-gestkrun-web && npx vitest run

# E2E (Playwright)
cd tesis-gestkrun-web && npx playwright test
```

## Estructura del proyecto

```
tesis-gestkrun/
├── tesis-gestkrun-api/       # FastAPI backend
│   ├── app/
│   │   ├── api/              # Endpoints REST
│   │   ├── application/      # Casos de uso
│   │   ├── core/             # Configuración, DB
│   │   ├── domain/           # Entidades, VOs, servicios
│   │   └── infrastructure/   # Persistencia, auth
│   └── tests/                # Tests
├── tesis-gestkrun-web/       # React frontend
│   ├── src/
│   │   ├── app/              # Router, layouts
│   │   ├── features/         # Servicios por feature
│   │   ├── pages/            # Páginas (rutas)
│   │   └── services/         # HTTP client
│   └── e2e/                  # Tests E2E Playwright
├── docker/                   # Docker Compose
└── .github/workflows/        # CI/CD
```

## API endpoints principales

- `POST /api/v1/auth/register` — Registro
- `POST /api/v1/auth/login` — Login (JWT)
- `GET/POST /api/v1/projects` — CRUD proyectos
- `GET/POST /api/v1/projects/{id}/backlog` — Backlog
- `POST /api/v1/projects/{id}/sprints` — Planificar sprint
- `GET /api/v1/boards/{sprintId}` — Tablero Kanban
- `PATCH /api/v1/boards/tasks/{id}/transition` — Mover tarea
- `POST /api/v1/projects/{id}/messages` — Chat
- `POST /api/v1/artifacts` — Subir artefacto
- `GET /api/v1/dashboard/{id}/metrics` — Métricas
