"use client";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { cn } from "@/lib/utils";
import { User } from "@/types/user";
import { getNameInitials } from "@/utils/misc";
import { getUserProfile } from "@/utils/nectar/users";
import { logout } from "@/utils/supabase/auth";
import { getUserAccessToken } from "@/utils/supabase/client";
import { ChevronDown } from "lucide-react";
import React, { useEffect, useState } from "react";

type UserNavProps = React.ComponentPropsWithoutRef<typeof DropdownMenuTrigger>;

export function UserNav({ className }: UserNavProps) {
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  useEffect(() => {
    const fetchCurrentUser = async () => {
      try {
        const userToken = await getUserAccessToken();
        if (userToken === undefined) {
          throw Error("User needs to login!");
        }
        const user = await getUserProfile(userToken);
        setCurrentUser(user);
      } catch (error) {}
    };
    fetchCurrentUser();
  }, []);

  const handleLogout = async () => {
    await logout();
  };

  return (
    <>
      {currentUser !== null && (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className={cn("w-full", className)}>
              <Avatar className="mr-2 h-5 w-5 rounded-lg">
                <AvatarImage
                  src={currentUser.avatarUrl}
                  alt={currentUser.name}
                />
                <AvatarFallback className="text-xs bg-slate-200">
                  {getNameInitials(currentUser.name)}
                </AvatarFallback>
              </Avatar>
              <div className="text-ellipsis overflow-hidden">
                {currentUser.name}
              </div>
              <ChevronDown className="ml-auto h-4 w-4 shrink-0 opacity-50" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-56" align="start" forceMount>
            <DropdownMenuLabel className="font-normal">
              <div className="flex flex-col space-y-1">
                <p className="text-sm font-medium leading-none">
                  {currentUser.name}
                </p>
                <p className="text-xs leading-none text-muted-foreground">
                  {currentUser.email}
                </p>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={handleLogout}>Log out</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      )}
      {currentUser === null && (
        <Button
          variant="outline"
          className={cn("flex justify-start", className)}
        >
          <Avatar className="mr-2 h-5 w-5 rounded-lg bg-slate-50"></Avatar>
          <div className="h-5 w-16 bg-slate-50 rounded-lg"></div>
        </Button>
      )}
    </>
  );
}
