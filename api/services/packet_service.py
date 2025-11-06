from datetime import datetime

from models.device import Device
from models.sensor_reading import SensorReading
from sqlalchemy.orm import Session


class PacketService:
    """Service para gerenciar operações relacionadas a pacotes de dados."""

    @staticmethod
    def _get_or_create_device(db: Session, device_uid: str) -> Device:
        """Obtém ou cria um dispositivo."""
        device = db.query(Device).filter(Device.device_uid == device_uid).first()
        if not device:
            device = Device(device_uid=device_uid, description=f"Device {device_uid}")
            db.add(device)
            db.commit()
            db.refresh(device)
        return device

    @staticmethod
    def _create_sensor_reading(
        db: Session,
        device_id: int,
        sensor_type: str,
        value: float,
        timestamp: datetime | None = None,
    ) -> SensorReading:
        """Cria uma leitura de sensor."""
        reading = SensorReading(
            device_id=device_id,
            sensor_type=sensor_type,
            value=value,
            timestamp=timestamp or datetime.now(),
        )
        db.add(reading)
        return reading

    @staticmethod
    def create_packet_record(
        db: Session,
        fluxo: float,
        pulso: int,
        sensor: int,
        t: float,
        h: float,
        g: float,
        solo: float,
        device_id: str,
    ) -> dict:
        """
        Cria um novo registro de pacote no banco de dados.
        Usa a nova estrutura (Device + SensorReading) mas mantém compatibilidade.
        Retorna um dict com os mesmos campos que PacketRecord tinha.
        """
        # Obter ou criar dispositivo
        device = PacketService._get_or_create_device(db, device_id)

        # Criar leituras apenas para valores > 0
        readings = []
        if fluxo > 0:
            readings.append(
                PacketService._create_sensor_reading(db, device.id, "fluxo", fluxo)
            )
        if pulso > 0:
            readings.append(
                PacketService._create_sensor_reading(
                    db, device.id, "pulso", float(pulso)
                )
            )
        if sensor > 0:
            readings.append(
                PacketService._create_sensor_reading(
                    db, device.id, "sensor", float(sensor)
                )
            )
        if t > 0:
            readings.append(
                PacketService._create_sensor_reading(db, device.id, "temperatura", t)
            )
        if h > 0:
            readings.append(
                PacketService._create_sensor_reading(db, device.id, "umidade", h)
            )
        if g > 0:
            readings.append(
                PacketService._create_sensor_reading(db, device.id, "gas", g)
            )
        if solo > 0:
            readings.append(
                PacketService._create_sensor_reading(db, device.id, "solo", solo)
            )

        # Commit todas as leituras
        db.commit()
        for reading in readings:
            db.refresh(reading)

        # Retornar no formato compatível (simulando PacketRecord)
        # Usar o timestamp da última leitura ou agora
        last_timestamp = readings[-1].timestamp if readings else datetime.now()

        return {
            "id": readings[0].id if readings else 0,
            "device_id": device_id,
            "fluxo": fluxo,
            "pulso": pulso,
            "sensor": sensor,
            "t": t,
            "h": h,
            "g": g,
            "solo": solo,
            "timestamp": last_timestamp,
        }

    @staticmethod
    def get_combined_last_readings(
        device_id: str, db: Session
    ) -> tuple[dict, datetime | None]:
        """
        Busca as últimas leituras de cada tipo de dado e combina em uma única leitura.
        Retorna (combined_dict, last_timestamp).
        Usa a nova estrutura (Device + SensorReading).
        """
        # Buscar dispositivo
        device = db.query(Device).filter(Device.device_uid == device_id).first()
        if not device:
            return (
                {
                    "fluxo": 0.0,
                    "pulso": 0,
                    "sensor": 0,
                    "t": 0.0,
                    "h": 0.0,
                    "g": 0.0,
                    "solo": 0.0,
                    "last_timestamp": None,
                },
                None,
            )

        # Buscar última leitura de cada tipo de sensor
        sensor_types = {
            "temperatura": "t",
            "umidade": "h",
            "gas": "g",
            "fluxo": "fluxo",
            "pulso": "pulso",
            "sensor": "sensor",
            "solo": "solo",
        }

        combined = {
            "fluxo": 0.0,
            "pulso": 0,
            "sensor": 0,
            "t": 0.0,
            "h": 0.0,
            "g": 0.0,
            "solo": 0.0,
            "last_timestamp": None,
        }

        last_timestamp = None

        # Buscar última leitura de cada tipo
        for sensor_type, key in sensor_types.items():
            last_reading = (
                db.query(SensorReading)
                .filter(
                    SensorReading.device_id == device.id,
                    SensorReading.sensor_type == sensor_type,
                )
                .order_by(SensorReading.timestamp.desc())
                .first()
            )

            if last_reading:
                if sensor_type in ["pulso", "sensor"]:
                    combined[key] = int(last_reading.value)
                else:
                    combined[key] = last_reading.value

                # Atualizar último timestamp
                if not last_timestamp or last_reading.timestamp > last_timestamp:
                    last_timestamp = last_reading.timestamp

        combined["last_timestamp"] = last_timestamp

        # Buscar última leitura de qualquer tipo para garantir que temos timestamp
        last_any = (
            db.query(SensorReading)
            .filter(SensorReading.device_id == device.id)
            .order_by(SensorReading.timestamp.desc())
            .first()
        )

        if last_any and (not last_timestamp or last_any.timestamp > last_timestamp):
            last_timestamp = last_any.timestamp

        return combined, last_timestamp
