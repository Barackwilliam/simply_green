import Image from "next/image";
import Link from "next/link";
import { ArrowRight, MapPin, Users } from "lucide-react";

import { Badge, ButtonLink, Container, Section, SectionHeading } from "@/components/ui";
import type { Programme } from "@/lib/types";

export function ProgrammeShowcase({
  programmes,
  fallbackImage,
}: {
  programmes: Programme[];
  fallbackImage: string;
}) {
  if (programmes.length === 0) return null;

  return (
    <Section>
      <Container>
        <div className="flex flex-col gap-6 sm:flex-row sm:items-end sm:justify-between">
          <SectionHeading
            eyebrow="On the ground"
            title="Programmes running now"
            description="Community-led work in schools, markets and coastal villages across Dar es Salaam."
          />
          <ButtonLink href="/programmes" variant="outline" className="shrink-0">
            All programmes
            <ArrowRight className="h-4 w-4" aria-hidden />
          </ButtonLink>
        </div>

        <ul className="mt-14 grid gap-6 lg:grid-cols-3">
          {programmes.slice(0, 3).map((programme) => (
            <li key={programme.id}>
              <Link
                href={`/programmes/${programme.slug}`}
                className="group flex h-full flex-col overflow-hidden rounded-2xl border border-sand-200 bg-white transition-all duration-300 ease-[var(--ease-out-soft)] hover:-translate-y-1 hover:border-green-300 hover:shadow-xl hover:shadow-ink-950/5"
              >
                <div className="relative aspect-[16/10] overflow-hidden bg-sand-100">
                  <Image
                    src={programme.featured_image ?? fallbackImage}
                    alt={programme.title}
                    fill
                    sizes="(min-width: 1024px) 30vw, (min-width: 640px) 50vw, 100vw"
                    className="object-cover transition-transform duration-500 ease-[var(--ease-out-soft)] group-hover:scale-[1.04]"
                  />
                  <div className="absolute left-4 top-4">
                    <Badge
                      tone={
                        programme.status === "ongoing" ? "green" : "neutral"
                      }
                      className="shadow-sm"
                    >
                      {programme.status_label}
                    </Badge>
                  </div>
                </div>

                <div className="flex flex-1 flex-col p-6">
                  <h3 className="font-display text-lg font-bold leading-snug text-ink-950 group-hover:text-green-700">
                    {programme.title}
                  </h3>

                  <p className="mt-3 flex-1 text-sm leading-relaxed text-sand-700">
                    {programme.summary.length > 170
                      ? `${programme.summary.slice(0, 170).trimEnd()}…`
                      : programme.summary}
                  </p>

                  <dl className="mt-5 space-y-2 border-t border-sand-100 pt-4 text-xs text-sand-600">
                    {programme.location ? (
                      <div className="flex items-start gap-2">
                        <dt className="sr-only">Location</dt>
                        <MapPin
                          className="mt-px h-3.5 w-3.5 shrink-0 text-green-600"
                          aria-hidden
                        />
                        <dd>{programme.location}</dd>
                      </div>
                    ) : null}
                    {programme.beneficiaries ? (
                      <div className="flex items-start gap-2">
                        <dt className="sr-only">Beneficiaries</dt>
                        <Users
                          className="mt-px h-3.5 w-3.5 shrink-0 text-green-600"
                          aria-hidden
                        />
                        <dd>{programme.beneficiaries}</dd>
                      </div>
                    ) : null}
                  </dl>
                </div>
              </Link>
            </li>
          ))}
        </ul>
      </Container>
    </Section>
  );
}
