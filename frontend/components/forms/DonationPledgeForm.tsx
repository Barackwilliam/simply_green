"use client";

import { Loader2 } from "lucide-react";
import { useState } from "react";

import { Field, FormStatus, Honeypot, Select, TextArea, TextInput } from "@/components/forms/fields";
import { submitDonationPledge } from "@/lib/submit";
import type { DonationMethod } from "@/lib/types";

/**
 * Records a donor's intention to give.
 *
 * This form never asks for card numbers, PINs or mobile money credentials.
 * The donor pays through their own bank or mobile money app using the
 * published details; this just tells the organisation to expect it, so they
 * can acknowledge and receipt the gift.
 */
export function DonationPledgeForm({
  methods,
  designations,
}: {
  methods: DonationMethod[];
  designations: string[];
}) {
  const [state, setState] = useState<"idle" | "sending" | "done" | "error">("idle");
  const [message, setMessage] = useState("");
  const [errors, setErrors] = useState<Record<string, string[]>>({});

  async function handleSubmit(formEvent: React.FormEvent<HTMLFormElement>) {
    formEvent.preventDefault();
    setState("sending");
    setErrors({});

    const raw = Object.fromEntries(new FormData(formEvent.currentTarget));
    const payload: Record<string, unknown> = {
      ...raw,
      is_anonymous: raw.is_anonymous === "on",
    };
    if (!payload.amount) delete payload.amount;
    if (!payload.method) delete payload.method;

    const result = await submitDonationPledge(payload);

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
        successTitle="Thank you"
        successBody="We have recorded your pledge. Once your transfer arrives we will confirm it and send an acknowledgement."
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
        <Field id="email" label="Email" required error={errors.email?.[0]}>
          <TextInput id="email" type="email" required autoComplete="email" error={errors.email?.[0]} />
        </Field>
      </div>

      <div className="grid gap-5 sm:grid-cols-2">
        <Field id="phone" label="Phone" error={errors.phone?.[0]}>
          <TextInput id="phone" type="tel" autoComplete="tel" error={errors.phone?.[0]} />
        </Field>
        <Field id="organisation" label="Organisation" error={errors.organisation?.[0]}>
          <TextInput id="organisation" error={errors.organisation?.[0]} />
        </Field>
      </div>

      <div className="grid gap-5 sm:grid-cols-2">
        <Field id="amount" label="Amount" hint="Leave blank if you prefer not to say" error={errors.amount?.[0]}>
          <TextInput id="amount" type="number" min="0" step="0.01" inputMode="decimal" error={errors.amount?.[0]} />
        </Field>
        <Field id="currency" label="Currency" error={errors.currency?.[0]}>
          <Select id="currency" defaultValue="TZS" error={errors.currency?.[0]}>
            <option value="TZS">TZS — Tanzanian Shilling</option>
            <option value="USD">USD — US Dollar</option>
            <option value="EUR">EUR — Euro</option>
            <option value="GBP">GBP — Pound Sterling</option>
          </Select>
        </Field>
      </div>

      {methods.length > 0 ? (
        <Field id="method" label="How you plan to give" error={errors.method?.[0]}>
          <Select id="method" defaultValue="" error={errors.method?.[0]}>
            <option value="">Please choose…</option>
            {methods.map((method) => (
              <option key={method.id} value={method.id}>
                {method.label}
              </option>
            ))}
          </Select>
        </Field>
      ) : null}

      {designations.length > 0 ? (
        <Field id="designation" label="Programme you want to support" error={errors.designation?.[0]}>
          <Select id="designation" defaultValue="" error={errors.designation?.[0]}>
            <option value="">Wherever it is needed most</option>
            {designations.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </Select>
        </Field>
      ) : null}

      <Field id="message" label="Message" error={errors.message?.[0]}>
        <TextArea id="message" rows={3} error={errors.message?.[0]} />
      </Field>

      <label className="flex items-start gap-3 text-sm text-sand-700">
        <input
          type="checkbox"
          name="is_anonymous"
          className="mt-0.5 h-4 w-4 rounded border-sand-300 text-green-600 focus:ring-green-500"
        />
        Keep my gift anonymous in any public acknowledgement
      </label>

      <p className="rounded-xl border border-sand-200 bg-sand-50 px-4 py-3 text-xs leading-relaxed text-sand-600">
        This form records your intention to give. It never asks for a card
        number, PIN or mobile money password — you pay through your own bank or
        mobile money app using the details above.
      </p>

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
          "Record my pledge"
        )}
      </button>
    </form>
  );
}
