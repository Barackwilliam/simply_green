import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, CalendarDays, MapPin } from "lucide-react";

import { Container, PageHeader, Section } from "@/components/ui";
import { getAlbum, getAlbumSlugs } from "@/lib/api";
import { slugParams } from "@/lib/static-params";
import { formatDate, truncate } from "@/lib/utils";

type Params = Promise<{ slug: string }>;

export async function generateStaticParams() {
  return slugParams(await getAlbumSlugs());
}

export async function generateMetadata({
  params,
}: {
  params: Params;
}): Promise<Metadata> {
  const { slug } = await params;
  const album = await getAlbum(slug);
  if (!album) return { title: "Album not found" };

  return {
    title: album.title,
    description: truncate(album.description, 158) || `Photographs from ${album.title}.`,
    alternates: { canonical: `/gallery/${album.slug}` },
    openGraph: album.cover_image ? { images: [{ url: album.cover_image }] } : undefined,
  };
}

export default async function AlbumPage({ params }: { params: Params }) {
  const { slug } = await params;
  const album = await getAlbum(slug);
  if (!album) notFound();

  const photos = album.photos ?? [];

  return (
    <>
      <PageHeader eyebrow="Gallery" title={album.title} description={album.description}>
        <div className="flex flex-wrap items-center gap-x-6 gap-y-2 text-sm text-ink-200">
          {album.date ? (
            <span className="inline-flex items-center gap-2">
              <CalendarDays className="h-4 w-4 text-green-400" aria-hidden />
              {formatDate(album.date)}
            </span>
          ) : null}
          {album.location ? (
            <span className="inline-flex items-center gap-2">
              <MapPin className="h-4 w-4 text-green-400" aria-hidden />
              {album.location}
            </span>
          ) : null}
        </div>
      </PageHeader>

      <Section>
        <Container>
          <Link
            href="/gallery"
            className="inline-flex items-center gap-1.5 text-sm font-semibold text-green-700 transition-colors hover:text-green-800"
          >
            <ArrowLeft className="h-4 w-4" aria-hidden />
            All albums
          </Link>

          {photos.length === 0 ? (
            <p className="mt-10 rounded-2xl border border-dashed border-sand-300 bg-sand-50 px-6 py-14 text-center text-sand-600">
              This album has no photographs yet.
            </p>
          ) : (
            <ul className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {photos.map((photo) => (
                <li key={photo.id}>
                  <figure>
                    <div className="relative aspect-[4/3] overflow-hidden rounded-2xl bg-sand-100">
                      <Image
                        src={photo.image}
                        alt={photo.alt_text || photo.caption || album.title}
                        fill
                        sizes="(min-width: 1024px) 30vw, (min-width: 640px) 50vw, 100vw"
                        className="object-cover transition-transform duration-500 hover:scale-[1.03]"
                      />
                    </div>
                    {photo.caption || photo.credit ? (
                      <figcaption className="mt-2.5 text-sm text-sand-600">
                        {photo.caption}
                        {photo.credit ? (
                          <span className="block text-xs text-sand-400">
                            Photo: {photo.credit}
                          </span>
                        ) : null}
                      </figcaption>
                    ) : null}
                  </figure>
                </li>
              ))}
            </ul>
          )}
        </Container>
      </Section>
    </>
  );
}
