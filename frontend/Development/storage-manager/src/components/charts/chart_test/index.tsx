"use client"

import {Pie, PieChart, Bar, BarChart, Area, AreaChart, CartesianGrid, XAxis} from "recharts"

import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"

interface chart_data_interface {
  ID: number
  Name: string
  Details: string
  ID_image: number
  ID_storage: number
  value: number
  Token_product: string
  Category: string
  State: string
}

interface Props {
  data: chart_data_interface[]
}

const chartConfig = {
  value: {
    label: "Valor",
    color: "hsl(var(--chart-1))",
  },
}

export function ProductsChart({ data }: Props) {
  return (
    <ChartContainer config={chartConfig}>
      <AreaChart data={data}>
        <CartesianGrid vertical={false} />

        <XAxis
          dataKey="State"
          tickLine={false}
          axisLine={false}
        />

        <ChartTooltip
          content={<ChartTooltipContent />}
        />

        <Area
          dataKey="value"
          fill="var(--color-value)"
          radius={8}
        />
      </AreaChart>
    </ChartContainer>
  )
}