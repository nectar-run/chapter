import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import Image from "next/image";
import { timeAgo } from "@/utils/misc";
import { type Person } from "@/types/person";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import {
  Divide,
  ExternalLink,
  Maximize2,
  Users,
  Factory,
  MapPin,
  Landmark,
  Banknote,
  Target,
  Loader,
  StickyNote,
  ChevronRight,
  CircleUserIcon,
  Linkedin,
  Mail,
  CircleUserRoundIcon,
} from "lucide-react";
import Link from "next/link";

import { Opportunity } from "@/types/opportunity";
import { OpportunityPropList } from "./OpportunityPropList";
import { OpportunityBrand } from "./OpportunityBrand";
import { OpportunityJobPost } from "./OpportunityJobPost";

import { Separator } from "@/components/ui/separator";
import { Investor } from "@/types/company";

interface OpportunityDrawerProps {
  opportunity: Opportunity;
}

export function OpportunityContacts({ opportunity }: OpportunityDrawerProps) {
  return (
    <>
      <h3 className="text-base font-medium my-4 text-zinc-700 dark:text-zinc-200 ps-2">
        Contacts{" "}
      </h3>
      {opportunity.contacts !== null &&
        opportunity.contacts.length > 0 &&
        opportunity.contacts.map((contact: Person, index) => (
          <div
            className="flex flex-row items-center justify-between text-sm text-zinc-700"
            key={index}
          >
            <div className="flex flex-row p-2 hover:bg-zinc-100 dark:hover:bg-zinc-700/20 gap-x-1 rounded-lg text-sm items-center cursor-pointer">
              <CircleUserRoundIcon
                width={18}
                className="text-zinc-400 dark:text-zinc-300"
              />
              <p
                className="font-medium text-zinc-700 dark:text-zinc-200"
                key={index}
              >
                {contact.fullName}
              </p>
              <p className="font-medium text-zinc-500 dark:text-zinc-300">·</p>
              <p className="text-zinc-500 dark:text-zinc-400" key={index}>
                {contact.occupation}
              </p>
            </div>

            <div
              className="flex flex-row justify-end gap-x-2 items-center"
              key={index}
            >
              {contact.linkedinProfileUrl && (
                <>
                  <a
                    href={contact.linkedinProfileUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <Button
                      className="dark:bg-zinc-700/50 dark:hover:bg-zinc-600/50"
                      variant={"secondary"}
                    >
                      <ExternalLink className="mr-2 h-4 w-4" />
                      LinkedIn
                    </Button>
                  </a>
                </>
              )}
              {contact.workEmails && (
                <>
                  <a
                    href={contact.workEmails[0]}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <Button
                      variant={"secondary"}
                      className="dark:bg-zinc-700/50 dark:hover:bg-zinc-600/50"
                    >
                      <Mail className="mr-2 h-4 w-4" />
                      <p>Copy</p>
                    </Button>
                  </a>
                </>
              )}
            </div>
          </div>
        ))}
    </>
  );
}
