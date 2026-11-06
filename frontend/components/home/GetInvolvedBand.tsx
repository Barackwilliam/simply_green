import Link from "next/link";
import { ArrowRight, Handshake, HandHeart, Heart } from "lucide-react";

import { Container, Section } from "@/components/ui";

const PATHS = [
  {
    title: "Become a volunteer",
    description:
      "Join clean-ups, restoration days and school sessions. Give the time you have.",
    href: "/get-involved/volunteer",
    Icon: HandHeart,
    tone: "bg-green-500/15 text-green-300",
  },
  {
    title: "Partner with us",
    description:
      "Fund a programme, bring technical support, or deliver work together.",
    href: "/get-involved/partner",
    Icon: Handshake,
    tone: "bg-sky-500/15 text-sky-300",
  },
  {
    title: "Support our work",
    description:
      "A donation puts tools, training and trees into the hands of communities.",
    href: "/donate",
    Icon: Heart,
    tone: "bg-gold-400/15 text-gold-300",
  },
];

export function GetInvolvedBand() {
  return (
    <Section tone="dark">
      <Container>
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl text-white sm:text-4xl lg:text-[2.75rem] lg:leading-[1.1]">
            There is a way in for everyone
          </h2>
          <p className="mt-5 text-lg leading-relaxed text-ink-200">
            Whether you have an afternoon, a skill or a budget — the work needs
            you.
          </p>
        </div>

        <ul className="mt-14 grid gap-5 md:grid-cols-3">
          {PATHS.map(({ title, description, href, Icon, tone }) => (
            <li key={href}>
              <Link
                href={href}
                className="group flex h-full flex-col rounded-2xl border border-white/10 bg-white/[0.04] p-7 transition-all duration-300 ease-[var(--ease-out-soft)] hover:-translate-y-1 hover:border-green-400/40 hover:bg-white/[0.08]"
              >
                <span
                  className={`mb-5 inline-flex h-12 w-12 items-center justify-center rounded-xl ${tone}`}
                >
                  <Icon className="h-6 w-6" aria-hidden />
                </span>
                <h3 className="font-display text-lg font-bold text-white">
                  {title}
                </h3>
                <p className="mt-3 flex-1 text-sm leading-relaxed text-ink-200">
                  {description}
                </p>
                <span className="mt-6 inline-flex items-center gap-1.5 text-sm font-semibold text-green-400">
                  Start here
                  <ArrowRight
                    className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-1"
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
