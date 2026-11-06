"use client";

/**
 * Write-side API calls, made from the browser.
 *
 * These are never cached. Every payload carries the `website_url` honeypot
 * field the backend expects to be empty.
 */

const API_BASE_URL = (
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000"
).replace(/\/$/, "");

export interface SubmitResult {
  ok: boolean;
  /** Field name -> messages, straight from DRF. */
  errors?: Record<string, string[]>;
  message?: string;
}

async function post(
  path: string,
  payload: Record<string, unknown> | FormData,
): Promise<SubmitResult> {
  try {
    const isFormData = payload instanceof FormData;
    const response = await fetch(`${API_BASE_URL}/api${path}`, {
      method: "POST",
      headers: isFormData ? undefined : { "Content-Type": "application/json" },
      body: isFormData ? payload : JSON.stringify(payload),
    });

    if (response.ok) return { ok: true };

    if (response.status === 429) {
      return {
        ok: false,
        message:
          "Too many submissions from this connection. Please try again later.",
      };
    }

    let errors: Record<string, string[]> | undefined;
    try {
      errors = (await response.json()) as Record<string, string[]>;
    } catch {
      /* non-JSON error body */
    }
    return {
      ok: false,
      errors,
      message: "Please check the form and try again.",
    };
  } catch {
    return {
      ok: false,
      message: "We could not reach the server. Please check your connection.",
    };
  }
}

export const submitContact = (data: Record<string, unknown>) =>
  post("/engage/contact/", data);

export const submitVolunteer = (data: FormData) =>
  post("/engage/volunteer/", data);

export const submitPartnerEnquiry = (data: Record<string, unknown>) =>
  post("/engage/partner-enquiry/", data);

export const submitNewsletter = (data: Record<string, unknown>) =>
  post("/engage/newsletter/", data);

export const submitDonationPledge = (data: Record<string, unknown>) =>
  post("/engage/donate/", data);

export const submitEventRegistration = (data: Record<string, unknown>) =>
  post("/news/event-registrations/", data);
