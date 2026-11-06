import { Container } from "@/components/ui";
import type { ImpactStat } from "@/lib/types";

export function ImpactStats({ stats }: { stats: ImpactStat[] }) {
  if (stats.length === 0) return null;

  return (
    <div className="relative z-20 -mt-16 sm:-mt-20">
      <Container>
        <dl className="grid gap-px overflow-hidden rounded-2xl bg-sand-200 shadow-xl shadow-ink-950/10 sm:grid-cols-2 lg:grid-cols-4">
          {stats.slice(0, 4).map((stat) => (
            <div key={stat.id} className="bg-white px-7 py-8">
              <dt className="text-sm font-medium text-sand-600">
                {stat.label}
              </dt>
              <dd className="mt-2 font-display text-4xl font-extrabold tracking-tight text-ink-950">
                {stat.value}
                {stat.suffix ? (
                  <span className="text-green-600">{stat.suffix}</span>
                ) : null}
              </dd>
              {stat.description ? (
                <p className="mt-2 text-xs leading-relaxed text-sand-500">
                  {stat.description}
                </p>
              ) : null}
            </div>
          ))}
        </dl>
      </Container>
    </div>
  );
}
