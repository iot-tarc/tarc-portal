from models.packet_record import PacketRecord
from sqlalchemy.orm import Session


class PacketService:
    """Service para gerenciar operações relacionadas a pacotes de dados."""

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
    ) -> PacketRecord:
        """Cria um novo registro de pacote no banco de dados."""
        packet_record = PacketRecord(
            fluxo=fluxo,
            pulso=pulso,
            sensor=sensor,
            t=t,
            h=h,
            g=g,
            solo=solo,
            device_id=device_id,
        )
        db.add(packet_record)
        db.commit()
        db.refresh(packet_record)
        return packet_record

    @staticmethod
    def get_combined_last_readings(
        device_id: str, db: Session
    ) -> tuple[dict, PacketRecord | None]:
        """
        Busca as últimas leituras de cada tipo de dado e combina em uma única leitura.
        Retorna (combined_dict, last_any_record).
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
