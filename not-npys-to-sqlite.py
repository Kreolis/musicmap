import argparse
import json
import pathlib
import sqlite3
from io import BytesIO

import numpy as np
from tqdm import tqdm

from musicmap import schema

parser = argparse.ArgumentParser("extract-marius-npys")
parser.add_argument("npy_dir", type=pathlib.Path)
parser.add_argument("--graph-dict", default=None, type=pathlib.Path)
parser.add_argument("--drop-schema", action="store_true")

if __name__ == "__main__":
    args = parser.parse_args()

    not_npys = list(pathlib.Path(args.npy_dir).rglob("*.npy"))

    add_coords = args.graph_dict is not None

    if add_coords:
        g = np.load(args.graph_dict, allow_pickle=True).item()
        assert isinstance(g, dict)
    else:
        g = None

    db = sqlite3.Connection("musicmap.db")

    if args.drop_schema:
        db.executescript(schema.DROP_TABLES)
        db.commit()

    db.executescript(schema.CREATE_TABLES)
    db.commit()
    for nnpy in tqdm(not_npys):
        try:
            d = np.load(nnpy, allow_pickle=True).item()
        except:
            print(f"Failed to open {nnpy}")
            continue
        meta = {
            "file_name": pathlib.Path(d["filename"]).name,
            **{k: v for k, [v] in d["mp3tag"].items()},
        }
        meta_json = json.dumps(meta)
        f = BytesIO()
        np.save(
            f,
            d["features"]["max_pool"].max(0).astype("<f4"),
            allow_pickle=False,
        )
        b = f.getbuffer()

        q_song = db.execute(
            """
INSERT INTO songs(file_name, title, album, meta_json, musicnn_max_pool)
VALUES (:fn, :title, :album, :meta, :npy) ON CONFLICT DO NOTHING
RETURNING rowid
""",
            {
                "fn": meta["file_name"],
                "title": meta.get("title", meta["file_name"]),
                "album": meta.get("album", None),
                "meta": meta_json,
                "npy": b,
            },
        )
        # [rowid] = q_song.fetchone()
        if add_coords and nnpy.name in g:
            [rowid] = db.execute(
                "SELECT rowid FROM songs WHERE file_name=?", (meta["file_name"],)
            ).fetchone()
            x, y = g[nnpy.name]
            db.execute(
                """
INSERT INTO vic_coords(song, x, y) VALUES (?, ?, ?)
""",
                (rowid, x, y),
            )
        db.commit()
