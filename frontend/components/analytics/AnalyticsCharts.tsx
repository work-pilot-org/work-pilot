"use client";

import React from "react";
import { 
  BarChart as RechartsBarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer,
  PieChart as RechartsPieChart,
  Pie,
  Cell
} from "recharts";

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

interface BarChartProps {
  data: any[];
  xAxisKey: string;
  bars: { key: string; color: string; name?: string }[];
}

export function CustomBarChart({ data, xAxisKey, bars }: BarChartProps) {
  if (!data || data.length === 0) {
    return <div className="flex h-64 items-center justify-center text-gray-500">No data available</div>;
  }

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <RechartsBarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={xAxisKey} />
          <YAxis />
          <Tooltip />
          <Legend />
          {bars.map((bar) => (
            <Bar key={bar.key} dataKey={bar.key} name={bar.name || bar.key} fill={bar.color} />
          ))}
        </RechartsBarChart>
      </ResponsiveContainer>
    </div>
  );
}

interface PieChartProps {
  data: any[];
  dataKey: string;
  nameKey: string;
}

export function CustomPieChart({ data, dataKey, nameKey }: PieChartProps) {
  if (!data || data.length === 0) {
    return <div className="flex h-64 items-center justify-center text-gray-500">No data available</div>;
  }

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <RechartsPieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name}: ${((percent || 0) * 100).toFixed(0)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey={dataKey}
            nameKey={nameKey}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
        </RechartsPieChart>
      </ResponsiveContainer>
    </div>
  );
}
