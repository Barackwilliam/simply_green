"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { ChevronDown, Heart, Menu, X } from "lucide-react";
import { useEffect, useState } from "react";

import { NAV_ITEMS } from "@/lib/navigation";
import { cn } from "@/lib/utils";

export function SiteHeader({
  organisationName,
  logoUrl,
  donateEnabled,
}: {
  organisationName: string;
  logoUrl: string | null;
  donateEnabled: boolean;
}) {
  const pathname = usePathname();
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [openSection, setOpenSection] = useState<string | null>(null);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // Close the mobile drawer whenever the route changes.
  useEffect(() => {
    setMobileOpen(false);
    setOpenSection(null);
  }, [pathname]);

  // Stop the page scrolling behind the open drawer.
  useEffect(() => {
    document.body.style.overflow = mobileOpen ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [mobileOpen]);

  const isActive = (href: string) => {
    const base = href.split("?")[0].split("#")[0];
    if (base === "/") return pathname === "/";
    return pathname === base || pathname.startsWith(`${base}/`);
  };

  return (
    <>
      <a
        href="#main"
        className={cn(
          "sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[100]",
          "focus:rounded-full focus:bg-green-600 focus:px-5 focus:py-2.5",
          "focus:text-sm focus:font-semibold focus:text-white",
        )}
      >
        Skip to content
      </a>

      <header
        className={cn(
          "fixed inset-x-0 top-0 z-50 transition-all duration-300",
          scrolled || mobileOpen
            ? "bg-white/95 shadow-sm backdrop-blur-md"
            : "bg-transparent",
        )}
      >
        <div className="container-page">
          <div className="flex h-20 items-center justify-between gap-6">
            {/* Logo */}
            <Link
              href="/"
              className="flex shrink-0 items-center gap-3"
              aria-label={`${organisationName} — home`}
            >
              {logoUrl ? (
                <Image
                  src={logoUrl}
                  alt={organisationName}
                  width={180}
                  height={56}
                  priority
                  className="h-11 w-auto sm:h-12"
                />
              ) : (
                <span
                  className={cn(
                    "font-display text-lg font-bold leading-tight",
                    scrolled || mobileOpen ? "text-ink-950" : "text-white",
                  )}
                >
                  Simply Green
                </span>
              )}
            </Link>

            {/* Desktop navigation */}
            <nav
              className="hidden items-center gap-0.5 xl:flex"
              aria-label="Main"
            >
              {NAV_ITEMS.map((item) => (
                <div key={item.label} className="group relative">
                  <Link
                    href={item.href}
                    className={cn(
                      "flex items-center gap-1 whitespace-nowrap rounded-full px-3 py-2",
                      "text-[0.8125rem] font-semibold transition-colors",
                      scrolled
                        ? isActive(item.href)
                          ? "text-green-700"
                          : "text-ink-800 hover:text-green-700"
                        : isActive(item.href)
                          ? "text-green-300"
                          : "text-white/90 hover:text-white",
                    )}
                  >
                    {item.label}
                    {item.children ? (
                      <ChevronDown
                        className="h-3.5 w-3.5 transition-transform duration-200 group-hover:rotate-180"
                        aria-hidden
                      />
                    ) : null}
                  </Link>

                  {item.children ? (
                    <div
                      className={cn(
                        "invisible absolute left-0 top-full z-50 w-72 pt-3 opacity-0",
                        "transition-all duration-200 ease-[var(--ease-out-soft)]",
                        "group-hover:visible group-hover:opacity-100",
                        "group-focus-within:visible group-focus-within:opacity-100",
                      )}
                    >
                      <div className="overflow-hidden rounded-2xl border border-sand-200 bg-white p-2 shadow-xl shadow-ink-950/10">
                        {item.children.map((child) => (
                          <Link
                            key={child.href}
                            href={child.href}
                            className="block rounded-xl px-3.5 py-2.5 transition-colors hover:bg-green-50"
                          >
                            <span className="block text-sm font-semibold text-ink-900">
                              {child.label}
                            </span>
                            {child.description ? (
                              <span className="mt-0.5 block text-xs leading-snug text-sand-600">
                                {child.description}
                              </span>
                            ) : null}
                          </Link>
                        ))}
                      </div>
                    </div>
                  ) : null}
                </div>
              ))}
            </nav>

            {/* Actions */}
            <div className="flex items-center gap-3">
              {donateEnabled ? (
                <Link
                  href="/donate"
                  className={cn(
                    "hidden items-center gap-2 rounded-full px-5 py-2.5",
                    "text-sm font-semibold transition-all sm:inline-flex",
                    "bg-green-600 text-white hover:bg-green-700",
                    "hover:shadow-lg hover:shadow-green-600/25",
                  )}
                >
                  <Heart className="h-4 w-4" aria-hidden />
                  Donate
                </Link>
              ) : null}

              <button
                type="button"
                onClick={() => setMobileOpen((open) => !open)}
                aria-expanded={mobileOpen}
                aria-controls="mobile-nav"
                aria-label={mobileOpen ? "Close menu" : "Open menu"}
                className={cn(
                  "inline-flex h-11 w-11 items-center justify-center rounded-full",
                  "transition-colors xl:hidden",
                  scrolled || mobileOpen
                    ? "text-ink-950 hover:bg-sand-100"
                    : "text-white hover:bg-white/10",
                )}
              >
                {mobileOpen ? (
                  <X className="h-6 w-6" aria-hidden />
                ) : (
                  <Menu className="h-6 w-6" aria-hidden />
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile drawer */}
        <div
          id="mobile-nav"
          hidden={!mobileOpen}
          className={cn(
            "xl:hidden",
            "max-h-[calc(100dvh-5rem)] overflow-y-auto overscroll-contain",
            "border-t border-sand-200 bg-white",
          )}
        >
          <nav className="container-page py-4" aria-label="Mobile">
            <ul className="divide-y divide-sand-100">
              {NAV_ITEMS.map((item) => {
                const expanded = openSection === item.label;
                return (
                  <li key={item.label} className="py-1">
                    <div className="flex items-center">
                      <Link
                        href={item.href}
                        className={cn(
                          "flex-1 py-3 font-display text-base font-semibold",
                          isActive(item.href) ? "text-green-700" : "text-ink-900",
                        )}
                      >
                        {item.label}
                      </Link>
                      {item.children ? (
                        <button
                          type="button"
                          onClick={() =>
                            setOpenSection(expanded ? null : item.label)
                          }
                          aria-expanded={expanded}
                          aria-label={`${expanded ? "Hide" : "Show"} ${item.label} links`}
                          className="inline-flex h-10 w-10 items-center justify-center rounded-full text-sand-600 hover:bg-sand-100"
                        >
                          <ChevronDown
                            className={cn(
                              "h-4 w-4 transition-transform duration-200",
                              expanded && "rotate-180",
                            )}
                            aria-hidden
                          />
                        </button>
                      ) : null}
                    </div>

                    {item.children && expanded ? (
                      <ul className="mb-2 ml-3 space-y-0.5 border-l-2 border-green-100 pl-4">
                        {item.children.map((child) => (
                          <li key={child.href}>
                            <Link
                              href={child.href}
                              className="block py-2 text-sm text-sand-700 hover:text-green-700"
                            >
                              {child.label}
                            </Link>
                          </li>
                        ))}
                      </ul>
                    ) : null}
                  </li>
                );
              })}
            </ul>

            {donateEnabled ? (
              <Link
                href="/donate"
                className="mt-5 mb-2 flex w-full items-center justify-center gap-2 rounded-full bg-green-600 px-6 py-3.5 font-semibold text-white sm:hidden"
              >
                <Heart className="h-4 w-4" aria-hidden />
                Donate
              </Link>
            ) : null}
          </nav>
        </div>
      </header>
    </>
  );
}
