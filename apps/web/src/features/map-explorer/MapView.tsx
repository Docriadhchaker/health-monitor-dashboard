import { useEffect, useRef, useMemo, useState } from 'react'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import Supercluster from 'supercluster'
import type { EventListItem } from '@/types/event'

const MAP_STYLE_PREFERRED = 'https://openmaptiles.github.io/positron-gl-style/style-cdn.json'
const MAP_STYLE_FALLBACK = 'https://demotiles.maplibre.org/style.json'
const INDEX_MAX_ZOOM = 16
const MAX_ZOOM = 20

function isApproximatePrecision(p?: string): boolean {
  return p === 'region_fallback' || p === 'fallback' || p === 'region' || p === 'country' || !p
}

interface MapViewProps {
  events: EventListItem[]
  selectedEventId: string | null
  onSelectEvent: (id: string) => void
  onSelectCluster?: (eventIds: string[]) => void
}

export function MapView({ events, selectedEventId, onSelectEvent, onSelectCluster }: MapViewProps) {
  const mapContainerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<maplibregl.Map | null>(null)
  const markersRef = useRef<maplibregl.Marker[]>([])
  const styleLoadFailedRef = useRef(false)
  const hasLoadedSuccessRef = useRef(false)
  const [mapLoaded, setMapLoaded] = useState(false)

  const points = useMemo(() => {
    return events
      .filter((e) => e.lat != null && e.lon != null)
      .map((e) => ({
        type: 'Feature' as const,
        properties: { eventId: e.id, title: e.title, geo_precision: e.geo_precision ?? undefined },
        geometry: { type: 'Point' as const, coordinates: [e.lon!, e.lat!] },
      }))
  }, [events])

  const index = useMemo(() => {
    const idx = new Supercluster<{ eventId: string; title: string; geo_precision?: string }>({
      radius: 60,
      maxZoom: INDEX_MAX_ZOOM,
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
    const container = mapContainerRef.current
    if (!container) return

    const styleUrl = styleLoadFailedRef.current ? MAP_STYLE_FALLBACK : MAP_STYLE_PREFERRED
    const map = new maplibregl.Map({
      container,
      style: styleUrl,
      center: [20, 20],
      zoom: 2,
    })
    map.addControl(new maplibregl.NavigationControl(), 'top-right')
    mapRef.current = map

    const tryFallback = () => {
      if (styleLoadFailedRef.current || hasLoadedSuccessRef.current) return
      styleLoadFailedRef.current = true
      if (import.meta.env.DEV) {
        console.warn('[MapView] Basemap style failed to load, using fallback.', styleUrl)
      }
      map.remove()
      mapRef.current = null
      const fallbackMap = new maplibregl.Map({
        container,
        style: MAP_STYLE_FALLBACK,
        center: [20, 20],
        zoom: 2,
      })
      fallbackMap.addControl(new maplibregl.NavigationControl(), 'top-right')
      mapRef.current = fallbackMap
      fallbackMap.once('load', () => {
        hasLoadedSuccessRef.current = true
        setMapLoaded(true)
      })
    }

    map.on('error', (e: { error?: { message?: string } }) => {
      if (import.meta.env.DEV && e?.error?.message) {
        console.warn('[MapView] Map error:', e.error.message)
      }
      tryFallback()
    })
    map.once('load', () => {
      hasLoadedSuccessRef.current = true
      setMapLoaded(true)
    })

    return () => {
      mapRef.current?.remove()
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
        const props = cluster.properties as {
          cluster?: boolean
          cluster_id?: number
          point_count?: number
          eventId?: string
          geo_precision?: string
        }
        const isCluster = props.cluster === true && props.cluster_id != null
        const el = document.createElement('div')
        const approximate = !isCluster && isApproximatePrecision(props.geo_precision)
        el.className = isCluster
          ? 'event-marker event-marker--cluster'
          : approximate
            ? 'event-marker event-marker--single event-marker--approximate'
            : 'event-marker event-marker--single event-marker--exact'
        if (isCluster) {
          const count = Math.max(1, props.point_count ?? 0)
          el.textContent = String(count)
          el.style.cssText = `
            width: 38px; height: 38px; min-width: 38px; min-height: 38px;
            border-radius: 50%;
            background: var(--color-accent-primary, #0F6CBD); color: white;
            display: flex; align-items: center; justify-content: center;
            font-size: 13px; font-weight: 700; cursor: pointer;
            border: 3px solid rgba(255,255,255,0.95); box-shadow: 0 2px 8px rgba(0,0,0,0.2);
          `
        } else if (approximate) {
          el.textContent = ''
          el.style.cssText = `
            width: 22px; height: 22px; min-width: 22px; min-height: 22px;
            border-radius: 50%;
            background: rgba(255,255,255,0.9); cursor: pointer;
            border: 2px dashed var(--color-accent-primary, #0F6CBD);
            box-shadow: 0 1px 4px rgba(0,0,0,0.15);
          `
        } else {
          el.textContent = ''
          el.style.cssText = `
            width: 22px; height: 22px; min-width: 22px; min-height: 22px;
            border-radius: 50%;
            background: var(--color-accent-primary, #0F6CBD); cursor: pointer;
            border: 2px solid rgba(255,255,255,0.95); box-shadow: 0 1px 6px rgba(0,0,0,0.2);
          `
        }
        const marker = new maplibregl.Marker({ element: el })
          .setLngLat([lon, lat])
          .addTo(map)
        el.addEventListener('click', () => {
          if (isCluster && props.cluster_id != null) {
            const pointCount = props.point_count ?? 0
            if (pointCount > 1 && onSelectCluster) {
              const leaves = index.getLeaves(props.cluster_id, 500, 0)
              const eventIds = leaves
                .map((f) => (f.properties as { eventId?: string }).eventId)
                .filter((id): id is string => !!id)
              if (eventIds.length > 0) onSelectCluster(eventIds)
            }
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
  }, [mapLoaded, index, onSelectEvent, onSelectCluster])

  return <div ref={mapContainerRef} className="h-full w-full" />
}
