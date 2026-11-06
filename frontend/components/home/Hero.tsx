import Image from "next/image";
import { ArrowRight, Play } from "lucide-react";

import { ButtonLink, Container } from "@/components/ui";

export function Hero({
  organisationName,
  tagline,
  mission,
  imageUrl,
  imageAlt,
}: {
  organisationName: string;
  tagline: string;
  mission: string;
  imageUrl: string;
  imageAlt: string;
}) {
  return (
    <section className="relative isolate flex min-h-[38rem] items-center overflow-hidden lg:min-h-[44rem]">
      {/* Backdrop */}
      <Image
        src={imageUrl}
        alt={imageAlt}
        fill
        priority
        sizes="100vw"
        className="object-cover"
      />
      <div
        aria-hidden
        className="absolute inset-0 bg-gradient-to-br from-ink-950/92 via-ink-950/75 to-ink-900/55"
      />
      <div
        aria-hidden
        className="absolute inset-0 bg-[radial-gradient(45rem_25rem_at_80%_20%,rgba(153,190,61,0.22),transparent_60%)]"
      />

      <Container className="relative z-10 py-28 sm:py-32">
        <div className="max-w-3xl">
          <p className="animate-rise mb-6 inline-flex items-center gap-2.5 rounded-full border border-white/20 bg-white/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.14em] text-green-200 backdrop-blur-sm">
            <span className="h-1.5 w-1.5 rounded-full bg-green-400" />
            Registered NGO · Tanzania
          </p>

          <h1 className="animate-rise text-4xl leading-[1.08] text-white sm:text-5xl lg:text-[4rem]">
            {tagline || (
              <>
                A greener, more resilient{" "}
                <span className="text-green-400">Tanzania</span> — led by its
                own communities
              </>
            )}
          </h1>

          <p className="animate-rise mt-7 max-w-2xl text-lg leading-relaxed text-ink-100 sm:text-xl">
            {mission ||
              `${organisationName} empowers communities to protect the environment and address climate challenges through sustainable conservation practices, innovation, and livelihood initiatives.`}
          </p>

          <div className="animate-rise mt-10 flex flex-col gap-3 sm:flex-row sm:items-center">
            <ButtonLink href="/programmes" size="lg">
              See our programmes
              <ArrowRight className="h-4 w-4" aria-hidden />
            </ButtonLink>
            <ButtonLink href="/get-involved" variant="ghostLight" size="lg">
              <Play className="h-4 w-4" aria-hidden />
              Get involved
            </ButtonLink>
          </div>
        </div>
      </Container>
    </section>
  );
}
