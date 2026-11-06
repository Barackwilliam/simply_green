import type { Metadata } from "next";

import { Container, PageHeader, Section } from "@/components/ui";
import { getSiteSettings } from "@/lib/api";

export const metadata: Metadata = {
  title: "Privacy Policy",
  description:
    "How Simply Green Organization collects, uses and protects the personal information you share through this website.",
  alternates: { canonical: "/privacy" },
};

export default async function PrivacyPage() {
  const settings = await getSiteSettings();
  const org = settings.organisation_name;
  const contact = settings.email || "our contact address";

  return (
    <>
      <PageHeader
        eyebrow="Legal"
        title="Privacy policy"
        description={`How ${org} handles the information you share with us through this website.`}
      />

      <Section>
        <Container>
          <div className="prose-content mx-auto max-w-3xl">
            <h2>What we collect</h2>
            <p>
              We only collect information you choose to give us through the
              forms on this site:
            </p>
            <ul>
              <li>
                <strong>Contact form</strong> — your name, email address,
                optional phone number, and your message.
              </li>
              <li>
                <strong>Volunteer application</strong> — your name, contact
                details, location, occupation, skills, availability, and a CV
                if you attach one.
              </li>
              <li>
                <strong>Partnership enquiry</strong> — your organisation, your
                name, contact details and your proposal.
              </li>
              <li>
                <strong>Newsletter</strong> — your email address, and your name
                if you give it.
              </li>
              <li>
                <strong>Event registration</strong> — your name, contact
                details and organisation.
              </li>
              <li>
                <strong>Donation pledge</strong> — your name, contact details
                and the amount you intend to give.
              </li>
            </ul>

            <h2>What we never collect</h2>
            <p>
              We do not ask for and never store card numbers, bank passwords,
              mobile money PINs or any other payment credential. Donations are
              made through your own bank or mobile money service using the
              published account details. Any message claiming to be from us and
              asking for a PIN or password is not from us.
            </p>

            <h2>How we use it</h2>
            <p>
              We use your information only to reply to you, to organise the
              volunteering, partnership, event or donation you asked about, and
              to send you the newsletter if you subscribed. We do not sell your
              information, and we do not share it with anyone outside the
              organisation except where the law requires it.
            </p>

            <h2>How long we keep it</h2>
            <p>
              We keep enquiries and applications for as long as they are useful
              to the work they relate to, and donation records for as long as
              our financial reporting obligations require. You can ask us to
              delete your information at any time.
            </p>

            <h2>Newsletter</h2>
            <p>
              Every newsletter includes a way to unsubscribe. You can also ask
              us directly and we will remove you.
            </p>

            <h2>Cookies and analytics</h2>
            <p>
              This site does not set advertising or tracking cookies. If
              website analytics are enabled, they are used only to understand
              which pages are useful, never to profile individuals.
            </p>

            <h2>Your rights</h2>
            <p>
              You can ask us what information we hold about you, ask us to
              correct it, or ask us to delete it. Write to {contact} and we
              will respond.
            </p>

            <h2>Changes</h2>
            <p>
              If this policy changes we will update this page. Significant
              changes will be noted here.
            </p>

            <h2>Contact</h2>
            <p>
              Questions about this policy can be sent to {contact}
              {settings.address ? `, or by post to ${settings.address}` : ""}.
            </p>
          </div>
        </Container>
      </Section>
    </>
  );
}
