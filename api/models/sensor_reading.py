from database import Base
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class SensorReading(Base):
    """Model para leituras de sensores."""

    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False, index=True)
    sensor_type = Column(
        String, nullable=False, index=True
    )  # temperatura, gas, fluxo_taxa, etc.
    value = Column(Float, nullable=False)
    timestamp = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )

    # Relacionamento com dispositivo
    device = relationship("Device", back_populates="sensor_readings")
