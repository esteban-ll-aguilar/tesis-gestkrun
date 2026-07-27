#!/usr/bin/env python3
"""
init_db.py — Script de inicialización de base de datos.

Lee las entidades del diagrama de clases PSM y genera el esquema
relacional en PostgreSQL, incluyendo tipos enumerados, constraints
de integridad referencial e índices GIN para búsquedas textuales.

Uso:
    python scripts/init_db.py

Requiere:
    - Variable de entorno DATABASE_URL con la conexión a PostgreSQL
    - O pasar --database-url por línea de comando
"""

import argparse
import asyncio
import os
import sys

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


SQL_ENUMS = """
DO $$ BEGIN
    CREATE TYPE rol AS ENUM ('ADMIN', 'PRODUCT_OWNER', 'SCRUM_MASTER', 'DEVELOPER');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE estado_tarea AS ENUM ('PENDIENTE', 'EN_PROCESO', 'BLOQUEADO', 'EN_REVISION', 'TERMINADO', 'CANCELADO');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE estado_sprint AS ENUM ('PLANIFICADO', 'EN_EJECUCION', 'FINALIZADO', 'CANCELADO');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE estado_proyecto AS ENUM ('ACTIVO', 'INACTIVO', 'FINALIZADO', 'CANCELADO');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE estado_modulo AS ENUM ('ACTIVO', 'INACTIVO');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE prioridad AS ENUM ('BAJA', 'MEDIA', 'ALTA', 'CRITICA');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE tipo_artefacto AS ENUM ('REQUISITO', 'DIAGRAMA', 'ACTA', 'DOCUMENTO', 'CODIGO');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE tipo_mensaje AS ENUM ('PROYECTO', 'TAREA');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE tipo_evento_scrum AS ENUM ('SPRINT_PLANNING', 'DAILY_SCRUM', 'SPRINT_REVIEW', 'SPRINT_RETROSPECTIVE');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;
"""

SQL_TABLES = """
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(512) NOT NULL,
    rol rol NOT NULL DEFAULT 'DEVELOPER',
    fecha_registro TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS projects (
    id VARCHAR(36) PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL DEFAULT '',
    estado estado_proyecto NOT NULL DEFAULT 'ACTIVO',
    fecha_inicio DATE NOT NULL DEFAULT CURRENT_DATE,
    owner_id VARCHAR(36) NOT NULL REFERENCES users(id),
    wip_limit INT NOT NULL DEFAULT 3,
    deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS modules (
    id VARCHAR(36) PRIMARY KEY,
    project_id VARCHAR(36) NOT NULL REFERENCES projects(id),
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL DEFAULT '',
    estado estado_modulo NOT NULL DEFAULT 'ACTIVO',
    deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS project_assignments (
    id VARCHAR(36) PRIMARY KEY,
    project_id VARCHAR(36) NOT NULL REFERENCES projects(id),
    user_id VARCHAR(36) NOT NULL REFERENCES users(id),
    UNIQUE(project_id, user_id)
);

CREATE TABLE IF NOT EXISTS epicas (
    id VARCHAR(36) PRIMARY KEY,
    project_id VARCHAR(36) NOT NULL REFERENCES projects(id),
    modulo_id VARCHAR(36) REFERENCES modules(id),
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL DEFAULT '',
    prioridad prioridad NOT NULL DEFAULT 'MEDIA',
    orden INT NOT NULL DEFAULT 0,
    deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS historias_usuario (
    id VARCHAR(36) PRIMARY KEY,
    epica_id VARCHAR(36) NOT NULL REFERENCES epicas(id),
    modulo_id VARCHAR(36) REFERENCES modules(id),
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL DEFAULT '',
    criterios_aceptacion TEXT NOT NULL DEFAULT '',
    prioridad prioridad NOT NULL DEFAULT 'MEDIA',
    estimacion INT NOT NULL DEFAULT 1,
    orden INT NOT NULL DEFAULT 0,
    deleted_at TIMESTAMP,
    CONSTRAINT fk_estimacion_fibonacci CHECK (estimacion IN (1, 2, 3, 5, 8, 13, 21))
);

CREATE TABLE IF NOT EXISTS sprints (
    id VARCHAR(36) PRIMARY KEY,
    project_id VARCHAR(36) NOT NULL REFERENCES projects(id),
    nombre VARCHAR(255) NOT NULL,
    objetivo TEXT NOT NULL DEFAULT '',
    duracion_dias INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    estado estado_sprint NOT NULL DEFAULT 'PLANIFICADO',
    meeting_link VARCHAR(512) NOT NULL DEFAULT '',
    deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sprint_eventos (
    id VARCHAR(36) PRIMARY KEY,
    sprint_id VARCHAR(36) NOT NULL REFERENCES sprints(id),
    tipo tipo_evento_scrum NOT NULL,
    fecha_hora TIMESTAMP NOT NULL DEFAULT NOW(),
    notas TEXT NOT NULL DEFAULT '',
    created_by VARCHAR(36) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS tasks (
    id VARCHAR(36) PRIMARY KEY,
    historia_usuario_id VARCHAR(36) NOT NULL REFERENCES historias_usuario(id),
    sprint_id VARCHAR(36) REFERENCES sprints(id),
    assigned_to VARCHAR(36) REFERENCES users(id),
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL DEFAULT '',
    estado estado_tarea NOT NULL DEFAULT 'PENDIENTE',
    fecha_creacion TIMESTAMP NOT NULL DEFAULT NOW(),
    fecha_limite DATE,
    deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS task_state_transitions (
    id VARCHAR(36) PRIMARY KEY,
    task_id VARCHAR(36) NOT NULL REFERENCES tasks(id),
    from_estado estado_tarea NOT NULL,
    to_estado estado_tarea NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    user_id VARCHAR(36) REFERENCES users(id),
    reason TEXT
);

CREATE TABLE IF NOT EXISTS messages (
    id VARCHAR(36) PRIMARY KEY,
    proyecto_id VARCHAR(36) REFERENCES projects(id),
    tarea_id VARCHAR(36) REFERENCES tasks(id),
    sender_id VARCHAR(36) NOT NULL REFERENCES users(id),
    contenido TEXT NOT NULL,
    tipo tipo_mensaje NOT NULL DEFAULT 'PROYECTO',
    fecha_envio TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS artifacts (
    id VARCHAR(36) PRIMARY KEY,
    task_id VARCHAR(36) NOT NULL REFERENCES tasks(id),
    nombre VARCHAR(255) NOT NULL,
    tipo tipo_artefacto NOT NULL DEFAULT 'DOCUMENTO',
    deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS artifact_versions (
    id VARCHAR(36) PRIMARY KEY,
    artifact_id VARCHAR(36) NOT NULL REFERENCES artifacts(id),
    version INT NOT NULL DEFAULT 1,
    file_path VARCHAR(1024) NOT NULL,
    uploaded_by VARCHAR(36) REFERENCES users(id),
    uploaded_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(artifact_id, version)
);
"""

