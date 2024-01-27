import { useMemo, useState } from 'react'

import Entries from './Entries.tsx';
import { allPosFromEntries, filterEntries } from './transform.ts';
import { RawEntry } from './types.ts';

import conc_data from './assets/taylor.json'

const posMap : { [index: string] : string } = {
  ADJ: 'adjective',
  ADP: 'adposition',
  ADV: 'adverb',
  AUX: 'auxiliary',
  CCONJ: 'coordinating conjunction',
  DET: 'determiner',
  INTJ: 'interjection',
  NOUN: 'noun',
  NUM: 'numeral',
  PART: 'particle',
  PRON: 'pronoun',
  PROPN: 'proper noun',
  PUNCT: 'punctuation',
  SCONJ: 'subordinating conjunction',
  SYM: 'symbol',
  VERB: 'verb',
  X: 'other',
};

function PosRadio(props: { parts: string[], setPosFilter: (v: string) => void }) {
  const { parts, setPosFilter } = props;

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const cb = (e: any) => setPosFilter((e.target as any).value);

  const radios = parts.map((part: string) => {
    const name: string = posMap[part];
    return (
    <span key={part}>
      <input name="pos" type="radio" value={part} onInput={cb}/>
      <label>{name}&nbsp;</label>
    </span>
    );
  });

  return (
    <small>
      <details>
        <summary>
          Parts of speech
        </summary>
        <span key='all'>
          <input name="pos" type="radio" value={''} onInput={() => setPosFilter('')}/>
          <label>all&nbsp;</label>
        </span>
        {radios}
      </details>
    </small>
  );
}

function App() {
  const [prefix, setPrefix] = useState('a')
  const [posFilter, setPosFilter] = useState('')

  const allEntries = (conc_data as RawEntry[]);

  const entries = useMemo(() => {
    return filterEntries(allEntries, prefix, posFilter);
  }, [allEntries, prefix, posFilter]);
  

  const parts = useMemo(()=>allPosFromEntries(allEntries), [allEntries]);

  const letterLinks = useMemo(() => {
    return Array.from('abcdefghijklmnopqrstuvwxyz')
      .map(c => {
        return (
          <span key={c}>
            <a href="#" onClick={() => setPrefix(c)}>{c}</a>
            &nbsp;
          </span>
        )
      })
  }, [])

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const onSearchInput = (e: any) => setPrefix((e.target as any).value)

  return (
    <>
      <h2>The (Taylor's Version) Concordance</h2>
      <hr></hr>
      <div>
        <input id="search" type="text" value={prefix} onInput={onSearchInput}></input>
        &nbsp;
        {letterLinks}
        <span>{entries.length} words</span>
      </div>
      <PosRadio parts={parts} setPosFilter={setPosFilter} />
      <hr/>
      <Entries entries={entries} />
    </>
  )
}

export default App
