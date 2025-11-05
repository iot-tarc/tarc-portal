from pydantic import BaseModel, Field


class PacketData(BaseModel):
    fluxo: float = Field(default=0.0)
    pulso: int = Field(default=0)
    sensor: int = Field(default=0)
    t: float = Field(default=0)
    h: float = Field(default=0)
    g: float = Field(default=0)
    device_id: str = Field(default="")


class PacketResponse(BaseModel):
    id: int
    data: float
    pulso: int
    sensor: int
    temperatura: float
    umidade: float
    gas: float
    device_id: str
    timestamp: str


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


class FluxoData(BaseModel):
    fluxo: float = Field(default=0.0)
    pulso: int = Field(default=0)
    device_id: str = Field(default="")
    descricao: str = Field(default="")
