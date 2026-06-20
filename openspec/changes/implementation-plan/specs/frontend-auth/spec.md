# Spec: Frontend Auth

## Description
Login, registro, recovery de contraseña, guards de autenticación y manejo de sesión.

## Requirements

### RFA-01: Login page
- Formulario con email + contraseña
- Validación Zod en frontend
- Loading state, error state
- Redirect a dashboard post-login
- "Recordarme" opcional

### RFA-02: Register page
- Formulario con nombre, email, contraseña, confirmar contraseña
- Validación Zod
- Mensaje de éxito/error
- Redirect a login

### RFA-03: Recover password
- Formulario de email
- Estado: enviado (instrucciones por email)
- Reset password con token

### RFA-04: Auth guard
- React Router guard: redirect a /login si no autenticado
- Role guard: acceso denegado si no tiene rol
- Silent refresh en app startup

### RFA-05: Session management
- Zustand store: user, token, isAuthenticated
- Persistencia de sesión en localStorage (solo metadata, no token)
- Logout: limpia store + invalida refresh token