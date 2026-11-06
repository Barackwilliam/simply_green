import type { Metadata } from "next";
import Image from "next/image";
import { ArrowRight, CheckCircle2, Compass, Eye } from "lucide-react";

import { Icon } from "@/components/ui/Icon";
import {
  ButtonLink,
  Container,
  PageHeader,
  Section,
  SectionHeading,
} from "@/components/ui";
import { getCoreValues, getObjectives, getSiteSettings } from "@/lib/api";
import { stripHtml, truncate } from "@/lib/utils";

export async function generateMetadata(): Promise<Metadata> {
  const settings = await getSiteSettings();
  return {
    title: "About Us",
    description: truncate(
      stripHtml(settings.who_we_are) || settings.mission,
      158,
    ),
    alternates: { canonical: "/about" },
  };
}

export default async function AboutPage() {
  const [settings, values, objectives] = await Promise.all([
    getSiteSettings(),
    getCoreValues(),
    getObjectives(),
  ]);

  return (
    <>
      <PageHeader
        eyebrow="About us"
        title="Who we are"
        description={`${settings.organisation_name} works across Mainland Tanzania on environmental sustainability, climate action, community empowerment and sustainable livelihoods.`}
      />

      {/* Story */}
      <Section>
        <Container>
          <div className="grid gap-14 lg:grid-cols-12 lg:gap-16">
            <div className="lg:col-span-7">
              {settings.who_we_are ? (
                <div
                  className="prose-content"
                  dangerouslySetInnerHTML={{ __html: settings.who_we_are }}
                />
              ) : (
                <p className="prose-content">
                  Content for this section has not been added yet.
                </p>
              )}

              {settings.registration_number ? (
                <dl className="mt-10 grid gap-px overflow-hidden rounded-2xl bg-sand-200 sm:grid-cols-2">
                  <div className="bg-sand-50 px-6 py-5">
                    <dt className="text-xs font-semibold uppercase tracking-wider text-sand-500">
                      Registration number
                    </dt>
                    <dd className="mt-1.5 font-display text-lg font-bold text-ink-950">
                      {settings.registration_number}
                    </dd>
                  </div>
                  <div className="bg-sand-50 px-6 py-5">
                    <dt className="text-xs font-semibold uppercase tracking-wider text-sand-500">
                      Operating across
                    </dt>
                    <dd className="mt-1.5 font-display text-lg font-bold text-ink-950">
                      Mainland {settings.country}
                    </dd>
                  </div>
                </dl>
              ) : null}
            </div>

            <div className="lg:col-span-5">
              <div className="relative aspect-[4/5] overflow-hidden rounded-3xl">
                <Image
                  src="/images/team-waste.jpg"
                  alt="Simply Green Organization team at a community clean-up"
                  fill
                  sizes="(min-width: 1024px) 40vw, 100vw"
                  className="object-cover"
                />
              </div>
            </div>
          </div>
        </Container>
      </Section>

      {/* Vision & mission */}
      <Section tone="muted" id="vision">
        <Container>
          <div className="grid gap-6 lg:grid-cols-2">
            <div className="rounded-2xl border border-sky-200 bg-white p-8 sm:p-10">
              <span className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-sky-100 text-sky-700">
                <Eye className="h-6 w-6" aria-hidden />
              </span>
              <h2 className="mt-6 font-display text-2xl font-bold text-ink-950">
                Our Vision
              </h2>
              <p className="mt-4 text-lg leading-relaxed text-sand-700">
                {settings.vision}
              </p>
            </div>

            <div className="rounded-2xl border border-green-200 bg-white p-8 sm:p-10">
              <span className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-green-100 text-green-700">
                <Compass className="h-6 w-6" aria-hidden />
              </span>
              <h2 className="mt-6 font-display text-2xl font-bold text-ink-950">
                Our Mission
              </h2>
              <p className="mt-4 text-lg leading-relaxed text-sand-700">
                {settings.mission}
              </p>
            </div>
          </div>
        </Container>
      </Section>

      {/* Core values */}
      {values.length > 0 ? (
        <Section id="values">
          <Container>
            <SectionHeading
              eyebrow="What guides us"
              title="Our core values"
              align="center"
            />
            <ul className="mt-14 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {values.map((value) => (
                <li
                  key={value.id}
                  className="rounded-2xl border border-sand-200 bg-white p-7 transition-colors hover:border-green-300"
                >
                  <span className="inline-flex h-11 w-11 items-center justify-center rounded-xl bg-green-50 text-green-700">
                    <Icon name={value.icon || "leaf"} className="h-5 w-5" />
                  </span>
                  <h3 className="mt-5 font-display text-lg font-bold text-ink-950">
                    {value.title}
                  </h3>
                  <p className="mt-3 text-[0.9375rem] leading-relaxed text-sand-700">
                    {value.description}
                  </p>
                </li>
              ))}
            </ul>
          </Container>
        </Section>
      ) : null}

      {/* Objectives */}
      {objectives.length > 0 ? (
        <Section tone="dark" id="objectives">
          <Container>
            <div className="grid gap-14 lg:grid-cols-12 lg:gap-16">
              <div className="lg:col-span-5">
                <SectionHeading
                  eyebrow="What we set out to do"
                  title="Our objectives"
                  tone="light"
                />
                <div className="mt-8">
                  <ButtonLink href="/programmes" variant="light">
                    See this in practice
                    <ArrowRight className="h-4 w-4" aria-hidden />
                  </ButtonLink>
                </div>
              </div>

              <ol className="space-y-4 lg:col-span-7">
                {objectives.map((objective, index) => (
                  <li key={objective.id} className="flex gap-4">
                    <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-green-500/15 font-display text-sm font-bold text-green-400">
                      {index + 1}
                    </span>
                    <p className="pt-1 leading-relaxed text-ink-100">
                      {objective.text}
                    </p>
                  </li>
                ))}
              </ol>
            </div>
          </Container>
        </Section>
      ) : null}

      {/* Registration note */}
      {settings.registration_statement ? (
        <Section tone="muted" className="py-14 sm:py-16">
          <Container>
            <div className="flex items-start gap-4 rounded-2xl border border-sand-200 bg-white p-7">
              <CheckCircle2
                className="mt-0.5 h-5 w-5 shrink-0 text-green-600"
                aria-hidden
              />
              <p className="text-sm leading-relaxed text-sand-700">
                {settings.registration_statement}
              </p>
            </div>
          </Container>
        </Section>
      ) : null}
    </>
  );
}
