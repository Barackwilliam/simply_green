import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { Images, Play } from "lucide-react";

import { Container, EmptyState, PageHeader, Section } from "@/components/ui";
import { getVideos } from "@/lib/api";
import { formatDate } from "@/lib/utils";

export const metadata: Metadata = {
  title: "Videos",
  description:
    "Film from Simply Green Organization's environmental work across Tanzania.",
  alternates: { canonical: "/gallery/videos" },
};

export default async function VideosPage() {
  const videos = await getVideos();

  return (
    <>
      <PageHeader eyebrow="Gallery" title="Videos" description="Film from the field.">
        <Link
          href="/gallery"
          className="inline-flex items-center gap-2 rounded-full border-2 border-white/30 px-5 py-2.5 text-sm font-semibold text-white transition-colors hover:border-white hover:bg-white/10"
        >
          <Images className="h-4 w-4" aria-hidden />
          Browse photos instead
        </Link>
      </PageHeader>

      <Section>
        <Container>
          {videos.length === 0 ? (
            <EmptyState
              icon={<Play className="h-10 w-10" />}
              title="No videos yet"
              description="Videos added in the admin — YouTube, Vimeo or uploaded files — will appear here."
            />
          ) : (
            <ul className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {videos.map((video) => (
                <li key={video.id}>
                  <article className="group flex h-full flex-col overflow-hidden rounded-2xl border border-sand-200 bg-white transition-all duration-300 hover:-translate-y-1 hover:border-green-300 hover:shadow-xl hover:shadow-ink-950/5">
                    <a
                      href={video.video_url || video.video_file || "#"}
                      target="_blank"
                      rel="noreferrer noopener"
                      className="relative block aspect-video overflow-hidden bg-ink-900"
                    >
                      {video.thumbnail ? (
                        <Image
                          src={video.thumbnail}
                          alt={video.title}
                          fill
                          sizes="(min-width: 1024px) 30vw, (min-width: 640px) 50vw, 100vw"
                          className="object-cover opacity-80 transition-opacity group-hover:opacity-100"
                        />
                      ) : null}
                      <span className="absolute inset-0 flex items-center justify-center">
                        <span className="flex h-14 w-14 items-center justify-center rounded-full bg-white/90 text-ink-950 transition-transform group-hover:scale-110">
                          <Play className="ml-0.5 h-6 w-6 fill-current" aria-hidden />
                        </span>
                      </span>
                      {video.duration_label ? (
                        <span className="absolute bottom-3 right-3 rounded bg-ink-950/80 px-2 py-0.5 text-xs font-medium text-white">
                          {video.duration_label}
                        </span>
                      ) : null}
                    </a>

                    <div className="flex flex-1 flex-col p-6">
                      <h2 className="font-display text-base font-bold leading-snug text-ink-950">
                        {video.title}
                      </h2>
                      {video.description ? (
                        <p className="mt-2.5 flex-1 text-sm leading-relaxed text-sand-700">
                          {video.description}
                        </p>
                      ) : null}
                      <p className="mt-4 text-xs text-sand-500">
                        {[video.source_label, video.date ? formatDate(video.date) : ""]
                          .filter(Boolean)
                          .join(" · ")}
                      </p>
                    </div>
                  </article>
                </li>
              ))}
            </ul>
          )}
        </Container>
      </Section>
    </>
  );
}
