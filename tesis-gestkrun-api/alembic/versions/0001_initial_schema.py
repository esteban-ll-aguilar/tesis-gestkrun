"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-06-20
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def create_enum_types():
    sa.Enum("ADMIN", "PRODUCT_OWNER", "SCRUM_MASTER", "DEVELOPER", name="rol_enum").create(op.get_bind())
    sa.Enum(
        "ACTIVO", "INACTIVO", "FINALIZADO", "CANCELADO", name="estado_proyecto_enum"
    ).create(op.get_bind())
    sa.Enum("ACTIVO", "INACTIVO", name="estado_modulo_enum").create(op.get_bind())
    sa.Enum(
        "PLANIFICADO", "EN_EJECUCION", "FINALIZADO", "CANCELADO", name="estado_sprint_enum"
    ).create(op.get_bind())
    sa.Enum(
        "PENDIENTE", "EN_PROCESO", "BLOQUEADO", "EN_REVISION", "TERMINADO", "CANCELADO",
        name="estado_tarea_enum",
    ).create(op.get_bind())
    sa.Enum("BAJA", "MEDIA", "ALTA", "CRITICA", name="prioridad_enum").create(op.get_bind())
    sa.Enum("REQUISITO", "DIAGRAMA", "ACTA", "DOCUMENTO", "CODIGO", name="tipo_artefacto_enum").create(
        op.get_bind()
    )
    sa.Enum("PROYECTO", "TAREA", name="tipo_mensaje_enum").create(op.get_bind())
    sa.Enum(
        "SPRINT_PLANNING", "DAILY_SCRUM", "SPRINT_REVIEW", "SPRINT_RETROSPECTIVE",
        name="tipo_evento_scrum_enum",
    ).create(op.get_bind())


def drop_enum_types():
    sa.Enum(name="tipo_evento_scrum_enum").drop(op.get_bind())
    sa.Enum(name="tipo_mensaje_enum").drop(op.get_bind())
    sa.Enum(name="tipo_artefacto_enum").drop(op.get_bind())
    sa.Enum(name="prioridad_enum").drop(op.get_bind())
    sa.Enum(name="estado_tarea_enum").drop(op.get_bind())
    sa.Enum(name="estado_sprint_enum").drop(op.get_bind())
    sa.Enum(name="estado_modulo_enum").drop(op.get_bind())
    sa.Enum(name="estado_proyecto_enum").drop(op.get_bind())
    sa.Enum(name="rol_enum").drop(op.get_bind())


