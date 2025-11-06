from datetime import datetime

from database import get_db
from fastapi import APIRouter, Depends
from schemas.packet import (
    FluxoData,
    GasData,
    HumidityData,
    PacketData,
    PacketResponse,
    SoloData,
    TemperatureData,
)
from services.packet_service import PacketService
from sqlalchemy.orm import Session

router = APIRouter(tags=["packets"])


@router.post("/", response_model=PacketResponse)
def create_packet(data: PacketData, db: Session = Depends(get_db)):
    """Cria um novo registro de pacote no banco de dados."""
    packet_record = PacketService.create_packet_record(
        db=db,
        fluxo=data.fluxo,
        pulso=data.pulso,
        sensor=data.sensor,
        t=data.t,
        h=data.h,
        g=data.g,
        solo=0.0,
        device_id=data.device_id,
    )

    print(f"Saved packet: {data}")

    return {
        "id": packet_record["id"],
        "data": data.fluxo,
        "pulso": data.pulso,
        "sensor": data.sensor,
        "temperatura": data.t,
        "umidade": data.h,
        "gas": data.g,
        "device_id": data.device_id,
        "timestamp": packet_record["timestamp"].isoformat()
        if isinstance(packet_record["timestamp"], datetime)
        else packet_record["timestamp"],
    }


@router.post("/gas")
def create_gas(data: GasData, db: Session = Depends(get_db)):
    """Cria um novo registro de gás no banco de dados."""
    packet_record = PacketService.create_packet_record(
        db=db,
        fluxo=0.0,
        pulso=0,
        sensor=0,
        t=0.0,
        h=0.0,
        g=data.gas,
        solo=0.0,
        device_id=data.device_id,
    )

    print(f"Saved gas: {data}")

    return {
        "id": packet_record["id"],
        "gas": data.gas,
        "device_id": data.device_id,
        "timestamp": packet_record["timestamp"].isoformat()
        if isinstance(packet_record["timestamp"], datetime)
        else packet_record["timestamp"],
    }


@router.post("/temperatura")
def create_temperature(data: TemperatureData, db: Session = Depends(get_db)):
    """Cria um novo registro de temperatura no banco de dados."""
    packet_record = PacketService.create_packet_record(
        db=db,
        fluxo=0.0,
        pulso=0,
        sensor=0,
        t=data.temperatura,
        h=0.0,
        g=0.0,
        solo=0.0,
        device_id=data.device_id,
    )

    print(f"Saved temperature: {data}")

    return {
        "id": packet_record["id"],
        "temperatura": data.temperatura,
        "device_id": data.device_id,
        "timestamp": packet_record["timestamp"].isoformat()
        if isinstance(packet_record["timestamp"], datetime)
        else packet_record["timestamp"],
    }


@router.post("/solo")
def create_solo(data: SoloData, db: Session = Depends(get_db)):
    """Cria um novo registro de solo no banco de dados."""
    packet_record = PacketService.create_packet_record(
        db=db,
        fluxo=0.0,
        pulso=0,
        sensor=0,
        t=0.0,
        h=0.0,
        g=0.0,
        solo=data.solo,
        device_id=data.device_id,
    )

    print(f"Saved solo: {data}")

    return {
        "id": packet_record["id"],
        "solo": data.solo,
        "device_id": data.device_id,
        "timestamp": packet_record["timestamp"].isoformat()
        if isinstance(packet_record["timestamp"], datetime)
        else packet_record["timestamp"],
    }


@router.post("/fluxo")
def create_fluxo(data: FluxoData, db: Session = Depends(get_db)):
    """Cria um novo registro de fluxo no banco de dados."""
    packet_record = PacketService.create_packet_record(
        db=db,
        fluxo=data.fluxo,
        pulso=data.pulso,
        sensor=0,
        t=0.0,
        h=0.0,
        g=0.0,
        solo=0.0,
        device_id=data.device_id,
    )

    print(f"Saved fluxo: {data}")

    return {
        "id": packet_record["id"],
        "fluxo": data.fluxo,
        "pulso": data.pulso,
        "device_id": data.device_id,
        "timestamp": packet_record["timestamp"].isoformat()
        if isinstance(packet_record["timestamp"], datetime)
        else packet_record["timestamp"],
    }


@router.post("/umidade")
def create_humidity(data: HumidityData, db: Session = Depends(get_db)):
    """Cria um novo registro de umidade no banco de dados."""
    packet_record = PacketService.create_packet_record(
        db=db,
        fluxo=0.0,
        pulso=0,
        sensor=0,
        t=0.0,
        h=data.umidade,
        g=0.0,
        solo=0.0,
        device_id=data.device_id,
    )

    print(f"Saved humidity: {data}")

    return {
        "id": packet_record["id"],
        "umidade": data.umidade,
        "device_id": data.device_id,
        "timestamp": packet_record["timestamp"].isoformat()
        if isinstance(packet_record["timestamp"], datetime)
        else packet_record["timestamp"],
    }
