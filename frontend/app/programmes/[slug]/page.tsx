import type { Metadata } from "next";
import Image from "next/image";
import { notFound } from "next/navigation";
import { CalendarDays, MapPin, Target, Users } from "lucide-react";

import { Badge, ButtonLink, Container, Section, SectionHeading } from "@/components/ui";
import { getProgramme, getProgrammeSlugs } from "@/lib/api";
import { slugParams } from "@/lib/static-params";
import { SITE_URL, formatDateRange, stripHtml, truncate } from "@/lib/utils";

type Params = Promise<{ slug: string }>;

export async function generateStaticParams() {
  return slugParams(await getProgrammeSlugs());
}

export async function generateMetadata({
  params,
}: {
  params: Params;
}): Promise<Metadata> {
  const { slug } = await params;
  const programme = await getProgramme(slug);
  if (!programme) return { title: "Programme not found" };

  const description =
    programme.meta_description || truncate(programme.summary, 158);

  return {
    title: programme.meta_title || programme.title,
    description,
    alternates: { canonical: `/programmes/${programme.slug}` },
    robots: programme.noindex ? { index: false, follow: true } : undefined,
    openGraph: {
      type: "article",
      title: programme.title,
      description,
      images: programme.og_image
        ? [{ url: programme.og_image }]
        : programme.featured_image
          ? [{ url: programme.featured_image }]
          : undefined,
    },
  };
}