SQL_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_tasks_sprint_id ON tasks(sprint_id);
CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX IF NOT EXISTS idx_tasks_estado ON tasks(estado);
CREATE INDEX IF NOT EXISTS idx_sprints_project_id ON sprints(project_id);
CREATE INDEX IF NOT EXISTS idx_epicas_project_id ON epicas(project_id);
CREATE INDEX IF NOT EXISTS idx_historias_epica_id ON historias_usuario(epica_id);
CREATE INDEX IF NOT EXISTS idx_messages_proyecto_id ON messages(proyecto_id);
CREATE INDEX IF NOT EXISTS idx_artifacts_task_id ON artifacts(task_id);

CREATE INDEX IF NOT EXISTS idx_epicas_titulo_gin ON epicas USING gin(to_tsvector('spanish', titulo || ' ' || descripcion));
CREATE INDEX IF NOT EXISTS idx_historias_titulo_gin ON historias_usuario USING gin(to_tsvector('spanish', titulo || ' ' || descripcion));
"""


async def init_db(database_url: str) -> None:
    print(f"Conectando a: {database_url}")
    engine = create_async_engine(database_url)

    async with engine.begin() as conn:
        print("Creando tipos enumerados...")
        await conn.execute(text(SQL_ENUMS))

        print("Creando tablas...")
        await conn.execute(text(SQL_TABLES))

        print("Creando índices...")
        await conn.execute(text(SQL_INDEXES))

    await engine.dispose()
    print("Base de datos inicializada exitosamente.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inicializa el esquema de base de datos para GESTKRUN"
    )
    parser.add_argument(
        "--database-url",
        default=os.environ.get("DATABASE_URL"),
        help="URL de conexión a PostgreSQL (o variable DATABASE_URL)",
    )
    args = parser.parse_args()

    if not args.database_url:
        print("Error: Debes especificar DATABASE_URL o pasar --database-url")
        sys.exit(1)

    asyncio.run(init_db(args.database_url))


if __name__ == "__main__":
    main()
