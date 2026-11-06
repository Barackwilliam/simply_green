import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { ProgrammeCard } from "@/components/cards";
import { Container, PageHeader, Section, SectionHeading } from "@/components/ui";
import {
  getFocusArea,
  getFocusAreaSlugs,
  getProgrammes,
} from "@/lib/api";
import { slugParams } from "@/lib/static-params";
import { stripHtml, truncate } from "@/lib/utils";

type Params = Promise<{ slug: string }>;

export async function generateStaticParams() {
  return slugParams(await getFocusAreaSlugs());
}

export async function generateMetadata({
  params,
}: {
  params: Params;
}): Promise<Metadata> {
  const { slug } = await params;
  const area = await getFocusArea(slug);
  if (!area) return { title: "Focus area not found" };

  return {
    title: area.meta_title || area.title,
    description:
      area.meta_description ||
      truncate(area.summary || stripHtml(area.body ?? ""), 158),
    alternates: { canonical: `/focus-areas/${area.slug}` },
    robots: area.noindex ? { index: false, follow: true } : undefined,
    openGraph: area.og_image
      ? { images: [{ url: area.og_image }] }
      : undefined,
  };
}

export default async function FocusAreaPage({ params }: { params: Params }) {
  const { slug } = await params;
  const area = await getFocusArea(slug);
  if (!area) notFound();

  const programmes = await getProgrammes({ focusArea: slug });

  return (
    <>
      <PageHeader
        eyebrow="Focus area"
        title={area.title}
        description={area.summary}
      />

      {area.body ? (
        <Section>
          <Container>
            <div
              className="prose-content mx-auto max-w-3xl"
              dangerouslySetInnerHTML={{ __html: area.body }}
            />
          </Container>
        </Section>
      ) : null}

      {programmes.length > 0 ? (
        <Section tone="muted">
          <Container>
            <SectionHeading
              eyebrow="In practice"
              title={`Programmes under ${area.title}`}
            />
            <ul className="mt-12 grid gap-6 lg:grid-cols-3">
              {programmes.map((programme) => (
                <li key={programme.id}>
                  <ProgrammeCard programme={programme} />
                </li>
              ))}
            </ul>
          </Container>
        </Section>
      ) : null}
    </>
  );
}
