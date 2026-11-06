import type { MetadataRoute } from "next";

import {
  getAlbumSlugs,
  getEventSlugs,
  getFocusAreaSlugs,
  getPostSlugs,
  getProgrammeSlugs,
} from "@/lib/api";
import { SITE_URL } from "@/lib/utils";

/** Pages that always exist, with how often they are worth recrawling. */
const STATIC_ROUTES: {
  path: string;
  changeFrequency: MetadataRoute.Sitemap[number]["changeFrequency"];
  priority: number;
}[] = [
  { path: "/", changeFrequency: "weekly", priority: 1 },
  { path: "/about", changeFrequency: "monthly", priority: 0.9 },
  { path: "/about/team", changeFrequency: "monthly", priority: 0.7 },
  { path: "/focus-areas", changeFrequency: "monthly", priority: 0.9 },
  { path: "/programmes", changeFrequency: "weekly", priority: 0.9 },
  { path: "/resources", changeFrequency: "weekly", priority: 0.8 },
  { path: "/news", changeFrequency: "daily", priority: 0.8 },
  { path: "/events", changeFrequency: "daily", priority: 0.8 },
  { path: "/gallery", changeFrequency: "weekly", priority: 0.6 },
  { path: "/gallery/videos", changeFrequency: "weekly", priority: 0.6 },
  { path: "/get-involved", changeFrequency: "monthly", priority: 0.8 },
  { path: "/get-involved/volunteer", changeFrequency: "monthly", priority: 0.7 },
  { path: "/get-involved/partner", changeFrequency: "monthly", priority: 0.7 },
  { path: "/donate", changeFrequency: "monthly", priority: 0.9 },
  { path: "/contact", changeFrequency: "monthly", priority: 0.7 },
  { path: "/privacy", changeFrequency: "yearly", priority: 0.2 },
];

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const [programmes, focusAreas, posts, events, albums] = await Promise.all([
    getProgrammeSlugs(),
    getFocusAreaSlugs(),
    getPostSlugs(),
    getEventSlugs(),
    getAlbumSlugs(),
  ]);

  const entries: MetadataRoute.Sitemap = STATIC_ROUTES.map((route) => ({
    url: `${SITE_URL}${route.path}`,
    changeFrequency: route.changeFrequency,
    priority: route.priority,
  }));

  const dynamic: [string[], string, number][] = [
    [programmes, "/programmes", 0.8],
    [focusAreas, "/focus-areas", 0.7],
    [posts, "/news", 0.7],
    [events, "/events", 0.6],
    [albums, "/gallery", 0.5],
  ];

  for (const [slugs, prefix, priority] of dynamic) {
    for (const slug of slugs) {
      entries.push({
        url: `${SITE_URL}${prefix}/${slug}`,
        changeFrequency: "monthly",
        priority,
      });
    }
  }

  return entries;
}
