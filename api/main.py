from datetime import datetime, timedelta, timezone

from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from models import PacketRecord
from pydantic import BaseModel, Field
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
    temperatura: float = Field(default=0.0)
    device_id: str = Field(default="")
    descricao: str = Field(default="")


class HumidityData(BaseModel):
    umidade: float = Field(default=0.0)
    device_id: str = Field(default="")
    descricao: str = Field(default="")


class SoloData(BaseModel):
    solo: float = Field(default=0.0)
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
        solo=0.0,
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
        solo=0.0,
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
        t=data.temperatura,
        h=0.0,
        g=0.0,
        solo=0.0,
        device_id=data.device_id,
    )
    db.add(packet_record)
    db.commit()
    db.refresh(packet_record)

    print(f"Saved temperature: {data}")

    return {
        "id": packet_record.id,
        "temperatura": data.temperatura,
        "device_id": data.device_id,
        "timestamp": packet_record.timestamp.isoformat(),
    }


@app.post("/solo")
def read_solo_info(data: SoloData, db: Session = Depends(get_db)):
    # Cria um novo registro no banco de dados
    packet_record = PacketRecord(
        fluxo=0.0,
        pulso=0,
        sensor=0,
        t=0.0,
        h=0.0,
        g=0.0,
        solo=data.solo,
        device_id=data.device_id,
    )
    db.add(packet_record)
    db.commit()
    db.refresh(packet_record)

    print(f"Saved solo: {data}")

    return {
        "id": packet_record.id,
        "solo": data.solo,
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
        h=data.umidade,
        g=0.0,
        solo=0.0,
        device_id=data.device_id,
    )
    db.add(packet_record)
    db.commit()
    db.refresh(packet_record)

    print(f"Saved humidity: {data}")

    return {
        "id": packet_record.id,
        "umidade": data.umidade,
        "device_id": data.device_id,
        "timestamp": packet_record.timestamp.isoformat(),
    }


def get_combined_last_readings(device_id: str, db: Session):
    """
    Busca as últimas leituras de cada tipo de dado e combina em uma única leitura.
    """
    # Buscar última leitura de temperatura (t > 0)
    last_temp = (
        db.query(PacketRecord)
        .filter(PacketRecord.device_id == device_id, PacketRecord.t > 0)
        .order_by(PacketRecord.timestamp.desc())
        .first()
    )

    # Buscar última leitura de umidade (h > 0)
    last_humidity = (
        db.query(PacketRecord)
        .filter(PacketRecord.device_id == device_id, PacketRecord.h > 0)
        .order_by(PacketRecord.timestamp.desc())
        .first()
    )

    # Buscar última leitura de gás (g > 0)
    last_gas = (
        db.query(PacketRecord)
        .filter(PacketRecord.device_id == device_id, PacketRecord.g > 0)
        .order_by(PacketRecord.timestamp.desc())
        .first()
    )

    # Buscar última leitura de fluxo (fluxo > 0)
    last_fluxo = (
        db.query(PacketRecord)
        .filter(PacketRecord.device_id == device_id, PacketRecord.fluxo > 0)
        .order_by(PacketRecord.timestamp.desc())
        .first()
    )

    # Buscar última leitura de pulso (pulso > 0)
    last_pulso = (
        db.query(PacketRecord)
        .filter(PacketRecord.device_id == device_id, PacketRecord.pulso > 0)
        .order_by(PacketRecord.timestamp.desc())
        .first()
    )

    # Buscar última leitura de solo (solo > 0)
    last_solo = (
        db.query(PacketRecord)
        .filter(PacketRecord.device_id == device_id, PacketRecord.solo > 0)
        .order_by(PacketRecord.timestamp.desc())
        .first()
    )

    # Buscar última atualização de qualquer tipo para determinar status
    last_any = (
        db.query(PacketRecord)
        .filter(PacketRecord.device_id == device_id)
        .order_by(PacketRecord.timestamp.desc())
        .first()
    )

    # Combinar as leituras
    combined = {
        "fluxo": last_fluxo.fluxo if last_fluxo else 0.0,
        "pulso": last_pulso.pulso if last_pulso else 0,
        "sensor": last_any.sensor if last_any else 0,
        "t": last_temp.t if last_temp else 0.0,
        "h": last_humidity.h if last_humidity else 0.0,
        "g": last_gas.g if last_gas else 0.0,
        "solo": last_solo.solo if last_solo else 0.0,
        "last_timestamp": last_any.timestamp if last_any else None,
    }

    return combined, last_any


