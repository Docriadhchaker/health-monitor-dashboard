import { Routes, Route } from 'react-router-dom'
import { MapExplorerLayout } from '@/features/map-explorer/MapExplorerLayout'
import { MapExplorerProvider } from '@/features/map-explorer/MapExplorerContext'

export function AppRouter() {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <MapExplorerProvider>
            <MapExplorerLayout />
          </MapExplorerProvider>
        }
      />
    </Routes>
  )
}
