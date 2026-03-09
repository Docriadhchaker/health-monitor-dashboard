import type { EventDetail } from '@/types/event'

interface EventCardProps {
  event: EventDetail
  onClose: () => void
}

function formatDate(iso: string | null): string {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleDateString(undefined, { dateStyle: 'medium' })
}

function formatRelative(iso: string | null): string {
  if (!iso) return ''
  const d = new Date(iso)
  const now = new Date()
  const diffMs = now.getTime() - d.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)
  if (diffMins < 60) return `${diffMins} minutes ago`
  if (diffHours < 24) return `${diffHours} hours ago`
  if (diffDays === 1) return '1 day ago'
  if (diffDays < 30) return `${diffDays} days ago`
  if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`
  return `${Math.floor(diffDays / 365)} years ago`
}

function stripHtmlToPlain(text: string): string {
  if (!text) return ''
  const div = document.createElement('div')
  div.innerHTML = text
  return (div.textContent ?? div.innerText ?? '').replace(/\s+/g, ' ').trim()
}

function getDisplayDate(event: EventDetail): { label: string; text: string; relative: string } {
  const published = event.source_published_at
  const ingested = event.ingested_at
  if (published) {
    return {
      label: 'Date',
      text: formatDate(published),
      relative: formatRelative(published),
    }
  }
  if (ingested) {
    return {
      label: 'Ingested',
      text: formatDate(ingested),
      relative: formatRelative(ingested),
    }
  }
  return { label: 'Date', text: '—', relative: '' }
}

export function EventCard({ event, onClose }: EventCardProps) {
  const location = [event.location_name, event.country_code].filter(Boolean).join(', ') || '—'
  const rawSummary = event.summary_en || event.translations[0]?.translated_summary || ''
  const summary = stripHtmlToPlain(rawSummary)
  const displayDate = getDisplayDate(event)

  return (
    <div
      className="absolute right-4 top-4 z-[30] w-[min(440px,calc(100vw-2rem)] rounded-[14px] border border-[var(--color-border-default)] bg-[var(--color-bg-surface)] p-4 shadow-[var(--shadow-md)]"
      style={{ zIndex: 30 }}
      role="dialog"
      aria-label="Event details"
    >
      <div className="flex items-start justify-between gap-2">
        <h2 className="text-[18px] font-semibold leading-tight text-[var(--color-text-primary)] line-clamp-2">
          {stripHtmlToPlain(event.title)}
        </h2>
        <button
          type="button"
          onClick={onClose}
          className="shrink-0 rounded p-1 text-[var(--color-text-muted)] hover:bg-[var(--color-bg-muted)]"
          aria-label="Close"
        >
          ×
        </button>
      </div>

      <div className="mt-2 flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-[var(--color-text-muted)]">
        <span>{event.layer_name}</span>
        <span aria-hidden>·</span>
        <span>{event.source_class_name}</span>
        <span aria-hidden>·</span>
        <span>{event.trust_tier_name}</span>
        <span aria-hidden>·</span>
        <span>{event.evidence_status_name}</span>
      </div>

      {summary && (
        <p className="mt-3 text-[14px] leading-[1.5] text-[var(--color-text-primary)] line-clamp-5">
          {summary}
        </p>
      )}

      {(event.specialty_names.length > 0 || event.topic_names.length > 0) && (
        <div className="mt-2 flex flex-wrap gap-1">
          {event.specialty_names.map((s) => (
            <span
              key={s}
              className="rounded-full bg-[var(--color-bg-muted)] px-2 py-0.5 text-xs text-[var(--color-text-secondary)]"
            >
              {s}
            </span>
          ))}
          {event.topic_names.map((t) => (
            <span
              key={t}
              className="rounded-full bg-[var(--color-bg-muted)] px-2 py-0.5 text-xs text-[var(--color-text-secondary)]"
            >
              {t}
            </span>
          ))}
        </div>
      )}

      <dl className="mt-3 space-y-1 text-sm">
        <div className="flex flex-col gap-0.5">
          <div className="flex gap-2">
            <dt className="text-[var(--color-text-muted)]">{displayDate.label}</dt>
            <dd>{displayDate.text}</dd>
          </div>
          {displayDate.relative && (
            <dd className="text-xs text-[var(--color-text-muted)]">{displayDate.relative}</dd>
          )}
        </div>
        <div className="flex gap-2">
          <dt className="text-[var(--color-text-muted)]">Location</dt>
          <dd className="text-[var(--color-text-secondary)]">{location}</dd>
        </div>
        <div className="flex gap-2">
          <dt className="text-[var(--color-text-muted)]">Source</dt>
          <dd className="text-[var(--color-text-secondary)]">{event.source_name}</dd>
        </div>
      </dl>

      <div className="mt-4 flex flex-wrap gap-2">
        {event.source_url && (
          <a
            href={event.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center rounded-md bg-[var(--color-accent-primary)] px-3 py-2 text-sm font-medium text-white hover:opacity-90"
          >
            Open Source
          </a>
        )}
        {event.source_url && (
          <button
            type="button"
            onClick={() => navigator.clipboard.writeText(event.source_url!)}
            className="inline-flex items-center rounded-md border border-[var(--color-border-default)] bg-[var(--color-bg-surface)] px-3 py-2 text-sm text-[var(--color-text-primary)]"
          >
            Copy Link
          </button>
        )}
      </div>
    </div>
  )
}
