from database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.device import DeviceResponse, DeviceStats
from schemas.reading import ReadingResponse
from services.device_service import DeviceService
from sqlalchemy.orm import Session

router = APIRouter(tags=["devices"])


@router.get("/devices", response_model=list[DeviceResponse])
def get_devices(db: Session = Depends(get_db)):
    """
    Retorna lista de todos os dispositivos com suas últimas leituras combinadas.
    """
    return DeviceService.get_all_devices(db)


@router.get("/devices/{device_id}", response_model=DeviceResponse)
def get_device(device_id: str, db: Session = Depends(get_db)):
    """
    Retorna os detalhes de um dispositivo específico, incluindo a última leitura combinada.
    """
    device = DeviceService.get_device_by_id(device_id, db)
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    return device


@router.get("/devices/{device_id}/readings", response_model=list[ReadingResponse])
def get_device_readings(
    device_id: str,
    time_range: str = Query(default="24h", description="Período: 1h, 24h, 7d, 30d"),
    db: Session = Depends(get_db),
):
    """
    Retorna histórico de leituras de um dispositivo para um período específico.
    """
    readings = DeviceService.get_device_readings(device_id, time_range, db)
    if readings is None:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    return readings


@router.get("/stats", response_model=DeviceStats)
def get_stats(db: Session = Depends(get_db)):
    """
    Retorna estatísticas agregadas de todos os dispositivos.
    """
    return DeviceService.get_stats(db)
