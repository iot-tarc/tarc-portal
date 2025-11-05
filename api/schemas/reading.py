from pydantic import BaseModel


class ReadingResponse(BaseModel):
    timestamp: str
    t: float
    h: float
    g: float
    fluxo: float
    pulso: int
    sensor: int
    solo: float
