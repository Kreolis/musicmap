import argparse
import glob
import json
import pathlib
import sqlite3
from io import BytesIO

import numpy as np
from tqdm import tqdm

from musicmap import schema

parser = argparse.ArgumentParser("extract-marius-npys")
parser.add_argument("pkl", type=pathlib.Path)


def s_npy_mp3(name: str):
    assert name.endswith(".npy")
    return f"{name.removesuffix('.npy')}.mp3"


def get_id(db, mp3_name) -> int:
    rowids = db.execute(
        "SELECT rowid FROM songs WHERE file_name=?", (mp3_name,)
    ).fetchall()

    if len(rowids) == 0:
        (rowid,) = db.execute(
            "INSERT INTO songs(file_name) VALUES(?) RETURNING rowid", (mp3_name,)
        ).fetchone()
    else:
        [(rowid,)] = rowids
    return rowid


if __name__ == "__main__":
    args = parser.parse_args()

    g = np.load(args.pkl, allow_pickle=True).item()
    assert isinstance(g, dict)

    db = sqlite3.Connection("musicmap.db")

    db.executescript(schema.CREATE_TABLES)
    db.commit()

    values = [
        (get_id(db, s_npy_mp3(npy_name)), float(x), float(y))
        for npy_name, (x, y) in g.items()
    ]
    db.executemany(
        "INSERT OR REPLACE INTO vic_coords(song, x, y) VALUES(?, ?, ?) ON CONFLICT DO NOTHING",
        values,
    )
    db.commit()
