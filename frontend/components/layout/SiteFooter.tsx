import Image from "next/image";
import Link from "next/link";
import {
  Facebook,
  Instagram,
  Linkedin,
  Mail,
  MapPin,
  Phone,
  Send,
  Twitter,
  Youtube,
} from "lucide-react";
import type { ComponentType } from "react";

import { NewsletterForm } from "@/components/forms/NewsletterForm";
import { Container } from "@/components/ui";
import { getCurrentYear } from "@/lib/time";
import type { SiteSettings } from "@/lib/types";

const SOCIAL_ICONS: Record<string, ComponentType<{ className?: string }>> = {
  facebook: Facebook,
  instagram: Instagram,
  linkedin: Linkedin,
  x: Twitter,
  youtube: Youtube,
  telegram: Send,
};

const EXPLORE_LINKS = [
  { label: "About Us", href: "/about" },
  { label: "Focus Areas", href: "/focus-areas" },
  { label: "Programmes", href: "/programmes" },
  { label: "Resource Centre", href: "/resources" },
  { label: "News & Events", href: "/news" },
  { label: "Gallery", href: "/gallery" },
];

const INVOLVE_LINKS = [
  { label: "Become a Volunteer", href: "/get-involved/volunteer" },
  { label: "Partner With Us", href: "/get-involved/partner" },
  { label: "Support Our Work", href: "/donate" },
  { label: "Contact Us", href: "/contact" },
];

export async function SiteFooter({
  settings,
}: {
  settings: SiteSettings;
}) {
  const year = await getCurrentYear();

  return (
    <footer className="bg-ink-950 text-ink-200">
      {settings.newsletter_enabled ? (
        <div className="border-b border-white/10">
          <Container>
            <div className="flex flex-col gap-8 py-14 lg:flex-row lg:items-center lg:justify-between">
              <div className="max-w-xl">
                <h2 className="text-2xl text-white sm:text-3xl">
                  Stay with the work
                </h2>
                <p className="mt-3 text-ink-300">
                  Updates on our programmes, research and events across
                  Tanzania — a few times a year, never more.
                </p>
              </div>
              <div className="w-full lg:max-w-md">
                <NewsletterForm source="footer" tone="dark" />
              </div>
            </div>
          </Container>
        </div>
      ) : null}

      <Container>
        <div className="grid gap-12 py-16 md:grid-cols-2 lg:grid-cols-12">
          {/* Identity */}
          <div className="lg:col-span-4">
            {settings.logo_light || settings.logo ? (
              <Image
                src={(settings.logo_light ?? settings.logo) as string}
                alt={settings.organisation_name}
                width={200}
                height={64}
                className="h-14 w-auto brightness-0 invert"
              />
            ) : (
              <span className="font-display text-xl font-bold text-white">
                {settings.organisation_name}
              </span>
            )}

            {settings.tagline ? (
              <p className="mt-5 text-sm leading-relaxed text-ink-300">
                {settings.tagline}
              </p>
            ) : null}

            {settings.registration_number ? (
              <p className="mt-5 text-xs leading-relaxed text-ink-400">
                Registered in Tanzania under the Non-Governmental Organizations
                Act No. 24 of 2002
                <br />
                <span className="font-medium text-ink-300">
                  Registration No. {settings.registration_number}
                </span>
              </p>
            ) : null}

            {settings.social_links.length > 0 ? (
              <ul className="mt-7 flex flex-wrap gap-2.5">
                {settings.social_links.map((social) => {
                  const Icon = SOCIAL_ICONS[social.platform];
                  return (
                    <li key={social.platform}>
                      <a
                        href={social.url}
                        target="_blank"
                        rel="noreferrer noopener"
                        aria-label={social.label}
                        className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-white/10 text-white transition-colors hover:bg-green-600"
                      >
                        {Icon ? (
                          <Icon className="h-[18px] w-[18px]" />
                        ) : (
                          <span className="text-xs font-bold">
                            {social.label.charAt(0)}
                          </span>
                        )}
                      </a>
                    </li>
                  );
                })}
              </ul>
            ) : null}
          </div>

          {/* Explore */}
          <nav className="lg:col-span-2" aria-label="Explore">
            <h3 className="font-display text-sm font-bold uppercase tracking-wider text-white">
              Explore
            </h3>
            <ul className="mt-5 space-y-3">
              {EXPLORE_LINKS.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm text-ink-300 transition-colors hover:text-green-400"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>

          {/* Get involved */}
          <nav className="lg:col-span-3" aria-label="Get involved">
            <h3 className="font-display text-sm font-bold uppercase tracking-wider text-white">
              Get Involved
            </h3>
            <ul className="mt-5 space-y-3">
              {INVOLVE_LINKS.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm text-ink-300 transition-colors hover:text-green-400"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>

          {/* Contact */}
          <div className="lg:col-span-3">
            <h3 className="font-display text-sm font-bold uppercase tracking-wider text-white">
              Reach Us
            </h3>
            <ul className="mt-5 space-y-4 text-sm">
              {settings.address ? (
                <li className="flex gap-3">
                  <MapPin
                    className="mt-0.5 h-4 w-4 shrink-0 text-green-400"
                    aria-hidden
                  />
                  <span className="whitespace-pre-line text-ink-300">
                    {settings.address}
                  </span>
                </li>
              ) : null}
              {settings.phone ? (
                <li className="flex gap-3">
                  <Phone
                    className="mt-0.5 h-4 w-4 shrink-0 text-green-400"
                    aria-hidden
                  />
                  <a
                    href={`tel:${settings.phone.replace(/\s/g, "")}`}
                    className="text-ink-300 transition-colors hover:text-green-400"
                  >
                    {settings.phone}
                  </a>
                </li>
              ) : null}
              {settings.email ? (
                <li className="flex gap-3">
                  <Mail
                    className="mt-0.5 h-4 w-4 shrink-0 text-green-400"
                    aria-hidden
                  />
                  <a
                    href={`mailto:${settings.email}`}
                    className="break-all text-ink-300 transition-colors hover:text-green-400"
                  >
                    {settings.email}
                  </a>
                </li>
              ) : null}
            </ul>
          </div>
        </div>
      </Container>

      <div className="border-t border-white/10">
        <Container>
          <div className="flex flex-col items-center justify-between gap-3 py-6 text-xs text-ink-400 sm:flex-row">
            <p>
              © {year} {settings.organisation_name}. All rights reserved.
            </p>
            <nav aria-label="Legal">
              <ul className="flex gap-6">
                <li>
                  <Link
                    href="/privacy"
                    className="transition-colors hover:text-green-400"
                  >
                    Privacy Policy
                  </Link>
                </li>
                <li>
                  <Link
                    href="/contact"
                    className="transition-colors hover:text-green-400"
                  >
                    Contact
                  </Link>
                </li>
              </ul>
            </nav>
          </div>
        </Container>
      </div>
    </footer>
  );
}
