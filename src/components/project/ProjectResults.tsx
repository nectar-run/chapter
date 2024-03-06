"use client";

import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";
import { z } from "zod";
import { parseISO } from "date-fns";
import { Separator } from "@/components/ui/separator";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";

import { Project, ProjectResponse } from "@/types/project";
import { DataTable } from "@/components/data-table/data-table";
import {
  resultColumns,
  ProjectResponseRecord,
  ProjectResponseRecordSchema,
  filters,
} from "@/components/project/result-columns";
import { ProjectResponseDetails } from "@/components/project/ProjectResponseDetails";

interface ProjectResultsProps {
  project: Project;
}

function titleCaseToCamelCase(titleCaseString: string): string {
  return titleCaseString
    .replace(/\s(.)/g, ($1) => $1.toUpperCase())
    .replace(/\s/g, "")
    .replace(/^(.)/, ($1) => $1.toLowerCase());
}

async function getProjectResponses(id: string) {
  // TODO: Fetch project responses
  const jwtToken =
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDk4MDYwOTQsInN1YiI6InRlc3RAbmVjdGFyLnJ1biIsImlhdCI6MTcwOTcxOTY5NCwiZXh0cmFzIjp7fX0.1bjE2vGjg1gV1B_8oE-h80YX3-lfSA3W07vhtAFxRy8";
  const response = await fetch(
    "http://localhost:8000/api/projects/" + id + "/responses",
    {
      method: "GET",
      headers: {
        Authorization: `Bearer ${jwtToken}`,
      },
    },
  );
  if (!response.ok) {
    throw new Error("Failed to fetch data");
  }
  const data = await response.json();
  const projectResponses =
    "items" in data
      ? data["items"].map((item: any) => ({
          ...item,
          startedAt: parseISO(item.startedAt),
        }))
      : [];
  return z.array(ProjectResponseRecord).parse(
    projectResponses.map((response: ProjectResponse) => {
      const record: Record<string, any> = {
        id: response.id,
        date: response.startedAt.toLocaleString(),
        participant: response.participant.name,
        stage: response.state.stage,
      };
      response.scores.forEach((item) => {
        record[titleCaseToCamelCase(item.name)] = item.score;
      });
      return record;
    }),
  );
}

export function ProjectResults({ project }: ProjectResultsProps) {
  const defaultCollapsed = false;
  const defaultLayout = [80, 20];
  const navCollapsedSize = 20;
  const [responses, setResponses] = useState<ProjectResponseRecordSchema[]>([]);
  const [selectedRow, setSelectedRow] = useState<ProjectResponse | null>(null);

  useEffect(() => {
    const fetchProject = async () => {
      try {
        const resp = await getProjectResponses(project.id);
        setResponses(resp);
      } catch (error) {
        console.log(error);
      }
    };
    fetchProject();
  }, [project]);

  const handleRowClick = function <TData>(data: TData) {
    setSelectedRow(data as ProjectResponse);
  };

  return (
    <>
      <ResizablePanelGroup direction="horizontal" className="items-stretch">
        <ResizablePanel
          defaultSize={defaultLayout[0]}
          collapsedSize={navCollapsedSize}
          collapsible={true}
          minSize={20}
          maxSize={80}
        >
          <div className="px-6">
            <div className="items-center justify-between py-5">
              <h2 className="text-xl font-semibold my-2">
                {responses.length}{" "}
                {responses.length === 1 ? "Response" : "Responses"}
              </h2>
            </div>
            <DataTable
              columns={resultColumns}
              data={responses}
              filters={filters}
              filterColumnName="participant"
              onRowClick={handleRowClick}
            />
          </div>
        </ResizablePanel>
        <ResizableHandle />
        <ResizablePanel
          defaultSize={defaultLayout[1]}
          minSize={20}
          maxSize={50}
        >
          <ProjectResponseDetails projectResponse={selectedRow} />
        </ResizablePanel>
      </ResizablePanelGroup>
    </>
  );
}
