import type { EventsFilters } from '@/types/event'

const REGION_PRESETS = ['World', 'Americas', 'MENA', 'Europe', 'Asia', 'Africa', 'Oceania'] as const

const TIME_WINDOWS = [
  { value: '24h', label: 'Last 24 hours' },
  { value: '7d', label: 'Last 7 days' },
  { value: '30d', label: 'Last 30 days' },
] as const

interface LayerItem {
  id: number
  code: string
  name: string
}

interface LeftRailProps {
  filters: EventsFilters
  setFilters: (f: EventsFilters) => void
  layers: LayerItem[]
}

export function LeftRail({ filters, setFilters, layers }: LeftRailProps) {
  const allLayerIds = layers.map((l) => l.id)

  const toggleLayer = (layerId: number) => {
    const current = filters.layer_ids ?? allLayerIds
    const isCurrentlyShown = current.includes(layerId)
    let next: number[] | null
    if (isCurrentlyShown) {
      next = current.filter((id) => id !== layerId)
      next = next.length > 0 ? next : null
    } else {
      const added = [...current, layerId]
      next = added.length === allLayerIds.length ? null : added
    }
    setFilters({ ...filters, layer_ids: next })
  }

  const isLayerActive = (id: number) => {
    const ids = filters.layer_ids
    return ids == null || ids.length === 0 || ids.includes(id)
  }

  return (
    <div className="space-y-4 p-4">
      <section>
        <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-[var(--color-text-muted)]">
          Layers
        </h2>
        <div className="flex flex-col gap-1">
          {layers.map((layer) => (
            <label
              key={layer.id}
              className="flex cursor-pointer items-center gap-2 rounded-md px-2 py-1.5 text-sm hover:bg-[var(--color-bg-muted)]"
            >
              <input
                type="checkbox"
                checked={isLayerActive(layer.id)}
                onChange={() => toggleLayer(layer.id)}
                className="h-4 w-4 rounded border-[var(--color-border-default)]"
              />
              <span className="text-[var(--color-text-primary)]">{layer.name}</span>
            </label>
          ))}
        </div>
      </section>

      <section>
        <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-[var(--color-text-muted)]">
          Region
        </h2>
        <select
          value={filters.region_code ?? ''}
          onChange={(e) =>
            setFilters({
              ...filters,
              region_code: e.target.value || null,
            })
          }
          className="w-full rounded-md border border-[var(--color-border-default)] bg-[var(--color-bg-surface)] px-3 py-2 text-sm text-[var(--color-text-primary)]"
        >
          <option value="">World</option>
          {REGION_PRESETS.filter((r) => r !== 'World').map((r) => (
            <option key={r} value={r.toUpperCase().replace(/\s+/, '_')}>
              {r}
            </option>
          ))}
        </select>
      </section>

      <section>
        <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-[var(--color-text-muted)]">
          Time
        </h2>
        <select
          value={filters.time_window ?? '7d'}
          onChange={(e) =>
            setFilters({
              ...filters,
              time_window: e.target.value as '24h' | '7d' | '30d',
            })
          }
          className="w-full rounded-md border border-[var(--color-border-default)] bg-[var(--color-bg-surface)] px-3 py-2 text-sm text-[var(--color-text-primary)]"
        >
          {TIME_WINDOWS.map(({ value, label }) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
      </section>
    </div>
  )
}
