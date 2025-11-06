"""Create new structure with devices and sensor_readings tables

Revision ID: new_structure_v1
Revises: bc38cf936955
Create Date: 2025-01-XX XX:XX:XX.XXXXXX

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "new_structure_v1"
down_revision: Union[str, None] = "bc38cf936955"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Criar tabela devices
    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("device_uid", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_devices_id"), "devices", ["id"], unique=False)
    op.create_index(
        op.f("ix_devices_device_uid"), "devices", ["device_uid"], unique=True
    )

    # Criar tabela sensor_readings
    op.create_table(
        "sensor_readings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("device_id", sa.Integer(), nullable=False),
        sa.Column("sensor_type", sa.String(), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["device_id"],
            ["devices.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_sensor_readings_id"), "sensor_readings", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_sensor_readings_device_id"),
        "sensor_readings",
        ["device_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_sensor_readings_sensor_type"),
        "sensor_readings",
        ["sensor_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_sensor_readings_timestamp"),
        "sensor_readings",
        ["timestamp"],
        unique=False,
    )


def downgrade() -> None:
    # Remover índices e tabelas na ordem inversa
    op.drop_index(op.f("ix_sensor_readings_timestamp"), table_name="sensor_readings")
    op.drop_index(op.f("ix_sensor_readings_sensor_type"), table_name="sensor_readings")
    op.drop_index(op.f("ix_sensor_readings_device_id"), table_name="sensor_readings")
    op.drop_index(op.f("ix_sensor_readings_id"), table_name="sensor_readings")
    op.drop_table("sensor_readings")

    op.drop_index(op.f("ix_devices_device_uid"), table_name="devices")
    op.drop_index(op.f("ix_devices_id"), table_name="devices")
    op.drop_table("devices")
