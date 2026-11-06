"use client";

import { Loader2 } from "lucide-react";
import { useState } from "react";

import { Field, FormStatus, Honeypot, TextArea, TextInput } from "@/components/forms/fields";
import { submitVolunteer } from "@/lib/submit";

export function VolunteerForm({ focusAreas }: { focusAreas: string[] }) {
  const [state, setState] = useState<"idle" | "sending" | "done" | "error">("idle");
  const [message, setMessage] = useState("");
  const [errors, setErrors] = useState<Record<string, string[]>>({});

  async function handleSubmit(formEvent: React.FormEvent<HTMLFormElement>) {
    formEvent.preventDefault();
    setState("sending");
    setErrors({});

    // FormData keeps the CV upload intact.
    const result = await submitVolunteer(new FormData(formEvent.currentTarget));

    if (result.ok) {
      setState("done");
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
        successTitle="Application received"
        successBody="Thank you for offering your time. We will review your application and contact you about what is coming up."
      />
    );
  }

  return (
    <form onSubmit={handleSubmit} className="relative space-y-5" noValidate>
      <Honeypot />

      <div className="grid gap-5 sm:grid-cols-2">
        <Field id="full_name" label="Full name" required error={errors.full_name?.[0]}>
          <TextInput id="full_name" required autoComplete="name" error={errors.full_name?.[0]} />
        </Field>
        <Field id="email" label="Email" required error={errors.email?.[0]}>
          <TextInput id="email" type="email" required autoComplete="email" error={errors.email?.[0]} />
        </Field>
      </div>

      <div className="grid gap-5 sm:grid-cols-2">
        <Field id="phone" label="Phone" required error={errors.phone?.[0]}>
          <TextInput id="phone" type="tel" required autoComplete="tel" placeholder="+255 ..." error={errors.phone?.[0]} />
        </Field>
        <Field id="location" label="Where you are based" error={errors.location?.[0]}>
          <TextInput id="location" placeholder="e.g. Temeke, Dar es Salaam" error={errors.location?.[0]} />
        </Field>
      </div>

      <div className="grid gap-5 sm:grid-cols-2">
        <Field id="occupation" label="Occupation or studies" error={errors.occupation?.[0]}>
          <TextInput id="occupation" error={errors.occupation?.[0]} />
        </Field>
        <Field
          id="availability"
          label="Availability"
          hint="e.g. weekends, two days a week"
          error={errors.availability?.[0]}
        >
          <TextInput id="availability" error={errors.availability?.[0]} />
        </Field>
      </div>

      <Field
        id="areas_of_interest"
        label="What you would like to work on"
        hint={focusAreas.length ? `Our focus areas: ${focusAreas.join(", ")}` : undefined}
        error={errors.areas_of_interest?.[0]}
      >
        <TextArea id="areas_of_interest" rows={3} error={errors.areas_of_interest?.[0]} />
      </Field>

      <Field id="skills" label="Skills you bring" error={errors.skills?.[0]}>
        <TextArea id="skills" rows={3} error={errors.skills?.[0]} />
      </Field>

      <Field id="motivation" label="Why you want to volunteer" error={errors.motivation?.[0]}>
        <TextArea id="motivation" rows={4} error={errors.motivation?.[0]} />
      </Field>

      <Field
        id="cv"
        label="CV"
        hint="PDF or Word document, if you have one ready"
        error={errors.cv?.[0]}
      >
        <input
          id="cv"
          name="cv"
          type="file"
          accept=".pdf,.doc,.docx"
          className="w-full rounded-xl border border-sand-300 bg-white px-4 py-3 text-sm text-sand-700 file:mr-4 file:rounded-full file:border-0 file:bg-green-50 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-green-700 hover:file:bg-green-100"
        />
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
          "Submit application"
        )}
      </button>
    </form>
  );
}
