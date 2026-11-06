import Image from "next/image";
import Link from "next/link";
import { ArrowUpRight, CalendarDays, Clock, Download, FileText, MapPin, Users } from "lucide-react";

import { Badge } from "@/components/ui";
import type { Album, Post, Programme, Publication, SiteEvent, TeamMember } from "@/lib/types";
import { formatDate, formatDateTime, truncate } from "@/lib/utils";

const CARD = [
  "group flex h-full flex-col overflow-hidden rounded-2xl",
  "border border-sand-200 bg-white",
  "transition-all duration-300 ease-[var(--ease-out-soft)]",
  "hover:-translate-y-1 hover:border-green-300 hover:shadow-xl hover:shadow-ink-950/5",
].join(" ");

/* ------------------------------------------------------------------ */

export function ProgrammeCard({
  programme,
  fallbackImage = "/images/team-waste.jpg",
}: {
  programme: Programme;
  fallbackImage?: string;
}) {
  return (
    <Link href={`/programmes/${programme.slug}`} className={CARD}>
      <div className="relative aspect-[16/10] overflow-hidden bg-sand-100">
        <Image
          src={programme.featured_image ?? fallbackImage}
          alt={programme.title}
          fill
          sizes="(min-width: 1024px) 30vw, (min-width: 640px) 50vw, 100vw"
          className="object-cover transition-transform duration-500 ease-[var(--ease-out-soft)] group-hover:scale-[1.04]"
        />
        <div className="absolute left-4 top-4">
          <Badge tone={programme.status === "ongoing" ? "green" : "neutral"}>
            {programme.status_label}
          </Badge>
        </div>
      </div>

      <div className="flex flex-1 flex-col p-6">
        <h3 className="font-display text-lg font-bold leading-snug text-ink-950 group-hover:text-green-700">
          {programme.title}
        </h3>
        <p className="mt-3 flex-1 text-sm leading-relaxed text-sand-700">
          {truncate(programme.summary, 165)}
        </p>

        <dl className="mt-5 space-y-2 border-t border-sand-100 pt-4 text-xs text-sand-600">
          {programme.location ? (
            <div className="flex items-start gap-2">
              <dt className="sr-only">Location</dt>
              <MapPin className="mt-px h-3.5 w-3.5 shrink-0 text-green-600" aria-hidden />
              <dd>{programme.location}</dd>
            </div>
          ) : null}
          {programme.beneficiaries ? (
            <div className="flex items-start gap-2">
              <dt className="sr-only">Beneficiaries</dt>
              <Users className="mt-px h-3.5 w-3.5 shrink-0 text-green-600" aria-hidden />
              <dd>{programme.beneficiaries}</dd>
            </div>
          ) : null}
        </dl>
      </div>
    </Link>
  );
}

/* ------------------------------------------------------------------ */

export function PostCard({
  post,
  fallbackImage = "/images/tying-sacks.jpg",
}: {
  post: Post;
  fallbackImage?: string;
}) {
  return (
    <Link href={`/news/${post.slug}`} className={CARD}>
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
          {post.category ? <Badge tone="neutral">{post.category.name}</Badge> : null}
        </div>

        <h3 className="font-display text-lg font-bold leading-snug text-ink-950 group-hover:text-green-700">
          {post.title}
        </h3>

        {post.excerpt ? (
          <p className="mt-3 flex-1 text-sm leading-relaxed text-sand-700">
            {truncate(post.excerpt, 150)}
          </p>
        ) : null}

        <div className="mt-5 flex items-center gap-3 border-t border-sand-100 pt-4 text-xs text-sand-500">
          <time dateTime={post.published_at}>{formatDate(post.published_at)}</time>
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
  );
}

/* ------------------------------------------------------------------ */

export function EventCard({
  event,
  fallbackImage = "/images/community-group.jpg",
}: {
  event: SiteEvent;
  fallbackImage?: string;
}) {
  return (
    <Link href={`/events/${event.slug}`} className={CARD}>
      <div className="relative aspect-[16/10] overflow-hidden bg-sand-100">
        <Image
          src={event.featured_image ?? fallbackImage}
          alt={event.title}
          fill
          sizes="(min-width: 1024px) 30vw, (min-width: 768px) 50vw, 100vw"
          className="object-cover transition-transform duration-500 ease-[var(--ease-out-soft)] group-hover:scale-[1.04]"
        />
        <div className="absolute left-4 top-4">
          <Badge tone={event.status === "upcoming" ? "green" : "neutral"}>
            {event.status_label}
          </Badge>
        </div>
      </div>

      <div className="flex flex-1 flex-col p-6">
        <h3 className="font-display text-lg font-bold leading-snug text-ink-950 group-hover:text-green-700">
          {event.title}
        </h3>
        {event.summary ? (
          <p className="mt-3 flex-1 text-sm leading-relaxed text-sand-700">
            {truncate(event.summary, 140)}
          </p>
        ) : null}

        <dl className="mt-5 space-y-2 border-t border-sand-100 pt-4 text-xs text-sand-600">
          <div className="flex items-start gap-2">
            <dt className="sr-only">When</dt>
            <CalendarDays className="mt-px h-3.5 w-3.5 shrink-0 text-green-600" aria-hidden />
            <dd>{formatDateTime(event.start_datetime)}</dd>
          </div>
          {event.venue ? (
            <div className="flex items-start gap-2">
              <dt className="sr-only">Where</dt>
              <MapPin className="mt-px h-3.5 w-3.5 shrink-0 text-green-600" aria-hidden />
              <dd>{event.is_online ? "Online" : event.venue}</dd>
            </div>
          ) : null}
        </dl>
      </div>
    </Link>
  );
}

