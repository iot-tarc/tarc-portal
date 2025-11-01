import type { Device } from "./mock-data"

// Re-exportar tipos para uso externo
export type { Device, SensorReading } from "./mock-data"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://10.13.22.191:8000"

export interface HistoricalReading {
  timestamp: string
  t: number
  h: number
  g: number
  fluxo: number
  pulso: number
  sensor: number
}

export interface Stats {
  totalDevices: number
  onlineDevices: number
  offlineDevices: number
  avgTemperature: number
  avgHumidity: number
}

/**
 * Busca lista de todos os dispositivos
 */
export async function getDevices(): Promise<Device[]> {
  const response = await fetch(`${API_URL}/devices`)
  if (!response.ok) {
    throw new Error(`Erro ao buscar dispositivos: ${response.statusText}`)
  }
  return response.json()
}

/**
 * Busca detalhes de um dispositivo específico
 */
export async function getDevice(deviceId: string): Promise<Device> {
  const response = await fetch(`${API_URL}/devices/${deviceId}`)
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error("Dispositivo não encontrado")
    }
    throw new Error(`Erro ao buscar dispositivo: ${response.statusText}`)
  }
  return response.json()
}

/**
 * Busca histórico de leituras de um dispositivo
 */
export async function getDeviceReadings(
  deviceId: string,
  timeRange: string = "24h"
): Promise<HistoricalReading[]> {
  const response = await fetch(
    `${API_URL}/devices/${deviceId}/readings?time_range=${timeRange}`
  )
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error("Dispositivo não encontrado")
    }
    throw new Error(`Erro ao buscar histórico: ${response.statusText}`)
  }
  return response.json()
}

/**
 * Busca estatísticas agregadas
 */
export async function getStats(): Promise<Stats> {
  const response = await fetch(`${API_URL}/stats`)
  if (!response.ok) {
    throw new Error(`Erro ao buscar estatísticas: ${response.statusText}`)
  }
  return response.json()
}

