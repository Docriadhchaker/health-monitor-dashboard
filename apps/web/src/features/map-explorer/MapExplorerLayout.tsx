import { MapExplorerContent } from './MapExplorerContext'
import { MapExplorerRail } from './MapExplorerContext'

export function MapExplorerLayout() {
  return (
    <div className="flex h-screen flex-col bg-[var(--color-bg-primary)] text-[var(--color-text-primary)]">
      <header
        className="flex h-14 shrink-0 items-center border-b border-[var(--color-border-default)] bg-[var(--color-bg-surface)] px-4"
        style={{ height: '56px' }}
      >
        <h1 className="text-lg font-semibold">HealthMonitor</h1>
      </header>
      <div className="flex min-h-0 flex-1">
        <aside className="w-80 shrink-0 overflow-y-auto border-r border-[var(--color-border-default)] bg-[var(--color-bg-surface)]">
          <MapExplorerRail />
        </aside>
        <main className="relative min-h-0 min-w-0 flex-1">
          <MapExplorerContent />
        </main>
      </div>
    </div>
  )
}
