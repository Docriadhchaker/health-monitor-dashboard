import type { EventDetail, EventsListResponse, EventsFilters } from '@/types/event'

const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

function buildParams(filters: EventsFilters & { bbox?: { minLon: number; minLat: number; maxLon: number; maxLat: number } }): string {
  const p = new URLSearchParams()
  if (filters.layer_ids?.length) filters.layer_ids.forEach((id) => p.append('layer_ids', String(id)))
  if (filters.region_code) p.set('region_code', filters.region_code)
  p.set('time_window', filters.time_window ?? '7d')
  if (filters.country_code) p.set('country_code', filters.country_code)
  if (filters.bbox) {
    p.set('min_lon', String(filters.bbox.minLon))
    p.set('min_lat', String(filters.bbox.minLat))
    p.set('max_lon', String(filters.bbox.maxLon))
    p.set('max_lat', String(filters.bbox.maxLat))
  }
  p.set('limit', '500')
  return p.toString()
}

export async function fetchEvents(
  filters: EventsFilters,
  bbox?: { minLon: number; minLat: number; maxLon: number; maxLat: number }
): Promise<EventsListResponse> {
  const q = buildParams({ ...filters, bbox })
  const res = await fetch(`${API_BASE}/api/v1/events?${q}`)
  if (!res.ok) throw new Error(`Events API error: ${res.status}`)
  return res.json()
}

export async function fetchEventById(id: string): Promise<EventDetail> {
  const res = await fetch(`${API_BASE}/api/v1/events/${id}`)
  if (!res.ok) throw new Error(`Event API error: ${res.status}`)
  return res.json()
}
