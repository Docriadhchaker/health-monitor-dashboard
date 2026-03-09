import { useCallback, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { MapView } from '@/features/map-explorer/MapView'
import { LeftRail } from '@/components/panels/LeftRail'
import { EventCard } from '@/components/event-card/EventCard'
import { fetchEventById, fetchEvents } from '@/services/eventsApi'
import type { EventsFilters } from '@/types/event'

const LAYERS_API = (import.meta.env.VITE_API_BASE_URL || '') + '/api/v1/layers'

export function MapExplorerPage() {
  const [filters, setFilters] = useState<EventsFilters>({
    layer_ids: null,
    region_code: null,
    time_window: '7d',
    country_code: null,
  })
  const [selectedEventId, setSelectedEventId] = useState<string | null>(null)

  const { data: layersData } = useQuery({
    queryKey: ['layers'],
    queryFn: async () => {
      const res = await fetch(LAYERS_API)
      if (!res.ok) throw new Error('Layers API error')
      return res.json() as Promise<{ items: { id: number; code: string; name: string }[] }>
    },
  })
  const layers = layersData?.items ?? []

  const { data: eventsData } = useQuery({
    queryKey: ['events', filters],
    queryFn: () => fetchEvents(filters),
  })
  const events = eventsData?.items ?? []

  const { data: selectedEvent } = useQuery({
    queryKey: ['event', selectedEventId],
    queryFn: () => fetchEventById(selectedEventId!),
    enabled: !!selectedEventId,
  })

  const handleSelectEvent = useCallback((id: string) => setSelectedEventId(id), [])
  const handleCloseCard = useCallback(() => setSelectedEventId(null), [])

  return (
    <div className="relative h-full w-full">
      <MapView
        events={events}
        selectedEventId={selectedEventId}
        onSelectEvent={handleSelectEvent}
      />
      {selectedEvent && (
        <EventCard event={selectedEvent} onClose={handleCloseCard} />
      )}
    </div>
  )
}

export function MapExplorerPageWithRail() {
  const [filters, setFilters] = useState<EventsFilters>({
    layer_ids: null,
    region_code: null,
    time_window: '7d',
    country_code: null,
  })
  const [selectedEventId, setSelectedEventId] = useState<string | null>(null)

  const { data: layersData } = useQuery({
    queryKey: ['layers'],
    queryFn: async () => {
      const res = await fetch(LAYERS_API)
      if (!res.ok) throw new Error('Layers API error')
      return res.json() as Promise<{ items: { id: number; code: string; name: string }[] }>
    },
  })
  const layers = layersData?.items ?? []

  const { data: eventsData } = useQuery({
    queryKey: ['events', filters],
    queryFn: () => fetchEvents(filters),
  })
  const events = eventsData?.items ?? []

  const { data: selectedEvent } = useQuery({
    queryKey: ['event', selectedEventId],
    queryFn: () => fetchEventById(selectedEventId!),
    enabled: !!selectedEventId,
  })

  const handleSelectEvent = useCallback((id: string) => setSelectedEventId(id), [])
  const handleCloseCard = useCallback(() => setSelectedEventId(null), [])

  return (
    <div className="flex h-full w-full">
      <aside className="w-80 shrink-0 border-r border-[var(--color-border-default)] bg-[var(--color-bg-surface)] overflow-y-auto">
        <LeftRail filters={filters} setFilters={setFilters} layers={layers} />
      </aside>
      <div className="relative flex-1 min-w-0">
        <MapView
          events={events}
          selectedEventId={selectedEventId}
          onSelectEvent={handleSelectEvent}
        />
        {selectedEvent && (
          <EventCard event={selectedEvent} onClose={handleCloseCard} />
        )}
      </div>
    </div>
  )
}
