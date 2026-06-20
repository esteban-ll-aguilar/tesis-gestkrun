# Spec: Frontend Base

## Description
Estructura base del frontend React con routing, layouts, providers, HTTP client, theme, i18n y componentes compartidos.

## Requirements

### RFB-01: Project structure
- src/app/ — Router, providers, layouts
- src/pages/ — Page components by route
- src/features/ — Feature modules
- src/components/ — Shared UI (shadcn/ui)
- src/hooks/ — Custom hooks
- src/services/ — HTTP client
- src/stores/ — Zustand stores
- src/types/ — TypeScript types
- src/utils/ — Helpers

### RFB-02: Routing
- React Router v6 con lazy loading
- Guards por rol (AdminRoute, PORoute, SMRoute, DevRoute)
- 404 page

### RFB-03: Providers
- QueryClientProvider (TanStack Query)
- AuthProvider (context + Zustand)
- ThemeProvider (dark/light)
- i18nextProvider

### RFB-04: HTTP Client
- Axios instance con base URL e interceptors
- Auth interceptor: adjunta access token
- Refresh interceptor: refresca token en 401, reintenta request
- Error interceptor: mapea errores a toast/notificaciones

### RFB-05: Layouts
- AuthLayout (login, register, recover)
- MainLayout (sidebar + header + content)
- AdminLayout (admin panel)
- KanbanLayout (full-width board)

### RFB-06: Shared components
- DataTable, Pagination, Modal, FormField, Toast, Skeleton, EmptyState, ErrorState, Badge, Avatar, Card, Dropdown

### RFB-07: Theme
- Tailwind CSS + shadcn/ui
- Dark/light mode toggle
- Responsive: desktop primary, tablet secondary

### RFB-08: i18n
- i18next: español (default) + inglés
- Namespaces por feature
- Lazy loading de translations