@app.get("/devices")
def get_devices(db: Session = Depends(get_db)):
    """
    Retorna lista de todos os dispositivos com suas últimas leituras combinadas.
    Combina as últimas leituras de cada tipo de dado (temperatura, umidade, gás).
    """
    # Obter lista única de device_ids
    device_ids = (
        db.query(PacketRecord.device_id)
        .distinct()
        .order_by(PacketRecord.device_id)
        .all()
    )

    result = []
    for (device_id,) in device_ids:
        combined, last_any = get_combined_last_readings(device_id, db)

        if not last_any:
            continue

        # Determinar status baseado na última atualização
        now = datetime.now(last_any.timestamp.tzinfo)
        time_diff = now - last_any.timestamp
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
                "id": device_id,
                "name": f"Sensor {device_id}",
                "status": "online" if is_online else "offline",
                "location": f"Dispositivo {device_id}",
                "lastUpdate": last_update,
                "lastReading": {
                    "fluxo": combined["fluxo"],
                    "pulso": combined["pulso"],
                    "sensor": combined["sensor"],
                    "t": combined["t"],
                    "h": combined["h"],
                    "g": combined["g"],
                    "solo": combined["solo"],
                },
            }
        )

    return result


@app.get("/devices/{device_id}")
def get_device(device_id: str, db: Session = Depends(get_db)):
    """
    Retorna os detalhes de um dispositivo específico, incluindo a última leitura combinada.
    Combina as últimas leituras de cada tipo de dado (temperatura, umidade, gás).
    """
    # Verificar se o dispositivo existe
    device_exists = (
        db.query(PacketRecord).filter(PacketRecord.device_id == device_id).first()
    )

    if not device_exists:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")

    # Obter leituras combinadas
    combined, last_any = get_combined_last_readings(device_id, db)

    if not last_any:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")

    # Determinar status
    now = datetime.now(last_any.timestamp.tzinfo)
    time_diff = now - last_any.timestamp
    is_online = time_diff < timedelta(minutes=5)

    return {
        "id": device_id,
        "name": f"Sensor {device_id}",
        "status": "online" if is_online else "offline",
        "location": f"Dispositivo {device_id}",
        "lastUpdate": last_any.timestamp.isoformat(),
        "lastReading": {
            "fluxo": combined["fluxo"],
            "pulso": combined["pulso"],
            "sensor": combined["sensor"],
            "t": combined["t"],
            "h": combined["h"],
            "g": combined["g"],
            "solo": combined["solo"],
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
    Combina leituras do mesmo intervalo de tempo para mostrar todos os valores juntos.
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
        interval_minutes = 5  # Agrupar por intervalos de 5 minutos
    elif time_range == "24h":
        start_time = now - timedelta(hours=24)
        interval_minutes = 60  # Agrupar por horas
    elif time_range == "7d":
        start_time = now - timedelta(days=7)
        interval_minutes = 360  # Agrupar por 6 horas
    elif time_range == "30d":
        start_time = now - timedelta(days=30)
        interval_minutes = 1440  # Agrupar por dias
    else:
        start_time = now - timedelta(hours=24)
        interval_minutes = 60

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

    # Agrupar leituras por intervalo de tempo e combinar valores
    grouped = {}

    for reading in readings:
        # Calcular o intervalo (normalizar timestamp para o início do intervalo)
        timestamp = reading.timestamp
        ts_seconds = int(timestamp.timestamp())

        # Normalizar para o início do intervalo
        interval_seconds = interval_minutes * 60
        interval_start = (ts_seconds // interval_seconds) * interval_seconds

        if interval_start not in grouped:
            grouped[interval_start] = {
                "timestamp": timestamp,
                "t": 0.0,
                "h": 0.0,
                "g": 0.0,
                "fluxo": 0.0,
                "pulso": 0,
                "sensor": 0,
                "solo": 0.0,
            }

        # Combinar valores (usar o último valor não-zero de cada tipo)
        if reading.t > 0:
            grouped[interval_start]["t"] = reading.t
        if reading.h > 0:
            grouped[interval_start]["h"] = reading.h
        if reading.g > 0:
            grouped[interval_start]["g"] = reading.g
        if reading.fluxo > 0:
            grouped[interval_start]["fluxo"] = reading.fluxo
        if reading.pulso > 0:
            grouped[interval_start]["pulso"] = reading.pulso
        if reading.sensor > 0:
            grouped[interval_start]["sensor"] = reading.sensor
        if reading.solo > 0:
            grouped[interval_start]["solo"] = reading.solo

        # Atualizar timestamp para o mais recente do intervalo
        if timestamp > grouped[interval_start]["timestamp"]:
            grouped[interval_start]["timestamp"] = timestamp

    # Converter para lista e formatar timestamps
    result = []
    for interval_start in sorted(grouped.keys()):
        data = grouped[interval_start]
        timestamp = data["timestamp"]

        # Formatar timestamp baseado no time_range
        if time_range in ["1h", "24h"]:
            timestamp_str = timestamp.strftime("%H:%M")
        else:
            timestamp_str = timestamp.strftime("%d/%m")

        result.append(
            {
                "timestamp": timestamp_str,
                "t": data["t"],
                "h": data["h"],
                "g": data["g"],
                "fluxo": data["fluxo"],
                "pulso": data["pulso"],
                "sensor": data["sensor"],
                "solo": data["solo"],
            }
        )

    return result


@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """
    Retorna estatísticas agregadas de todos os dispositivos.
    Usa leituras combinadas para cálculos mais precisos.
    """
    # Obter lista única de device_ids
    device_ids = (
        db.query(PacketRecord.device_id)
        .distinct()
        .order_by(PacketRecord.device_id)
        .all()
    )

    if not device_ids:
        return {
            "totalDevices": 0,
            "onlineDevices": 0,
            "offlineDevices": 0,
            "avgTemperature": 0.0,
            "avgHumidity": 0.0,
        }

    # Calcular estatísticas usando leituras combinadas
    now = datetime.now()
    online_count = 0
    total_temp = 0.0
    total_humidity = 0.0
    devices_with_temp = 0
    devices_with_humidity = 0

    for (device_id,) in device_ids:
        combined, last_any = get_combined_last_readings(device_id, db)

        if not last_any:
            continue

        # Verificar se está online
        if last_any.timestamp.tzinfo:
            device_now = datetime.now(last_any.timestamp.tzinfo)
        else:
            device_now = now

        time_diff = device_now - last_any.timestamp
        if time_diff < timedelta(minutes=5):
            online_count += 1

        # Somar apenas valores válidos (> 0)
        if combined["t"] > 0:
            total_temp += combined["t"]
            devices_with_temp += 1

        if combined["h"] > 0:
            total_humidity += combined["h"]
            devices_with_humidity += 1

    total_devices = len(device_ids)
    avg_temp = total_temp / devices_with_temp if devices_with_temp > 0 else 0.0
    avg_humidity = (
        total_humidity / devices_with_humidity if devices_with_humidity > 0 else 0.0
    )

    return {
        "totalDevices": total_devices,
        "onlineDevices": online_count,
        "offlineDevices": total_devices - online_count,
        "avgTemperature": round(avg_temp, 1),
        "avgHumidity": round(avg_humidity, 1),
    }
