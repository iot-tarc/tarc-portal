from datetime import datetime, timedelta, timezone

from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from models import PacketRecord
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session


class PacketData(BaseModel):
    fluxo: float = Field(default=0.0)
    pulso: int = Field(default=0.0)
    sensor: int = Field(default=0)
    t: float = Field(default=0)
    h: float = Field(default=0)
    g: float = Field(default=0)
    device_id: str = Field(default="")


class GasData(BaseModel):
    gas: float = Field(default=0.0)
    device_id: str = Field(default="")
    descricao: str = Field(default="")


class TemperatureData(BaseModel):
    temperature: float = Field(default=0.0)
    device_id: str = Field(default="")
    descricao: str = Field(default="")


class HumidityData(BaseModel):
    humidity: float = Field(default=0.0)
    device_id: str = Field(default="")
    descricao: str = Field(default="")


# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, substituir por URLs específicas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/")
def read_packet_info(data: PacketData, db: Session = Depends(get_db)):
    # Cria um novo registro no banco de dados
    packet_record = PacketRecord(
        fluxo=data.fluxo,
        pulso=data.pulso,
        sensor=data.sensor,
        t=data.t,
        h=data.h,
        g=data.g,
        device_id=data.device_id,
    )

    db.add(packet_record)
    db.commit()
    db.refresh(packet_record)

    print(f"Saved packet: {data}")

    return {
        "id": packet_record.id,
        "data": data.fluxo,
        "pulso": data.pulso,
        "sensor": data.sensor,
        "temperatura": data.t,
        "umidade": data.h,
        "gas": data.g,
        "device_id": data.device_id,
        "timestamp": packet_record.timestamp.isoformat(),
    }


@app.post("/gas")
def read_gas_info(data: GasData, db: Session = Depends(get_db)):
    # Cria um novo registro no banco de dados
    packet_record = PacketRecord(
        fluxo=0.0,
        pulso=0,
        sensor=0,
        t=0.0,
        h=0.0,
        g=data.gas,
        device_id=data.device_id,
    )

    db.add(packet_record)
    db.commit()
    db.refresh(packet_record)

    print(f"Saved gas: {data}")

    return {
        "id": packet_record.id,
        "gas": data.gas,
        "device_id": data.device_id,
        "timestamp": packet_record.timestamp.isoformat(),
    }


@app.post("/temperatura")
def read_temperature_info(data: TemperatureData, db: Session = Depends(get_db)):
    # Cria um novo registro no banco de dados
    packet_record = PacketRecord(
        fluxo=0.0,
        pulso=0,
        sensor=0,
        t=data.temperature,
        h=0.0,
        g=0.0,
        device_id=data.device_id,
    )
    db.add(packet_record)
    db.commit()
    db.refresh(packet_record)

    print(f"Saved temperature: {data}")

    return {
        "id": packet_record.id,
        "temperature": data.temperature,
        "device_id": data.device_id,
        "timestamp": packet_record.timestamp.isoformat(),
    }


@app.post("/umidade")
def read_humidity_info(data: HumidityData, db: Session = Depends(get_db)):
    # Cria um novo registro no banco de dados
    packet_record = PacketRecord(
        fluxo=0.0,
        pulso=0,
        sensor=0,
        t=0.0,
        h=data.humidity,
        g=0.0,
        device_id=data.device_id,
    )
    db.add(packet_record)
    db.commit()
    db.refresh(packet_record)

    print(f"Saved humidity: {data}")

    return {
        "id": packet_record.id,
        "humidity": data.humidity,
        "device_id": data.device_id,
        "timestamp": packet_record.timestamp.isoformat(),
    }


@app.get("/devices")
def get_devices(db: Session = Depends(get_db)):
    """
    Retorna lista de todos os dispositivos com suas últimas leituras.
    """
    # Query para obter a última leitura de cada dispositivo
    subquery = (
        db.query(
            PacketRecord.device_id,
            func.max(PacketRecord.timestamp).label("max_timestamp"),
        )
        .group_by(PacketRecord.device_id)
        .subquery()
    )

    # Query principal para obter os dados completos da última leitura
    devices_query = (
        db.query(PacketRecord)
        .join(
            subquery,
            (PacketRecord.device_id == subquery.c.device_id)
            & (PacketRecord.timestamp == subquery.c.max_timestamp),
        )
        .order_by(PacketRecord.device_id)
    )

    devices = devices_query.all()

    result = []
    for device in devices:
        # Determinar status baseado na última atualização (online se atualizou nos últimos 5 minutos)
        now = datetime.now(device.timestamp.tzinfo)
        time_diff = now - device.timestamp
        is_online = time_diff < timedelta(minutes=5)

        # Formatar última atualização
        if time_diff < timedelta(minutes=1):
            last_update = "Há poucos segundos"
        elif time_diff < timedelta(hours=1):
            minutes = int(time_diff.total_seconds() / 60)
            last_update = f"Há {minutes} minuto{'s' if minutes > 1 else ''}"
        elif time_diff < timedelta(days=1):
            hours = int(time_diff.total_seconds() / 3600)
            last_update = f"Há {hours} hora{'s' if hours > 1 else ''}"
        else:
            days = int(time_diff.total_seconds() / 86400)
            last_update = f"Há {days} dia{'s' if days > 1 else ''}"

        result.append(
            {
                "id": device.device_id,
                "name": f"Sensor {device.device_id}",
                "status": "online" if is_online else "offline",
                "location": f"Dispositivo {device.device_id}",
                "lastUpdate": last_update,
                "lastReading": {
                    "fluxo": device.fluxo,
                    "pulso": device.pulso,
                    "sensor": device.sensor,
                    "t": device.t,
                    "h": device.h,
                    "g": device.g,
                },
            }
        )

    return result


