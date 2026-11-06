import Link from "next/link";

import { ButtonLink, Container } from "@/components/ui";

export default function NotFound() {
  return (
    <div className="bg-forest-wash">
      <Container>
        <div className="flex min-h-[70vh] flex-col items-center justify-center py-32 text-center">
          <p className="font-display text-7xl font-extrabold text-green-400">
            404
          </p>
          <h1 className="mt-6 text-3xl text-white sm:text-4xl">
            We could not find that page
          </h1>
          <p className="mt-4 max-w-md text-ink-200">
            The link may be out of date, or the page may have moved.
          </p>
          <div className="mt-10 flex flex-col gap-3 sm:flex-row">
            <ButtonLink href="/" size="lg">
              Back to home
            </ButtonLink>
            <ButtonLink href="/contact" variant="ghostLight" size="lg">
              Contact us
            </ButtonLink>
          </div>
        </div>
      </Container>
    </div>
  );
}
