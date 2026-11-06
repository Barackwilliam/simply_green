"use client";

import { Loader2 } from "lucide-react";
import { useState } from "react";

import { Field, FormStatus, Honeypot, TextArea, TextInput } from "@/components/forms/fields";
import { submitEventRegistration } from "@/lib/submit";

export function EventRegistrationForm({ eventId }: { eventId: number }) {
  const [state, setState] = useState<"idle" | "sending" | "done" | "error">("idle");
  const [message, setMessage] = useState("");
  const [errors, setErrors] = useState<Record<string, string[]>>({});

  async function handleSubmit(formEvent: React.FormEvent<HTMLFormElement>) {
    formEvent.preventDefault();
    setState("sending");
    setErrors({});

    const data = Object.fromEntries(new FormData(formEvent.currentTarget));
    const result = await submitEventRegistration({ ...data, event: eventId });

    if (result.ok) {
      setState("done");
    } else {
      setState("error");
      setErrors(result.errors ?? {});
      setMessage(
        result.errors?.non_field_errors?.[0] ??
          result.message ??
          "Registration failed.",
      );
    }
  }

  if (state === "done") {
    return (
      <FormStatus
        state="done"
        successTitle="You are registered"
        successBody="We have your details and will be in touch with the final arrangements."
      />
    );
  }

  return (
    <form onSubmit={handleSubmit} className="relative space-y-4" noValidate>
      <Honeypot />

      <Field id="full_name" label="Full name" required error={errors.full_name?.[0]}>
        <TextInput id="full_name" required autoComplete="name" error={errors.full_name?.[0]} />
      </Field>

      <Field id="email" label="Email" required error={errors.email?.[0]}>
        <TextInput id="email" type="email" required autoComplete="email" error={errors.email?.[0]} />
      </Field>

      <Field id="phone" label="Phone" error={errors.phone?.[0]}>
        <TextInput id="phone" type="tel" autoComplete="tel" error={errors.phone?.[0]} />
      </Field>

      <Field id="organisation" label="Organisation" error={errors.organisation?.[0]}>
        <TextInput id="organisation" error={errors.organisation?.[0]} />
      </Field>

      <Field id="notes" label="Anything we should know" error={errors.notes?.[0]}>
        <TextArea id="notes" rows={3} error={errors.notes?.[0]} />
      </Field>

      <FormStatus state={state} message={message} successTitle="" successBody="" />

      <button
        type="submit"
        disabled={state === "sending"}
        className="inline-flex w-full items-center justify-center gap-2 rounded-full bg-green-600 px-6 py-3.5 font-semibold text-white transition-colors hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {state === "sending" ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin" aria-hidden />
            Registering
          </>
        ) : (
          "Register"
        )}
      </button>
    </form>
  );
}
