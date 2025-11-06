from database import Base
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Device(Base):
    """Model para dispositivos IoT."""

    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_uid = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relacionamento com leituras de sensores
    sensor_readings = relationship(
        "SensorReading", back_populates="device", cascade="all, delete-orphan"
    )
