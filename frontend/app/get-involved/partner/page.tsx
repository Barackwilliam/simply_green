import type { Metadata } from "next";

import { PartnerForm } from "@/components/forms/PartnerForm";
import { Icon } from "@/components/ui/Icon";
import { Container, PageHeader, Section } from "@/components/ui";
import { getPartnerReasons } from "@/lib/api";

export const metadata: Metadata = {
  title: "Partner With Us",
  description:
    "Partner with Simply Green Organization — funding, technical support, joint implementation and research collaboration in Tanzania.",
  alternates: { canonical: "/get-involved/partner" },
};

export default async function PartnerPage() {
  const reasons = await getPartnerReasons();

  return (
    <>
      <PageHeader
        eyebrow="Get involved"
        title="Partner with us"
        description="We work at the frontline, and we account for every shilling that gets us there."
      />

      <Section>
        <Container>
          <div className="grid gap-14 lg:grid-cols-12 lg:gap-16">
            <div className="lg:col-span-7">
              <PartnerForm />
            </div>

            <aside className="lg:col-span-5">
              {reasons.length > 0 ? (
                <ul className="space-y-3">
                  {reasons.map((reason) => (
                    <li
                      key={reason.id}
                      className="flex gap-4 rounded-2xl border border-sand-200 bg-white p-5"
                    >
                      <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-sky-50 text-sky-700">
                        <Icon name={reason.icon || "handshake"} className="h-5 w-5" />
                      </span>
                      <div>
                        <h2 className="font-display text-sm font-bold text-ink-950">
                          {reason.title}
                        </h2>
                        <p className="mt-1.5 text-sm leading-relaxed text-sand-700">
                          {reason.description}
                        </p>
                      </div>
                    </li>
                  ))}
                </ul>
              ) : null}
            </aside>
          </div>
        </Container>
      </Section>
    </>
  );
}
