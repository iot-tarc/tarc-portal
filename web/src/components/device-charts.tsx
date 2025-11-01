import { Card } from "@/components/ui/card";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import type { HistoricalReading } from "@/lib/api";

interface DeviceChartsProps {
  data: HistoricalReading[];
  timeRange: string;
}

export function DeviceCharts({ data }: DeviceChartsProps) {
  // Validar se há dados
  if (!data || data.length === 0) {
    return (
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6 bg-card border-border">
          <p className="text-muted-foreground">Nenhum dado disponível</p>
        </Card>
      </div>
    );
  }

  // Calcular domínios dinâmicos para melhor visualização
  const tempValues = data.map((d) => d.t).filter((v) => v != null && !isNaN(v));
  const tempMin = tempValues.length > 0 ? Math.min(...tempValues) : 0;
  const tempMax = tempValues.length > 0 ? Math.max(...tempValues) : 100;
  const tempRange = tempMax - tempMin || 1;
  const tempDomain =
    tempRange > 0
      ? [tempMin - tempRange * 0.1, tempMax + tempRange * 0.1]
      : [tempMin - 5, tempMax + 5];

  const humidityValues = data
    .map((d) => d.h)
    .filter((v) => v != null && !isNaN(v));
  const humidityMin =
    humidityValues.length > 0 ? Math.min(...humidityValues) : 0;
  const humidityMax =
    humidityValues.length > 0 ? Math.max(...humidityValues) : 100;
  const humidityRange = humidityMax - humidityMin || 1;
  const humidityDomain =
    humidityRange > 0
      ? [
          Math.max(0, humidityMin - humidityRange * 0.1),
          Math.min(100, humidityMax + humidityRange * 0.1),
        ]
      : [0, 100];

  const gasValues = data.map((d) => d.g).filter((v) => v != null && !isNaN(v));
  const gasMin = gasValues.length > 0 ? Math.min(...gasValues) : 0;
  const gasMax = gasValues.length > 0 ? Math.max(...gasValues) : 100;
  const gasRange = gasMax - gasMin || 1;
  const gasDomain =
    gasRange > 0
      ? [Math.max(0, gasMin - gasRange * 0.1), gasMax + gasRange * 0.1]
      : [0, gasMax + 10];

  const fluxoValues = data
    .map((d) => d.fluxo)
    .filter((v) => v != null && !isNaN(v));
  const pulsoValues = data
    .map((d) => d.pulso)
    .filter((v) => v != null && !isNaN(v));
  const soloValues = data
    .map((d) => d.solo)
    .filter((v) => v != null && !isNaN(v));
  const flowMin = fluxoValues.length > 0 ? Math.min(...fluxoValues) : 0;
  const flowMax = fluxoValues.length > 0 ? Math.max(...fluxoValues) : 100;
  const pulseMin = pulsoValues.length > 0 ? Math.min(...pulsoValues) : 0;
  const pulseMax = pulsoValues.length > 0 ? Math.max(...pulsoValues) : 100;
  const soloMin = soloValues.length > 0 ? Math.min(...soloValues) : 0;
  const soloMax = soloValues.length > 0 ? Math.max(...soloValues) : 100;
  const combinedMin = Math.min(flowMin, pulseMin);
  const combinedMax = Math.max(flowMax, pulseMax);
  const combinedRange = combinedMax - combinedMin || 1;
  const combinedDomain =
    combinedRange > 0
      ? [
          Math.max(0, combinedMin - combinedRange * 0.1),
          combinedMax + combinedRange * 0.1,
        ]
      : [0, combinedMax + 10];
  const soloRange = soloMax - soloMin || 1;
  const soloDomain =
    soloRange > 0
      ? [Math.max(0, soloMin - soloRange * 0.1), soloMax + soloRange * 0.1]
      : [0, soloMax + 10];

  // Verificar se há dados de solo
  const hasSoloData = soloValues.length > 0 && soloMax > 0;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Temperature Chart */}
      <Card className="p-6 bg-card border-border">
        <h3 className="text-sm font-medium text-foreground mb-4">
          Temperatura ao Longo do Tempo
        </h3>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart
            data={data}
            margin={{ top: 5, right: 10, left: 0, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
            <XAxis
              dataKey="timestamp"
              className="text-xs"
              tick={{ fill: "hsl(var(--muted-foreground))" }}
            />
            <YAxis
              className="text-xs"
              tick={{ fill: "hsl(var(--muted-foreground))" }}
              domain={tempDomain}
              allowDataOverflow={false}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(var(--card))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "var(--radius)",
              }}
            />
            <Line
              type="monotone"
              dataKey="t"
              stroke="hsl(220, 70%, 50%)"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4 }}
              name="Temperatura (°C)"
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </Card>

      {/* Humidity Chart */}
      <Card className="p-6 bg-card border-border">
        <h3 className="text-sm font-medium text-foreground mb-4">
          Umidade ao Longo do Tempo
        </h3>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart
            data={data}
            margin={{ top: 5, right: 10, left: 0, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
            <XAxis
              dataKey="timestamp"
              className="text-xs"
              tick={{ fill: "hsl(var(--muted-foreground))" }}
            />
            <YAxis
              className="text-xs"
              tick={{ fill: "hsl(var(--muted-foreground))" }}
              domain={humidityDomain}
              allowDataOverflow={false}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(var(--card))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "var(--radius)",
              }}
            />
            <Line
              type="monotone"
              dataKey="h"
              stroke="hsl(142, 76%, 36%)"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4 }}
              name="Umidade (%)"
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </Card>

      {/* Gas Chart */}
      <Card className="p-6 bg-card border-border">
        <h3 className="text-sm font-medium text-foreground mb-4">
          Nível de Gás ao Longo do Tempo
        </h3>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart
            data={data}
            margin={{ top: 5, right: 10, left: 0, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
            <XAxis
              dataKey="timestamp"
              className="text-xs"
              tick={{ fill: "hsl(var(--muted-foreground))" }}
            />
            <YAxis
              className="text-xs"
              tick={{ fill: "hsl(var(--muted-foreground))" }}
              domain={gasDomain}
              allowDataOverflow={false}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(var(--card))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "var(--radius)",
              }}
            />
            <Line
              type="monotone"
              dataKey="g"
              stroke="hsl(38, 92%, 50%)"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4 }}
              name="Gás (ppm)"
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </Card>

      {/* Flow and Pulse Chart */}
      <Card className="p-6 bg-card border-border">
        <h3 className="text-sm font-medium text-foreground mb-4">
          Fluxo e Pulsos ao Longo do Tempo
        </h3>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart
            data={data}
            margin={{ top: 5, right: 10, left: 0, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
            <XAxis
              dataKey="timestamp"
              className="text-xs"
              tick={{ fill: "hsl(var(--muted-foreground))" }}
            />
            <YAxis
              className="text-xs"
              tick={{ fill: "hsl(var(--muted-foreground))" }}
              domain={combinedDomain}
              allowDataOverflow={false}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(var(--card))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "var(--radius)",
              }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="fluxo"
              stroke="hsl(262, 83%, 58%)"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4 }}
              name="Fluxo"
              isAnimationActive={false}
            />
            <Line
              type="monotone"
              dataKey="pulso"
              stroke="hsl(291, 64%, 42%)"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4 }}
              name="Pulsos"
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </Card>

      {/* Solo Chart - apenas se houver dados */}
      {hasSoloData && (
        <Card className="p-6 bg-card border-border">
          <h3 className="text-sm font-medium text-foreground mb-4">
            Solo ao Longo do Tempo
          </h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart
              data={data}
              margin={{ top: 5, right: 10, left: 0, bottom: 5 }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="hsl(var(--border))"
              />
              <XAxis
                dataKey="timestamp"
                className="text-xs"
                tick={{ fill: "hsl(var(--muted-foreground))" }}
              />
              <YAxis
                className="text-xs"
                tick={{ fill: "hsl(var(--muted-foreground))" }}
                domain={soloDomain}
                allowDataOverflow={false}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: "var(--radius)",
                }}
              />
              <Line
                type="monotone"
                dataKey="solo"
                stroke="hsl(25, 95%, 53%)"
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4 }}
                name="Solo"
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </Card>
      )}
    </div>
  );
}
