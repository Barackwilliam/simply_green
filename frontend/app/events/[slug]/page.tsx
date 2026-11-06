import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, CalendarDays, Globe, MapPin } from "lucide-react";

import { EventRegistrationForm } from "@/components/forms/EventRegistrationForm";
import { Badge, Container, Section } from "@/components/ui";
import { getEvent, getEventSlugs } from "@/lib/api";
import { slugParams } from "@/lib/static-params";
import { SITE_URL, formatDateTime, truncate } from "@/lib/utils";

type Params = Promise<{ slug: string }>;

export async function generateStaticParams() {
  return slugParams(await getEventSlugs());
}

export async function generateMetadata({
  params,
}: {
  params: Params;
}): Promise<Metadata> {
  const { slug } = await params;
  const event = await getEvent(slug);
  if (!event) return { title: "Event not found" };

  const description = event.meta_description || truncate(event.summary, 158);

  return {
    title: event.meta_title || event.title,
    description,
    alternates: { canonical: `/events/${event.slug}` },
    robots: event.noindex ? { index: false, follow: true } : undefined,
    openGraph: {
      type: "article",
      title: event.title,
      description,
      images: event.featured_image ? [{ url: event.featured_image }] : undefined,
    },
  };
}

export default async function EventPage({ params }: { params: Params }) {
  const { slug } = await params;
  const event = await getEvent(slug);
  if (!event) notFound();

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Event",
    name: event.title,
    description: event.summary,
    startDate: event.start_datetime,
    endDate: event.end_datetime ?? undefined,
    eventAttendanceMode: event.is_online
      ? "https://schema.org/OnlineEventAttendanceMode"
      : "https://schema.org/OfflineEventAttendanceMode",
    eventStatus:
      event.status === "cancelled"
        ? "https://schema.org/EventCancelled"
        : "https://schema.org/EventScheduled",
    image: event.featured_image ?? undefined,
    url: `${SITE_URL}/events/${event.slug}`,
    location: event.is_online
      ? { "@type": "VirtualLocation", url: event.online_url || SITE_URL }
      : {
          "@type": "Place",
          name: event.venue || "Venue to be confirmed",
          address: event.address || event.venue || "Tanzania",
        },
    organizer: {
      "@type": "NGO",
      name: "Simply Green Organization",
      url: SITE_URL,
    },
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      <header className="relative isolate overflow-hidden pt-32 pb-16 text-white sm:pt-36 sm:pb-20">
        {event.featured_image ? (
          <>
            <Image src={event.featured_image} alt="" fill priority sizes="100vw" className="object-cover" />
            <div aria-hidden className="absolute inset-0 bg-gradient-to-r from-ink-950/94 via-ink-950/82 to-ink-950/55" />
          </>
        ) : (
          <div aria-hidden className="absolute inset-0 bg-forest-wash" />
        )}

        <Container className="relative z-10">
          <div className="max-w-3xl">
            <Link
              href="/events"
              className="inline-flex items-center gap-1.5 text-sm font-semibold text-green-300 transition-colors hover:text-green-200"
            >
              <ArrowLeft className="h-4 w-4" aria-hidden />
              All events
            </Link>

            <div className="mt-6">
              <Badge tone="light">{event.status_label}</Badge>
            </div>

            <h1 className="mt-5 text-3xl sm:text-4xl lg:text-5xl lg:leading-[1.1]">
              {event.title}
            </h1>

            <dl className="mt-7 flex flex-wrap gap-x-8 gap-y-3 text-sm text-ink-100">
              <div className="flex items-center gap-2">
                <dt className="sr-only">When</dt>
                <CalendarDays className="h-4 w-4 text-green-400" aria-hidden />
                <dd>{formatDateTime(event.start_datetime)}</dd>
              </div>
              <div className="flex items-center gap-2">
                <dt className="sr-only">Where</dt>
                {event.is_online ? (
                  <Globe className="h-4 w-4 text-green-400" aria-hidden />
                ) : (
                  <MapPin className="h-4 w-4 text-green-400" aria-hidden />
                )}
                <dd>{event.is_online ? "Online" : event.venue || "To be confirmed"}</dd>
              </div>
            </dl>
          </div>
        </Container>
      </header>

      <Section>
        <Container>
          <div className="grid gap-14 lg:grid-cols-12 lg:gap-16">
            <div className="lg:col-span-7">
              {event.summary ? (
                <p className="text-xl leading-relaxed text-ink-900">{event.summary}</p>
              ) : null}
              {event.body ? (
                <div className="prose-content mt-8" dangerouslySetInnerHTML={{ __html: event.body }} />
              ) : null}

              {event.address ? (
                <div className="mt-10 rounded-2xl border border-sand-200 bg-sand-50 p-6">
                  <h2 className="font-display text-sm font-bold uppercase tracking-wider text-sand-600">
                    Address
                  </h2>
                  <p className="mt-2 whitespace-pre-line text-sm text-ink-900">
                    {event.address}
                  </p>
                </div>
              ) : null}

              {event.map_embed_url ? (
                <div className="mt-6 overflow-hidden rounded-2xl border border-sand-200">
                  <iframe
                    src={event.map_embed_url}
                    title={`Map showing ${event.venue || event.title}`}
                    loading="lazy"
                    referrerPolicy="no-referrer-when-downgrade"
                    className="h-80 w-full border-0"
                  />
                </div>
              ) : null}
            </div>

            <aside className="lg:col-span-5">
              {event.registration_enabled && event.registration_open ? (
                <div className="rounded-2xl border border-green-200 bg-white p-7 shadow-sm">
                  <h2 className="font-display text-xl font-bold text-ink-950">
                    Register to attend
                  </h2>
                  <p className="mt-2 text-sm text-sand-700">
                    Reserve your place. We will email you the details.
                  </p>
                  <div className="mt-6">
                    <EventRegistrationForm eventId={event.id} />
                  </div>
                </div>
              ) : event.registration_enabled ? (
                <div className="rounded-2xl border border-sand-200 bg-sand-50 p-7">
                  <h2 className="font-display text-lg font-bold text-ink-950">
                    Registration is closed
                  </h2>
                  <p className="mt-2 text-sm text-sand-700">
                    This event is full, past, or the deadline has passed. Get in
                    touch if you would still like to take part.
                  </p>
                </div>
              ) : null}

              {event.is_online && event.online_url ? (
                <div className="mt-6 rounded-2xl bg-ink-950 p-7 text-white">
                  <h2 className="font-display text-lg font-bold">Join online</h2>
                  <a
                    href={event.online_url}
                    target="_blank"
                    rel="noreferrer noopener"
                    className="mt-3 inline-flex rounded-full bg-green-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-green-700"
                  >
                    Open the link
                  </a>
                </div>
              ) : null}
            </aside>
          </div>
        </Container>
      </Section>
    </>
  );
}
