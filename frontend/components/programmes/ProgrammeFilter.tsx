"use client";

import { useMemo, useState } from "react";

import { ProgrammeCard } from "@/components/cards";
import type { Programme } from "@/lib/types";
import { cn } from "@/lib/utils";

/**
 * Filtering happens in the browser over an already-prerendered list.
 *
 * Reading the filter from the URL would make this page dynamic and cost us
 * the static shell; the programme list is small enough that filtering client
 * side is both faster for the visitor and better for indexing.
 */
export function ProgrammeFilter({
  programmes,
  focusAreas,
}: {
  programmes: Programme[];
  focusAreas: { slug: string; title: string }[];
}) {
  const [status, setStatus] = useState<string>("all");
  const [area, setArea] = useState<string>("all");

  const statuses = useMemo(() => {
    const seen = new Map<string, string>();
    for (const programme of programmes) {
      seen.set(programme.status, programme.status_label);
    }
    return [...seen.entries()];
  }, [programmes]);

  const visible = programmes.filter((programme) => {
    if (status !== "all" && programme.status !== status) return false;
    if (
      area !== "all" &&
      !programme.focus_areas.some((focus) => focus.slug === area)
    ) {
      return false;
    }
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
            Status
          </legend>
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => setStatus("all")}
              className={chip(status === "all")}
              aria-pressed={status === "all"}
            >
              All
            </button>
            {statuses.map(([value, label]) => (
              <button
                key={value}
                type="button"
                onClick={() => setStatus(value)}
                className={chip(status === value)}
                aria-pressed={status === value}
              >
                {label}
              </button>
            ))}
          </div>
        </fieldset>

        {focusAreas.length > 0 ? (
          <fieldset>
            <legend className="mb-2.5 text-xs font-semibold uppercase tracking-wider text-sand-500">
              Focus area
            </legend>
            <div className="flex flex-wrap gap-2">
              <button
                type="button"
                onClick={() => setArea("all")}
                className={chip(area === "all")}
                aria-pressed={area === "all"}
              >
                All
              </button>
              {focusAreas.map((focus) => (
                <button
                  key={focus.slug}
                  type="button"
                  onClick={() => setArea(focus.slug)}
                  className={chip(area === focus.slug)}
                  aria-pressed={area === focus.slug}
                >
                  {focus.title}
                </button>
              ))}
            </div>
          </fieldset>
        ) : null}
      </div>

      <p className="mt-8 text-sm text-sand-600" role="status">
        Showing {visible.length} of {programmes.length} programmes
      </p>

      {visible.length === 0 ? (
        <p className="mt-10 rounded-2xl border border-dashed border-sand-300 bg-sand-50 px-6 py-14 text-center text-sand-600">
          No programmes match these filters.
        </p>
      ) : (
        <ul className="mt-6 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {visible.map((programme) => (
            <li key={programme.id}>
              <ProgrammeCard programme={programme} />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
