import type { Metadata } from "next";

import { FocusAreaGrid } from "@/components/home/FocusAreaGrid";
import { GetInvolvedBand } from "@/components/home/GetInvolvedBand";
import { Hero } from "@/components/home/Hero";
import { ImpactStats } from "@/components/home/ImpactStats";
import { NewsStrip } from "@/components/home/NewsStrip";
import { PartnerWall } from "@/components/home/PartnerWall";
import { ProgrammeShowcase } from "@/components/home/ProgrammeShowcase";
import { WhoWeAre } from "@/components/home/WhoWeAre";
import { WhyPartner } from "@/components/home/WhyPartner";
import {
  getFocusAreas,
  getImpactStats,
  getPartnerReasons,
  getPartners,
  getPosts,
  getProgrammes,
  getSiteSettings,
} from "@/lib/api";
import { stripHtml, truncate, truncateAtSentence } from "@/lib/utils";

export async function generateMetadata(): Promise<Metadata> {
  const settings = await getSiteSettings();
  const description =
    settings.default_meta_description ||
    truncate(
      stripHtml(settings.who_we_are) || settings.mission,
      158,
    ) ||
    "Environmental sustainability, climate action and community empowerment across Tanzania.";

  return {
    title: `${settings.organisation_name} — Environmental action across Tanzania`,
    description,
    alternates: { canonical: "/" },
  };
}

export default async function HomePage() {
  const [
    settings,
    stats,
    focusAreas,
    programmes,
    reasons,
    posts,
    partners,
  ] = await Promise.all([
    getSiteSettings(),
    getImpactStats(),
    getFocusAreas(),
    getProgrammes({ status: "ongoing" }),
    getPartnerReasons(),
    getPosts({ pageSize: 3 }),
    getPartners(),
  ]);

  const summary =
    stripHtml(settings.who_we_are) ||
    `${settings.organisation_name} works across Mainland Tanzania to promote environmental sustainability, climate action, community empowerment and sustainable livelihoods.`;

  return (
    <>
      <Hero
        organisationName={settings.organisation_name}
        tagline={settings.tagline}
        mission={settings.mission}
        imageUrl="/images/hero-cleanup.jpg"
        imageAlt="Simply Green Organization staff standing with sacks of waste collected during a coastal clean-up in Dar es Salaam"
      />

      <ImpactStats stats={stats} />

      <WhoWeAre
        vision={
          settings.vision ||
          "Communities better equipped to protect their environment, respond to climate challenges and build a greener, more resilient Tanzania."
        }
        mission={
          settings.mission ||
          "To empower communities to protect the environment and address climate challenges through sustainable conservation practices, innovation, and livelihood initiatives."
        }
        summary={truncateAtSentence(summary, 440)}
        imageUrl="/images/litter-collection.jpg"
        imageAlt="Three Simply Green Organization team members clearing plastic waste from a shoreline"
        registrationStatement={settings.registration_statement}
      />

      <FocusAreaGrid areas={focusAreas} />

      <ProgrammeShowcase
        programmes={programmes}
        fallbackImage="/images/team-waste.jpg"
      />

      <WhyPartner
        reasons={reasons}
        imageUrl="/images/planning-session.jpg"
        imageAlt="Simply Green Organization team planning a programme together"
      />

      <NewsStrip
        posts={posts.results}
        fallbackImage="/images/tying-sacks.jpg"
      />

      <PartnerWall partners={partners} />

      <GetInvolvedBand />
    </>
  );
}
