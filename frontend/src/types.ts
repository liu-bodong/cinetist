export interface ColorSwatch {
  hex: string
  coverage: number
}

export interface Shot {
  index: number
  start_ms: number
  end_ms: number
  duration_ms: number
  start_frame: number
  end_frame: number
  keyframe_ms: number
  palette: ColorSwatch[]
}

export interface MovieProfile {
  filename: string
  width: number
  height: number
  aspect_ratio: number
  duration_ms: number
  fps: number
  shot_count: number
  shots: Shot[]
}

export type JobStatus =
  | 'pending'
  | 'detecting_shots'
  | 'extracting_colors'
  | 'done'
  | 'error'

export interface Job {
  id: string
  status: JobStatus
  progress: number
  filename: string | null
  result: MovieProfile | null
  error: string | null
}
