import { useState, type SubmitEvent } from 'react'
import { useMovieStore } from './store/useMovieStore'
import { MovieBarcode } from './components/MovieBarcode'
import { ProgressBar } from './components/ProgressBar'
import { StatsPanel } from './components/StatsPanel'

const isBusy = (status: string) =>
  status === 'pending' || status === 'detecting_shots' || status === 'extracting_colors'

export default function App() {
  const [path, setPath] = useState('')
  const { profile, status, progress, filename, error, analyze } = useMovieStore()
  const busy = isBusy(status)

  const handleSubmit = (e: SubmitEvent) => {
    e.preventDefault()
    if (path.trim() && !busy) analyze(path.trim())
  }

  return (
    <div className="min-h-screen">
      <div className="max-w-5xl mx-auto px-6 py-10 space-y-8">
        <header>
          <h1 className="text-3xl font-semibold text-white tracking-tight">Cinetist</h1>
          <p className="text-neutral-500 text-sm mt-1">Treat your movies as structured datasets.</p>
        </header>

        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={path}
            onChange={(e) => setPath(e.target.value)}
            placeholder="/absolute/path/to/movie.mp4"
            className="flex-1 bg-neutral-900 border border-neutral-700 rounded-md px-3 py-2 text-sm text-white placeholder:text-neutral-600 focus:outline-none focus:border-violet-500 transition-colors"
          />
          <button
            type="submit"
            disabled={busy || !path.trim()}
            className="px-5 py-2 bg-white text-black text-sm rounded-md font-medium disabled:opacity-30 disabled:cursor-not-allowed hover:bg-neutral-200 transition-colors"
          >
            {busy ? 'Analyzing…' : 'Analyze'}
          </button>
        </form>

        {busy && <ProgressBar status={status} progress={progress} filename={filename} />}

        {error && (
          <p className="text-sm text-red-400 bg-red-950/40 border border-red-900/50 rounded-md px-3 py-2">
            {error}
          </p>
        )}

        {profile && (
          <div className="space-y-8">
            <div>
              <h2 className="text-xl font-medium text-white">{profile.filename}</h2>
            </div>
            <StatsPanel profile={profile} />
            <MovieBarcode profile={profile} />
          </div>
        )}
      </div>
    </div>
  )
}
