"use client";

import React from "react";

import { Cross2Icon } from "@radix-ui/react-icons";
import { Table } from "@tanstack/react-table";

import { Button } from "@/components/ui/button";
// import { Input } from "@/components/ui/input";
import { DataTableViewOptions } from "@/components/data-table/data-table-view-options";
import {
  DataTableFacetedFilter,
  FilterOptions,
} from "@/components/data-table/data-table-faceted-filter";

export interface ToolbarFilter {
  tableColumnName: string;
  label: string;
  filterOptions: FilterOptions[];
}

interface DataTableToolbarProps<TData> {
  table: Table<TData>;
  filters: ToolbarFilter[];
  filterColumnName: string;
  responseRecords: TData[];
}

export function DataTableToolbar<TData>({
  table,
  filters,
  filterColumnName,
  responseRecords,
}: DataTableToolbarProps<TData>) {
  const isFiltered = table.getState().columnFilters.length > 0;

  return (
    <div className="flex items-center justify-between relative space-x-3 px-4 h-14">
      <h2 className="flex text-sm font-medium">
        {responseRecords.length}{" "}
        {responseRecords.length === 1 ? "Response" : "Responses"}
      </h2>
      <div className="flex items-center space-x-2 relative">
        {filters.map((item, index) => (
          <DataTableFacetedFilter
            key={index}
            column={table.getColumn(item.tableColumnName)}
            title={item.label}
            options={item.filterOptions}
          />
        ))}
        {isFiltered && (
          <Button
            variant="ghost"
            onClick={() => table.resetColumnFilters()}
            className="h-8 px-2 lg:px-3"
          >
            Reset
            <Cross2Icon className="ml-2 h-4 w-4" />
          </Button>
        )}
        <DataTableViewOptions table={table} />
      </div>
    </div>
  );
}
