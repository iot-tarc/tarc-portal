from datetime import datetime, timedelta, timezone

from models.device import Device
from models.sensor_reading import SensorReading
from sqlalchemy.orm import Session

from services.packet_service import PacketService


class DeviceService:
    """Service para gerenciar operações relacionadas a dispositivos."""

    @staticmethod
    def get_all_devices(db: Session) -> list[dict]:
        """
        Retorna lista de todos os dispositivos com suas últimas leituras combinadas.
        Usa a nova estrutura (Device + SensorReading).
        """
        # Obter todos os dispositivos
        devices = db.query(Device).order_by(Device.device_uid).all()

        result = []
        for device in devices:
            combined, last_timestamp = PacketService.get_combined_last_readings(
                device.device_uid, db
            )

            if not last_timestamp:
                continue

            # Determinar status baseado na última atualização
            now = (
                datetime.now(last_timestamp.tzinfo)
                if last_timestamp.tzinfo
                else datetime.now()
            )
            time_diff = now - last_timestamp
            is_online = time_diff < timedelta(minutes=5)

            # Formatar última atualização
            last_update = DeviceService._format_last_update(time_diff)

            result.append(
                {
                    "id": device.device_uid,
                    "name": f"Sensor {device.device_uid}",
                    "status": "online" if is_online else "offline",
                    "location": device.description
                    or f"Dispositivo {device.device_uid}",
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

    @staticmethod
    def get_device_by_id(device_id: str, db: Session) -> dict | None:
        """
        Retorna os detalhes de um dispositivo específico, incluindo a última leitura combinada.
        Usa a nova estrutura (Device + SensorReading).
        """
        # Buscar dispositivo
        device = db.query(Device).filter(Device.device_uid == device_id).first()

        if not device:
            return None

        # Obter leituras combinadas
        combined, last_timestamp = PacketService.get_combined_last_readings(
            device_id, db
        )

        if not last_timestamp:
            return None

        # Determinar status
        now = (
            datetime.now(last_timestamp.tzinfo)
            if last_timestamp.tzinfo
            else datetime.now()
        )
        time_diff = now - last_timestamp
        is_online = time_diff < timedelta(minutes=5)

        return {
            "id": device.device_uid,
            "name": f"Sensor {device.device_uid}",
            "status": "online" if is_online else "offline",
            "location": device.description or f"Dispositivo {device.device_uid}",
            "lastUpdate": last_timestamp.isoformat(),
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

    @staticmethod
    def get_device_readings(
        device_id: str,
        time_range: str,
        db: Session,
    ) -> list[dict] | None:
        """
        Retorna histórico de leituras de um dispositivo para um período específico.
        Combina leituras do mesmo intervalo de tempo para mostrar todos os valores juntos.
        Usa a nova estrutura (Device + SensorReading).
        """
        # Buscar dispositivo
        device = db.query(Device).filter(Device.device_uid == device_id).first()
        if not device:
            return None

        # Obter uma leitura para verificar o timezone do banco
        sample = (
            db.query(SensorReading).filter(SensorReading.device_id == device.id).first()
        )

        # Calcular período baseado no time_range
        if sample and sample.timestamp.tzinfo:
            now = datetime.now(timezone.utc)
        else:
            now = datetime.now()

        # Configurar período e intervalo baseado no time_range
        time_config = {
            "1h": (timedelta(hours=1), 5),
            "24h": (timedelta(hours=24), 60),
            "7d": (timedelta(days=7), 360),
            "30d": (timedelta(days=30), 1440),
        }

        time_delta, interval_minutes = time_config.get(
            time_range, (timedelta(hours=24), 60)
        )
        start_time = now - time_delta

        # Query para obter leituras no período
        readings = (
            db.query(SensorReading)
            .filter(
                SensorReading.device_id == device.id,
                SensorReading.timestamp >= start_time,
            )
            .order_by(SensorReading.timestamp.asc())
            .all()
        )

        # Agrupar leituras por intervalo de tempo e combinar valores
        grouped = {}

        # Mapear tipos de sensor para chaves do formato antigo
        sensor_type_map = {
            "temperatura": "t",
            "umidade": "h",
            "gas": "g",
            "fluxo": "fluxo",
            "pulso": "pulso",
            "sensor": "sensor",
            "solo": "solo",
        }

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

            # Combinar valores (usar o último valor de cada tipo no intervalo)
            key = sensor_type_map.get(reading.sensor_type)
            if key:
                if reading.sensor_type in ["pulso", "sensor"]:
                    grouped[interval_start][key] = int(reading.value)
                else:
                    grouped[interval_start][key] = reading.value

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

    @staticmethod
    def get_stats(db: Session) -> dict:
        """
        Retorna estatísticas agregadas de todos os dispositivos.
        Usa leituras combinadas para cálculos mais precisos.
        Usa a nova estrutura (Device + SensorReading).
        """
        # Obter todos os dispositivos
        devices = db.query(Device).all()

        if not devices:
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

        for device in devices:
            combined, last_timestamp = PacketService.get_combined_last_readings(
                device.device_uid, db
            )

            if not last_timestamp:
                continue

            # Verificar se está online
            if last_timestamp.tzinfo:
                device_now = datetime.now(last_timestamp.tzinfo)
            else:
                device_now = now

            time_diff = device_now - last_timestamp
            if time_diff < timedelta(minutes=5):
                online_count += 1

            # Somar apenas valores válidos (> 0)
            if combined["t"] > 0:
                total_temp += combined["t"]
                devices_with_temp += 1

            if combined["h"] > 0:
                total_humidity += combined["h"]
                devices_with_humidity += 1

        total_devices = len(devices)
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

    @staticmethod
    def _format_last_update(time_diff: timedelta) -> str:
        """Formata a diferença de tempo em uma string legível."""
        if time_diff < timedelta(minutes=1):
            return "Há poucos segundos"
        elif time_diff < timedelta(hours=1):
            minutes = int(time_diff.total_seconds() / 60)
            return f"Há {minutes} minuto{'s' if minutes > 1 else ''}"
        elif time_diff < timedelta(days=1):
            hours = int(time_diff.total_seconds() / 3600)
            return f"Há {hours} hora{'s' if hours > 1 else ''}"
        else:
            days = int(time_diff.total_seconds() / 86400)
            return f"Há {days} dia{'s' if days > 1 else ''}"
