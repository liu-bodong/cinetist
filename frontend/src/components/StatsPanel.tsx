import { computeStats, formatDuration } from '../lib/format'
import type { MovieProfile } from '../types'

interface Props {
  profile: MovieProfile
}

function StatCard({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return (
    <div className="bg-neutral-900 border border-neutral-800 rounded-lg px-4 py-3">
      <p className="text-xs uppercase tracking-wide text-neutral-500">{label}</p>
      <p className="text-lg font-semibold text-white mt-0.5">{value}</p>
      {sub && <p className="text-xs text-neutral-500 mt-0.5">{sub}</p>}
    </div>
  )
}

export function StatsPanel({ profile }: Props) {
  const stats = computeStats(profile)

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
      <StatCard label="Duration" value={formatDuration(profile.duration_ms)} />
      <StatCard label="Resolution" value={`${profile.width}×${profile.height}`} sub={`${profile.fps.toFixed(2)} fps`} />
      <StatCard label="Shots" value={profile.shot_count.toLocaleString()} />
      <StatCard label="Avg. shot length" value={`${stats.averageShotLengthSec.toFixed(1)}s`} sub={`median ${stats.medianShotLengthSec.toFixed(1)}s`} />
      <StatCard label="Longest shot" value={`${stats.longestShot.durationSec.toFixed(1)}s`} sub={`shot #${stats.longestShot.index}`} />
      <StatCard label="Shortest shot" value={`${stats.shortestShot.durationSec.toFixed(1)}s`} sub={`shot #${stats.shortestShot.index}`} />
    </div>
  )
}
