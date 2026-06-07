import { useState } from 'react'
import type { MovieProfile, Shot } from '../types'
import { formatDuration } from '../lib/format'

interface Props {
  profile: MovieProfile
}

export function MovieBarcode({ profile }: Props) {
  const [hovered, setHovered] = useState<Shot | null>(null)

  return (
    <div className="space-y-2">
      <div className="flex items-baseline justify-between">
        <h2 className="text-sm font-medium text-neutral-300">Movie Barcode</h2>
        <p className="text-xs text-neutral-500 tabular-nums">
          {hovered
            ? `Shot #${hovered.index} · ${formatDuration(hovered.start_ms)}–${formatDuration(hovered.end_ms)} · ${(hovered.duration_ms / 1000).toFixed(1)}s`
            : `${profile.shot_count} shots over ${formatDuration(profile.duration_ms)}`}
        </p>
      </div>
      <div className="flex w-full h-20 rounded-md overflow-hidden ring-1 ring-neutral-800">
        {profile.shots.map((shot) => {
          const widthPct = (shot.duration_ms / profile.duration_ms) * 100
          const color = shot.palette[0]?.hex ?? '#000000'
          const isHovered = hovered?.index === shot.index
          return (
            <div
              key={shot.index}
              onMouseEnter={() => setHovered(shot)}
              onMouseLeave={() => setHovered(null)}
              style={{
                width: `${widthPct}%`,
                backgroundColor: color,
                minWidth: 1,
              }}
              className={`h-full transition-transform origin-bottom ${isHovered ? 'scale-y-110 ring-1 ring-white/60 z-10' : ''}`}
            />
          )
        })}
      </div>
    </div>
  )
}
