import { revalidateTag } from "next/cache";
import { NextResponse } from "next/server";

/**
 * On-demand cache invalidation, called by Django when content changes.
 *
 * Pages are prerendered and their data cached with `use cache`, so without
 * this the site would keep serving the previous version until the cache
 * lifetime expired. Django posts the tags that changed; we drop exactly
 * those entries and the next request re-renders.
 *
 * Protected by a shared secret. If REVALIDATE_SECRET is unset the endpoint
 * refuses every request rather than defaulting to open.
 */

/** Tags the backend is allowed to invalidate, matching lib/api.ts. */
const KNOWN_TAGS = new Set([
  "site-settings",
  "partners",
  "impact-stats",
  "about",
  "team",
  "focus-areas",
  "programmes",
  "publications",
  "posts",
  "events",
  "gallery",
  "donation-methods",
]);

/** Scoped tags look like `programme:tandika-clean-market`. */
const SCOPED_TAG = /^[a-z-]+:[a-z0-9-]+$/;

function isAllowed(tag: string) {
  return KNOWN_TAGS.has(tag) || SCOPED_TAG.test(tag);
}

export async function POST(request: Request) {
  const secret = process.env.REVALIDATE_SECRET;

  if (!secret) {
    return NextResponse.json(
      { error: "Revalidation is not configured." },
      { status: 503 },
    );
  }

  if (request.headers.get("x-revalidate-secret") !== secret) {
    return NextResponse.json({ error: "Unauthorised." }, { status: 401 });
  }

  let tags: unknown;
  try {
    ({ tags } = (await request.json()) as { tags?: unknown });
  } catch {
    return NextResponse.json({ error: "Invalid JSON body." }, { status: 400 });
  }

  if (!Array.isArray(tags) || tags.length === 0) {
    return NextResponse.json(
      { error: "Body must be { tags: string[] } with at least one tag." },
      { status: 400 },
    );
  }

  const accepted: string[] = [];
  const rejected: string[] = [];

  for (const tag of tags) {
    if (typeof tag === "string" && isAllowed(tag)) {
      revalidateTag(tag, "max");
      accepted.push(tag);
    } else {
      rejected.push(String(tag));
    }
  }

  return NextResponse.json({ revalidated: accepted, ignored: rejected });
}
