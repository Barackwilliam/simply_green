import type { Metadata } from "next";
import { Layers } from "lucide-react";

import { Icon } from "@/components/ui/Icon";
import { Container, EmptyState, PageHeader, Section } from "@/components/ui";
import { getFocusAreas } from "@/lib/api";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";

export const metadata: Metadata = {
  title: "Focus Areas",
  description:
    "Environmental conservation, climate action, waste management, community empowerment, sustainable livelihoods, research and green innovation.",
  alternates: { canonical: "/focus-areas" },
};

export default async function FocusAreasPage() {
  const areas = await getFocusAreas();

  return (
    <>
      <PageHeader
        eyebrow="What we work on"
        title="Focus areas"
        description="Our work spans conservation, climate and livelihoods — because environmental problems in Tanzania do not arrive one at a time."
      />

      <Section>
        <Container>
          {areas.length === 0 ? (
            <EmptyState
              icon={<Layers className="h-10 w-10" />}
              title="No focus areas yet"
              description="Add focus areas in the admin and they will appear here."
            />
          ) : (
            <ul className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {areas.map((area) => (
                <li key={area.id}>
                  <Link
                    href={`/focus-areas/${area.slug}`}
                    className="group flex h-full flex-col rounded-2xl border border-sand-200 bg-white p-7 transition-all duration-300 hover:-translate-y-1 hover:border-green-300 hover:shadow-xl hover:shadow-ink-950/5"
                  >
                    <span className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-green-50 text-green-700">
                      <Icon name={area.icon || "leaf"} className="h-6 w-6" />
                    </span>
                    <h2 className="mt-5 font-display text-xl font-bold text-ink-950">
                      {area.title}
                    </h2>
                    <p className="mt-3 flex-1 text-[0.9375rem] leading-relaxed text-sand-700">
                      {area.summary}
                    </p>
                    <span className="mt-6 inline-flex items-center gap-1.5 text-sm font-semibold text-green-700">
                      Learn more
                      <ArrowUpRight
                        className="h-4 w-4 transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5"
                        aria-hidden
                      />
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </Container>
      </Section>
    </>
  );
}
