import { Routes, Route } from 'react-router-dom'
import { AppLayout } from '@/components/layout/AppLayout'
import { MapExplorerPage } from '@/pages/MapExplorerPage'

export function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<AppLayout />}>
        <Route index element={<MapExplorerPage />} />
      </Route>
    </Routes>
  )
}
