import argparse
import json
import os


def serialize(slug):
    def deco(func):
        def wrapper(artist, in_data, force=False):
            path = f"data/{slug}/{artist}.json"
            if not os.path.exists(path) or force:
                data = func(artist, in_data)
                with open(path, "w", encoding="utf8") as fp:
                    print(f"...write {len(data)} to {path}")
                    json.dump(data, fp, indent=2)
            else:
                print(f"...read from {path}")
                with open(path, "r", encoding="utf8") as fp:
                    data = json.load(fp)
            return data

        return wrapper

    return deco

def phase(func, in_class):
    p = argparse.ArgumentParser()
    p.add_argument("artist")
    p.add_argument("--infile")
    p.add_argument("--outfile")
    args = p.parse_args()

    print(f"{func.__name__} {args.artist}...")
    with open(args.infile, "r", encoding="utf8") as fp:
        in_data = json.load(fp)

    out_data = func(args.artist, [in_class(**e) for e in in_data])

    print(f"... got {len(out_data)} records")

    def to_json(e):
        if isinstance(e, dict):
            return e
        return e.to_json()

    with open(args.outfile, "w", encoding="utf8") as fp:
        json.dump([to_json(e) for e in out_data], fp, indent=2)
    
