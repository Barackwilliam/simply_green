import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/** Merge Tailwind classes, letting later classes win conflicts. */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

const DATE_FORMAT = new Intl.DateTimeFormat("en-GB", {
  day: "numeric",
  month: "long",
  year: "numeric",
  timeZone: "Africa/Dar_es_Salaam",
});

const DATETIME_FORMAT = new Intl.DateTimeFormat("en-GB", {
  day: "numeric",
  month: "long",
  year: "numeric",
  hour: "2-digit",
  minute: "2-digit",
  timeZone: "Africa/Dar_es_Salaam",
});

export function formatDate(value: string | null | undefined): string {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "";
  return DATE_FORMAT.format(date);
}

export function formatDateTime(value: string | null | undefined): string {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "";
  return DATETIME_FORMAT.format(date);
}

/** "12 March 2025 – 14 March 2025", collapsing a same-day range. */
export function formatDateRange(
  start: string | null | undefined,
  end: string | null | undefined,
): string {
  const from = formatDate(start);
  const to = formatDate(end);
  if (!from) return to;
  if (!to || from === to) return from;
  return `${from} – ${to}`;
}

/** Cut text to a word boundary, with an ellipsis if anything was dropped. */
export function truncate(text: string, maxLength = 160): string {
  const clean = text.replace(/\s+/g, " ").trim();
  if (clean.length <= maxLength) return clean;
  const cut = clean.slice(0, maxLength);
  return `${cut.slice(0, cut.lastIndexOf(" "))}…`;
}

/**
 * Cut text at the last complete sentence that fits.
 *
 * Plain `truncate` leaves a clause dangling mid-thought, which reads badly in
 * a hero or card. This stops at a full stop instead, and only falls back to a
 * word-boundary cut when the first sentence is already too long.
 */
export function truncateAtSentence(text: string, maxLength = 420): string {
  const clean = text.replace(/\s+/g, " ").trim();
  if (clean.length <= maxLength) return clean;

  const window = clean.slice(0, maxLength + 1);
  const lastStop = Math.max(
    window.lastIndexOf(". "),
    window.lastIndexOf("! "),
    window.lastIndexOf("? "),
  );
  if (lastStop > maxLength * 0.4) {
    return clean.slice(0, lastStop + 1);
  }
  return truncate(clean, maxLength);
}

/** Strip HTML so rich text can be used in meta descriptions. */
export function stripHtml(html: string): string {
  return html
    .replace(/<[^>]*>/g, " ")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s+/g, " ")
    .trim();
}

/** Absolute site URL, used for canonical links, Open Graph and sitemaps. */
export const SITE_URL = (
  process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000"
).replace(/\/$/, "");

export function absoluteUrl(path = "/"): string {
  return `${SITE_URL}${path.startsWith("/") ? path : `/${path}`}`;
}
