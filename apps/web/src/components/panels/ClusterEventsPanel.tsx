import { useMemo } from 'react'
import type { EventListItem } from '@/types/event'

interface ClusterEventsPanelProps {
  events: EventListItem[]
  onSelectEvent: (id: string) => void
  onClose: () => void
}

function formatDate(iso: string | null): string {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString(undefined, { dateStyle: 'short' })
}

export function ClusterEventsPanel({ events, onSelectEvent, onClose }: ClusterEventsPanelProps) {
  const groupedByDate = useMemo(() => {
    const sorted = [...events].sort((a, b) => {
      const aT = a.source_published_at ? new Date(a.source_published_at).getTime() : 0
      const bT = b.source_published_at ? new Date(b.source_published_at).getTime() : 0
      return bT - aT
    })
    const byDate = new Map<string, EventListItem[]>()
    for (const e of sorted) {
      const k = e.source_published_at
        ? new Date(e.source_published_at).toLocaleDateString(undefined, { dateStyle: 'medium' })
        : 'No date'
      if (!byDate.has(k)) byDate.set(k, [])
      byDate.get(k)!.push(e)
    }
    return Array.from(byDate.entries(), ([key, items]) => ({ key, items }))
  }, [events])

  return (
    <div
      className="absolute right-4 top-4 z-[30] flex max-h-[75vh] w-[min(400px,calc(100vw-2rem))] flex-col rounded-xl border border-[var(--color-border-default)] bg-[var(--color-bg-surface)] shadow-lg"
      role="dialog"
      aria-label="Events at this location"
    >
      <div className="flex shrink-0 items-center justify-between border-b border-[var(--color-border-default)] px-4 py-3">
        <h2 className="text-sm font-semibold text-[var(--color-text-primary)]">
          Events at this location
        </h2>
        <button
          type="button"
          onClick={onClose}
          className="rounded p-1.5 text-[var(--color-text-muted)] hover:bg-[var(--color-bg-muted)]"
          aria-label="Close panel"
        >
          ×
        </button>
      </div>
      <ul className="min-h-0 flex-1 overflow-y-auto p-2">
        {groupedByDate.map(({ key, items }) => (
          <li key={key}>
            <div className="sticky top-0 z-10 bg-[var(--color-bg-surface)] px-2 py-1.5 text-xs font-medium text-[var(--color-text-muted)]">
              {key}
            </div>
            {items.map((ev) => (
              <button
                key={ev.id}
                type="button"
                onClick={() => onSelectEvent(ev.id)}
                className="mb-1 w-full rounded-lg border border-transparent px-3 py-2.5 text-left transition-colors hover:border-[var(--color-border-default)] hover:bg-[var(--color-bg-muted)]"
              >
                <div className="line-clamp-2 text-sm font-medium text-[var(--color-text-primary)]">
                  {ev.title}
                </div>
                <div className="mt-1 flex flex-wrap items-center gap-x-2 gap-y-0.5 text-xs text-[var(--color-text-muted)]">
                  {ev.source_name && <span>{ev.source_name}</span>}
                  {ev.source_name && ev.source_published_at && <span aria-hidden>·</span>}
                  <span>{formatDate(ev.source_published_at)}</span>
                  {ev.country_code && (
                    <>
                      <span aria-hidden>·</span>
                      <span>{ev.country_code}</span>
                    </>
                  )}
                  {ev.layer_name && (
                    <>
                      <span aria-hidden>·</span>
                      <span>{ev.layer_name}</span>
                    </>
                  )}
                </div>
              </button>
            ))}
          </li>
        ))}
      </ul>
    </div>
  )
}
