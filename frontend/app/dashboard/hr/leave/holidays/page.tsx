"use client";

import { useEffect, useState } from "react";
import { hrRepository } from "@/repositories/hrRepository";
import { HolidayResponse } from "@/types/hr";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/Table";
import { Badge } from "@/components/ui/Badge";
import { LoadingState } from "@/components/common/LoadingState";
import { ErrorState } from "@/components/common/ErrorState";
import { EmptyState } from "@/components/common/EmptyState";
import { CalendarDays } from "lucide-react";

export default function HolidaysPage() {
  const [holidays, setHolidays] = useState<HolidayResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHolidays = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await hrRepository.getHolidays();
      setHolidays(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load holidays.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHolidays();
  }, []);

  if (isLoading) return <LoadingState message="Loading holidays..." className="py-12" />;
  if (error) return <ErrorState message={error} onRetry={fetchHolidays} />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Holidays</h1>
      </div>

      {holidays.length === 0 ? (
        <EmptyState 
          title="No holidays found"
          description="There are currently no upcoming holidays scheduled."
          icon={<CalendarDays className="w-6 h-6" />}
        />
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Holiday Name</TableHead>
              <TableHead>Date</TableHead>
              <TableHead>Type</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {holidays.map((holiday) => (
              <TableRow key={holiday.id}>
                <TableCell className="font-bold">{holiday.name}</TableCell>
                <TableCell>{new Date(holiday.date).toLocaleDateString()}</TableCell>
                <TableCell>
                  <Badge variant={holiday.is_optional ? "outline" : "default"}>
                    {holiday.is_optional ? "Optional" : "Mandatory"}
                  </Badge>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </div>
  );
}
