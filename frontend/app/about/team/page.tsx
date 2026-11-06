import type { Metadata } from "next";
import { Users } from "lucide-react";

import { TeamCard } from "@/components/cards";
import { Container, EmptyState, PageHeader, Section, SectionHeading } from "@/components/ui";
import { getTeam } from "@/lib/api";
import type { TeamMember } from "@/lib/types";

export const metadata: Metadata = {
  title: "Our Team",
  description:
    "The people behind Simply Green Organization's work on environmental sustainability and climate action in Tanzania.",
  alternates: { canonical: "/about/team" },
};

/** Display order for the groups, so leadership leads. */
const GROUP_ORDER = ["leadership", "board", "staff", "advisor", "volunteer"];

export default async function TeamPage() {
  const members = await getTeam();

  const grouped = new Map<string, { label: string; people: TeamMember[] }>();
  for (const member of members) {
    const entry = grouped.get(member.group) ?? {
      label: member.group_label,
      people: [],
    };
    entry.people.push(member);
    grouped.set(member.group, entry);
  }

  const sections = GROUP_ORDER.filter((group) => grouped.has(group)).map(
    (group) => ({ group, ...grouped.get(group)! }),
  );

  return (
    <>
      <PageHeader
        eyebrow="About us"
        title="Our team"
        description="The people who turn plans into work on the ground."
      />

      <Section>
        <Container>
          {sections.length === 0 ? (
            <EmptyState
              icon={<Users className="h-10 w-10" />}
              title="Team members have not been added yet"
              description="Once staff and board members are added in the admin, they will appear here."
            />
          ) : (
            <div className="space-y-20">
              {sections.map((section) => (
                <div key={section.group}>
                  <SectionHeading title={section.label} />
                  <ul className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
                    {section.people.map((member) => (
                      <li key={member.id}>
                        <TeamCard member={member} />
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          )}
        </Container>
      </Section>
    </>
  );
}
