from datetime import datetime
from typing import Optional

from database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from schemas.chirpstack import (
    ChirpStackEventResponse,
    ChirpStackEventStats,
)
from services.chirpstack_service import ChirpStackService
from sqlalchemy.orm import Session

router = APIRouter(tags=["chirpstack"])


@router.post("/webhook/chirpstack", status_code=201)
async def receive_chirpstack_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Endpoint webhook para receber eventos do ChirpStack.

    Este endpoint aceita todos os tipos de eventos do ChirpStack:
    - up: Uplink de dados
    - join: Join de dispositivo
    - log: Eventos de log (warnings, errors, etc.)
    - ack: Confirmações

    Os eventos são automaticamente classificados e armazenados no banco de dados.
    """
    try:
        # Recebe o payload bruto como dict
        payload = await request.json()

        # Cria e salva o evento
        event = ChirpStackService.create_event(payload, db)

        return {
            "status": "success",
            "message": "Event received and stored",
            "event_id": event.id,
            "event_type": event.event_type,
            "dev_eui": event.dev_eui,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing webhook: {str(e)}"
        )


@router.get("/chirpstack/events", response_model=list[ChirpStackEventResponse])
def get_events(
    dev_eui: Optional[str] = Query(None, description="Filter by device EUI"),
    event_type: Optional[str] = Query(
        None, description="Filter by event type (up, join, log)"
    ),
    start_date: Optional[datetime] = Query(
        None, description="Filter events after this date"
    ),
    end_date: Optional[datetime] = Query(
        None, description="Filter events before this date"
    ),
    limit: int = Query(100, le=1000, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    db: Session = Depends(get_db),
):
    """
    Retorna lista de eventos do ChirpStack com filtros opcionais.
    """
    events = ChirpStackService.get_events(
        db=db,
        dev_eui=dev_eui,
        event_type=event_type,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset,
    )
    return events


@router.get("/chirpstack/events/{event_id}", response_model=ChirpStackEventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """
    Retorna detalhes de um evento específico.
    """
    event = ChirpStackService.get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.get("/chirpstack/stats", response_model=ChirpStackEventStats)
def get_stats(db: Session = Depends(get_db)):
    """
    Retorna estatísticas gerais dos eventos do ChirpStack.
    """
    stats = ChirpStackService.get_stats(db)
    return stats


@router.get("/chirpstack/devices/{dev_eui}/summary")
def get_device_summary(dev_eui: str, db: Session = Depends(get_db)):
    """
    Retorna um resumo dos eventos e estatísticas de um dispositivo específico.

    Inclui:
    - Total de eventos por tipo
    - Estatísticas de RF (RSSI, SNR) para eventos 'up'
    - Último evento registrado
    """
    summary = ChirpStackService.get_device_events_summary(db, dev_eui)

    if summary["total_events"] == 0:
        raise HTTPException(status_code=404, detail="No events found for this device")

    return summary


@router.get("/chirpstack/devices")
def get_devices(db: Session = Depends(get_db)):
    """
    Lista todos os dispositivos únicos que geraram eventos.
    """
    from models.chirpstack_event import ChirpStackEvent
    from sqlalchemy import func

    devices = (
        db.query(
            ChirpStackEvent.dev_eui,
            ChirpStackEvent.device_name,
            ChirpStackEvent.application_name,
            func.count(ChirpStackEvent.id).label("event_count"),
            func.max(ChirpStackEvent.event_time).label("last_event"),
        )
        .group_by(
            ChirpStackEvent.dev_eui,
            ChirpStackEvent.device_name,
            ChirpStackEvent.application_name,
        )
        .order_by(func.max(ChirpStackEvent.event_time).desc())
        .all()
    )

    return [
        {
            "dev_eui": dev_eui,
            "device_name": device_name,
            "application_name": application_name,
            "event_count": event_count,
            "last_event": last_event,
        }
        for dev_eui, device_name, application_name, event_count, last_event in devices
    ]