/* ------------------------------------------------------------------ */

export function PublicationCard({ publication }: { publication: Publication }) {
  return (
    <article className="group flex h-full flex-col rounded-2xl border border-sand-200 bg-white p-6 transition-all duration-300 hover:-translate-y-1 hover:border-green-300 hover:shadow-xl hover:shadow-ink-950/5">
      <div className="flex items-start justify-between gap-4">
        <Badge tone="gold">{publication.kind_label}</Badge>
        {publication.year ? (
          <span className="font-display text-sm font-bold text-sand-500">
            {publication.year}
          </span>
        ) : null}
      </div>

      <span className="mt-5 inline-flex h-11 w-11 items-center justify-center rounded-xl bg-green-50 text-green-700">
        <FileText className="h-5 w-5" aria-hidden />
      </span>

      <h3 className="mt-4 font-display text-base font-bold leading-snug text-ink-950">
        {publication.title}
      </h3>

      {publication.summary ? (
        <p className="mt-3 flex-1 text-sm leading-relaxed text-sand-700">
          {truncate(publication.summary, 150)}
        </p>
      ) : (
        <div className="flex-1" />
      )}

      <div className="mt-6 flex items-center justify-between border-t border-sand-100 pt-4">
        <span className="text-xs text-sand-500">
          {[publication.file_size_label, publication.page_count ? `${publication.page_count} pages` : ""]
            .filter(Boolean)
            .join(" · ")}
        </span>

        {publication.download_url ? (
          <a
            href={publication.download_url}
            target="_blank"
            rel="noreferrer noopener"
            className="inline-flex items-center gap-1.5 rounded-full bg-green-600 px-4 py-2 text-xs font-semibold text-white transition-colors hover:bg-green-700"
          >
            <Download className="h-3.5 w-3.5" aria-hidden />
            Download
          </a>
        ) : null}
      </div>
    </article>
  );
}

/* ------------------------------------------------------------------ */

export function AlbumCard({ album }: { album: Album }) {
  return (
    <Link href={`/gallery/${album.slug}`} className={CARD}>
      <div className="relative aspect-[4/3] overflow-hidden bg-sand-100">
        {album.cover_image ? (
          <Image
            src={album.cover_image}
            alt={album.title}
            fill
            sizes="(min-width: 1024px) 30vw, (min-width: 640px) 50vw, 100vw"
            className="object-cover transition-transform duration-500 ease-[var(--ease-out-soft)] group-hover:scale-[1.04]"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-sand-400">
            No cover image
          </div>
        )}
        <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-ink-950/80 to-transparent p-5">
          <h3 className="font-display text-base font-bold text-white">
            {album.title}
          </h3>
          <p className="mt-1 text-xs text-ink-200">
            {album.photo_count} photo{album.photo_count === 1 ? "" : "s"}
            {album.date ? ` · ${formatDate(album.date)}` : ""}
          </p>
        </div>
      </div>
    </Link>
  );
}

/* ------------------------------------------------------------------ */

export function TeamCard({ member }: { member: TeamMember }) {
  return (
    <article className="group flex flex-col overflow-hidden rounded-2xl border border-sand-200 bg-white transition-all duration-300 hover:-translate-y-1 hover:border-green-300 hover:shadow-xl hover:shadow-ink-950/5">
      <div className="relative aspect-[4/5] overflow-hidden bg-sand-100">
        {member.photo ? (
          <Image
            src={member.photo}
            alt={member.full_name}
            fill
            sizes="(min-width: 1024px) 25vw, (min-width: 640px) 50vw, 100vw"
            className="object-cover transition-transform duration-500 ease-[var(--ease-out-soft)] group-hover:scale-[1.04]"
          />
        ) : (
          <div className="flex h-full items-center justify-center bg-green-50 font-display text-4xl font-bold text-green-300">
            {member.full_name
              .split(" ")
              .slice(0, 2)
              .map((part) => part.charAt(0))
              .join("")}
          </div>
        )}
      </div>

      <div className="p-5">
        <h3 className="font-display text-base font-bold text-ink-950">
          {member.full_name}
        </h3>
        <p className="mt-1 text-sm font-medium text-green-700">{member.role}</p>
        {member.short_bio ? (
          <p className="mt-3 text-sm leading-relaxed text-sand-700">
            {member.short_bio}
          </p>
        ) : null}
      </div>
    </article>
  );
}

/* ------------------------------------------------------------------ */

export function FocusAreaCard({ area }: { area: { slug: string; title: string; summary: string } }) {
  return (
    <Link
      href={`/focus-areas/${area.slug}`}
      className="group flex h-full flex-col rounded-2xl border border-sand-200 bg-white p-7 transition-all duration-300 hover:-translate-y-1 hover:border-green-300 hover:shadow-xl hover:shadow-ink-950/5"
    >
      <h3 className="font-display text-xl font-bold text-ink-950">{area.title}</h3>
      <p className="mt-3 flex-1 text-[0.9375rem] leading-relaxed text-sand-700">
        {area.summary}
      </p>
      <span className="mt-6 inline-flex items-center gap-1.5 text-sm font-semibold text-green-700">
        Learn more
        <ArrowUpRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5" aria-hidden />
      </span>
    </Link>
  );
}
