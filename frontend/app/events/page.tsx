import type { Metadata } from "next";
import { CalendarDays } from "lucide-react";

import { EventCard } from "@/components/cards";
import { Container, EmptyState, PageHeader, Section, SectionHeading } from "@/components/ui";
import { getEvents } from "@/lib/api";

export const metadata: Metadata = {
  title: "Events",
  description:
    "Clean-ups, trainings, restoration days and community sessions run by Simply Green Organization across Tanzania.",
  alternates: { canonical: "/events" },
};

export default async function EventsPage() {
  const [upcoming, past] = await Promise.all([
    getEvents({ when: "upcoming" }),
    getEvents({ when: "past" }),
  ]);

  return (
    <>
      <PageHeader
        eyebrow="News & events"
        title="Events"
        description="Clean-ups, trainings and community sessions — come and take part."
      />

      <Section>
        <Container>
          {upcoming.length === 0 && past.length === 0 ? (
            <EmptyState
              icon={<CalendarDays className="h-10 w-10" />}
              title="No events scheduled yet"
              description="Events added in the admin will appear here, with optional online registration."
            />
          ) : (
            <div className="space-y-20">
              {upcoming.length > 0 ? (
                <div>
                  <SectionHeading eyebrow="Coming up" title="Upcoming events" />
                  <ul className="mt-10 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                    {upcoming.map((event) => (
                      <li key={event.id}>
                        <EventCard event={event} />
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}

              {past.length > 0 ? (
                <div>
                  <SectionHeading eyebrow="Archive" title="Past events" />
                  <ul className="mt-10 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                    {past.map((event) => (
                      <li key={event.id}>
                        <EventCard event={event} />
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}
            </div>
          )}
        </Container>
      </Section>
    </>
  );
}
