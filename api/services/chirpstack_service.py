from datetime import datetime
from typing import Dict, List, Optional

from models.chirpstack_event import ChirpStackEvent
from sqlalchemy import func
from sqlalchemy.orm import Session


class ChirpStackService:
    """Serviço para processar e armazenar eventos do ChirpStack."""

    @staticmethod
    def determine_event_type(payload: Dict) -> str:
        """Determina o tipo de evento baseado no payload."""
        if "level" in payload and "code" in payload:
            return "log"
        elif "deduplicationId" in payload and "rxInfo" in payload:
            return "up"
        elif (
            "deduplicationId" in payload
            and "devAddr" in payload
            and "rxInfo" not in payload
        ):
            return "join"
        elif "devAddr" in payload:
            return "ack"
        else:
            return "unknown"

    @staticmethod
    def parse_event_time(time_str: str) -> datetime:
        """Parse do timestamp do ChirpStack."""
        # Remove o +00:00 e adiciona Z para ISO format
        if time_str.endswith("+00:00"):
            time_str = time_str[:-6] + "Z"
        return datetime.fromisoformat(time_str.replace("Z", "+00:00"))

    @staticmethod
    def extract_rf_info(rx_info: Optional[List[Dict]]) -> tuple:
        """Extrai informações de RF do primeiro gateway."""
        if not rx_info or len(rx_info) == 0:
            return None, None

        first_rx = rx_info[0]
        rssi = first_rx.get("rssi")
        snr = first_rx.get("snr")

        return rssi, snr

    @staticmethod
    def extract_tx_info(tx_info: Optional[Dict]) -> tuple:
        """Extrai informações de transmissão."""
        if not tx_info:
            return None, None

        frequency = tx_info.get("frequency")
        modulation = tx_info.get("modulation", {})
        lora_info = modulation.get("lora", {})
        spreading_factor = lora_info.get("spreadingFactor")

        return frequency, spreading_factor

    @staticmethod
    def create_event(payload: Dict, db: Session) -> ChirpStackEvent:
        """Cria e salva um evento do ChirpStack no banco de dados."""

        event_type = ChirpStackService.determine_event_type(payload)
        device_info = payload.get("deviceInfo", {})

        # Extrai informações comuns
        dev_eui = device_info.get("devEui", "unknown")
        device_name = device_info.get("deviceName")
        application_name = device_info.get("applicationName")
        event_time = ChirpStackService.parse_event_time(payload.get("time"))

        # Extrai informações específicas do tipo de evento
        event_data = {
            "event_type": event_type,
            "dev_eui": dev_eui,
            "device_name": device_name,
            "application_name": application_name,
            "event_time": event_time,
            "payload": payload,
        }

        # Para eventos 'up'
        if event_type == "up":
            event_data["deduplication_id"] = payload.get("deduplicationId")
            event_data["f_cnt"] = payload.get("fCnt")
            event_data["f_port"] = payload.get("fPort")
            event_data["dr"] = payload.get("dr")

            # Informações de RF
            rssi, snr = ChirpStackService.extract_rf_info(payload.get("rxInfo"))
            event_data["rssi"] = rssi
            event_data["snr"] = snr

            # Informações de TX
            frequency, spreading_factor = ChirpStackService.extract_tx_info(
                payload.get("txInfo")
            )
            event_data["frequency"] = frequency
            event_data["spreading_factor"] = spreading_factor

        # Para eventos 'join'
        elif event_type == "join":
            event_data["deduplication_id"] = payload.get("deduplicationId")

        # Para eventos 'log'
        elif event_type == "log":
            event_data["log_level"] = payload.get("level")
            event_data["log_code"] = payload.get("code")
            event_data["log_description"] = payload.get("description")

        # Cria o evento
        event = ChirpStackEvent(**event_data)
        db.add(event)
        db.commit()
        db.refresh(event)

        return event

    @staticmethod
    def get_events(
        db: Session,
        dev_eui: Optional[str] = None,
        event_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ChirpStackEvent]:
        """Busca eventos com filtros opcionais."""

        query = db.query(ChirpStackEvent)

        if dev_eui:
            query = query.filter(ChirpStackEvent.dev_eui == dev_eui)

        if event_type:
            query = query.filter(ChirpStackEvent.event_type == event_type)

        if start_date:
            query = query.filter(ChirpStackEvent.event_time >= start_date)

        if end_date:
            query = query.filter(ChirpStackEvent.event_time <= end_date)

        query = query.order_by(ChirpStackEvent.event_time.desc())
        query = query.limit(limit).offset(offset)

        return query.all()

    @staticmethod
    def get_event_by_id(db: Session, event_id: int) -> Optional[ChirpStackEvent]:
        """Busca um evento específico por ID."""
        return db.query(ChirpStackEvent).filter(ChirpStackEvent.id == event_id).first()

    @staticmethod
    def get_stats(db: Session) -> Dict:
        """Retorna estatísticas dos eventos armazenados."""

        total_events = db.query(ChirpStackEvent).count()

        # Eventos por tipo
        events_by_type = {}
        type_counts = (
            db.query(ChirpStackEvent.event_type, func.count(ChirpStackEvent.id))
            .group_by(ChirpStackEvent.event_type)
            .all()
        )

        for event_type, count in type_counts:
            events_by_type[event_type] = count

        # Dispositivos únicos
        unique_devices = db.query(ChirpStackEvent.dev_eui).distinct().count()

        # Último evento
        latest_event = (
            db.query(ChirpStackEvent)
            .order_by(ChirpStackEvent.event_time.desc())
            .first()
        )

        # Range de datas
        date_range_query = db.query(
            func.min(ChirpStackEvent.event_time).label("min_date"),
            func.max(ChirpStackEvent.event_time).label("max_date"),
        ).first()

        return {
            "total_events": total_events,
            "events_by_type": events_by_type,
            "unique_devices": unique_devices,
            "latest_event": latest_event.event_time if latest_event else None,
            "date_range": {
                "start": date_range_query.min_date if date_range_query else None,
                "end": date_range_query.max_date if date_range_query else None,
            },
        }

    @staticmethod
    def get_device_events_summary(db: Session, dev_eui: str) -> Dict:
        """Retorna um resumo dos eventos de um dispositivo específico."""

        # Total de eventos
        total = (
            db.query(ChirpStackEvent).filter(ChirpStackEvent.dev_eui == dev_eui).count()
        )

        # Eventos por tipo
        events_by_type = {}
        type_counts = (
            db.query(ChirpStackEvent.event_type, func.count(ChirpStackEvent.id))
            .filter(ChirpStackEvent.dev_eui == dev_eui)
            .group_by(ChirpStackEvent.event_type)
            .all()
        )

        for event_type, count in type_counts:
            events_by_type[event_type] = count

        # Último evento
        latest_event = (
            db.query(ChirpStackEvent)
            .filter(ChirpStackEvent.dev_eui == dev_eui)
            .order_by(ChirpStackEvent.event_time.desc())
            .first()
        )

        # Estatísticas de RF (apenas para eventos 'up')
        rf_stats = (
            db.query(
                func.avg(ChirpStackEvent.rssi).label("avg_rssi"),
                func.min(ChirpStackEvent.rssi).label("min_rssi"),
                func.max(ChirpStackEvent.rssi).label("max_rssi"),
                func.avg(ChirpStackEvent.snr).label("avg_snr"),
                func.min(ChirpStackEvent.snr).label("min_snr"),
                func.max(ChirpStackEvent.snr).label("max_snr"),
            )
            .filter(
                ChirpStackEvent.dev_eui == dev_eui, ChirpStackEvent.event_type == "up"
            )
            .first()
        )

        rf_stats_dict = None
        if rf_stats.avg_rssi:
            rf_stats_dict = {
                "rssi": {
                    "avg": float(rf_stats.avg_rssi) if rf_stats.avg_rssi else None,
                    "min": rf_stats.min_rssi,
                    "max": rf_stats.max_rssi,
                },
                "snr": {
                    "avg": float(rf_stats.avg_snr) if rf_stats.avg_snr else None,
                    "min": rf_stats.min_snr,
                    "max": rf_stats.max_snr,
                },
            }

        return {
            "dev_eui": dev_eui,
            "total_events": total,
            "events_by_type": events_by_type,
            "latest_event": latest_event.event_time if latest_event else None,
            "rf_stats": rf_stats_dict,
        }
