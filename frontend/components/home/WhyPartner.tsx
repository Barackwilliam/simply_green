import Image from "next/image";

import { Container, Section, SectionHeading } from "@/components/ui";
import { Icon } from "@/components/ui/Icon";
import type { PartnerReason } from "@/lib/types";

export function WhyPartner({
  reasons,
  imageUrl,
  imageAlt,
}: {
  reasons: PartnerReason[];
  imageUrl: string;
  imageAlt: string;
}) {
  if (reasons.length === 0) return null;

  return (
    <Section tone="dark">
      <Container>
        <div className="grid gap-14 lg:grid-cols-12 lg:gap-16">
          <div className="lg:col-span-5">
            <SectionHeading
              eyebrow="For funders and partners"
              title="Why organisations choose to work with us"
              description="We work at the frontline, and we account for every shilling that gets us there."
              tone="light"
            />

            <div className="relative mt-10 hidden aspect-[4/3] overflow-hidden rounded-2xl lg:block">
              <Image
                src={imageUrl}
                alt={imageAlt}
                fill
                sizes="(min-width: 1024px) 40vw, 100vw"
                className="object-cover"
              />
            </div>
          </div>

          <ul className="space-y-3 lg:col-span-7">
            {reasons.map((reason, index) => (
              <li
                key={reason.id}
                className="group flex gap-5 rounded-2xl border border-white/10 bg-white/[0.04] p-6 transition-colors duration-300 hover:border-green-400/40 hover:bg-white/[0.07]"
              >
                <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-green-500/15 text-green-400">
                  <Icon
                    name={reason.icon || DEFAULT_ICONS[index % DEFAULT_ICONS.length]}
                    className="h-5 w-5"
                  />
                </span>
                <div>
                  <h3 className="font-display text-base font-bold text-white">
                    {reason.title}
                  </h3>
                  <p className="mt-2 text-sm leading-relaxed text-ink-200">
                    {reason.description}
                  </p>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </Container>
    </Section>
  );
}

const DEFAULT_ICONS = [
  "scale",
  "users",
  "globe",
  "shield-check",
  "lightbulb",
] as const;
