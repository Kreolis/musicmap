import argparse
import glob
import json
import pathlib
import sqlite3
from io import BytesIO

import numpy as np
from tqdm import tqdm

parser = argparse.ArgumentParser("extract-marius-npys")
parser.add_argument("npy_dir", type=pathlib.Path)
parser.add_argument("--drop-schema", action="store_true")

if __name__ == "__main__":
    args = parser.parse_args()

    not_npys = list(pathlib.Path(args.npy_dir).rglob("*.npy"))

    db = sqlite3.Connection("musicmap.db")

    if args.drop_schema:
        db.executescript("DROP TABLE IF EXISTS songs")
        db.commit()

    db.executescript(
        """
CREATE TABLE IF NOT EXISTS songs (
    rowid INTEGER PRIMARY KEY,
    file_name text,
    title text,
    album text,
    meta_json text,
    musicnn_max_pool blob
);

CREATE UNIQUE INDEX IF NOT EXISTS songs_file_name ON songs(file_name);
"""
    )
    db.commit()
    for nnpy in tqdm(not_npys):
        try:
            d = np.load(nnpy, allow_pickle=True).item()
        except:
            print(f"Failed to open {nnpy}")
            continue
        meta = {
            "file_name": pathlib.Path(d["filename"]).name,
            **{k: v for k, [v] in d.get("mp3tag", {}).items()},
        }
        meta_json = json.dumps(meta)
        f = BytesIO()
        np.save(
            f,
            d["features"]["max_pool"].max(0).astype("<f4"),
            allow_pickle=False,
        )
        b = f.getbuffer()

        db.execute(
            """
INSERT INTO songs(file_name, title, album, meta_json, musicnn_max_pool)
VALUES (:fn, :title, :album, :meta, :npy) ON CONFLICT DO NOTHING
""",
            {
                "fn": meta["file_name"],
                "title": meta.get("title", meta["file_name"]),
                "album": meta.get("album", None),
                "meta": meta_json,
                "npy": b,
            },
        )
        db.commit()
