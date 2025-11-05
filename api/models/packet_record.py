from database import Base
from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func


class PacketRecord(Base):
    __tablename__ = "packets"

    id = Column(Integer, primary_key=True, index=True)
    fluxo = Column(Float, nullable=False)
    pulso = Column(Integer, nullable=False)
    sensor = Column(Integer, nullable=False)
    t = Column(Float, nullable=False)  # temperatura
    h = Column(Float, nullable=False)  # umidade
    g = Column(Float, nullable=False)  # gas
    solo = Column(Float, nullable=False, default=0.0)  # solo
    device_id = Column(String, nullable=False)
    timestamp = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
