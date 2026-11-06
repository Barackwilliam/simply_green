import type { Metadata } from "next";
import { Sprout } from "lucide-react";

import { ProgrammeFilter } from "@/components/programmes/ProgrammeFilter";
import { Container, EmptyState, PageHeader, Section } from "@/components/ui";
import { getFocusAreas, getProgrammes } from "@/lib/api";

export const metadata: Metadata = {
  title: "Programmes",
  description:
    "Community-led environmental programmes run by Simply Green Organization in schools, markets and coastal villages across Dar es Salaam.",
  alternates: { canonical: "/programmes" },
};

export default async function ProgrammesPage() {
  const [programmes, focusAreas] = await Promise.all([
    getProgrammes(),
    getFocusAreas(),
  ]);

  return (
    <>
      <PageHeader
        eyebrow="Our work"
        title="Programmes"
        description="What we are running now, and what we have delivered."
      />

      <Section>
        <Container>
          {programmes.length === 0 ? (
            <EmptyState
              icon={<Sprout className="h-10 w-10" />}
              title="No programmes published yet"
              description="Programmes added in the admin will appear here."
            />
          ) : (
            <ProgrammeFilter
              programmes={programmes}
              focusAreas={focusAreas.map((area) => ({
                slug: area.slug,
                title: area.title,
              }))}
            />
          )}
        </Container>
      </Section>
    </>
  );
}
