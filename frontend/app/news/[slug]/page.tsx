import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, Clock } from "lucide-react";

import { PostCard } from "@/components/cards";
import { Badge, Container, Section, SectionHeading } from "@/components/ui";
import { getPost, getPostSlugs, getPosts } from "@/lib/api";
import { slugParams } from "@/lib/static-params";
import { SITE_URL, formatDate, stripHtml, truncate } from "@/lib/utils";

type Params = Promise<{ slug: string }>;

export async function generateStaticParams() {
  return slugParams(await getPostSlugs());
}

export async function generateMetadata({
  params,
}: {
  params: Params;
}): Promise<Metadata> {
  const { slug } = await params;
  const post = await getPost(slug);
  if (!post) return { title: "Article not found" };

  const description =
    post.meta_description ||
    post.excerpt ||
    truncate(stripHtml(post.body ?? ""), 158);

  return {
    title: post.meta_title || post.title,
    description,
    alternates: { canonical: `/news/${post.slug}` },
    robots: post.noindex ? { index: false, follow: true } : undefined,
    openGraph: {
      type: "article",
      title: post.title,
      description,
      publishedTime: post.published_at,
      authors: post.author_display ? [post.author_display] : undefined,
      images: post.og_image
        ? [{ url: post.og_image }]
        : post.featured_image
          ? [{ url: post.featured_image }]
          : undefined,
    },
  };
}

export default async function PostPage({ params }: { params: Params }) {
  const { slug } = await params;
  const post = await getPost(slug);
  if (!post) notFound();

  const related = await getPosts({ kind: post.kind, pageSize: 4 });
  const others = related.results.filter((item) => item.slug !== post.slug).slice(0, 3);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    headline: post.title,
    description: post.excerpt || truncate(stripHtml(post.body ?? ""), 200),
    image: post.featured_image ?? undefined,
    datePublished: post.published_at,
    author: post.author_display
      ? { "@type": "Person", name: post.author_display }
      : { "@type": "Organization", name: "Simply Green Organization" },
    publisher: {
      "@type": "NGO",
      name: "Simply Green Organization",
      url: SITE_URL,
    },
    mainEntityOfPage: `${SITE_URL}/news/${post.slug}`,
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      <header className="bg-forest-wash pt-32 pb-14 text-white sm:pt-36 sm:pb-16">
        <Container>
          <div className="mx-auto max-w-3xl">
            <Link
              href="/news"
              className="inline-flex items-center gap-1.5 text-sm font-semibold text-green-300 transition-colors hover:text-green-200"
            >
              <ArrowLeft className="h-4 w-4" aria-hidden />
              All news
            </Link>

            <div className="mt-6 flex flex-wrap gap-2">
              <Badge tone="light">{post.kind_label}</Badge>
              {post.category ? <Badge tone="light">{post.category.name}</Badge> : null}
            </div>

            <h1 className="mt-5 text-3xl sm:text-4xl lg:text-5xl lg:leading-[1.1]">
              {post.title}
            </h1>

            <div className="mt-6 flex flex-wrap items-center gap-3 text-sm text-ink-300">
              {post.author_display ? <span>{post.author_display}</span> : null}
              {post.author_display ? <span aria-hidden>·</span> : null}
              <time dateTime={post.published_at}>
                {formatDate(post.published_at)}
              </time>
              {post.reading_minutes ? (
                <>
                  <span aria-hidden>·</span>
                  <span className="inline-flex items-center gap-1">
                    <Clock className="h-3.5 w-3.5" aria-hidden />
                    {post.reading_minutes} min read
                  </span>
                </>
              ) : null}
            </div>
          </div>
        </Container>
      </header>

      {post.featured_image ? (
        <Container className="-mt-8">
          <figure className="mx-auto max-w-4xl">
            <div className="relative aspect-[16/9] overflow-hidden rounded-2xl bg-sand-100 shadow-xl shadow-ink-950/10">
              <Image
                src={post.featured_image}
                alt={post.featured_image_alt || post.title}
                fill
                priority
                sizes="(min-width: 1024px) 60vw, 100vw"
                className="object-cover"
              />
            </div>
            {post.featured_image_credit ? (
              <figcaption className="mt-2.5 text-center text-xs text-sand-500">
                {post.featured_image_credit}
              </figcaption>
            ) : null}
          </figure>
        </Container>
      ) : null}

      <Section>
        <Container>
          <article className="mx-auto max-w-3xl">
            {post.excerpt ? (
              <p className="text-xl leading-relaxed text-ink-900">
                {post.excerpt}
              </p>
            ) : null}

            {post.audio_url || post.audio_file ? (
              <div className="mt-8 rounded-2xl border border-sand-200 bg-sand-50 p-6">
                <p className="mb-3 font-display text-sm font-bold uppercase tracking-wider text-sand-600">
                  Listen
                </p>
                {post.audio_file ? (
                  <audio controls preload="none" className="w-full">
                    <source src={post.audio_file} />
                    Your browser does not support audio playback.
                  </audio>
                ) : (
                  <a
                    href={post.audio_url}
                    target="_blank"
                    rel="noreferrer noopener"
                    className="text-sm font-semibold text-sky-700 underline underline-offset-4"
                  >
                    Open the episode
                  </a>
                )}
              </div>
            ) : null}

            {post.body ? (
              <div
                className="prose-content mt-8"
                dangerouslySetInnerHTML={{ __html: post.body }}
              />
            ) : null}

            {post.tags.length > 0 ? (
              <ul className="mt-12 flex flex-wrap gap-2 border-t border-sand-200 pt-8">
                {post.tags.map((tag) => (
                  <li key={tag}>
                    <Badge tone="neutral">{tag}</Badge>
                  </li>
                ))}
              </ul>
            ) : null}
          </article>
        </Container>
      </Section>

      {others.length > 0 ? (
        <Section tone="muted">
          <Container>
            <SectionHeading title="More like this" />
            <ul className="mt-10 grid gap-6 md:grid-cols-3">
              {others.map((item) => (
                <li key={item.id}>
                  <PostCard post={item} />
                </li>
              ))}
            </ul>
          </Container>
        </Section>
      ) : null}
    </>
  );
}
