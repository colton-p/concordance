import { Usage, Track, Entry } from './types.ts'

function Usage(props: { usage: Usage }) {
    const { usage } = props;
    const { pos, pre, word, post } = usage;

    const pad = word.endsWith(' ') ? ' ' : ''
    return (
        <li>
            <span>
                <b>{pos}</b>
            </span>
            &nbsp;
            <span>
                {pre}
                <code>{word.trimEnd()}</code>
                {pad}
                {post}
            </span>
        </li>
    )
}

function Track(props: { track: Track }) {
    const { track } = props;
    const { title, album, usages } = track
    const usages_html = usages
        .slice(0, 5)
        .map((usage: Usage, ix: number) => (
            <Usage key={`${usage.word}-${ix}`} usage={usage} />
        ));

    return (
        <ul>
            <li>{title} — <i>{album}</i></li>
            <ul>
                {usages_html}
            </ul>
        </ul>
    )
}

function Word(props: { entry: Entry }) {
    const { entry } = props;
    const { word, tracks, n_tracks, n_usages } = entry;
    const tracks_html = tracks
        .map(track => (
            <Track key={`${word}-${track.title}`} track={track} />
        ));

    return (
        <div id={word}>
            <h3>{word}</h3>
            <span> {n_tracks} songs; {n_usages} usages </span>
            <ul>
                {tracks_html}
            </ul>
        </div>
    )
}

export default function Entries(props: { entries: Entry[] }) {
    const { entries } = props;

    const entries_html = entries.map((entry: Entry) => {
        return (<Word key={entry.word} entry={entry} />);
    });

    return <>{entries_html}</>;
}