import Link from "next/link";
import { ArrowUpRight } from "lucide-react";

import { Container, Section, SectionHeading } from "@/components/ui";
import { Icon } from "@/components/ui/Icon";
import type { FocusArea } from "@/lib/types";

export function FocusAreaGrid({ areas }: { areas: FocusArea[] }) {
  if (areas.length === 0) return null;

  return (
    <Section tone="muted" id="focus-areas">
      <Container>
        <SectionHeading
          eyebrow="What we work on"
          title="Seven focus areas, one goal"
          description="Our work spans conservation, climate and livelihoods — because environmental problems in Tanzania do not arrive one at a time."
        />

        <ul className="mt-14 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {areas.map((area, index) => (
            <li key={area.id}>
              <Link
                href={`/focus-areas/${area.slug}`}
                className="group relative flex h-full flex-col overflow-hidden rounded-2xl border border-sand-200 bg-white p-7 transition-all duration-300 ease-[var(--ease-out-soft)] hover:-translate-y-1 hover:border-green-300 hover:shadow-xl hover:shadow-ink-950/5"
              >
                <span
                  aria-hidden
                  className="absolute inset-x-0 top-0 h-1 origin-left scale-x-0 bg-gradient-to-r from-green-500 to-sky-500 transition-transform duration-300 group-hover:scale-x-100"
                />

                <span
                  className="mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl"
                  style={{
                    backgroundColor:
                      area.accent_colour || CYCLE[index % CYCLE.length].bg,
                    color: area.accent_colour
                      ? "#fff"
                      : CYCLE[index % CYCLE.length].fg,
                  }}
                >
                  <Icon name={area.icon || "leaf"} className="h-6 w-6" />
                </span>

                <h3 className="font-display text-xl font-bold text-ink-950">
                  {area.title}
                </h3>
                <p className="mt-3 flex-1 text-[0.9375rem] leading-relaxed text-sand-700">
                  {area.summary}
                </p>

                <span className="mt-6 inline-flex items-center gap-1.5 text-sm font-semibold text-green-700">
                  Learn more
                  <ArrowUpRight
                    className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-0.5 group-hover:-translate-y-0.5"
                    aria-hidden
                  />
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </Container>
    </Section>
  );
}

/** Rotating tints so the grid reads as a set without seven hand-picked colours. */
const CYCLE = [
  { bg: "#e8f4ce", fg: "#5f7e24" },
  { bg: "#d9f3ff", fg: "#0c6c94" },
  { bg: "#fef2c7", fg: "#b2660c" },
  { bg: "#e0ebe5", fg: "#345147" },
] as const;
