export interface SensorReading {
  fluxo: number
  pulso: number
  sensor: number
  t: number
  h: number
  g: number
  solo: number
}

export interface Device {
  id: string
  name: string
  status: "online" | "offline"
  location: string
  lastUpdate: string
  lastReading: SensorReading
}

export const mockDevices: Device[] = [
  {
    id: "IOT-001",
    name: "Sensor Sala Principal",
    status: "online",
    location: "Sala A - Andar 1",
    lastUpdate: "Há 2 minutos",
    lastReading: {
      fluxo: 45.32,
      pulso: 234,
      sensor: 1,
      t: 24.5,
      h: 62.3,
      g: 145.2,
      solo: 45.2,
    },
  },
  {
    id: "IOT-002",
    name: "Sensor Laboratório",
    status: "online",
    location: "Lab B - Andar 2",
    lastUpdate: "Há 1 minuto",
    lastReading: {
      fluxo: 38.21,
      pulso: 189,
      sensor: 2,
      t: 22.1,
      h: 58.7,
      g: 98.5,
      solo: 0.0,
    },
  },
  {
    id: "IOT-003",
    name: "Sensor Armazém",
    status: "offline",
    location: "Armazém C - Térreo",
    lastUpdate: "Há 2 horas",
    lastReading: {
      fluxo: 12.45,
      pulso: 67,
      sensor: 3,
      t: 28.3,
      h: 71.2,
      g: 234.8,
      solo: 0.0,
    },
  },
  {
    id: "IOT-004",
    name: "Sensor Escritório",
    status: "online",
    location: "Escritório D - Andar 3",
    lastUpdate: "Há 30 segundos",
    lastReading: {
      fluxo: 52.18,
      pulso: 312,
      sensor: 4,
      t: 23.8,
      h: 55.4,
      g: 112.3,
      solo: 0.0,
    },
  },
  {
    id: "IOT-005",
    name: "Sensor Produção",
    status: "online",
    location: "Produção E - Andar 1",
    lastUpdate: "Há 5 minutos",
    lastReading: {
      fluxo: 67.89,
      pulso: 445,
      sensor: 5,
      t: 26.7,
      h: 48.9,
      g: 187.6,
      solo: 0.0,
    },
  },
  {
    id: "IOT-006",
    name: "Sensor Estoque",
    status: "online",
    location: "Estoque F - Subsolo",
    lastUpdate: "Há 3 minutos",
    lastReading: {
      fluxo: 29.34,
      pulso: 156,
      sensor: 6,
      t: 19.2,
      h: 68.5,
      g: 76.4,
      solo: 0.0,
    },
  },
]

export function generateHistoricalData(timeRange: string) {
  const now = new Date()
  let dataPoints = 24
  let intervalMinutes = 60

  switch (timeRange) {
    case "1h":
      dataPoints = 12
      intervalMinutes = 5
      break
    case "24h":
      dataPoints = 24
      intervalMinutes = 60
      break
    case "7d":
      dataPoints = 28
      intervalMinutes = 360
      break
    case "30d":
      dataPoints = 30
      intervalMinutes = 1440
      break
  }

  return Array.from({ length: dataPoints }, (_, i) => {
    const timestamp = new Date(now.getTime() - (dataPoints - i - 1) * intervalMinutes * 60000)
    const timeString =
      timeRange === "1h"
        ? timestamp.toLocaleTimeString("pt-BR", {
            hour: "2-digit",
            minute: "2-digit",
          })
        : timeRange === "24h"
          ? timestamp.toLocaleTimeString("pt-BR", {
              hour: "2-digit",
              minute: "2-digit",
            })
          : timestamp.toLocaleDateString("pt-BR", {
              day: "2-digit",
              month: "2-digit",
            })

    return {
      timestamp: timeString,
      t: 20 + Math.random() * 10 + Math.sin(i / 3) * 3,
      h: 50 + Math.random() * 20 + Math.cos(i / 4) * 10,
      g: 100 + Math.random() * 200 + Math.sin(i / 2) * 50,
      fluxo: 30 + Math.random() * 40 + Math.cos(i / 3) * 15,
      pulso: Math.floor(150 + Math.random() * 300 + Math.sin(i / 2) * 100),
      solo: 0.0,
    }
  })
}
