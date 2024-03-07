"use client";
import React, { useEffect, useState, useRef } from "react";
import { ServerCrash } from "lucide-react";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button, buttonVariants } from "@/components/ui/button";

import { ProjectDefinition } from "@/components/project/ProjectDefinition";
import { ProjectResults } from "@/components/project/ProjectResults";
import { ErrorMessage } from "@/components/ErrorMessage";
import { Project } from "@/types/project";

async function getProject(id: string) {
  const jwtToken =
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDk4OTU3NzgsInN1YiI6InRlc3RAbmVjdGFyLnJ1biIsImlhdCI6MTcwOTgwOTM3OCwiZXh0cmFzIjp7fX0.f1reY5_k-8m5tRU9G9Y5ZVVgfQpgV8wEyQb7kyknyyg";
  const response = await fetch("http://localhost:8000/api/projects/" + id, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${jwtToken}`,
    },
  });
  if (!response.ok) {
    throw new Error("Failed to fetch data");
  }
  const data = await response.json();
  const project = data as Project;
  return project;
}

interface ProjectDetailsProps {
  projectId: string;
}

export function ProjectDetails({ projectId }: ProjectDetailsProps) {
  const errorOccurred = useRef<boolean>(true);
  const [project, setProject] = useState<Project | null>(null);

  useEffect(() => {
    const fetchProject = async () => {
      try {
        const proj = await getProject(projectId);
        setProject(proj);
        errorOccurred.current = false;
      } catch (error) {
        errorOccurred.current = true;
      }
    };
    fetchProject();
  }, [projectId]);

  return (
    <>
      {!errorOccurred.current && project !== null ? (
        <Tabs defaultValue="definition">
          <div className="flex flex-col h-dvh overflow-hidden">
            {/* <div className="flex items-center justify-between py-4 border-b border-slate-100 h-16"></div> */}

            <div className="flex flex-row items-center justify-between py-4 border-b border-slate-100 h-16 px-6 ">
              <div className="flex flex-1 flex-shrink-0 overflow-hidden   me-8">
                <p className="text-slate-700 text-base font-medium truncate text-ellipsis">
                  {project.name}
                </p>
              </div>

              <div className="space-between flex-1 items-center justify-center">
                <TabsList>
                  <TabsTrigger value="definition" className="relative">
                    Create
                  </TabsTrigger>
                  <TabsTrigger value="results">Responses</TabsTrigger>
                  <TabsTrigger value="insights" disabled>
                    Insights
                  </TabsTrigger>
                </TabsList>
              </div>
              <div className="overflow-hidden justify-end">
                <Button variant="outline" className="me-2">
                  Preview
                </Button>
                <Button variant="default">Publish</Button>
              </div>
            </div>

            <TabsContent
              value="definition"
              className="mt-0 data-[state=active]:flex flex-1 overflow-hidden p-0"
            >
              <ProjectDefinition project={project} setProject={setProject} />
            </TabsContent>

            <TabsContent
              value="results"
              className="content-start border-none p-0 data-[state=active]:flex flex-1 overflow-hidden mt-0"
            >
              <ProjectResults project={project} />
            </TabsContent>
          </div>
        </Tabs>
      ) : (
        <ErrorMessage />
      )}
    </>
  );
}
