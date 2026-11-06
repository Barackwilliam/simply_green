import Link from "next/link";
import type { ComponentProps, ReactNode } from "react";

import { cn } from "@/lib/utils";

/* ------------------------------------------------------------------ */
/* Layout primitives                                                   */
/* ------------------------------------------------------------------ */

export function Container({
  className,
  children,
}: {
  className?: string;
  children: ReactNode;
}) {
  return <div className={cn("container-page", className)}>{children}</div>;
}

export function Section({
  className,
  children,
  tone = "default",
  id,
}: {
  className?: string;
  children: ReactNode;
  tone?: "default" | "muted" | "dark" | "green";
  id?: string;
}) {
  const tones = {
    default: "bg-white",
    muted: "bg-sand-50",
    dark: "bg-forest-wash text-white",
    green: "bg-green-600 text-white",
  } as const;

  return (
    <section
      id={id}
      className={cn("py-16 sm:py-20 lg:py-24", tones[tone], className)}
    >
      {children}
    </section>
  );
}

/* ------------------------------------------------------------------ */
/* Headings                                                            */
/* ------------------------------------------------------------------ */

export function Eyebrow({
  children,
  tone = "green",
  className,
}: {
  children: ReactNode;
  tone?: "green" | "sky" | "light";
  className?: string;
}) {
  const tones = {
    green: "text-green-700 before:bg-green-500",
    sky: "text-sky-700 before:bg-sky-500",
    light: "text-green-200 before:bg-green-400",
  } as const;

  return (
    <p
      className={cn(
        "mb-4 inline-flex items-center gap-2.5 text-xs font-semibold",
        "uppercase tracking-[0.16em]",
        "before:block before:h-px before:w-8 before:content-['']",
        tones[tone],
        className,
      )}
    >
      {children}
    </p>
  );
}

export function SectionHeading({
  eyebrow,
  title,
  description,
  align = "left",
  tone = "dark",
  className,
}: {
  eyebrow?: string;
  title: ReactNode;
  description?: ReactNode;
  align?: "left" | "center";
  tone?: "dark" | "light";
  className?: string;
}) {
  return (
    <div
      className={cn(
        "max-w-3xl",
        align === "center" && "mx-auto text-center",
        className,
      )}
    >
      {eyebrow ? (
        <Eyebrow tone={tone === "light" ? "light" : "green"}>{eyebrow}</Eyebrow>
      ) : null}
      <h2
        className={cn(
          "text-3xl sm:text-4xl lg:text-[2.75rem] lg:leading-[1.1]",
          tone === "light" ? "text-white" : "text-ink-950",
        )}
      >
        {title}
      </h2>
      {description ? (
        <p
          className={cn(
            "mt-5 text-lg leading-relaxed",
            tone === "light" ? "text-ink-100" : "text-sand-700",
          )}
        >
          {description}
        </p>
      ) : null}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Button                                                              */
/* ------------------------------------------------------------------ */

const buttonBase = cn(
  "inline-flex items-center justify-center gap-2 rounded-full",
  "font-semibold transition-all duration-200",
  "disabled:cursor-not-allowed disabled:opacity-60",
);

const buttonVariants = {
  primary: "bg-green-600 text-white hover:bg-green-700 hover:shadow-lg hover:shadow-green-600/25",
  sky: "bg-sky-600 text-white hover:bg-sky-700 hover:shadow-lg hover:shadow-sky-600/25",
  outline: "border-2 border-ink-950/15 text-ink-950 hover:border-green-600 hover:text-green-700",
  light: "bg-white text-ink-950 hover:bg-green-50",
  ghostLight: "border-2 border-white/30 text-white hover:border-white hover:bg-white/10",
} as const;

const buttonSizes = {
  sm: "px-4 py-2 text-sm",
  md: "px-6 py-3 text-[0.9375rem]",
  lg: "px-8 py-4 text-base",
} as const;

export type ButtonVariant = keyof typeof buttonVariants;

export function Button({
  variant = "primary",
  size = "md",
  className,
  ...props
}: ComponentProps<"button"> & {
  variant?: ButtonVariant;
  size?: keyof typeof buttonSizes;
}) {
  return (
    <button
      className={cn(
        buttonBase,
        buttonVariants[variant],
        buttonSizes[size],
        className,
      )}
      {...props}
    />
  );
}

export function ButtonLink({
  variant = "primary",
  size = "md",
  className,
  ...props
}: ComponentProps<typeof Link> & {
  variant?: ButtonVariant;
  size?: keyof typeof buttonSizes;
}) {
  return (
    <Link
      className={cn(
        buttonBase,
        buttonVariants[variant],
        buttonSizes[size],
        className,
      )}
      {...props}
    />
  );
}

/* ------------------------------------------------------------------ */
/* Badge                                                               */
/* ------------------------------------------------------------------ */

export function Badge({
  children,
  tone = "green",
  className,
}: {
  children: ReactNode;
  tone?: "green" | "sky" | "gold" | "neutral" | "light";
  className?: string;
}) {
  const tones = {
    green: "bg-green-100 text-green-800",
    sky: "bg-sky-100 text-sky-800",
    gold: "bg-gold-100 text-gold-800",
    neutral: "bg-sand-100 text-sand-800",
    light: "bg-white/15 text-white backdrop-blur-sm",
  } as const;

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-3 py-1",
        "text-xs font-semibold tracking-wide",
        tones[tone],
        className,
      )}
    >
      {children}
    </span>
  );
}

