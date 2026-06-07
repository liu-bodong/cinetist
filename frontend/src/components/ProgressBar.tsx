import { PHASE_LABELS } from '../lib/format'
import type { JobStatus } from '../types'

interface Props {
  status: JobStatus | 'idle'
  progress: number
  filename: string | null
}

export function ProgressBar({ status, progress, filename }: Props) {
  const pct = Math.round(progress * 100)

  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm text-neutral-400">
        <span>
          {filename && <span className="text-neutral-200 font-medium">{filename}</span>}
          {filename && ' · '}
          {PHASE_LABELS[status] ?? status}
        </span>
        <span className="tabular-nums">{pct}%</span>
      </div>
      <div className="w-full h-2 rounded-full bg-neutral-800 overflow-hidden">
        <div
          className="h-full rounded-full bg-gradient-to-r from-violet-500 to-fuchsia-500 transition-[width] duration-300 ease-out"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}
