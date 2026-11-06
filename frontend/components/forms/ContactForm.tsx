"use client";

import { Loader2, Send } from "lucide-react";
import { useState } from "react";

import { Field, FormStatus, Honeypot, TextArea, TextInput } from "@/components/forms/fields";
import { submitContact } from "@/lib/submit";

export function ContactForm() {
  const [state, setState] = useState<"idle" | "sending" | "done" | "error">("idle");
  const [message, setMessage] = useState("");
  const [errors, setErrors] = useState<Record<string, string[]>>({});

  async function handleSubmit(formEvent: React.FormEvent<HTMLFormElement>) {
    formEvent.preventDefault();
    setState("sending");
    setErrors({});
    setMessage("");

    const data = Object.fromEntries(new FormData(formEvent.currentTarget));
    const result = await submitContact(data);

    if (result.ok) {
      setState("done");
      formEvent.currentTarget.reset();
    } else {
      setState("error");
      setErrors(result.errors ?? {});
      setMessage(result.message ?? "Something went wrong.");
    }
  }

  if (state === "done") {
    return (
      <FormStatus
        state="done"
        successTitle="Message sent"
        successBody="Thank you for getting in touch. We read every message and will reply as soon as we can."
      />
    );
  }

  return (
    <form onSubmit={handleSubmit} className="relative space-y-5" noValidate>
      <Honeypot />

      <div className="grid gap-5 sm:grid-cols-2">
        <Field id="full_name" label="Your name" required error={errors.full_name?.[0]}>
          <TextInput id="full_name" required autoComplete="name" error={errors.full_name?.[0]} />
        </Field>
        <Field id="email" label="Email address" required error={errors.email?.[0]}>
          <TextInput id="email" type="email" required autoComplete="email" error={errors.email?.[0]} />
        </Field>
      </div>

      <div className="grid gap-5 sm:grid-cols-2">
        <Field id="phone" label="Phone" error={errors.phone?.[0]}>
          <TextInput id="phone" type="tel" autoComplete="tel" placeholder="+255 ..." error={errors.phone?.[0]} />
        </Field>
        <Field id="subject" label="Subject" error={errors.subject?.[0]}>
          <TextInput id="subject" error={errors.subject?.[0]} />
        </Field>
      </div>

      <Field id="message" label="Message" required error={errors.message?.[0]}>
        <TextArea id="message" required rows={6} error={errors.message?.[0]} />
      </Field>

      <FormStatus state={state} message={message} successTitle="" successBody="" />

      <button
        type="submit"
        disabled={state === "sending"}
        className="inline-flex items-center justify-center gap-2 rounded-full bg-green-600 px-7 py-3.5 font-semibold text-white transition-colors hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {state === "sending" ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin" aria-hidden />
            Sending
          </>
        ) : (
          <>
            <Send className="h-4 w-4" aria-hidden />
            Send message
          </>
        )}
      </button>
    </form>
  );
}
