import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight, Handshake, HandHeart, Heart } from "lucide-react";

import { Container, PageHeader, Section } from "@/components/ui";

export const metadata: Metadata = {
  title: "Get Involved",
  description:
    "Volunteer, partner with us, or support our work. There is a way into Simply Green Organization's environmental work for everyone.",
  alternates: { canonical: "/get-involved" },
};

const PATHS = [
  {
    title: "Become a volunteer",
    description:
      "Join clean-ups, restoration days and school sessions. Whether you have one afternoon or every weekend, there is work for you.",
    href: "/get-involved/volunteer",
    cta: "Apply to volunteer",
    Icon: HandHeart,
    tone: "bg-green-50 text-green-700 border-green-200",
  },
  {
    title: "Partner with us",
    description:
      "Fund a programme, bring technical expertise, or deliver work together. We report transparently and align with national frameworks and the SDGs.",
    href: "/get-involved/partner",
    cta: "Start a conversation",
    Icon: Handshake,
    tone: "bg-sky-50 text-sky-700 border-sky-200",
  },
  {
    title: "Support our work",
    description:
      "A donation puts tools, training and trees into the hands of the communities doing the work.",
    href: "/donate",
    cta: "Make a donation",
    Icon: Heart,
    tone: "bg-gold-50 text-gold-700 border-gold-200",
  },
];

export default function GetInvolvedPage() {
  return (
    <>
      <PageHeader
        eyebrow="Get involved"
        title="There is a way in for everyone"
        description="Whether you have an afternoon, a skill or a budget — the work needs you."
      />

      <Section>
        <Container>
          <ul className="grid gap-6 lg:grid-cols-3">
            {PATHS.map(({ title, description, href, cta, Icon, tone }) => (
              <li key={href}>
                <Link
                  href={href}
                  className="group flex h-full flex-col rounded-2xl border border-sand-200 bg-white p-8 transition-all duration-300 hover:-translate-y-1 hover:border-green-300 hover:shadow-xl hover:shadow-ink-950/5"
                >
                  <span
                    className={`inline-flex h-14 w-14 items-center justify-center rounded-2xl border ${tone}`}
                  >
                    <Icon className="h-7 w-7" aria-hidden />
                  </span>
                  <h2 className="mt-6 font-display text-xl font-bold text-ink-950">
                    {title}
                  </h2>
                  <p className="mt-3 flex-1 leading-relaxed text-sand-700">
                    {description}
                  </p>
                  <span className="mt-7 inline-flex items-center gap-1.5 font-semibold text-green-700">
                    {cta}
                    <ArrowRight
                      className="h-4 w-4 transition-transform group-hover:translate-x-1"
                      aria-hidden
                    />
                  </span>
                </Link>
              </li>
            ))}
          </ul>
        </Container>
      </Section>
    </>
  );
}
