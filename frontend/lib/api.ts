/**
 * Read-side API client.
 *
 * Every function here is cached with the `use cache` directive, tagged so the
 * Django admin can invalidate exactly what changed (see app/api/revalidate),
 * and given a lifetime so the site keeps serving even if the API is briefly
 * unreachable. Pages built on these functions are prerendered, which is what
 * makes the site fast and indexable.
 *
 * Submissions (contact, volunteer, donate, …) do NOT belong here — they are
 * uncached writes and live in lib/submit.ts.
 */

import { cacheLife, cacheTag } from "next/cache";

import type {
  Album,
  Category,
  CoreValue,
  DonationMethod,
  FocusArea,
  ImpactStat,
  Objective,
  Paginated,
  Partner,
  PartnerReason,
  Post,
  Programme,
  Publication,
  SiteEvent,
  SiteSettings,
  TeamMember,
  Video,
} from "./types";

export const API_BASE_URL = (
  process.env.API_URL ??
  process.env.NEXT_PUBLIC_API_URL ??
  "http://127.0.0.1:8000"
).replace(/\/$/, "");

/** Thrown when the API answers, but not with a success status. */
export class ApiError extends Error {
  constructor(
    readonly status: number,
    readonly path: string,
  ) {
    super(`API ${status} for ${path}`);
    this.name = "ApiError";
  }
}

async function request<T>(path: string): Promise<T> {
  const url = `${API_BASE_URL}/api${path}`;
  const response = await fetch(url, {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new ApiError(response.status, path);
  }
  return (await response.json()) as T;
}

/**
 * Fetch that returns a fallback instead of throwing.
 *
 * The site must still render when a section has no content yet, or when the
 * backend is briefly down — an NGO homepage that 500s because the gallery is
 * empty is worse than one missing its gallery.
 */
async function safe<T>(path: string, fallback: T): Promise<T> {
  try {
    return await request<T>(path);
  } catch {
    return fallback;
  }
}

function query(params: Record<string, string | number | boolean | undefined>) {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== "") {
      search.set(key, String(value));
    }
  }
  const qs = search.toString();
  return qs ? `?${qs}` : "";
}

const EMPTY = <T,>(): Paginated<T> => ({
  count: 0,
  next: null,
  previous: null,
  results: [],
});

/* ------------------------------------------------------------------ */
/* Site-wide                                                           */
/* ------------------------------------------------------------------ */

const SITE_FALLBACK: SiteSettings = {
  organisation_name: "Simply Green Organization",
  acronym: "SGO",
  tagline: "",
  logo: null,
  logo_light: null,
  favicon: null,
  registration_number: "",
  registration_statement: "",
  vision: "",
  mission: "",
  who_we_are: "",
  email: "",
  secondary_email: "",
  phone: "",
  secondary_phone: "",
  whatsapp: "",
  address: "",
  postal_address: "",
  city: "Dar es Salaam",
  country: "Tanzania",
  map_embed_url: "",
  latitude: null,
  longitude: null,
  default_meta_title: "",
  default_meta_description: "",
  default_og_image: null,
  google_analytics_id: "",
  google_site_verification: "",
  donate_enabled: true,
  volunteer_enabled: true,
  newsletter_enabled: true,
  social_links: [],
};

export async function getSiteSettings(): Promise<SiteSettings> {
  "use cache";
  cacheLife("hours");
  cacheTag("site-settings");
  return safe<SiteSettings>("/site-settings/", SITE_FALLBACK);
}

export async function getPartners(
  options: { kind?: string; featured?: boolean } = {},
): Promise<Partner[]> {
  "use cache";
  cacheLife("hours");
  cacheTag("partners");
  const qs = query({ kind: options.kind, is_featured: options.featured });
  const data = await safe(`/partners/${qs}`, EMPTY<Partner>());
  return data.results;
}

export async function getImpactStats(): Promise<ImpactStat[]> {
  "use cache";
  cacheLife("hours");
  cacheTag("impact-stats");
  return safe<ImpactStat[]>("/impact-stats/", []);
}

/* ------------------------------------------------------------------ */
/* About                                                               */
/* ------------------------------------------------------------------ */

export async function getCoreValues(): Promise<CoreValue[]> {
  "use cache";
  cacheLife("hours");
  cacheTag("about");
  return safe<CoreValue[]>("/about/core-values/", []);
}

export async function getObjectives(): Promise<Objective[]> {
  "use cache";
  cacheLife("hours");
  cacheTag("about");
  return safe<Objective[]>("/about/objectives/", []);
}

export async function getPartnerReasons(): Promise<PartnerReason[]> {
  "use cache";
  cacheLife("hours");
  cacheTag("about");
  return safe<PartnerReason[]>("/about/partner-reasons/", []);
}

export async function getTeam(group?: string): Promise<TeamMember[]> {
  "use cache";
  cacheLife("hours");
  cacheTag("team");
  return safe<TeamMember[]>(`/about/team/${query({ group })}`, []);
}