export default async function ProgrammePage({ params }: { params: Params }) {
  const { slug } = await params;
  const programme = await getProgramme(slug);
  if (!programme) notFound();

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Project",
    name: programme.title,
    description: programme.summary,
    url: `${SITE_URL}/programmes/${programme.slug}`,
    image: programme.featured_image ?? undefined,
    location: programme.location
      ? { "@type": "Place", name: programme.location }
      : undefined,
    startDate: programme.start_date ?? undefined,
    endDate: programme.end_date ?? undefined,
    parentOrganization: {
      "@type": "NGO",
      name: "Simply Green Organization",
      url: SITE_URL,
    },
  };

  const facts = [
    programme.location && {
      icon: MapPin,
      label: "Where",
      value: programme.location,
    },
    programme.beneficiaries && {
      icon: Users,
      label: "Who it reaches",
      value: programme.beneficiaries,
    },
    (programme.start_date || programme.end_date) && {
      icon: CalendarDays,
      label: "When",
      value: formatDateRange(programme.start_date, programme.end_date),
    },
    programme.beneficiary_count && {
      icon: Target,
      label: "People reached",
      value: programme.beneficiary_count.toLocaleString("en-GB"),
    },
  ].filter(Boolean) as {
    icon: typeof MapPin;
    label: string;
    value: string;
  }[];

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* Hero */}
      <header className="relative isolate overflow-hidden pt-32 pb-16 text-white sm:pt-36 sm:pb-20">
        {programme.featured_image ? (
          <>
            <Image
              src={programme.featured_image}
              alt=""
              fill
              priority
              sizes="100vw"
              className="object-cover"
            />
            <div
              aria-hidden
              className="absolute inset-0 bg-gradient-to-r from-ink-950/94 via-ink-950/82 to-ink-950/55"
            />
          </>
        ) : (
          <div aria-hidden className="absolute inset-0 bg-forest-wash" />
        )}

        <Container className="relative z-10">
          <div className="max-w-3xl">
            <div className="mb-5 flex flex-wrap gap-2">
              <Badge tone="light">{programme.status_label}</Badge>
              {programme.focus_areas.map((area) => (
                <Badge key={area.id} tone="light">
                  {area.title}
                </Badge>
              ))}
            </div>

            <h1 className="text-3xl sm:text-4xl lg:text-5xl lg:leading-[1.1]">
              {programme.title}
            </h1>

            {programme.subtitle ? (
              <p className="mt-5 text-lg leading-relaxed text-ink-100">
                {programme.subtitle}
              </p>
            ) : null}
          </div>
        </Container>
      </header>

      {/* Facts */}
      {facts.length > 0 ? (
        <div className="border-b border-sand-200 bg-sand-50">
          <Container>
            <dl className="grid gap-8 py-10 sm:grid-cols-2 lg:grid-cols-4">
              {facts.map((fact) => (
                <div key={fact.label} className="flex gap-3">
                  <fact.icon
                    className="mt-0.5 h-5 w-5 shrink-0 text-green-600"
                    aria-hidden
                  />
                  <div>
                    <dt className="text-xs font-semibold uppercase tracking-wider text-sand-500">
                      {fact.label}
                    </dt>
                    <dd className="mt-1 text-sm font-medium text-ink-900">
                      {fact.value}
                    </dd>
                  </div>
                </div>
              ))}
            </dl>
          </Container>
        </div>
      ) : null}

      {/* Body */}
      <Section>
        <Container>
          <div className="grid gap-14 lg:grid-cols-12 lg:gap-16">
            <div className="lg:col-span-8">
              <p className="text-xl leading-relaxed text-ink-900">
                {programme.summary}
              </p>

              {programme.body ? (
                <div
                  className="prose-content mt-10"
                  dangerouslySetInnerHTML={{ __html: programme.body }}
                />
              ) : null}
            </div>

            <aside className="lg:col-span-4">
              {programme.outcomes && programme.outcomes.length > 0 ? (
                <div className="rounded-2xl border border-green-200 bg-green-50 p-7">
                  <h2 className="font-display text-sm font-bold uppercase tracking-wider text-green-800">
                    Results so far
                  </h2>
                  <dl className="mt-5 space-y-5">
                    {programme.outcomes.map((outcome) => (
                      <div key={outcome.id}>
                        <dd className="font-display text-3xl font-extrabold text-green-700">
                          {outcome.value}
                        </dd>
                        <dt className="mt-1 text-sm text-green-900">
                          {outcome.label}
                        </dt>
                      </div>
                    ))}
                  </dl>
                </div>
              ) : null}

              {programme.partners && programme.partners.length > 0 ? (
                <div className="mt-6 rounded-2xl border border-sand-200 bg-white p-7">
                  <h2 className="font-display text-sm font-bold uppercase tracking-wider text-sand-600">
                    Delivered with
                  </h2>
                  <ul className="mt-4 space-y-2">
                    {programme.partners.map((partner) => (
                      <li key={partner.id} className="text-sm text-ink-900">
                        {partner.name}
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}

              <div className="mt-6 rounded-2xl bg-ink-950 p-7 text-white">
                <h2 className="font-display text-lg font-bold">
                  Support this work
                </h2>
                <p className="mt-2.5 text-sm leading-relaxed text-ink-200">
                  Funding and volunteers keep this programme in the field.
                </p>
                <div className="mt-5 flex flex-col gap-2.5">
                  <ButtonLink href="/donate" size="sm">
                    Donate
                  </ButtonLink>
                  <ButtonLink
                    href="/get-involved/partner"
                    variant="ghostLight"
                    size="sm"
                  >
                    Partner with us
                  </ButtonLink>
                </div>
              </div>
            </aside>
          </div>
        </Container>
      </Section>

      {/* Gallery */}
      {programme.images && programme.images.length > 0 ? (
        <Section tone="muted">
          <Container>
            <SectionHeading title="From the field" />
            <ul className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {programme.images.map((image) => (
                <li key={image.id}>
                  <figure>
                    <div className="relative aspect-[4/3] overflow-hidden rounded-2xl bg-sand-100">
                      <Image
                        src={image.image}
                        alt={image.alt_text || image.caption || programme.title}
                        fill
                        sizes="(min-width: 1024px) 30vw, (min-width: 640px) 50vw, 100vw"
                        className="object-cover"
                      />
                    </div>
                    {image.caption ? (
                      <figcaption className="mt-2.5 text-sm text-sand-600">
                        {image.caption}
                      </figcaption>
                    ) : null}
                  </figure>
                </li>
              ))}
            </ul>
          </Container>
        </Section>
      ) : null}
    </>
  );
}
