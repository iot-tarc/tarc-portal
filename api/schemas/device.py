from pydantic import BaseModel


class LastReading(BaseModel):
    fluxo: float
    pulso: int
    sensor: int
    t: float
    h: float
    g: float
    solo: float


class DeviceResponse(BaseModel):
    id: str
    name: str
    status: str
    location: str
    lastUpdate: str
    lastReading: LastReading


class DeviceStats(BaseModel):
    totalDevices: int
    onlineDevices: int
    offlineDevices: int
    avgTemperature: float
    avgHumidity: float
