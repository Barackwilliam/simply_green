"use client";

import { useEffect } from "react";

import { Button, Container } from "@/components/ui";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Surface the digest so the failure can be matched to a server log.
    console.error("Unhandled page error", error);
  }, [error]);

  return (
    <div className="bg-forest-wash">
      <Container>
        <div className="flex min-h-[70vh] flex-col items-center justify-center py-32 text-center">
          <h1 className="text-3xl text-white sm:text-4xl">
            Something went wrong
          </h1>
          <p className="mt-4 max-w-md text-ink-200">
            We hit an unexpected error loading this page. Please try again.
          </p>
          {error.digest ? (
            <p className="mt-3 font-mono text-xs text-ink-400">
              Reference: {error.digest}
            </p>
          ) : null}
          <Button onClick={reset} className="mt-10" size="lg">
            Try again
          </Button>
        </div>
      </Container>
    </div>
  );
}
