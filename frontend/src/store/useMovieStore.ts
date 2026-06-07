import { create } from 'zustand'
import type { Job, JobStatus, MovieProfile } from '../types'

const POLL_INTERVAL_MS = 400

interface MovieStore {
  profile: MovieProfile | null
  status: JobStatus | 'idle'
  progress: number
  filename: string | null
  error: string | null
  analyze: (path: string) => Promise<void>
}

async function fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, init)
  if (!res.ok) {
    const body = await res.json().catch(() => null)
    throw new Error(body?.detail ?? `Request failed (${res.status})`)
  }
  return res.json()
}

export const useMovieStore = create<MovieStore>((set, get) => ({
  profile: null,
  status: 'idle',
  progress: 0,
  filename: null,
  error: null,

  analyze: async (path: string) => {
    set({ status: 'pending', progress: 0, error: null, profile: null, filename: null })

    try {
      const job = await fetchJson<Job>('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path }),
      })
      set({ filename: job.filename })

      const poll = async () => {
        const current = await fetchJson<Job>(`/api/jobs/${job.id}`)
        set({ status: current.status, progress: current.progress })

        if (current.status === 'done') {
          set({ profile: current.result })
        } else if (current.status === 'error') {
          set({ error: current.error ?? 'Analysis failed' })
        } else if (get().status !== 'idle') {
          setTimeout(poll, POLL_INTERVAL_MS)
        }
      }
      poll()
    } catch (e) {
      set({ status: 'error', error: (e as Error).message })
    }
  },
}))
