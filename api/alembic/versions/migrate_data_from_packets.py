"""Migrate data from packets table to new structure

Revision ID: migrate_data_v1
Revises: new_structure_v1
Create Date: 2025-01-XX XX:XX:XX.XXXXXX

Este script migra os dados da tabela antiga 'packets' para a nova estrutura
com 'devices' e 'sensor_readings'.

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "migrate_data_v1"
down_revision: Union[str, None] = "new_structure_v1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Migra dados da tabela 'packets' para a nova estrutura.
    """
    connection = op.get_bind()

    # 1. Criar dispositivos únicos baseados nos device_id da tabela packets
    connection.execute(
        sa.text("""
        INSERT INTO devices (device_uid, description, created_at)
        SELECT DISTINCT 
            device_id as device_uid,
            'Migrated device' as description,
            MIN(timestamp) as created_at
        FROM packets
        WHERE NOT EXISTS (
            SELECT 1 FROM devices WHERE devices.device_uid = packets.device_id
        )
        GROUP BY device_id
    """)
    )

    # 2. Migrar leituras de temperatura (t > 0)
    connection.execute(
        sa.text("""
        INSERT INTO sensor_readings (device_id, sensor_type, value, timestamp)
        SELECT 
            d.id as device_id,
            'temperatura' as sensor_type,
            p.t as value,
            p.timestamp
        FROM packets p
        INNER JOIN devices d ON d.device_uid = p.device_id
        WHERE p.t > 0
    """)
    )

    # 3. Migrar leituras de umidade (h > 0)
    connection.execute(
        sa.text("""
        INSERT INTO sensor_readings (device_id, sensor_type, value, timestamp)
        SELECT 
            d.id as device_id,
            'umidade' as sensor_type,
            p.h as value,
            p.timestamp
        FROM packets p
        INNER JOIN devices d ON d.device_uid = p.device_id
        WHERE p.h > 0
    """)
    )

    # 4. Migrar leituras de gás (g > 0)
    connection.execute(
        sa.text("""
        INSERT INTO sensor_readings (device_id, sensor_type, value, timestamp)
        SELECT 
            d.id as device_id,
            'gas' as sensor_type,
            p.g as value,
            p.timestamp
        FROM packets p
        INNER JOIN devices d ON d.device_uid = p.device_id
        WHERE p.g > 0
    """)
    )

    # 5. Migrar leituras de fluxo (fluxo > 0)
    connection.execute(
        sa.text("""
        INSERT INTO sensor_readings (device_id, sensor_type, value, timestamp)
        SELECT 
            d.id as device_id,
            'fluxo' as sensor_type,
            p.fluxo as value,
            p.timestamp
        FROM packets p
        INNER JOIN devices d ON d.device_uid = p.device_id
        WHERE p.fluxo > 0
    """)
    )

    # 6. Migrar leituras de pulso (pulso > 0)
    connection.execute(
        sa.text("""
        INSERT INTO sensor_readings (device_id, sensor_type, value, timestamp)
        SELECT 
            d.id as device_id,
            'pulso' as sensor_type,
            p.pulso::float as value,
            p.timestamp
        FROM packets p
        INNER JOIN devices d ON d.device_uid = p.device_id
        WHERE p.pulso > 0
    """)
    )

    # 7. Migrar leituras de solo (solo > 0)
    connection.execute(
        sa.text("""
        INSERT INTO sensor_readings (device_id, sensor_type, value, timestamp)
        SELECT 
            d.id as device_id,
            'solo' as sensor_type,
            p.solo as value,
            p.timestamp
        FROM packets p
        INNER JOIN devices d ON d.device_uid = p.device_id
        WHERE p.solo > 0
    """)
    )

    # 8. Migrar leituras de sensor (sensor > 0)
    connection.execute(
        sa.text("""
        INSERT INTO sensor_readings (device_id, sensor_type, value, timestamp)
        SELECT 
            d.id as device_id,
            'sensor' as sensor_type,
            p.sensor::float as value,
            p.timestamp
        FROM packets p
        INNER JOIN devices d ON d.device_uid = p.device_id
        WHERE p.sensor > 0
    """)
    )


def downgrade() -> None:
    """
    Reverter a migração de dados (apenas remove os dados migrados, não restaura packets).
    """
    connection = op.get_bind()

    # Remover dados migrados
    connection.execute(sa.text("DELETE FROM sensor_readings"))
    connection.execute(sa.text("DELETE FROM devices"))
