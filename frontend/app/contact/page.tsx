import type { Metadata } from "next";
import { Mail, MapPin, Phone } from "lucide-react";

import { ContactForm } from "@/components/forms/ContactForm";
import { Container, PageHeader, Section, SectionHeading } from "@/components/ui";
import { getSiteSettings } from "@/lib/api";
import { SITE_URL } from "@/lib/utils";

export const metadata: Metadata = {
  title: "Contact Us",
  description:
    "Get in touch with Simply Green Organization in Dar es Salaam, Tanzania.",
  alternates: { canonical: "/contact" },
};

export default async function ContactPage() {
  const settings = await getSiteSettings();

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "ContactPage",
    url: `${SITE_URL}/contact`,
    mainEntity: {
      "@type": "NGO",
      name: settings.organisation_name,
      email: settings.email || undefined,
      telephone: settings.phone || undefined,
      address: {
        "@type": "PostalAddress",
        streetAddress: settings.address || undefined,
        addressLocality: settings.city,
        addressCountry: settings.country,
      },
    },
  };

  const details = [
    settings.address && { Icon: MapPin, label: "Office", value: settings.address },
    settings.phone && {
      Icon: Phone,
      label: "Phone",
      value: settings.phone,
      href: `tel:${settings.phone.replace(/\s/g, "")}`,
    },
    settings.email && {
      Icon: Mail,
      label: "Email",
      value: settings.email,
      href: `mailto:${settings.email}`,
    },
  ].filter(Boolean) as {
    Icon: typeof MapPin;
    label: string;
    value: string;
    href?: string;
  }[];

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      <PageHeader
        eyebrow="Reach us"
        title="Contact us"
        description="Questions, proposals, press enquiries — we read everything that comes in."
      />

      <Section>
        <Container>
          <div className="grid gap-14 lg:grid-cols-12 lg:gap-16">
            <div className="lg:col-span-7">
              <SectionHeading title="Send us a message" />
              <div className="mt-8">
                <ContactForm />
              </div>
            </div>

            <aside className="lg:col-span-5">
              {details.length > 0 ? (
                <ul className="space-y-4">
                  {details.map((detail) => (
                    <li
                      key={detail.label}
                      className="flex gap-4 rounded-2xl border border-sand-200 bg-white p-6"
                    >
                      <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-green-50 text-green-700">
                        <detail.Icon className="h-5 w-5" aria-hidden />
                      </span>
                      <div className="min-w-0">
                        <p className="text-xs font-semibold uppercase tracking-wider text-sand-500">
                          {detail.label}
                        </p>
                        {detail.href ? (
                          <a
                            href={detail.href}
                            className="mt-1 block break-words font-medium text-ink-950 hover:text-green-700"
                          >
                            {detail.value}
                          </a>
                        ) : (
                          <p className="mt-1 whitespace-pre-line font-medium text-ink-950">
                            {detail.value}
                          </p>
                        )}
                      </div>
                    </li>
                  ))}
                </ul>
              ) : (
                <div className="rounded-2xl border border-dashed border-sand-300 bg-sand-50 p-7 text-sm text-sand-600">
                  Contact details have not been added yet. They can be set in
                  the admin under Site settings.
                </div>
              )}

              {settings.social_links.length > 0 ? (
                <div className="mt-6 rounded-2xl border border-sand-200 bg-white p-6">
                  <p className="text-xs font-semibold uppercase tracking-wider text-sand-500">
                    Follow us
                  </p>
                  <ul className="mt-3 flex flex-wrap gap-x-5 gap-y-2">
                    {settings.social_links.map((social) => (
                      <li key={social.platform}>
                        <a
                          href={social.url}
                          target="_blank"
                          rel="noreferrer noopener"
                          className="text-sm font-medium text-sky-700 hover:text-sky-800"
                        >
                          {social.label}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}

              {settings.map_embed_url ? (
                <div className="mt-6 overflow-hidden rounded-2xl border border-sand-200">
                  <iframe
                    src={settings.map_embed_url}
                    title={`Map showing the ${settings.organisation_name} office`}
                    loading="lazy"
                    referrerPolicy="no-referrer-when-downgrade"
                    className="h-72 w-full border-0"
                  />
                </div>
              ) : null}
            </aside>
          </div>
        </Container>
      </Section>
    </>
  );
}