/* ------------------------------------------------------------------ */
/* Card                                                                */
/* ------------------------------------------------------------------ */

export function Card({
  className,
  children,
  as: Tag = "div",
}: {
  className?: string;
  children: ReactNode;
  as?: "div" | "article" | "li";
}) {
  return (
    <Tag
      className={cn(
        "group relative flex flex-col overflow-hidden rounded-2xl",
        "border border-sand-200 bg-white",
        "transition-all duration-300 ease-[var(--ease-out-soft)]",
        "hover:-translate-y-1 hover:border-green-300 hover:shadow-xl hover:shadow-ink-950/5",
        className,
      )}
    >
      {children}
    </Tag>
  );
}

/* ------------------------------------------------------------------ */
/* Empty state                                                         */
/* ------------------------------------------------------------------ */

export function EmptyState({
  title,
  description,
  icon,
}: {
  title: string;
  description?: string;
  icon?: ReactNode;
}) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center rounded-2xl",
        "border border-dashed border-sand-300 bg-sand-50",
        "px-6 py-16 text-center",
      )}
    >
      {icon ? <div className="mb-4 text-sand-400">{icon}</div> : null}
      <p className="font-display text-lg font-semibold text-ink-900">{title}</p>
      {description ? (
        <p className="mt-2 max-w-md text-sm text-sand-600">{description}</p>
      ) : null}
    </div>
  );
}

/* ------------------------------------------------------------------ */
/* Page header, used at the top of inner pages                         */
/* ------------------------------------------------------------------ */

export function PageHeader({
  eyebrow,
  title,
  description,
  children,
}: {
  eyebrow?: string;
  title: string;
  description?: string;
  children?: ReactNode;
}) {
  return (
    <header className="bg-forest-wash pt-32 pb-16 text-white sm:pt-36 sm:pb-20">
      <Container>
        <div className="max-w-3xl">
          {eyebrow ? <Eyebrow tone="light">{eyebrow}</Eyebrow> : null}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl lg:leading-[1.05]">
            {title}
          </h1>
          {description ? (
            <p className="mt-6 text-lg leading-relaxed text-ink-100">
              {description}
            </p>
          ) : null}
          {children ? <div className="mt-8">{children}</div> : null}
        </div>
      </Container>
    </header>
  );
}
