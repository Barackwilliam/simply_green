"use client";

import { Check, Loader2 } from "lucide-react";
import { useState } from "react";

import { submitNewsletter } from "@/lib/submit";
import { cn } from "@/lib/utils";

export function NewsletterForm({
  source = "footer",
  tone = "light",
}: {
  source?: string;
  tone?: "light" | "dark";
}) {
  const [email, setEmail] = useState("");
  const [state, setState] = useState<"idle" | "sending" | "done" | "error">(
    "idle",
  );
  const [message, setMessage] = useState("");

  async function handleSubmit(formEvent: React.FormEvent<HTMLFormElement>) {
    formEvent.preventDefault();
    setState("sending");
    setMessage("");

    const result = await submitNewsletter({ email, source });

    if (result.ok) {
      setState("done");
      setEmail("");
    } else {
      setState("error");
      setMessage(
        result.errors?.email?.[0] ??
          result.message ??
          "Something went wrong. Please try again.",
      );
    }
  }

  if (state === "done") {
    return (
      <p
        className={cn(
          "flex items-center gap-2 rounded-xl px-4 py-3 text-sm font-medium",
          tone === "dark"
            ? "bg-green-500/15 text-green-200"
            : "bg-green-50 text-green-800",
        )}
        role="status"
      >
        <Check className="h-4 w-4 shrink-0" aria-hidden />
        Thank you — you are on the list.
      </p>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="flex flex-col gap-2.5 sm:flex-row">
        <label htmlFor={`newsletter-${source}`} className="sr-only">
          Email address
        </label>
        <input
          id={`newsletter-${source}`}
          type="email"
          required
          value={email}
          onChange={(changeEvent) => setEmail(changeEvent.target.value)}
          placeholder="your.name@example.com"
          autoComplete="email"
          className={cn(
            "min-w-0 flex-1 rounded-full px-5 py-3 text-sm outline-none transition-colors",
            tone === "dark"
              ? "border border-white/20 bg-white/10 text-white placeholder:text-white/50 focus:border-green-400"
              : "border border-sand-300 bg-white text-ink-950 placeholder:text-sand-500 focus:border-green-500",
          )}
        />
        <button
          type="submit"
          disabled={state === "sending"}
          className={cn(
            "inline-flex shrink-0 items-center justify-center gap-2 rounded-full",
            "px-6 py-3 text-sm font-semibold transition-colors",
            "disabled:cursor-not-allowed disabled:opacity-60",
            "bg-green-600 text-white hover:bg-green-700",
          )}
        >
          {state === "sending" ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" aria-hidden />
              Subscribing
            </>
          ) : (
            "Subscribe"
          )}
        </button>
      </div>

      {state === "error" && message ? (
        <p
          className={cn(
            "mt-2.5 text-sm",
            tone === "dark" ? "text-gold-300" : "text-red-700",
          )}
          role="alert"
        >
          {message}
        </p>
      ) : null}
    </form>
  );
}
