/**
 * Build-time params for dynamic routes.
 *
 * With Cache Components enabled, Next.js rejects a `generateStaticParams`
 * that returns nothing — it cannot then prove the route has no unguarded
 * dynamic access. A section with no content yet (no events, no albums)
 * legitimately produces an empty list, which would fail the build.
 *
 * So when the list is empty we return one sentinel slug. The page looks it
 * up, finds nothing, and calls `notFound()`, exactly as it would for any
 * other unknown slug. It renders the 404 page, carries no links and is never
 * indexed. Once real content exists the sentinel disappears on the next build.
 */
export const EMPTY_SLUG = "not-found";

export function slugParams(slugs: string[]): { slug: string }[] {
  if (slugs.length === 0) {
    return [{ slug: EMPTY_SLUG }];
  }
  return slugs.map((slug) => ({ slug }));
}