def upgrade() -> None:
    create_enum_types()

    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("nombre", sa.String(150), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("rol", postgresql.ENUM(name="rol_enum", create_type=False), nullable=False, server_default="DEVELOPER"),
        sa.Column("fecha_registro", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_by", sa.String(36), nullable=True),
        sa.Column("updated_by", sa.String(36), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "projects",
        sa.Column("id", sa.String(36), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("nombre", sa.String(200), nullable=False),
        sa.Column("descripcion", sa.Text, nullable=False, server_default=""),
        sa.Column("estado", postgresql.ENUM(name="estado_proyecto_enum", create_type=False), nullable=False, server_default="ACTIVO"),
        sa.Column("fecha_inicio", sa.Date, nullable=False),
        sa.Column("wip_limit", sa.Integer, nullable=False, server_default="3"),
        sa.Column("owner_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_by", sa.String(36), nullable=True),
        sa.Column("updated_by", sa.String(36), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "project_assignments",
        sa.Column("id", sa.String(36), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("rol", postgresql.ENUM(name="rol_enum", create_type=False), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_by", sa.String(36), nullable=True),
        sa.Column("updated_by", sa.String(36), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "modules",
        sa.Column("id", sa.String(36), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("nombre", sa.String(200), nullable=False),
        sa.Column("descripcion", sa.Text, nullable=False, server_default=""),
        sa.Column("estado", postgresql.ENUM(name="estado_modulo_enum", create_type=False), nullable=False, server_default="ACTIVO"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_by", sa.String(36), nullable=True),
        sa.Column("updated_by", sa.String(36), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "epicas",
        sa.Column("id", sa.String(36), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("titulo", sa.String(200), nullable=False),
        sa.Column("descripcion", sa.Text, nullable=False, server_default=""),
        sa.Column("prioridad", postgresql.ENUM(name="prioridad_enum", create_type=False), nullable=False, server_default="MEDIA"),
        sa.Column("estado", sa.String(20), nullable=False, server_default="ACTIVA"),
        sa.Column("orden", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_by", sa.String(36), nullable=True),
        sa.Column("updated_by", sa.String(36), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "historias_usuario",
        sa.Column("id", sa.String(36), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("epica_id", sa.String(36), sa.ForeignKey("epicas.id"), nullable=False),
        sa.Column("modulo_id", sa.String(36), sa.ForeignKey("modules.id"), nullable=True),
        sa.Column("titulo", sa.String(200), nullable=False),
        sa.Column("descripcion", sa.Text, nullable=False, server_default=""),
        sa.Column("criterios_aceptacion", sa.Text, nullable=False, server_default=""),
        sa.Column("prioridad", postgresql.ENUM(name="prioridad_enum", create_type=False), nullable=False, server_default="MEDIA"),
        sa.Column("estimacion", sa.Integer, nullable=False, server_default="0"),
        sa.Column("orden", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_by", sa.String(36), nullable=True),
        sa.Column("updated_by", sa.String(36), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "sprints",
        sa.Column("id", sa.String(36), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("project_id", sa.String(36), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("nombre", sa.String(200), nullable=False),
        sa.Column("objetivo", sa.Text, nullable=False, server_default=""),
        sa.Column("duracion_dias", sa.Integer, nullable=False),
        sa.Column("fecha_inicio", sa.Date, nullable=False),
        sa.Column("fecha_fin", sa.Date, nullable=False),
        sa.Column("estado", postgresql.ENUM(name="estado_sprint_enum", create_type=False), nullable=False, server_default="PLANIFICADO"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_by", sa.String(36), nullable=True),
        sa.Column("updated_by", sa.String(36), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "sprint_eventos",
        sa.Column("id", sa.String(36), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("sprint_id", sa.String(36), sa.ForeignKey("sprints.id"), nullable=False),
        sa.Column("tipo", postgresql.ENUM(name="tipo_evento_scrum_enum", create_type=False), nullable=False),
        sa.Column("fecha", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("notas", sa.Text, nullable=False, server_default=""),
        sa.Column("duracion_minutos", sa.Integer, nullable=False),
        sa.Column("created_by", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
    )

    op.create_table(
        "tasks",
        sa.Column("id", sa.String(36), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("historia_usuario_id", sa.String(36), sa.ForeignKey("historias_usuario.id"), nullable=False),
        sa.Column("sprint_id", sa.String(36), sa.ForeignKey("sprints.id"), nullable=True),
        sa.Column("assigned_to", sa.String(36), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("titulo", sa.String(200), nullable=False),
        sa.Column("descripcion", sa.Text, nullable=False, server_default=""),
        sa.Column("estado", postgresql.ENUM(name="estado_tarea_enum", create_type=False), nullable=False, server_default="PENDIENTE"),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("fecha_limite", sa.Date, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_by", sa.String(36), nullable=True),
        sa.Column("updated_by", sa.String(36), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.execute(
        """
        CREATE TABLE task_state_transitions (
            id VARCHAR(36) NOT NULL DEFAULT gen_random_uuid(),
            task_id VARCHAR(36) NOT NULL REFERENCES tasks(id),
            from_estado estado_tarea_enum NOT NULL,
            to_estado estado_tarea_enum NOT NULL,
            timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            user_id VARCHAR(36) NOT NULL REFERENCES users(id),
            reason TEXT,
            PRIMARY KEY (id, timestamp)
        ) PARTITION BY RANGE (timestamp)
        """
    )

    op.execute(
        """
        CREATE TABLE task_state_transitions_2026_01 PARTITION OF task_state_transitions
        FOR VALUES FROM ('2026-01-01') TO ('2026-02-01')
        """
    )
    op.execute(
        """
        CREATE TABLE task_state_transitions_2026_02 PARTITION OF task_state_transitions
        FOR VALUES FROM ('2026-02-01') TO ('2026-03-01')
        """
    )
    op.execute(
        """
        CREATE TABLE task_state_transitions_2026_03 PARTITION OF task_state_transitions
        FOR VALUES FROM ('2026-03-01') TO ('2026-04-01')
        """
    )
    op.execute(
        """
        CREATE TABLE task_state_transitions_2026_04 PARTITION OF task_state_transitions
        FOR VALUES FROM ('2026-04-01') TO ('2026-05-01')
        """
    )
    op.execute(
        """
        CREATE TABLE task_state_transitions_2026_05 PARTITION OF task_state_transitions
        FOR VALUES FROM ('2026-05-01') TO ('2026-06-01')
        """
    )
    op.execute(
        """
        CREATE TABLE task_state_transitions_2026_06 PARTITION OF task_state_transitions
        FOR VALUES FROM ('2026-06-01') TO ('2026-07-01')
        """
    )
    op.execute(
        """
        CREATE TABLE task_state_transitions_2026_07 PARTITION OF task_state_transitions
        FOR VALUES FROM ('2026-07-01') TO ('2026-08-01')
        """
    )
    op.execute(
        """
        CREATE TABLE task_state_transitions_2026_08 PARTITION OF task_state_transitions
        FOR VALUES FROM ('2026-08-01') TO ('2026-09-01')
        """
    )
    op.execute(
        """
        CREATE TABLE task_state_transitions_2026_09 PARTITION OF task_state_transitions
        FOR VALUES FROM ('2026-09-01') TO ('2026-10-01')
        """
    )
    op.execute(
        """
        CREATE TABLE task_state_transitions_2026_10 PARTITION OF task_state_transitions
        FOR VALUES FROM ('2026-10-01') TO ('2026-11-01')
        """
    )
    op.execute(
        """
        CREATE TABLE task_state_transitions_2026_11 PARTITION OF task_state_transitions
        FOR VALUES FROM ('2026-11-01') TO ('2026-12-01')
        """
    )
    op.execute(
        """
        CREATE TABLE task_state_transitions_2026_12 PARTITION OF task_state_transitions
        FOR VALUES FROM ('2026-12-01') TO ('2027-01-01')
        """
    )
    op.execute(
        """
        CREATE TABLE task_state_transitions_default PARTITION OF task_state_transitions
        DEFAULT
        """
    )

    op.create_table(
        "messages",
        sa.Column("id", sa.String(36), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("proyecto_id", sa.String(36), sa.ForeignKey("projects.id"), nullable=True),
        sa.Column("task_id", sa.String(36), sa.ForeignKey("tasks.id"), nullable=True),
        sa.Column("sender_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("contenido", sa.Text, nullable=False),
        sa.Column("fecha_envio", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("tipo", postgresql.ENUM(name="tipo_mensaje_enum", create_type=False), nullable=False),
    )

    op.create_table(
        "artifacts",
        sa.Column("id", sa.String(36), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("task_id", sa.String(36), sa.ForeignKey("tasks.id"), nullable=False),
        sa.Column("nombre", sa.String(255), nullable=False),
        sa.Column("tipo", postgresql.ENUM(name="tipo_artefacto_enum", create_type=False), nullable=False),
        sa.Column("version_actual", sa.Integer, nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_by", sa.String(36), nullable=True),
        sa.Column("updated_by", sa.String(36), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "artifact_versions",
        sa.Column("id", sa.String(36), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("artifact_id", sa.String(36), sa.ForeignKey("artifacts.id"), nullable=False),
        sa.Column("version", sa.Integer, nullable=False),
        sa.Column("content_url", sa.String(500), nullable=False),
        sa.Column("uploaded_by", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_index("uq_users_email_active", "users", ["email"], unique=True,
                     postgresql_where=sa.text("deleted_at IS NULL"))
    op.create_index("ix_tasks_assigned_estado", "tasks", ["assigned_to", "estado"],
                     postgresql_where=sa.text("deleted_at IS NULL"))
    op.create_index("ix_tasks_sprint_estado", "tasks", ["sprint_id", "estado"],
                     postgresql_where=sa.text("deleted_at IS NULL"))
    op.create_index("ix_task_transitions_task_timestamp", "task_state_transitions", ["task_id", "timestamp"])
    op.create_index("ix_messages_proyecto_fecha", "messages", ["proyecto_id", "fecha_envio"])
    op.create_index("ix_messages_task_fecha", "messages", ["task_id", "fecha_envio"])
    op.create_index("ix_epicas_project_orden", "epicas", ["project_id", "orden"])
    op.create_index("ix_historias_epica_orden", "historias_usuario", ["epica_id", "orden"])

    op.execute(
        """
        CREATE MATERIALIZED VIEW mv_dashboard_metrics AS
        SELECT
            p.id AS project_id,
            COUNT(DISTINCT t.id) AS total_tasks,
            COALESCE(jsonb_agg(DISTINCT jsonb_build_object('estado', t.estado, 'count', cnt.cnt)) FILTER (WHERE cnt.cnt IS NOT NULL), '[]'::jsonb) AS tasks_by_status
        FROM projects p
        LEFT JOIN sprints s ON s.project_id = p.id AND s.deleted_at IS NULL
        LEFT JOIN tasks t ON t.sprint_id = s.id AND t.deleted_at IS NULL
        LEFT JOIN (
            SELECT estado, COUNT(*) AS cnt FROM tasks WHERE deleted_at IS NULL GROUP BY estado
        ) cnt ON cnt.estado = t.estado
        WHERE p.deleted_at IS NULL
        GROUP BY p.id
        WITH DATA
        """
    )

    op.execute(
        """
        CREATE UNIQUE INDEX idx_mv_dashboard_metrics_project ON mv_dashboard_metrics (project_id)
        """
    )

    op.execute(
        """
        CREATE MATERIALIZED VIEW mv_sprint_velocity AS
        SELECT
            s.id AS sprint_id,
            s.project_id,
            COALESCE(SUM(CASE WHEN hu.estimacion IS NOT NULL THEN hu.estimacion ELSE 0 END), 0) AS planned_points,
            COALESCE(SUM(CASE WHEN t.estado IN ('TERMINADO') AND hu.estimacion IS NOT NULL THEN hu.estimacion ELSE 0 END), 0) AS completed_points
        FROM sprints s
        LEFT JOIN tasks t ON t.sprint_id = s.id AND t.deleted_at IS NULL
        LEFT JOIN historias_usuario hu ON hu.id = t.historia_usuario_id
        WHERE s.deleted_at IS NULL
        GROUP BY s.id, s.project_id
        WITH DATA
        """
    )

    op.execute(
        """
        CREATE UNIQUE INDEX idx_mv_sprint_velocity_sprint ON mv_sprint_velocity (sprint_id)
        """
    )


def downgrade() -> None:
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_sprint_velocity CASCADE")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_dashboard_metrics CASCADE")

    op.drop_index("ix_historias_epica_orden", table_name="historias_usuario")
    op.drop_index("ix_epicas_project_orden", table_name="epicas")
    op.drop_index("ix_messages_task_fecha", table_name="messages")
    op.drop_index("ix_messages_proyecto_fecha", table_name="messages")
    op.drop_index("ix_task_transitions_task_timestamp", table_name="task_state_transitions")
    op.drop_index("ix_tasks_sprint_estado", table_name="tasks")
    op.drop_index("ix_tasks_assigned_estado", table_name="tasks")
    op.drop_index("uq_users_email_active", table_name="users")

    op.drop_table("artifact_versions")
    op.drop_table("artifacts")
    op.drop_table("messages")

    op.execute("DROP TABLE IF EXISTS task_state_transitions CASCADE")

    op.drop_table("tasks")
    op.drop_table("sprint_eventos")
    op.drop_table("sprints")
    op.drop_table("historias_usuario")
    op.drop_table("epicas")
    op.drop_table("modules")
    op.drop_table("project_assignments")
    op.drop_table("projects")
    op.drop_table("users")

    drop_enum_types()
