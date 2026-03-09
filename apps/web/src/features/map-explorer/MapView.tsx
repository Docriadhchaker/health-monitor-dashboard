import { useEffect, useRef, useMemo } from 'react'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import Supercluster from 'supercluster'
import type { EventListItem } from '@/types/event'

const MAP_STYLE = 'https://demotiles.maplibre.org/style.json'

interface MapViewProps {
  events: EventListItem[]
  selectedEventId: string | null
  onSelectEvent: (id: string) => void
}

export function MapView({ events, selectedEventId, onSelectEvent }: MapViewProps) {
  const mapContainerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<maplibregl.Map | null>(null)
  const markersRef = useRef<maplibregl.Marker[]>([])

  const points = useMemo(() => {
    return events
      .filter((e) => e.lat != null && e.lon != null)
      .map((e) => ({
        type: 'Feature' as const,
        properties: { eventId: e.id, title: e.title },
        geometry: { type: 'Point' as const, coordinates: [e.lon!, e.lat!] },
      }))
  }, [events])

  const index = useMemo(() => {
    const idx = new Supercluster<{ eventId: string; title: string }>({
      radius: 60,
      maxZoom: 16,
    })
    idx.load(
      points.map((p) => ({
        type: 'Feature' as const,
        properties: p.properties,
        geometry: p.geometry,
      }))
    )
    return idx
  }, [points])

  useEffect(() => {
    if (!mapContainerRef.current) return
    const map = new maplibregl.Map({
      container: mapContainerRef.current,
      style: MAP_STYLE,
      center: [20, 20],
      zoom: 2,
    })
    map.addControl(new maplibregl.NavigationControl(), 'top-right')
    mapRef.current = map
    return () => {
      map.remove()
      mapRef.current = null
    }
  }, [])

  useEffect(() => {
    const map = mapRef.current
    if (!map) return

    const updateMarkers = () => {
      markersRef.current.forEach((m) => m.remove())
      markersRef.current = []

      const bbox = map.getBounds()
      const zoom = map.getZoom()
      const bounds: [number, number, number, number] = [
        bbox.getWest(),
        bbox.getSouth(),
        bbox.getEast(),
        bbox.getNorth(),
      ]
      const clusters = index.getClusters(bounds, Math.floor(zoom))

      clusters.forEach((cluster) => {
        const [lon, lat] = cluster.geometry.coordinates
        const isCluster = (cluster.properties as { cluster?: boolean }).cluster
        const props = cluster.properties as { cluster?: boolean; point_count?: number; eventId?: string; id?: number }
        const el = document.createElement('div')
        el.className = 'event-marker'
        if (isCluster) {
          el.textContent = String(props.point_count ?? 0)
          el.style.cssText = `
            width: 32px; height: 32px; border-radius: 50%;
            background: var(--color-accent-primary, #0F6CBD); color: white;
            display: flex; align-items: center; justify-content: center;
            font-size: 12px; font-weight: 600; cursor: pointer;
            border: 2px solid white; box-shadow: 0 1px 4px rgba(0,0,0,0.2);
          `
        } else {
          el.style.cssText = `
            width: 24px; height: 24px; border-radius: 50%;
            background: var(--color-accent-primary, #0F6CBD); cursor: pointer;
            border: 2px solid white; box-shadow: 0 1px 4px rgba(0,0,0,0.2);
          `
        }
        const marker = new maplibregl.Marker({ element: el })
          .setLngLat([lon, lat])
          .addTo(map)
        el.addEventListener('click', () => {
          if (isCluster && props.id != null) {
            const expansionZoom = Math.min(index.getClusterExpansionZoom(props.id), 20)
            map.flyTo({ center: [lon, lat], zoom: expansionZoom })
          } else if (props.eventId) {
            onSelectEvent(props.eventId)
          }
        })
        markersRef.current.push(marker)
      })
    }

    if (map.isStyleLoaded()) {
      updateMarkers()
    } else {
      map.once('load', updateMarkers)
    }
    map.on('moveend', updateMarkers)
    return () => {
      map.off('moveend', updateMarkers)
      markersRef.current.forEach((m) => m.remove())
      markersRef.current = []
    }
  }, [index, onSelectEvent])

  return <div ref={mapContainerRef} className="h-full w-full" />
}
