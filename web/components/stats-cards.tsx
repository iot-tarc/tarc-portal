import { Card } from "@/components/ui/card"
import { Activity, Thermometer, Droplets } from "lucide-react"

interface StatsCardsProps {
  onlineDevices: number
  totalDevices: number
  avgTemperature: number
  avgHumidity: number
}

export function StatsCards({ onlineDevices, totalDevices, avgTemperature, avgHumidity }: StatsCardsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <Card className="p-6 bg-card border-border">
        <div className="flex items-start justify-between mb-4">
          <div className="p-3 rounded-lg bg-green-500/10">
            <Activity className="w-6 h-6 text-green-500" />
          </div>
        </div>
        <h3 className="text-sm font-medium text-muted-foreground mb-1">Dispositivos Online</h3>
        <p className="text-3xl font-semibold text-foreground">{onlineDevices}</p>
        <p className="text-xs text-muted-foreground mt-2">
          {((onlineDevices / totalDevices) * 100).toFixed(0)}% do total
        </p>
      </Card>

      <Card className="p-6 bg-card border-border">
        <div className="flex items-start justify-between mb-4">
          <div className="p-3 rounded-lg bg-primary/10">
            <Activity className="w-6 h-6 text-primary" />
          </div>
        </div>
        <h3 className="text-sm font-medium text-muted-foreground mb-1">Total de Dispositivos</h3>
        <p className="text-3xl font-semibold text-foreground">{totalDevices}</p>
        <p className="text-xs text-muted-foreground mt-2">Cadastrados</p>
      </Card>

      <Card className="p-6 bg-card border-border">
        <div className="flex items-start justify-between mb-4">
          <div className="p-3 rounded-lg bg-chart-1/10">
            <Thermometer className="w-6 h-6 text-chart-1" />
          </div>
        </div>
        <h3 className="text-sm font-medium text-muted-foreground mb-1">Temperatura Média</h3>
        <p className="text-3xl font-semibold text-foreground">{avgTemperature.toFixed(1)}°C</p>
        <p className="text-xs text-muted-foreground mt-2">Todos os dispositivos</p>
      </Card>

      <Card className="p-6 bg-card border-border">
        <div className="flex items-start justify-between mb-4">
          <div className="p-3 rounded-lg bg-chart-2/10">
            <Droplets className="w-6 h-6 text-chart-2" />
          </div>
        </div>
        <h3 className="text-sm font-medium text-muted-foreground mb-1">Umidade Média</h3>
        <p className="text-3xl font-semibold text-foreground">{avgHumidity.toFixed(1)}%</p>
        <p className="text-xs text-muted-foreground mt-2">Todos os dispositivos</p>
      </Card>
    </div>
  )
}
