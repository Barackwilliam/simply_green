import type { Metadata } from "next";
import Image from "next/image";

import { VolunteerForm } from "@/components/forms/VolunteerForm";
import { Container, PageHeader, Section } from "@/components/ui";
import { getFocusAreas } from "@/lib/api";

export const metadata: Metadata = {
  title: "Become a Volunteer",
  description:
    "Volunteer with Simply Green Organization — join clean-ups, restoration days, school sessions and community trainings across Tanzania.",
  alternates: { canonical: "/get-involved/volunteer" },
};

export default async function VolunteerPage() {
  const focusAreas = await getFocusAreas();

  return (
    <>
      <PageHeader
        eyebrow="Get involved"
        title="Become a volunteer"
        description="Give the time you have. We will find work that fits it."
      />

      <Section>
        <Container>
          <div className="grid gap-14 lg:grid-cols-12 lg:gap-16">
            <div className="lg:col-span-7">
              <VolunteerForm focusAreas={focusAreas.map((area) => area.title)} />
            </div>

            <aside className="lg:col-span-5">
              <div className="relative aspect-[4/3] overflow-hidden rounded-2xl">
                <Image
                  src="/images/litter-collection.jpg"
                  alt="Volunteers clearing waste from a shoreline in Dar es Salaam"
                  fill
                  sizes="(min-width: 1024px) 40vw, 100vw"
                  className="object-cover"
                />
              </div>

              <div className="mt-6 rounded-2xl border border-sand-200 bg-sand-50 p-7">
                <h2 className="font-display text-lg font-bold text-ink-950">
                  What volunteering looks like
                </h2>
                <ul className="mt-4 space-y-3 text-sm leading-relaxed text-sand-700">
                  <li>Coastal and market clean-ups in Dar es Salaam</li>
                  <li>Mangrove nursery and planting days</li>
                  <li>School sessions on waste separation and reuse</li>
                  <li>Community trainings and awareness events</li>
                  <li>Data collection, documentation and photography</li>
                </ul>
                <p className="mt-5 text-xs leading-relaxed text-sand-500">
                  We will only use your details to contact you about
                  volunteering. We never share them with anyone else.
                </p>
              </div>
            </aside>
          </div>
        </Container>
      </Section>
    </>
  );
}
