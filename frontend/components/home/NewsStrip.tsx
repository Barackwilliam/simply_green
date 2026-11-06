import Image from "next/image";
import Link from "next/link";
import { ArrowRight, Clock } from "lucide-react";

import { Badge, ButtonLink, Container, Section, SectionHeading } from "@/components/ui";
import type { Post } from "@/lib/types";
import { formatDate } from "@/lib/utils";

export function NewsStrip({
  posts,
  fallbackImage,
}: {
  posts: Post[];
  fallbackImage: string;
}) {
  if (posts.length === 0) return null;

  return (
    <Section tone="muted">
      <Container>
        <div className="flex flex-col gap-6 sm:flex-row sm:items-end sm:justify-between">
          <SectionHeading
            eyebrow="Latest"
            title="News and stories"
            description="What we are learning, publishing and seeing change."
          />
          <ButtonLink href="/news" variant="outline" className="shrink-0">
            All news
            <ArrowRight className="h-4 w-4" aria-hidden />
          </ButtonLink>
        </div>

        <ul className="mt-14 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {posts.slice(0, 3).map((post) => (
            <li key={post.id}>
              <Link
                href={`/news/${post.slug}`}
                className="group flex h-full flex-col overflow-hidden rounded-2xl border border-sand-200 bg-white transition-all duration-300 ease-[var(--ease-out-soft)] hover:-translate-y-1 hover:border-green-300 hover:shadow-xl hover:shadow-ink-950/5"
              >
                <div className="relative aspect-[16/10] overflow-hidden bg-sand-100">
                  <Image
                    src={post.featured_image ?? fallbackImage}
                    alt={post.featured_image_alt || post.title}
                    fill
                    sizes="(min-width: 1024px) 30vw, (min-width: 768px) 50vw, 100vw"
                    className="object-cover transition-transform duration-500 ease-[var(--ease-out-soft)] group-hover:scale-[1.04]"
                  />
                </div>

                <div className="flex flex-1 flex-col p-6">
                  <div className="mb-3 flex flex-wrap items-center gap-2">
                    <Badge tone="sky">{post.kind_label}</Badge>
                    {post.category ? (
                      <Badge tone="neutral">{post.category.name}</Badge>
                    ) : null}
                  </div>

                  <h3 className="font-display text-lg font-bold leading-snug text-ink-950 group-hover:text-green-700">
                    {post.title}
                  </h3>

                  {post.excerpt ? (
                    <p className="mt-3 flex-1 text-sm leading-relaxed text-sand-700">
                      {post.excerpt.length > 150
                        ? `${post.excerpt.slice(0, 150).trimEnd()}…`
                        : post.excerpt}
                    </p>
                  ) : null}

                  <div className="mt-5 flex items-center gap-3 border-t border-sand-100 pt-4 text-xs text-sand-500">
                    <time dateTime={post.published_at}>
                      {formatDate(post.published_at)}
                    </time>
                    {post.reading_minutes ? (
                      <>
                        <span aria-hidden>·</span>
                        <span className="inline-flex items-center gap-1">
                          <Clock className="h-3 w-3" aria-hidden />
                          {post.reading_minutes} min read
                        </span>
                      </>
                    ) : null}
                  </div>
                </div>
              </Link>
            </li>
          ))}
        </ul>
      </Container>
    </Section>
  );
}
