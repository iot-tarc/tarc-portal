import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  ArrowLeft,
  Thermometer,
  Droplets,
  Wind,
  Gauge,
  Zap,
  Loader2,
  AlertCircle,
  TreePine,
} from "lucide-react";
import { DeviceCharts } from "@/components/device-charts";
import {
  getDevice,
  getDeviceReadings,
  type Device,
  type HistoricalReading,
} from "@/lib/api";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export default function DevicePage() {
  const { id } = useParams<{ id: string }>();
  const [timeRange, setTimeRange] = useState("24h");
  const [device, setDevice] = useState<Device | null>(null);
  const [historicalData, setHistoricalData] = useState<HistoricalReading[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;

    const fetchDeviceData = async () => {
      try {
        setLoading(true);
        setError(null);
        const deviceData = await getDevice(id);
        setDevice(deviceData);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Erro ao carregar dispositivo"
        );
        console.error("Erro ao buscar dispositivo:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchDeviceData();
  }, [id]);

  useEffect(() => {
    if (!device || !id) return;

    const fetchHistoricalData = async () => {
      try {
        const readings = await getDeviceReadings(id, timeRange);
        setHistoricalData(readings);
      } catch (err) {
        console.error("Erro ao buscar histórico:", err);
        setHistoricalData([]);
      }
    };

    fetchHistoricalData();
  }, [id, timeRange, device]);

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin mx-auto mb-4 text-muted-foreground" />
          <p className="text-muted-foreground">Carregando dispositivo...</p>
        </div>
      </div>
    );
  }

  if (error || !device) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center max-w-md">
          <AlertCircle className="w-8 h-8 mx-auto mb-4 text-destructive" />
          <p className="text-destructive mb-4">
            {error || "Dispositivo não encontrado"}
          </p>
          <div className="flex gap-4 justify-center">
            <Button
              onClick={() => {
                if (!id) return;
                const fetchDeviceData = async () => {
                  try {
                    setLoading(true);
                    setError(null);
                    const deviceData = await getDevice(id);
                    setDevice(deviceData);
                  } catch (err) {
                    setError(
                      err instanceof Error
                        ? err.message
                        : "Erro ao carregar dispositivo"
                    );
                    console.error("Erro ao buscar dispositivo:", err);
                  } finally {
                    setLoading(false);
                  }
                };
                fetchDeviceData();
              }}
            >
              Tentar Novamente
            </Button>
            <Link to="/">
              <Button variant="outline">Voltar ao Dashboard</Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card sticky top-0 z-10">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link to="/">
                <Button variant="ghost" size="sm">
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Voltar
                </Button>
              </Link>
              <div>
                <h1 className="text-2xl font-semibold text-foreground">
                  {device.name}
                </h1>
                <p className="text-sm text-muted-foreground mt-1">
                  ID: {device.id} • {device.location}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <Badge
                variant={device.status === "online" ? "default" : "secondary"}
                className={
                  device.status === "online"
                    ? "bg-green-500/10 text-green-500 hover:bg-green-500/20"
                    : ""
                }
              >
                <div
                  className={`w-2 h-2 rounded-full mr-2 ${
                    device.status === "online"
                      ? "bg-green-500 animate-pulse"
                      : "bg-muted-foreground"
                  }`}
                />
                {device.status === "online" ? "Online" : "Offline"}
              </Badge>
              <Select value={timeRange} onValueChange={setTimeRange}>
                <SelectTrigger className="w-[140px]">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1h">Última hora</SelectItem>
                  <SelectItem value="24h">Últimas 24h</SelectItem>
                  <SelectItem value="7d">Últimos 7 dias</SelectItem>
                  <SelectItem value="30d">Últimos 30 dias</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-6 py-8">
        {/* Current Readings */}
        <div className="mb-8">
          <h2 className="text-lg font-medium text-foreground mb-4">
            Leituras Atuais
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4">
            {device.lastReading.t > 0 && (
              <Card className="p-4 bg-card border-border">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-chart-1/10">
                    <Thermometer className="w-5 h-5 text-chart-1" />
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Temperatura</p>
                    <p className="text-xl font-semibold text-foreground">
                      {device.lastReading.t.toFixed(1)}°C
                    </p>
                  </div>
                </div>
              </Card>
            )}

            {device.lastReading.h > 0 && (
              <Card className="p-4 bg-card border-border">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-chart-2/10">
                    <Droplets className="w-5 h-5 text-chart-2" />
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Umidade</p>
                    <p className="text-xl font-semibold text-foreground">
                      {device.lastReading.h.toFixed(1)}%
                    </p>
                  </div>
                </div>
              </Card>
            )}

            {device.lastReading.g > 0 && (
              <Card className="p-4 bg-card border-border">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-chart-3/10">
                    <Wind className="w-5 h-5 text-chart-3" />
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Gás</p>
                    <p className="text-xl font-semibold text-foreground">
                      {device.lastReading.g.toFixed(0)} ppm
                    </p>
                  </div>
                </div>
              </Card>
            )}

            {device.lastReading.fluxo > 0 && (
              <Card className="p-4 bg-card border-border">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-chart-4/10">
                    <Gauge className="w-5 h-5 text-chart-4" />
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Fluxo</p>
                    <p className="text-xl font-semibold text-foreground">
                      {device.lastReading.fluxo.toFixed(2)}
                    </p>
                  </div>
                </div>
              </Card>
            )}

            {device.lastReading.pulso > 0 && (
              <Card className="p-4 bg-card border-border">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-chart-5/10">
                    <Zap className="w-5 h-5 text-chart-5" />
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Pulsos</p>
                    <p className="text-xl font-semibold text-foreground">
                      {device.lastReading.pulso}
                    </p>
                  </div>
                </div>
              </Card>
            )}

            {device.lastReading.solo > 0 && (
              <Card className="p-4 bg-card border-border">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-orange-500/10">
                    <TreePine className="w-5 h-5 text-orange-500" />
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground">Solo</p>
                    <p className="text-xl font-semibold text-foreground">
                      {device.lastReading.solo.toFixed(1)}
                    </p>
                  </div>
                </div>
              </Card>
            )}
          </div>
        </div>

        {/* Charts */}
        <div className="mb-8">
          <h2 className="text-lg font-medium text-foreground mb-4">
            Histórico de Leituras
          </h2>
          <DeviceCharts data={historicalData} timeRange={timeRange} />
        </div>

        {/* Data Table */}
        <div>
          <h2 className="text-lg font-medium text-foreground mb-4">
            Dados Detalhados
          </h2>
          <Card className="bg-card border-border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Timestamp</TableHead>
                  {historicalData.some((r) => r.t > 0) && (
                    <TableHead>Temperatura</TableHead>
                  )}
                  {historicalData.some((r) => r.h > 0) && (
                    <TableHead>Umidade</TableHead>
                  )}
                  {historicalData.some((r) => r.g > 0) && (
                    <TableHead>Gás</TableHead>
                  )}
                  {historicalData.some((r) => r.fluxo > 0) && (
                    <TableHead>Fluxo</TableHead>
                  )}
                  {historicalData.some((r) => r.pulso > 0) && (
                    <TableHead>Pulsos</TableHead>
                  )}
                  {historicalData.some((r) => r.solo > 0) && (
                    <TableHead>Solo</TableHead>
                  )}
                </TableRow>
              </TableHeader>
              <TableBody>
                {historicalData.slice(0, 10).map((reading) => (
                  <TableRow
                    key={`${reading.timestamp}-${reading.t}-${reading.h}`}
                  >
                    <TableCell className="font-mono text-xs">
                      {reading.timestamp}
                    </TableCell>
                    {historicalData.some((r) => r.t > 0) && (
                      <TableCell>
                        {reading.t > 0 ? `${reading.t.toFixed(1)}°C` : "—"}
                      </TableCell>
                    )}
                    {historicalData.some((r) => r.h > 0) && (
                      <TableCell>
                        {reading.h > 0 ? `${reading.h.toFixed(1)}%` : "—"}
                      </TableCell>
                    )}
                    {historicalData.some((r) => r.g > 0) && (
                      <TableCell>
                        {reading.g > 0 ? `${reading.g.toFixed(0)} ppm` : "—"}
                      </TableCell>
                    )}
                    {historicalData.some((r) => r.fluxo > 0) && (
                      <TableCell>
                        {reading.fluxo > 0 ? reading.fluxo.toFixed(2) : "—"}
                      </TableCell>
                    )}
                    {historicalData.some((r) => r.pulso > 0) && (
                      <TableCell>
                        {reading.pulso > 0 ? reading.pulso : "—"}
                      </TableCell>
                    )}
                    {historicalData.some((r) => r.solo > 0) && (
                      <TableCell>
                        {reading.solo > 0 ? reading.solo.toFixed(1) : "—"}
                      </TableCell>
                    )}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Card>
        </div>
      </main>
    </div>
  );
}
