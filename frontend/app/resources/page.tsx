import type { Metadata } from "next";
import { FileText } from "lucide-react";

import { PublicationFilter } from "@/components/resources/PublicationFilter";
import { Container, EmptyState, PageHeader, Section } from "@/components/ui";
import { getPublications } from "@/lib/api";

export const metadata: Metadata = {
  title: "Resource Centre",
  description:
    "Annual reports, financial reports, project reports, strategic plans and research published by Simply Green Organization.",
  alternates: { canonical: "/resources" },
};

export default async function ResourcesPage() {
  const publications = await getPublications();

  return (
    <>
      <PageHeader
        eyebrow="Resource centre"
        title="Publications and reports"
        description="Our reporting, research and the documents that hold us to account."
      />

      <Section>
        <Container>
          {publications.length === 0 ? (
            <EmptyState
              icon={<FileText className="h-10 w-10" />}
              title="No documents published yet"
              description="Annual reports, financial reports and research uploaded in the admin will appear here."
            />
          ) : (
            <PublicationFilter publications={publications} />
          )}
        </Container>
      </Section>
    </>
  );
}
