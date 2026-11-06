"use client";

import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

const CONTROL = cn(
  "w-full rounded-xl border border-sand-300 bg-white px-4 py-3",
  "text-[0.9375rem] text-ink-950 placeholder:text-sand-400",
  "outline-none transition-colors",
  "focus:border-green-500 focus:ring-4 focus:ring-green-500/10",
  "disabled:cursor-not-allowed disabled:bg-sand-50",
  "aria-[invalid=true]:border-red-400 aria-[invalid=true]:focus:ring-red-500/10",
);

export function Field({
  id,
  label,
  error,
  hint,
  required,
  children,
  className,
}: {
  id: string;
  label: string;
  error?: string;
  hint?: string;
  required?: boolean;
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={className}>
      <label
        htmlFor={id}
        className="mb-1.5 block text-sm font-semibold text-ink-900"
      >
        {label}
        {required ? (
          <span className="ml-1 text-red-600" aria-hidden>
            *
          </span>
        ) : (
          <span className="ml-1.5 text-xs font-normal text-sand-500">
            (optional)
          </span>
        )}
      </label>
      {children}
      {hint && !error ? (
        <p id={`${id}-hint`} className="mt-1.5 text-xs text-sand-500">
          {hint}
        </p>
      ) : null}
      {error ? (
        <p id={`${id}-error`} className="mt-1.5 text-xs font-medium text-red-700">
          {error}
        </p>
      ) : null}
    </div>
  );
}

export function TextInput({
  id,
  error,
  hint,
  ...props
}: React.ComponentProps<"input"> & { id: string; error?: string; hint?: string }) {
  return (
    <input
      id={id}
      name={props.name ?? id}
      aria-invalid={error ? true : undefined}
      aria-describedby={error ? `${id}-error` : hint ? `${id}-hint` : undefined}
      className={CONTROL}
      {...props}
    />
  );
}

export function TextArea({
  id,
  error,
  hint,
  rows = 5,
  ...props
}: React.ComponentProps<"textarea"> & {
  id: string;
  error?: string;
  hint?: string;
}) {
  return (
    <textarea
      id={id}
      name={props.name ?? id}
      rows={rows}
      aria-invalid={error ? true : undefined}
      aria-describedby={error ? `${id}-error` : hint ? `${id}-hint` : undefined}
      className={cn(CONTROL, "resize-y")}
      {...props}
    />
  );
}

export function Select({
  id,
  error,
  children,
  ...props
}: React.ComponentProps<"select"> & { id: string; error?: string }) {
  return (
    <select
      id={id}
      name={props.name ?? id}
      aria-invalid={error ? true : undefined}
      aria-describedby={error ? `${id}-error` : undefined}
      className={CONTROL}
      {...props}
    >
      {children}
    </select>
  );
}

/**
 * A field real visitors never see and never fill.
 *
 * Hidden from sight and from screen readers, and skipped by tabbing, so only
 * an automated form-filler puts anything in it. The backend rejects any
 * submission where it is non-empty.
 */
export function Honeypot() {
  return (
    <div aria-hidden className="absolute left-[-9999px] h-px w-px overflow-hidden">
      <label htmlFor="website_url">Leave this field empty</label>
      <input
        id="website_url"
        name="website_url"
        type="text"
        tabIndex={-1}
        autoComplete="off"
      />
    </div>
  );
}

export function FormStatus({
  state,
  message,
  successTitle,
  successBody,
}: {
  state: "idle" | "sending" | "done" | "error";
  message?: string;
  successTitle: string;
  successBody: string;
}) {
  if (state === "done") {
    return (
      <div
        role="status"
        className="rounded-2xl border border-green-200 bg-green-50 p-6 text-center"
      >
        <p className="font-display text-lg font-bold text-green-900">
          {successTitle}
        </p>
        <p className="mt-2 text-sm text-green-800">{successBody}</p>
      </div>
    );
  }

  if (state === "error" && message) {
    return (
      <p
        role="alert"
        className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-800"
      >
        {message}
      </p>
    );
  }

  return null;
}
