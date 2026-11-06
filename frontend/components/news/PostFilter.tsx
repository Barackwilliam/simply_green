"use client";

import { useMemo, useState } from "react";

import { PostCard } from "@/components/cards";
import type { Category, Post } from "@/lib/types";
import { cn } from "@/lib/utils";

export function PostFilter({
  posts,
  categories,
}: {
  posts: Post[];
  categories: Category[];
}) {
  const [kind, setKind] = useState("all");
  const [category, setCategory] = useState("all");

  const kinds = useMemo(() => {
    const seen = new Map<string, string>();
    for (const post of posts) seen.set(post.kind, post.kind_label);
    return [...seen.entries()];
  }, [posts]);

  const visible = posts.filter((post) => {
    if (kind !== "all" && post.kind !== kind) return false;
    if (category !== "all" && post.category?.slug !== category) return false;
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
            Type
          </legend>
          <div className="flex flex-wrap gap-2">
            <button type="button" onClick={() => setKind("all")} className={chip(kind === "all")} aria-pressed={kind === "all"}>
              All
            </button>
            {kinds.map(([value, label]) => (
              <button
                key={value}
                type="button"
                onClick={() => setKind(value)}
                className={chip(kind === value)}
                aria-pressed={kind === value}
              >
                {label}
              </button>
            ))}
          </div>
        </fieldset>

        {categories.length > 0 ? (
          <fieldset>
            <legend className="mb-2.5 text-xs font-semibold uppercase tracking-wider text-sand-500">
              Topic
            </legend>
            <div className="flex flex-wrap gap-2">
              <button type="button" onClick={() => setCategory("all")} className={chip(category === "all")} aria-pressed={category === "all"}>
                All
              </button>
              {categories.map((item) => (
                <button
                  key={item.slug}
                  type="button"
                  onClick={() => setCategory(item.slug)}
                  className={chip(category === item.slug)}
                  aria-pressed={category === item.slug}
                >
                  {item.name}
                </button>
              ))}
            </div>
          </fieldset>
        ) : null}
      </div>

      <p className="mt-8 text-sm text-sand-600" role="status">
        Showing {visible.length} of {posts.length} articles
      </p>

      {visible.length === 0 ? (
        <p className="mt-10 rounded-2xl border border-dashed border-sand-300 bg-sand-50 px-6 py-14 text-center text-sand-600">
          Nothing matches these filters.
        </p>
      ) : (
        <ul className="mt-6 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {visible.map((post) => (
            <li key={post.id}>
              <PostCard post={post} />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
