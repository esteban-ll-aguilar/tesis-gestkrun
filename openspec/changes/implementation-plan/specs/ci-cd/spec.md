# Spec: CI/CD & Deployment

## Description
Pipeline CI/CD con GitHub Actions, Docker multi-stage builds, linting, testing, security scanning y despliegue a staging.

## Requirements

### RCI-01: GitHub Actions pipeline
- Trigger: push a main, pull requests
- Jobs: lint → test → build → security scan → deploy (staging)
- Matrix para tests (Python 3.12, Node 20)

### RCI-02: Lint
- Backend: Ruff (PEP 8)
- Frontend: ESLint + Prettier
- Verificación en CI (fail on warnings)

### RCI-03: Security scan
- Backend: Bandit, Semgrep
- Frontend: npm audit
- Secrets detection (git leaks)

### RCI-04: Docker builds
- Multi-stage builds para backend y frontend
- Docker Compose para staging
- Imágenes optimizadas (slim)

### RCI-05: Quality gates
- Cobertura ≥ 85% backend
- Cobertura ≥ 75% frontend
- No warnings de linter
- No vulnerabilidades críticas

### RCI-06: README
- Descripción del proyecto
- Stack tecnológico
- Instrucciones de setup (make up)
- Estructura del proyecto
- Enlaces a documentación