/* ------------------------------------------------------------------ */
/* Programmes                                                          */
/* ------------------------------------------------------------------ */

export async function getFocusAreas(): Promise<FocusArea[]> {
  "use cache";
  cacheLife("hours");
  cacheTag("focus-areas");
  return safe<FocusArea[]>("/programmes/focus-areas/", []);
}

export async function getFocusArea(slug: string): Promise<FocusArea | null> {
  "use cache";
  cacheLife("hours");
  cacheTag("focus-areas", `focus-area:${slug}`);
  try {
    return await request<FocusArea>(`/programmes/focus-areas/${slug}/`);
  } catch {
    return null;
  }
}

export async function getProgrammes(
  options: { status?: string; featured?: boolean; focusArea?: string } = {},
): Promise<Programme[]> {
  "use cache";
  cacheLife("hours");
  cacheTag("programmes");
  const qs = query({
    status: options.status,
    is_featured: options.featured,
    focus_areas__slug: options.focusArea,
  });
  const data = await safe(`/programmes/${qs}`, EMPTY<Programme>());
  return data.results;
}

export async function getProgramme(slug: string): Promise<Programme | null> {
  "use cache";
  cacheLife("hours");
  cacheTag("programmes", `programme:${slug}`);
  try {
    return await request<Programme>(`/programmes/${slug}/`);
  } catch {
    return null;
  }
}

/* ------------------------------------------------------------------ */
/* Resource centre                                                     */
/* ------------------------------------------------------------------ */

export async function getPublications(
  options: { kind?: string; year?: number; featured?: boolean } = {},
): Promise<Publication[]> {
  "use cache";
  cacheLife("hours");
  cacheTag("publications");
  const qs = query({
    kind: options.kind,
    year: options.year,
    is_featured: options.featured,
  });
  const data = await safe(
    `/resources/publications/${qs}`,
    EMPTY<Publication>(),
  );
  return data.results;
}

/* ------------------------------------------------------------------ */
/* News, posts and events                                              */
/* ------------------------------------------------------------------ */

export async function getPosts(
  options: {
    kind?: string;
    category?: string;
    featured?: boolean;
    pageSize?: number;
    page?: number;
  } = {},
): Promise<Paginated<Post>> {
  "use cache";
  cacheLife("hours");
  cacheTag("posts");
  const qs = query({
    kind: options.kind,
    category__slug: options.category,
    is_featured: options.featured,
    page_size: options.pageSize,
    page: options.page,
  });
  return safe(`/news/posts/${qs}`, EMPTY<Post>());
}

export async function getPost(slug: string): Promise<Post | null> {
  "use cache";
  cacheLife("hours");
  cacheTag("posts", `post:${slug}`);
  try {
    return await request<Post>(`/news/posts/${slug}/`);
  } catch {
    return null;
  }
}

export async function getCategories(): Promise<Category[]> {
  "use cache";
  cacheLife("hours");
  cacheTag("posts");
  return safe<Category[]>("/news/categories/", []);
}

export async function getEvents(
  options: { when?: "upcoming" | "past"; featured?: boolean } = {},
): Promise<SiteEvent[]> {
  "use cache";
  cacheLife("hours");
  cacheTag("events");
  const qs = query({ when: options.when, is_featured: options.featured });
  const data = await safe(`/news/events/${qs}`, EMPTY<SiteEvent>());
  return data.results;
}

export async function getEvent(slug: string): Promise<SiteEvent | null> {
  "use cache";
  cacheLife("hours");
  cacheTag("events", `event:${slug}`);
  try {
    return await request<SiteEvent>(`/news/events/${slug}/`);
  } catch {
    return null;
  }
}

/* ------------------------------------------------------------------ */
/* Gallery                                                             */
/* ------------------------------------------------------------------ */

export async function getAlbums(featured?: boolean): Promise<Album[]> {
  "use cache";
  cacheLife("hours");
  cacheTag("gallery");
  const data = await safe(
    `/gallery/albums/${query({ is_featured: featured })}`,
    EMPTY<Album>(),
  );
  return data.results;
}

export async function getAlbum(slug: string): Promise<Album | null> {
  "use cache";
  cacheLife("hours");
  cacheTag("gallery", `album:${slug}`);
  try {
    return await request<Album>(`/gallery/albums/${slug}/`);
  } catch {
    return null;
  }
}

export async function getVideos(featured?: boolean): Promise<Video[]> {
  "use cache";
  cacheLife("hours");
  cacheTag("gallery");
  const data = await safe(
    `/gallery/videos/${query({ is_featured: featured })}`,
    EMPTY<Video>(),
  );
  return data.results;
}

/* ------------------------------------------------------------------ */
/* Donations                                                           */
/* ------------------------------------------------------------------ */

export async function getDonationMethods(): Promise<DonationMethod[]> {
  "use cache";
  cacheLife("hours");
  cacheTag("donation-methods");
  return safe<DonationMethod[]>("/engage/donation-methods/", []);
}
