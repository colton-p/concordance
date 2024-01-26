export interface Usage {
  pos: string
  pre: string
  post: string
  word: string
}

export interface Track {
  album: string
  title: string
  usages: Usage[]
}

export interface RawEntry {
  word: string
  tracks: Track[]
}

export interface Entry extends RawEntry {
  n_tracks: number
  n_usages: number
}

