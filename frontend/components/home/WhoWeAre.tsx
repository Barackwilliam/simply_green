import Image from "next/image";
import { ArrowRight, Compass, Eye } from "lucide-react";

import { ButtonLink, Container, Section, SectionHeading } from "@/components/ui";

export function WhoWeAre({
  vision,
  mission,
  summary,
  imageUrl,
  imageAlt,
  registrationStatement,
}: {
  vision: string;
  mission: string;
  summary: string;
  imageUrl: string;
  imageAlt: string;
  registrationStatement: string;
}) {
  return (
    <Section id="who-we-are">
      <Container>
        <div className="grid items-center gap-14 lg:grid-cols-2 lg:gap-20">
          {/* Image side */}
          <div className="relative">
            <div className="relative aspect-[4/5] overflow-hidden rounded-3xl sm:aspect-[4/3] lg:aspect-[4/5]">
              <Image
                src={imageUrl}
                alt={imageAlt}
                fill
                sizes="(min-width: 1024px) 45vw, 100vw"
                className="object-cover"
              />
            </div>

            {/* Floating vision/mission card */}
            <div className="relative z-10 mx-4 -mt-16 rounded-2xl border border-sand-200 bg-white p-6 shadow-xl shadow-ink-950/10 sm:mx-8 sm:p-7">
              <div className="flex gap-4">
                <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-sky-100 text-sky-700">
                  <Eye className="h-5 w-5" aria-hidden />
                </span>
                <div>
                  <h3 className="font-display text-sm font-bold uppercase tracking-wider text-sky-800">
                    Our Vision
                  </h3>
                  <p className="mt-2 text-sm leading-relaxed text-sand-700">
                    {vision}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Text side */}
          <div>
            <SectionHeading
              eyebrow="Who we are"
              title="Communities protecting their own environment"
              description={summary}
            />

            <div className="mt-8 rounded-2xl border-l-4 border-green-500 bg-green-50 p-6">
              <div className="flex gap-4">
                <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-green-600 text-white">
                  <Compass className="h-5 w-5" aria-hidden />
                </span>
                <div>
                  <h3 className="font-display text-sm font-bold uppercase tracking-wider text-green-800">
                    Our Mission
                  </h3>
                  <p className="mt-2 text-[0.9375rem] leading-relaxed text-green-900">
                    {mission}
                  </p>
                </div>
              </div>
            </div>

            {registrationStatement ? (
              <p className="mt-6 text-sm leading-relaxed text-sand-600">
                {registrationStatement}
              </p>
            ) : null}

            <div className="mt-9">
              <ButtonLink href="/about" size="lg">
                More about us
                <ArrowRight className="h-4 w-4" aria-hidden />
              </ButtonLink>
            </div>
          </div>
        </div>
      </Container>
    </Section>
  );
}
