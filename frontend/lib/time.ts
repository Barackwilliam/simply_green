import { cacheLife } from "next/cache";

/**
 * The current year, as a cached value.
 *
 * With Cache Components on, reading the clock during prerender is an error —
 * the value would be frozen into the static shell. Caching it with a daily
 * lifetime keeps the footer prerenderable and still correct.
 */
export async function getCurrentYear(): Promise<number> {
  "use cache";
  cacheLife("days");
  return new Date().getFullYear();
}
