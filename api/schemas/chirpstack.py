from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ChirpStackWebhookRequest(BaseModel):
    """Schema para receber qualquer tipo de evento do ChirpStack."""

    # Campos comuns a todos os eventos
    time: str
    deviceInfo: Dict[str, Any]

    # Campos opcionais dependendo do tipo de evento
    deduplicationId: Optional[str] = None
    devAddr: Optional[str] = None
    adr: Optional[bool] = None
    dr: Optional[int] = None
    fCnt: Optional[int] = None
    fPort: Optional[int] = None
    confirmed: Optional[bool] = None
    data: Optional[str] = None
    object: Optional[Dict[str, Any]] = None
    rxInfo: Optional[list] = None
    txInfo: Optional[Dict[str, Any]] = None
    regionConfigId: Optional[str] = None

    # Campos para eventos de log
    level: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "time": "2025-11-10T23:28:41.938+00:00",
                "deviceInfo": {
                    "devEui": "45d5e6d1248778f6",
                    "deviceName": "ED LoRa ESP32 - #1",
                },
            }
        }


class ChirpStackEventResponse(BaseModel):
    """Schema de resposta para eventos armazenados."""

    id: int
    event_type: str
    dev_eui: str
    device_name: Optional[str] = None
    application_name: Optional[str] = None
    event_time: datetime
    deduplication_id: Optional[str] = None
    f_cnt: Optional[int] = None
    f_port: Optional[int] = None
    dr: Optional[int] = None
    rssi: Optional[int] = None
    snr: Optional[int] = None
    frequency: Optional[int] = None
    spreading_factor: Optional[int] = None
    log_level: Optional[str] = None
    log_code: Optional[str] = None
    log_description: Optional[str] = None
    payload: Dict[str, Any]
    received_at: datetime

    class Config:
        from_attributes = True


class ChirpStackEventStats(BaseModel):
    """Estatísticas dos eventos do ChirpStack."""

    total_events: int
    events_by_type: Dict[str, int]
    unique_devices: int
    latest_event: Optional[datetime] = None
    date_range: Dict[str, Optional[datetime]]


class ChirpStackEventFilter(BaseModel):
    """Filtros para buscar eventos."""

    dev_eui: Optional[str] = None
    event_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(default=100, le=1000)
    offset: int = Field(default=0, ge=0)
