"use client";

import { useMemo, useState } from "react";

import { PublicationCard } from "@/components/cards";
import type { Publication } from "@/lib/types";
import { cn } from "@/lib/utils";

export function PublicationFilter({
  publications,
}: {
  publications: Publication[];
}) {
  const [kind, setKind] = useState("all");
  const [year, setYear] = useState("all");

  const kinds = useMemo(() => {
    const seen = new Map<string, string>();
    for (const item of publications) seen.set(item.kind, item.kind_label);
    return [...seen.entries()];
  }, [publications]);

  const years = useMemo(() => {
    const seen = new Set<number>();
    for (const item of publications) if (item.year) seen.add(item.year);
    return [...seen].sort((a, b) => b - a);
  }, [publications]);

  const visible = publications.filter((item) => {
    if (kind !== "all" && item.kind !== kind) return false;
    if (year !== "all" && String(item.year) !== year) return false;
    return true;
  });

  const chip = (active: boolean) =>
    cn(
      "rounded-full px-4 py-2 text-sm font-semibold transition-colors",
      active
        ? "bg-green-600 text-white"
        : "bg-sand-100 text-sand-700 hover:bg-sand-200",
    );

  return (
    <div>
      <div className="space-y-4">
        <fieldset>
          <legend className="mb-2.5 text-xs font-semibold uppercase tracking-wider text-sand-500">
            Document type
          </legend>
          <div className="flex flex-wrap gap-2">
            <button type="button" onClick={() => setKind("all")} className={chip(kind === "all")} aria-pressed={kind === "all"}>
              All
            </button>
            {kinds.map(([value, label]) => (
              <button key={value} type="button" onClick={() => setKind(value)} className={chip(kind === value)} aria-pressed={kind === value}>
                {label}
              </button>
            ))}
          </div>
        </fieldset>

        {years.length > 0 ? (
          <fieldset>
            <legend className="mb-2.5 text-xs font-semibold uppercase tracking-wider text-sand-500">
              Year
            </legend>
            <div className="flex flex-wrap gap-2">
              <button type="button" onClick={() => setYear("all")} className={chip(year === "all")} aria-pressed={year === "all"}>
                All
              </button>
              {years.map((value) => (
                <button key={value} type="button" onClick={() => setYear(String(value))} className={chip(year === String(value))} aria-pressed={year === String(value)}>
                  {value}
                </button>
              ))}
            </div>
          </fieldset>
        ) : null}
      </div>

      <p className="mt-8 text-sm text-sand-600" role="status">
        Showing {visible.length} of {publications.length} documents
      </p>

      {visible.length === 0 ? (
        <p className="mt-10 rounded-2xl border border-dashed border-sand-300 bg-sand-50 px-6 py-14 text-center text-sand-600">
          No documents match these filters.
        </p>
      ) : (
        <ul className="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {visible.map((publication) => (
            <li key={publication.id}>
              <PublicationCard publication={publication} />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
