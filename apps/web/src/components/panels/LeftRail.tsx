/**
 * Left filter rail: layers, region, time window, source filters.
 * Placeholder for Phase 1 — full filters in later phase.
 */
export function LeftRail() {
  return (
    <div className="p-4 space-y-4">
      <section>
        <h2 className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-muted)] mb-2">
          Layers
        </h2>
        <p className="text-sm text-[var(--color-text-secondary)]">
          Layer toggles (placeholder)
        </p>
      </section>
      <section>
        <h2 className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-muted)] mb-2">
          Region
        </h2>
        <p className="text-sm text-[var(--color-text-secondary)]">
          Region presets (placeholder)
        </p>
      </section>
      <section>
        <h2 className="text-xs font-semibold uppercase tracking-wide text-[var(--color-text-muted)] mb-2">
          Time
        </h2>
        <p className="text-sm text-[var(--color-text-secondary)]">
          Time window (placeholder)
        </p>
      </section>
    </div>
  )
}
