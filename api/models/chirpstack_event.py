from database import Base
from sqlalchemy import Column, DateTime, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func


class ChirpStackEvent(Base):
    """Model para armazenar eventos do ChirpStack recebidos via webhook."""

    __tablename__ = "chirpstack_events"

    id = Column(Integer, primary_key=True, index=True)

    # Tipo de evento: up, log, join, etc.
    event_type = Column(String(50), nullable=False, index=True)

    # Informações do dispositivo extraídas para facilitar queries
    dev_eui = Column(String(16), nullable=False, index=True)
    device_name = Column(String(255), nullable=True)
    application_name = Column(String(255), nullable=True)

    # Timestamp do evento (do payload do ChirpStack)
    event_time = Column(DateTime(timezone=True), nullable=False, index=True)

    # Para eventos 'up'
    deduplication_id = Column(String(100), nullable=True, index=True)
    f_cnt = Column(Integer, nullable=True)  # Frame counter
    f_port = Column(Integer, nullable=True)
    dr = Column(Integer, nullable=True)  # Data rate

    # Para eventos 'up' - informações de RF
    rssi = Column(Integer, nullable=True)  # Signal strength
    snr = Column(Integer, nullable=True)  # Signal to noise ratio
    frequency = Column(Integer, nullable=True)
    spreading_factor = Column(Integer, nullable=True)

    # Para eventos 'log'
    log_level = Column(String(50), nullable=True)
    log_code = Column(String(100), nullable=True)
    log_description = Column(Text, nullable=True)

    # Payload completo em JSON para análise detalhada
    payload = Column(JSONB, nullable=False)

    # Timestamp de quando o evento foi recebido pela API
    received_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    # Índices compostos para queries comuns
    __table_args__ = (
        Index("idx_dev_eui_event_time", "dev_eui", "event_time"),
        Index("idx_event_type_event_time", "event_type", "event_time"),
    )
