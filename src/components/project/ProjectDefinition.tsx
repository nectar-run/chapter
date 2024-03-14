"use client";
import React, { useCallback, useEffect, useState } from "react";

import clsx from "clsx";

import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";
import { useToast } from "@/components/ui/use-toast";
import {
  type Project,
  ProjectOutroAction,
  ProjectResponseStage,
  type Question,
  QuestionFormat,
} from "@/types/project";
import { SparklesIcon, Trash2 } from "lucide-react";
import { updateProject, publishProject } from "@/utils/nectar/projects";
import { getUserAccessToken } from "@/utils/supabase/client";

import EmojiHeader from "@/components/project/EmojiHeader";

interface ProjectDefinitionProps {
  project: Project;
  setProject: React.Dispatch<React.SetStateAction<Project | null>>;
}

export function ProjectDefinition({
  project,
  setProject,
}: ProjectDefinitionProps) {
  const [dataChanged, setDataChanged] = useState(false);
  const { toast } = useToast();
  const saveChanges = useCallback(async () => {
    try {
      if (!dataChanged) {
        return;
      }
      const userToken = await getUserAccessToken();
      if (userToken === undefined) {
        throw Error("User needs to login!");
      }
      await updateProject(userToken, project);
      setDataChanged(false);
      toast({
        title: "Your changes have been saved!",
      });
    } catch {
      toast({
        title: "Oops! Failed to save :(",
        variant: "destructive",
      });
    }
  }, [project, dataChanged, toast]);

  useEffect(() => {
    window.addEventListener("beforeunload", saveChanges);
    return () => {
      window.removeEventListener("beforeunload", saveChanges);
    };
  }, [saveChanges]);

  useEffect(() => {
    setDataChanged(true);
  }, [project]);

  function classNames(...classes: string[]) {
    return classes.filter(Boolean).join(" ");
  }

  const handlePublish = async () => {
    const userToken = await getUserAccessToken();
    if (userToken === undefined) {
      throw Error("User needs to login!");
    }
    await publishProject(userToken, project.id);
  };

  return (
    <>
      <div className="flex flex-col bg-background  w-96 justify-start">
        <div>
          <div
            className={clsx(
              "flex flex-row pt-3 items-center justify-between gap-x-2 pb-3 px-6",
              {
                "bg-orange-100": !dataChanged,
              }
            )}
          >
            {!dataChanged && (
              <p className="text-sm text-slate-500">Changes auto saved...</p>
            )}

            <Button variant="default" onClick={handlePublish}>
              Publish
            </Button>
          </div>
          <Separator className="bg-slate-100" />
        </div>
        <div className="flex flex-col gap-y-3 pt-8">
          <CardContent>
            <div className="grid gap-y-6">
              <div className="grid gap-3">
                <Label htmlFor="subject">Project name</Label>
                <Input
                  id="subject"
                  placeholder="A short name for this project."
                  value={project.name}
                  onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                    setProject({
                      ...project,
                      ["name"]: event.target.value,
                    });
                  }}
                  onBlur={saveChanges}
                />
              </div>
              <div className="grid gap-3">
                <Label htmlFor="subject">Target user</Label>
                <Input
                  id="subject"
                  placeholder="e.g. Product Managers, UX Researchers"
                  value={project.candidatePersonas.join(", ")}
                  onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                    setProject({
                      ...project,
                      ["candidatePersonas"]: event.target.value
                        .split(",")
                        .map((token) => token.trim()),
                    });
                  }}
                  onBlur={saveChanges}
                />
              </div>
              <div className="grid gap-3">
                <Label htmlFor="description">Project goal</Label>
                <Textarea
                  id="description"
                  placeholder="What do you expect to learn from this project?"
                  value={project.goal}
                  onChange={(event: React.ChangeEvent<HTMLTextAreaElement>) => {
                    setProject({
                      ...project,
                      ["goal"]: event.target.value,
                    });
                  }}
                  onBlur={saveChanges}
                />
              </div>
              <Separator className="bg-slate-100 my-4" />
            </div>
          </CardContent>
          <CardContent>
            <div className="grid gap-y-6">
              <div className="grid gap-3">
                <Label htmlFor="subject">Interviewer name</Label>
                <Input
                  id="subject"
                  placeholder="I need help with..."
                  value={
                    project.authors.length > 0 ? project.authors[0].name : ""
                  }
                  readOnly
                />
              </div>
            </div>
          </CardContent>
        </div>
      </div>

      <div className="flex flex-1 flex-col overflow-auto bg-slate-100 gap-4">
        <div className="w-2/3 mx-auto">
          <ul className="flex-1 overflow-y-auto space-y-4 py-6">
            <li>
              <Card className="flex-none">
                <EmojiHeader status="Welcome" />
                <CardContent>
                  <form>
                    <div className="grid w-full items-center gap-1">
                      <div className="flex flex-col space-y-3">
                        <Label htmlFor="name">Welcome message</Label>
                        <Input
                          id="name"
                          placeholder="How you'd like to start the conversation"
                          value={project.intro.title}
                          onChange={(
                            event: React.ChangeEvent<HTMLInputElement>
                          ) => {
                            project.intro.title = event.target.value;
                            setProject({
                              ...project,
                              ["intro"]: {
                                title: event.target.value,
                                description: project.intro.description,
                              },
                            });
                          }}
                          onBlur={saveChanges}
                        />
                      </div>
                    </div>
                  </form>
                </CardContent>
              </Card>
            </li>

            {project.components.map((component, index) => (
              <li key={index}>
                <Card className="flex-none">
                  <div className="flex flex-row items-center justify-between">
                    <EmojiHeader status="Thread" />

                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="outline" size="icon" className="me-6">
                          <Trash2 className="h-4 w-4" />
                          <span className="sr-only">More</span>
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem
                          onClick={() => {
                            const updatedComponents: Question[] = [
                              ...project.components.slice(0, index),
                              ...project.components.slice(index + 1),
                            ];
                            setProject({
                              ...project,
                              ["components"]: updatedComponents,
                            });
                          }}
                        >
                          Delete
                        </DropdownMenuItem>
                        <DropdownMenuItem>Cancel</DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>

                  <CardContent>
                    <form>
                      <div className="grid w-full items-center gap-1">
                        <div className="flex flex-col space-y-3">
                          <Label htmlFor="name">Question</Label>
                          <Input
                            id="name"
                            placeholder="How you'd like to start the conversation"
                            value={component.question}
                            onChange={(
                              event: React.ChangeEvent<HTMLInputElement>
                            ) => {
                              const updatedComponents: Question[] = [
                                ...project.components,
                              ];
                              updatedComponents[index].question =
                                event.target.value;
                              setProject({
                                ...project,
                                ["components"]: updatedComponents,
                              });
                            }}
                            onBlur={saveChanges}
                          />
                          <div className="flex flex-row space-x-3 items-center">
                            <Button variant={"outline"} size={"sm"}>
                              <SparklesIcon className="mr-2 h-4 w-4" />
                              Improve
                            </Button>
                            <p className="text-xs text-slate-400 flex">
                              Remove bias or hypothetical questioning using AI
                            </p>
                          </div>
                        </div>

                        <Separator className="my-4" />

                        <div className="flex flex-row items-center justify-between ">
                          <Label htmlFor="name"># of followup questions</Label>
                          <Select
                            defaultValue={component.followups.toString()}
                            onValueChange={(value: string) => {
                              project.components[index].followups =
                                parseInt(value);
                            }}
                            onOpenChange={saveChanges}
                          >
                            <SelectTrigger className="w-[120px]">
                              <SelectValue placeholder="Select" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectGroup>
                                <SelectItem value="1">1</SelectItem>
                                <SelectItem value="2">2</SelectItem>
                                <SelectItem value="3">3</SelectItem>
                              </SelectGroup>
                            </SelectContent>
                          </Select>
                        </div>
                      </div>
                    </form>
                  </CardContent>
                </Card>
              </li>
            ))}

            <li>
              <Button
                variant="outline"
                className="w-full border-dashed bg-white/20"
                onClick={() => {
                  const updatedComponents: Question[] = [
                    ...project.components,
                    {
                      question: "",
                      format: QuestionFormat.OPEN_ENDED,
                      followups: 2,
                    },
                  ];
                  setProject({
                    ...project,
                    ["components"]: updatedComponents,
                  });
                }}
              >
                Add thread
              </Button>
            </li>

            <li>
              <Card className="flex-none">
                <EmojiHeader status="Thanks" />

                <CardContent>
                  <form>
                    <div className="grid w-full items-center gap-3">
                      <div className="flex flex-col space-y-3">
                        <Label htmlFor="name">Message</Label>
                        <Input
                          id="name"
                          placeholder="Wow! thanks for sharing your insights with us."
                          value={project.outros.COMPLETED.title}
                          onChange={(
                            event: React.ChangeEvent<HTMLInputElement>
                          ) => {
                            setProject({
                              ...project,
                              ["outros"]: {
                                [ProjectResponseStage.COMPLETED]: {
                                  title: event.target.value,
                                  description:
                                    project.outros.COMPLETED.description,
                                  actions: project.outros.COMPLETED.actions,
                                },
                              },
                            });
                          }}
                          onBlur={saveChanges}
                        />
                      </div>
                      <Separator className="my-4" />

                      <div className="grid grid-cols-2 gap-3">
                        <div className="flex flex-col space-y-3">
                          <div className="flex flex-row justify-start space-x-3 items-center">
                            <Label htmlFor="name">Add calendar link</Label>
                            <Switch
                              checked={project.outros.COMPLETED.actions.includes(
                                ProjectOutroAction.AUTHOR_CALENDAR_LINK
                              )}
                              onCheckedChange={(checked: boolean) => {
                                let newActions: ProjectOutroAction[] = [];
                                if (checked) {
                                  newActions = [
                                    ...project.outros.COMPLETED.actions,
                                    ProjectOutroAction.AUTHOR_CALENDAR_LINK,
                                  ];
                                } else {
                                  project.outros.COMPLETED.actions.filter(
                                    (value) =>
                                      value !==
                                      ProjectOutroAction.AUTHOR_CALENDAR_LINK
                                  );
                                }
                                setProject({
                                  ...project,
                                  ["outros"]: {
                                    [ProjectResponseStage.COMPLETED]: {
                                      title: project.outros.COMPLETED.title,
                                      description:
                                        project.outros.COMPLETED.description,
                                      actions: newActions,
                                    },
                                  },
                                });
                              }}
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </form>
                </CardContent>
              </Card>
            </li>
          </ul>
        </div>
      </div>
    </>
  );
}
