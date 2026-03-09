import { createContext, useCallback, useContext, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { MapView } from '@/features/map-explorer/MapView'
import { LeftRail } from '@/components/panels/LeftRail'
import { EventCard } from '@/components/event-card/EventCard'
import { fetchEventById, fetchEvents } from '@/services/eventsApi'
import type { EventsFilters } from '@/types/event'

const LAYERS_API = (import.meta.env.VITE_API_BASE_URL || '') + '/api/v1/layers'

interface MapExplorerState {
  filters: EventsFilters
  setFilters: (f: EventsFilters) => void
  layers: { id: number; code: string; name: string }[]
  events: import('@/types/event').EventListItem[]
  selectedEventId: string | null
  setSelectedEventId: (id: string | null) => void
  selectedEvent: import('@/types/event').EventDetail | undefined
}

const MapExplorerContext = createContext<MapExplorerState | null>(null)

export function useMapExplorer() {
  const ctx = useContext(MapExplorerContext)
  if (!ctx) throw new Error('useMapExplorer must be used within MapExplorerProvider')
  return ctx
}

export function MapExplorerProvider({ children }: { children: React.ReactNode }) {
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

  const state: MapExplorerState = {
    filters,
    setFilters,
    layers,
    events,
    selectedEventId,
    setSelectedEventId,
    selectedEvent,
  }

  return (
    <MapExplorerContext.Provider value={state}>
      {children}
    </MapExplorerContext.Provider>
  )
}

export function MapExplorerContent() {
  const { events, selectedEventId, setSelectedEventId, selectedEvent } = useMapExplorer()
  const handleSelect = useCallback((id: string) => setSelectedEventId(id), [setSelectedEventId])
  const handleClose = useCallback(() => setSelectedEventId(null), [setSelectedEventId])

  return (
    <div className="relative h-full w-full">
      <MapView
        events={events}
        selectedEventId={selectedEventId}
        onSelectEvent={handleSelect}
      />
      {selectedEvent && <EventCard event={selectedEvent} onClose={handleClose} />}
    </div>
  )
}

export function MapExplorerRail() {
  const { filters, setFilters, layers } = useMapExplorer()
  return <LeftRail filters={filters} setFilters={setFilters} layers={layers} />
}
