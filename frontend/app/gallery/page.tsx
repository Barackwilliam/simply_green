import type { Metadata } from "next";
import Link from "next/link";
import { Images, Video as VideoIcon } from "lucide-react";

import { AlbumCard } from "@/components/cards";
import { Container, EmptyState, PageHeader, Section } from "@/components/ui";
import { getAlbums } from "@/lib/api";

export const metadata: Metadata = {
  title: "Gallery",
  description:
    "Photographs from Simply Green Organization's clean-ups, trainings, restoration days and community work across Tanzania.",
  alternates: { canonical: "/gallery" },
};

export default async function GalleryPage() {
  const albums = await getAlbums();

  return (
    <>
      <PageHeader
        eyebrow="Gallery"
        title="Photos"
        description="The work, as it happens."
      >
        <Link
          href="/gallery/videos"
          className="inline-flex items-center gap-2 rounded-full border-2 border-white/30 px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:border-white hover:bg-white/10"
        >
          <VideoIcon className="h-4 w-4" aria-hidden />
          Watch videos instead
        </Link>
      </PageHeader>

      <Section>
        <Container>
          {albums.length === 0 ? (
            <EmptyState
              icon={<Images className="h-10 w-10" />}
              title="No albums yet"
              description="Photo albums created in the admin will appear here."
            />
          ) : (
            <ul className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {albums.map((album) => (
                <li key={album.id}>
                  <AlbumCard album={album} />
                </li>
              ))}
            </ul>
          )}
        </Container>
      </Section>
    </>
  );
}
