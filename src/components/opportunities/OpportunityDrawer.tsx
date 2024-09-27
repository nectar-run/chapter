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
} from "lucide-react";
import Link from "next/link";

import { Opportunity } from "@/types/opportunity";
import { OpportunityPropList } from "./OpportunityPropList";
import { OpportunityBrand } from "./OpportunityBrand";
import { OpportunityJobPost } from "./OpportunityJobPost";
import { OpportunityContacts } from "./OpportunityContacts";

import { Separator } from "@/components/ui/separator";
import { Investor } from "@/types/company";

interface OpportunityDrawerProps {
  opportunity: Opportunity;
  updateOpportunity: (updatedOpportunity: Opportunity) => void;
}

export function OpportunityDrawer({
  opportunity,
  updateOpportunity,
}: OpportunityDrawerProps) {
  return (
    <>
      <div className="flex flex-col flex-1 m-5 ">
        <OpportunityBrand opportunity={opportunity} />
        <OpportunityJobPost opportunity={opportunity} />
        <OpportunityContacts opportunity={opportunity} />
        <OpportunityPropList
          opportunity={opportunity}
          updateOpportunity={updateOpportunity}
        />
      </div>
    </>
  );
}
