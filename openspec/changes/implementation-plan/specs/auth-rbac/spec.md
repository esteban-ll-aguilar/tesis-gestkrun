# Spec: Authentication & RBAC

## Description
Autenticación JWT (access + refresh), registro, login, recovery, y RBAC con permisos por rol y recurso.

## Requirements

### RAR-01: Registration
- POST /auth/register con email, nombre, contraseña
- Validación de email único, contraseña ≥ 8 chars
- Hash Argon2id
- Asignación de rol por defecto (Developer)

### RAR-02: Login
- POST /auth/login con email + contraseña
- Retorna access token (15 min) + refresh token (7 días, httpOnly cookie)
- Rate limiting: 20 req/min

### RAR-03: JWT
- Access token: JWT con sub, rol, exp (15 min)
- Refresh token: JWT con sub, exp (7 días), rotación con invalidación
- Refresh en endpoint dedicado

### RAR-04: RBAC
- Dependencia `get_current_user` para proteger endpoints
- Dependencia `require_role(rol)` para endpoints por rol
- Dependencia `require_project_role(rol)` para permisos dentro de proyecto
- 4 roles: ADMIN, PRODUCT_OWNER, SCRUM_MASTER, DEVELOPER

### RAR-05: Password recovery
- POST /auth/recover-password (solicita)
- POST /auth/reset-password (token por email)

### RAR-06: Frontend
- Login page, Register page, RecoverPassword page
- Auth guard en React Router (redirect a /login)
- Refresh token interceptor automático
- Logout que invalida refresh token