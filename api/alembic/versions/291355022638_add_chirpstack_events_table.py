"""add chirpstack events table

Revision ID: 291355022638
Revises: migrate_data_v1
Create Date: 2025-11-10 21:23:29.174643

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = "291355022638"
down_revision: Union[str, None] = "migrate_data_v1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Criar tabela chirpstack_events
    op.create_table(
        "chirpstack_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_type", sa.String(length=50), nullable=False),
        sa.Column("dev_eui", sa.String(length=16), nullable=False),
        sa.Column("device_name", sa.String(length=255), nullable=True),
        sa.Column("application_name", sa.String(length=255), nullable=True),
        sa.Column("event_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deduplication_id", sa.String(length=100), nullable=True),
        sa.Column("f_cnt", sa.Integer(), nullable=True),
        sa.Column("f_port", sa.Integer(), nullable=True),
        sa.Column("dr", sa.Integer(), nullable=True),
        sa.Column("rssi", sa.Integer(), nullable=True),
        sa.Column("snr", sa.Integer(), nullable=True),
        sa.Column("frequency", sa.Integer(), nullable=True),
        sa.Column("spreading_factor", sa.Integer(), nullable=True),
        sa.Column("log_level", sa.String(length=50), nullable=True),
        sa.Column("log_code", sa.String(length=100), nullable=True),
        sa.Column("log_description", sa.Text(), nullable=True),
        sa.Column("payload", JSONB, nullable=False),
        sa.Column(
            "received_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Criar índices
    op.create_index(
        "idx_chirpstack_events_event_type", "chirpstack_events", ["event_type"]
    )
    op.create_index("idx_chirpstack_events_dev_eui", "chirpstack_events", ["dev_eui"])
    op.create_index(
        "idx_chirpstack_events_event_time", "chirpstack_events", ["event_time"]
    )
    op.create_index(
        "idx_chirpstack_events_deduplication_id",
        "chirpstack_events",
        ["deduplication_id"],
    )
    op.create_index(
        "idx_chirpstack_events_received_at", "chirpstack_events", ["received_at"]
    )

    # Criar índices compostos
    op.create_index(
        "idx_dev_eui_event_time", "chirpstack_events", ["dev_eui", "event_time"]
    )
    op.create_index(
        "idx_event_type_event_time", "chirpstack_events", ["event_type", "event_time"]
    )


def downgrade() -> None:
    # Remover índices compostos
    op.drop_index("idx_event_type_event_time", table_name="chirpstack_events")
    op.drop_index("idx_dev_eui_event_time", table_name="chirpstack_events")

    # Remover índices
    op.drop_index("idx_chirpstack_events_received_at", table_name="chirpstack_events")
    op.drop_index(
        "idx_chirpstack_events_deduplication_id", table_name="chirpstack_events"
    )
    op.drop_index("idx_chirpstack_events_event_time", table_name="chirpstack_events")
    op.drop_index("idx_chirpstack_events_dev_eui", table_name="chirpstack_events")
    op.drop_index("idx_chirpstack_events_event_type", table_name="chirpstack_events")

    # Remover tabela
    op.drop_table("chirpstack_events")
