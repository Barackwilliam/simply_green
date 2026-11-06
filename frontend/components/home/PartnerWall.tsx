import Image from "next/image";

import { Container, Section } from "@/components/ui";
import type { Partner } from "@/lib/types";

export function PartnerWall({ partners }: { partners: Partner[] }) {
  const withLogos = partners.filter((partner) => partner.logo);
  if (withLogos.length === 0) return null;

  return (
    <Section className="py-14 sm:py-16">
      <Container>
        <p className="text-center text-xs font-semibold uppercase tracking-[0.16em] text-sand-500">
          Working alongside
        </p>

        <ul className="mt-9 flex flex-wrap items-center justify-center gap-x-12 gap-y-8">
          {withLogos.map((partner) => {
            const logo = (
              <Image
                src={partner.logo as string}
                alt={partner.name}
                width={160}
                height={60}
                className="h-11 w-auto max-w-[9rem] object-contain opacity-60 grayscale transition-all duration-300 hover:opacity-100 hover:grayscale-0"
              />
            );

            return (
              <li key={partner.id}>
                {partner.website ? (
                  <a
                    href={partner.website}
                    target="_blank"
                    rel="noreferrer noopener"
                    title={partner.name}
                  >
                    {logo}
                  </a>
                ) : (
                  logo
                )}
              </li>
            );
          })}
        </ul>
      </Container>
    </Section>
  );
}
