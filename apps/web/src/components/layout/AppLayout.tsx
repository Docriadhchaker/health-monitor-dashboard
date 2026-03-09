import { Outlet } from 'react-router-dom'
import { LeftRail } from '../panels/LeftRail'

/**
 * Shared layout per spec: top bar 56px, left rail 320px, map viewport fills remainder.
 */
export function AppLayout() {
  return (
    <div className="flex h-screen flex-col bg-[var(--color-bg-primary)] text-[var(--color-text-primary)]">
      <header
        className="flex h-14 shrink-0 items-center border-b border-[var(--color-border-default)] bg-[var(--color-bg-surface)] px-4"
        style={{ height: '56px' }}
      >
        <h1 className="text-lg font-semibold">HealthMonitor</h1>
      </header>
      <div className="flex flex-1 min-h-0">
        <aside className="w-80 shrink-0 border-r border-[var(--color-border-default)] bg-[var(--color-bg-surface)] overflow-y-auto">
          <LeftRail />
        </aside>
        <main className="flex-1 min-w-0 min-h-0">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
