import type { Metadata } from "next";
import { Building2, Info, Smartphone } from "lucide-react";

import { DonationPledgeForm } from "@/components/forms/DonationPledgeForm";
import { Container, EmptyState, PageHeader, Section, SectionHeading } from "@/components/ui";
import { getDonationMethods, getProgrammes, getSiteSettings } from "@/lib/api";

export const metadata: Metadata = {
  title: "Support Our Work",
  description:
    "Donate to Simply Green Organization and fund community-led environmental conservation, climate action and sustainable livelihoods in Tanzania.",
  alternates: { canonical: "/donate" },
};

const BANK_CHANNELS = new Set(["bank"]);

export default async function DonatePage() {
  const [settings, methods, programmes] = await Promise.all([
    getSiteSettings(),
    getDonationMethods(),
    getProgrammes({ status: "ongoing" }),
  ]);

  const banks = methods.filter((method) => BANK_CHANNELS.has(method.channel));
  const mobile = methods.filter((method) => !BANK_CHANNELS.has(method.channel));

  return (
    <>
      <PageHeader
        eyebrow="Get involved"
        title="Support our work"
        description={`A donation to ${settings.organisation_name} puts tools, training and trees into the hands of the communities doing the work.`}
      />

      <Section>
        <Container>
          <div className="grid gap-14 lg:grid-cols-12 lg:gap-16">
            {/* Payment details */}
            <div className="lg:col-span-6">
              <SectionHeading eyebrow="How to give" title="Where to send your gift" />

              {methods.length === 0 ? (
                <div className="mt-8">
                  <EmptyState
                    icon={<Building2 className="h-10 w-10" />}
                    title="Payment details are not published yet"
                    description="Bank and mobile money details added in the admin will appear here."
                  />
                </div>
              ) : (
                <div className="mt-8 space-y-6">
                  {banks.length > 0 ? (
                    <div>
                      <h3 className="flex items-center gap-2 font-display text-sm font-bold uppercase tracking-wider text-sand-600">
                        <Building2 className="h-4 w-4" aria-hidden />
                        Bank transfer
                      </h3>
                      <ul className="mt-4 space-y-4">
                        {banks.map((method) => (
                          <li
                            key={method.id}
                            className="rounded-2xl border border-sand-200 bg-white p-6"
                          >
                            <p className="font-display text-base font-bold text-ink-950">
                              {method.label}
                            </p>
                            <dl className="mt-4 space-y-2 text-sm">
                              {method.account_name ? (
                                <div className="flex gap-3">
                                  <dt className="w-32 shrink-0 text-sand-500">Account name</dt>
                                  <dd className="font-medium text-ink-900">{method.account_name}</dd>
                                </div>
                              ) : null}
                              {method.account_number ? (
                                <div className="flex gap-3">
                                  <dt className="w-32 shrink-0 text-sand-500">Account number</dt>
                                  <dd className="font-mono font-medium text-ink-900">
                                    {method.account_number}
                                  </dd>
                                </div>
                              ) : null}
                              {method.bank_name ? (
                                <div className="flex gap-3">
                                  <dt className="w-32 shrink-0 text-sand-500">Bank</dt>
                                  <dd className="font-medium text-ink-900">{method.bank_name}</dd>
                                </div>
                              ) : null}
                              {method.branch ? (
                                <div className="flex gap-3">
                                  <dt className="w-32 shrink-0 text-sand-500">Branch</dt>
                                  <dd className="font-medium text-ink-900">{method.branch}</dd>
                                </div>
                              ) : null}
                              {method.swift_code ? (
                                <div className="flex gap-3">
                                  <dt className="w-32 shrink-0 text-sand-500">SWIFT</dt>
                                  <dd className="font-mono font-medium text-ink-900">
                                    {method.swift_code}
                                  </dd>
                                </div>
                              ) : null}
                              {method.currency ? (
                                <div className="flex gap-3">
                                  <dt className="w-32 shrink-0 text-sand-500">Currency</dt>
                                  <dd className="font-medium text-ink-900">{method.currency}</dd>
                                </div>
                              ) : null}
                            </dl>
                            {method.instructions ? (
                              <p className="mt-4 border-t border-sand-100 pt-4 text-sm text-sand-700">
                                {method.instructions}
                              </p>
                            ) : null}
                          </li>
                        ))}
                      </ul>
                    </div>
                  ) : null}

                  {mobile.length > 0 ? (
                    <div>
                      <h3 className="flex items-center gap-2 font-display text-sm font-bold uppercase tracking-wider text-sand-600">
                        <Smartphone className="h-4 w-4" aria-hidden />
                        Mobile money
                      </h3>
                      <ul className="mt-4 grid gap-4 sm:grid-cols-2">
                        {mobile.map((method) => (
                          <li
                            key={method.id}
                            className="rounded-2xl border border-sand-200 bg-white p-6"
                          >
                            <p className="text-xs font-semibold uppercase tracking-wider text-green-700">
                              {method.channel_label}
                            </p>
                            <p className="mt-2 font-display text-base font-bold text-ink-950">
                              {method.label}
                            </p>
                            {method.account_number ? (
                              <p className="mt-3 font-mono text-lg font-bold text-ink-950">
                                {method.account_number}
                              </p>
                            ) : null}
                            {method.account_name ? (
                              <p className="mt-1 text-sm text-sand-600">
                                {method.account_name}
                              </p>
                            ) : null}
                            {method.instructions ? (
                              <p className="mt-3 text-sm text-sand-700">
                                {method.instructions}
                              </p>
                            ) : null}
                          </li>
                        ))}
                      </ul>
                    </div>
                  ) : null}
                </div>
              )}

              <div className="mt-8 flex gap-3 rounded-2xl border border-sky-200 bg-sky-50 p-5">
                <Info className="mt-0.5 h-5 w-5 shrink-0 text-sky-700" aria-hidden />
                <p className="text-sm leading-relaxed text-sky-900">
                  Always confirm these account details with us by phone before
                  sending a large gift. We will never email you to say our bank
                  details have changed.
                </p>
              </div>
            </div>

            {/* Pledge form */}
            <div className="lg:col-span-6">
              <div className="rounded-2xl border border-green-200 bg-white p-7 shadow-sm sm:p-9">
                <SectionHeading
                  eyebrow="Tell us"
                  title="Let us know your gift is coming"
                />
                <p className="mt-4 text-sm leading-relaxed text-sand-700">
                  This helps us match your transfer when it arrives, thank you
                  properly, and send a receipt.
                </p>
                <div className="mt-8">
                  <DonationPledgeForm
                    methods={methods}
                    designations={programmes.map((programme) => programme.title)}
                  />
                </div>
              </div>
            </div>
          </div>
        </Container>
      </Section>
    </>
  );
}
