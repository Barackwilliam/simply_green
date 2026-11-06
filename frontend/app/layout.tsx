import type { Metadata, Viewport } from "next";
import { Inter, Plus_Jakarta_Sans } from "next/font/google";

import { SiteFooter } from "@/components/layout/SiteFooter";
import { SiteHeader } from "@/components/layout/SiteHeader";
import { getSiteSettings } from "@/lib/api";
import { SITE_URL } from "@/lib/utils";

import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const jakarta = Plus_Jakarta_Sans({
  subsets: ["latin"],
  variable: "--font-jakarta",
  display: "swap",
  weight: ["500", "600", "700", "800"],
});

export async function generateMetadata(): Promise<Metadata> {
  const settings = await getSiteSettings();

  const title =
    settings.default_meta_title ||
    `${settings.organisation_name} — Environmental sustainability in Tanzania`;
  const description =
    settings.default_meta_description ||
    "Simply Green Organization empowers communities across Tanzania to " +
      "protect the environment, respond to climate change and build " +
      "sustainable livelihoods.";

  return {
    metadataBase: new URL(SITE_URL),
    title: {
      default: title,
      template: `%s — ${settings.organisation_name}`,
    },
    description,
    applicationName: settings.organisation_name,
    keywords: [
      "environmental NGO Tanzania",
      "climate action Tanzania",
      "waste management Dar es Salaam",
      "mangrove restoration",
      "community empowerment",
      "sustainable livelihoods",
      settings.organisation_name,
    ],
    authors: [{ name: settings.organisation_name }],
    creator: settings.organisation_name,
    publisher: settings.organisation_name,
    alternates: { canonical: "/" },
    openGraph: {
      type: "website",
      locale: "en_GB",
      url: SITE_URL,
      siteName: settings.organisation_name,
      title,
      description,
      images: settings.default_og_image
        ? [{ url: settings.default_og_image, width: 1200, height: 630 }]
        : undefined,
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: settings.default_og_image
        ? [settings.default_og_image]
        : undefined,
    },
    robots: {
      index: true,
      follow: true,
      googleBot: {
        index: true,
        follow: true,
        "max-image-preview": "large",
        "max-snippet": -1,
        "max-video-preview": -1,
      },
    },
    verification: settings.google_site_verification
      ? { google: settings.google_site_verification }
      : undefined,
    icons: settings.favicon ? { icon: settings.favicon } : undefined,
  };
}

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#0f1f1c" },
  ],
  width: "device-width",
  initialScale: 1,
};

export default async function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  const settings = await getSiteSettings();

  const organisationJsonLd = {
    "@context": "https://schema.org",
    "@type": "NGO",
    name: settings.organisation_name,
    alternateName: settings.acronym || undefined,
    url: SITE_URL,
    logo: settings.logo ?? undefined,
    description:
      settings.default_meta_description ||
      settings.mission ||
      `${settings.organisation_name} works on environmental sustainability and climate action in Tanzania.`,
    email: settings.email || undefined,
    telephone: settings.phone || undefined,
    address: {
      "@type": "PostalAddress",
      streetAddress: settings.address || undefined,
      addressLocality: settings.city || undefined,
      addressCountry: settings.country || "Tanzania",
    },
    sameAs: settings.social_links.map((link) => link.url),
  };

  return (
    <html lang="en" className={`${inter.variable} ${jakarta.variable}`}>
      <body className="min-h-dvh antialiased">
        <script
          type="application/ld+json"
          // Structured data is generated here, not user input.
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(organisationJsonLd),
          }}
        />

        <SiteHeader
          organisationName={settings.organisation_name}
          logoUrl={settings.logo}
          donateEnabled={settings.donate_enabled}
        />

        <main id="main">{children}</main>

        <SiteFooter settings={settings} />
      </body>
    </html>
  );
}
