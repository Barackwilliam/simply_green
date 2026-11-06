"use client";

import { Loader2 } from "lucide-react";
import { useState } from "react";

import { Field, FormStatus, Honeypot, Select, TextArea, TextInput } from "@/components/forms/fields";
import { submitPartnerEnquiry } from "@/lib/submit";

const PARTNERSHIP_TYPES = [
  "Funding or grant",
  "Technical support",
  "Joint implementation",
  "Corporate social responsibility",
  "Research collaboration",
  "In-kind support",
  "Something else",
];

export function PartnerForm() {
  const [state, setState] = useState<"idle" | "sending" | "done" | "error">("idle");
  const [message, setMessage] = useState("");
  const [errors, setErrors] = useState<Record<string, string[]>>({});

  async function handleSubmit(formEvent: React.FormEvent<HTMLFormElement>) {
    formEvent.preventDefault();
    setState("sending");
    setErrors({});

    const data = Object.fromEntries(new FormData(formEvent.currentTarget));
    const result = await submitPartnerEnquiry(data);

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
        successTitle="Enquiry received"
        successBody="Thank you. Our team will review your proposal and come back to you directly."
      />
    );
  }

  return (
    <form onSubmit={handleSubmit} className="relative space-y-5" noValidate>
      <Honeypot />

      <div className="grid gap-5 sm:grid-cols-2">
        <Field id="organisation_name" label="Organisation" required error={errors.organisation_name?.[0]}>
          <TextInput id="organisation_name" required autoComplete="organization" error={errors.organisation_name?.[0]} />
        </Field>
        <Field id="contact_person" label="Contact person" required error={errors.contact_person?.[0]}>
          <TextInput id="contact_person" required autoComplete="name" error={errors.contact_person?.[0]} />
        </Field>
      </div>

      <div className="grid gap-5 sm:grid-cols-2">
        <Field id="email" label="Email" required error={errors.email?.[0]}>
          <TextInput id="email" type="email" required autoComplete="email" error={errors.email?.[0]} />
        </Field>
        <Field id="phone" label="Phone" error={errors.phone?.[0]}>
          <TextInput id="phone" type="tel" autoComplete="tel" error={errors.phone?.[0]} />
        </Field>
      </div>

      <div className="grid gap-5 sm:grid-cols-2">
        <Field id="website" label="Website" error={errors.website?.[0]}>
          <TextInput id="website" type="url" placeholder="https://" error={errors.website?.[0]} />
        </Field>
        <Field id="country" label="Country" error={errors.country?.[0]}>
          <TextInput id="country" autoComplete="country-name" error={errors.country?.[0]} />
        </Field>
      </div>

      <Field id="partnership_type" label="Type of partnership" error={errors.partnership_type?.[0]}>
        <Select id="partnership_type" defaultValue="" error={errors.partnership_type?.[0]}>
          <option value="">Please choose…</option>
          {PARTNERSHIP_TYPES.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </Select>
      </Field>

      <Field id="message" label="Tell us what you have in mind" required error={errors.message?.[0]}>
        <TextArea id="message" required rows={6} error={errors.message?.[0]} />
      </Field>

      <FormStatus state={state} message={message} successTitle="" successBody="" />

      <button
        type="submit"
        disabled={state === "sending"}
        className="inline-flex items-center justify-center gap-2 rounded-full bg-sky-600 px-7 py-3.5 font-semibold text-white transition-colors hover:bg-sky-700 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {state === "sending" ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin" aria-hidden />
            Sending
          </>
        ) : (
          "Send enquiry"
        )}
      </button>
    </form>
  );
}
