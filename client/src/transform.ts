import { Track, RawEntry, Entry } from './types.ts'

export function allPosFromEntries(entries: RawEntry[]) {
    const count: { [index: string]: number } = {};
    entries.forEach((word) => {
        word.tracks.forEach((track) => {
            track.usages.forEach(usage => {
                const { pos } = usage;
                count[pos] = (count[pos] || 0) + 1;
            })
        })
    })

    return Object.entries(count).sort((e1, e2) => e2[1] - e1[1]).map(([k]) => k);
}

export function filterEntries(entries: RawEntry[], prefix: string, pos: string): Entry[] {
    function filterTrack(track: Track) {
        const { usages } = track;

        const u = usages
            .filter(usage => !pos || usage.pos === pos);
        if (u.length === 0) { return null; }
        return {
            ...track,
            usages: u,
        }
    }

    const isTrack = (t: Track | null): t is Track => Boolean(t);
    const isEntry = (e: Entry | null): e is Entry => Boolean(e);

    return entries.map(entry => {
        const { word, tracks } = entry;
        if (prefix && !word.toLowerCase().startsWith(prefix)) { return null; }

        const keepTracks = tracks.map(filterTrack).filter(isTrack)
        if (keepTracks.length === 0) { return null; }

        return {
            ...entry,
            tracks: keepTracks,
            n_tracks: tracks.length,
            n_usages: tracks.reduce(((acc, t) => acc + t.usages.length), 0)
        }
    }).filter(isEntry);
}