@app.get("/devices/{device_id}")
def get_device(device_id: str, db: Session = Depends(get_db)):
    """
    Retorna os detalhes de um dispositivo específico, incluindo a última leitura.
    """
    # Obter a última leitura do dispositivo
    last_reading = (
        db.query(PacketRecord)
        .filter(PacketRecord.device_id == device_id)
        .order_by(PacketRecord.timestamp.desc())
        .first()
    )

    if not last_reading:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")

    # Determinar status
    now = datetime.now(last_reading.timestamp.tzinfo)
    time_diff = now - last_reading.timestamp
    is_online = time_diff < timedelta(minutes=5)

    return {
        "id": device_id,
        "name": f"Sensor {device_id}",
        "status": "online" if is_online else "offline",
        "location": f"Dispositivo {device_id}",
        "lastUpdate": last_reading.timestamp.isoformat(),
        "lastReading": {
            "fluxo": last_reading.fluxo,
            "pulso": last_reading.pulso,
            "sensor": last_reading.sensor,
            "t": last_reading.t,
            "h": last_reading.h,
            "g": last_reading.g,
        },
    }


@app.get("/devices/{device_id}/readings")
def get_device_readings(
    device_id: str,
    time_range: str = Query(default="24h", description="Período: 1h, 24h, 7d, 30d"),
    db: Session = Depends(get_db),
):
    """
    Retorna histórico de leituras de um dispositivo para um período específico.
    """
    # Verificar se o dispositivo existe
    device_exists = (
        db.query(PacketRecord).filter(PacketRecord.device_id == device_id).first()
    )
    if not device_exists:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")

    # Obter uma leitura para verificar o timezone do banco
    sample = db.query(PacketRecord).filter(PacketRecord.device_id == device_id).first()

    # Calcular período baseado no time_range
    if sample and sample.timestamp.tzinfo:
        now = datetime.now(timezone.utc)
    else:
        now = datetime.now()

    if time_range == "1h":
        start_time = now - timedelta(hours=1)
    elif time_range == "24h":
        start_time = now - timedelta(hours=24)
    elif time_range == "7d":
        start_time = now - timedelta(days=7)
    elif time_range == "30d":
        start_time = now - timedelta(days=30)
    else:
        start_time = now - timedelta(hours=24)

    # Query para obter leituras no período
    readings = (
        db.query(PacketRecord)
        .filter(
            PacketRecord.device_id == device_id,
            PacketRecord.timestamp >= start_time,
        )
        .order_by(PacketRecord.timestamp.asc())
        .all()
    )

    result = []
    for reading in readings:
        # Formatar timestamp baseado no time_range
        if time_range in ["1h", "24h"]:
            timestamp_str = reading.timestamp.strftime("%H:%M")
        else:
            timestamp_str = reading.timestamp.strftime("%d/%m")

        result.append(
            {
                "timestamp": timestamp_str,
                "t": reading.t,
                "h": reading.h,
                "g": reading.g,
                "fluxo": reading.fluxo,
                "pulso": reading.pulso,
                "sensor": reading.sensor,
            }
        )

    return result


@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """
    Retorna estatísticas agregadas de todos os dispositivos.
    """
    # Obter todas as últimas leituras de cada dispositivo
    subquery = (
        db.query(
            PacketRecord.device_id,
            func.max(PacketRecord.timestamp).label("max_timestamp"),
        )
        .group_by(PacketRecord.device_id)
        .subquery()
    )

    devices_query = db.query(PacketRecord).join(
        subquery,
        (PacketRecord.device_id == subquery.c.device_id)
        & (PacketRecord.timestamp == subquery.c.max_timestamp),
    )

    devices = devices_query.all()

    if not devices:
        return {
            "totalDevices": 0,
            "onlineDevices": 0,
            "offlineDevices": 0,
            "avgTemperature": 0.0,
            "avgHumidity": 0.0,
        }

    # Calcular estatísticas
    now = datetime.now()
    online_count = 0
    total_temp = 0.0
    total_humidity = 0.0

    for device in devices:
        if device.timestamp.tzinfo:
            device_now = datetime.now(device.timestamp.tzinfo)
        else:
            device_now = now

        time_diff = device_now - device.timestamp
        if time_diff < timedelta(minutes=5):
            online_count += 1

        total_temp += device.t
        total_humidity += device.h

    total_devices = len(devices)
    avg_temp = total_temp / total_devices if total_devices > 0 else 0.0
    avg_humidity = total_humidity / total_devices if total_devices > 0 else 0.0

    return {
        "totalDevices": total_devices,
        "onlineDevices": online_count,
        "offlineDevices": total_devices - online_count,
        "avgTemperature": round(avg_temp, 1),
        "avgHumidity": round(avg_humidity, 1),
    }
