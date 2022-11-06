CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS songs (
    rowid INTEGER PRIMARY KEY,
    file_name text,
    title text,
    album text,
    meta_json text,
    musicnn_max_pool blob
);

CREATE UNIQUE INDEX IF NOT EXISTS songs_file_name ON songs(file_name);

CREATE TABLE IF NOT EXISTS vic_coords (
    song INTEGER PRIMARY KEY,
    x REAL,
    y REAL
);
"""

DROP_TABLES = """
DROP INDEX IF EXISTS songs_file_name;
DROP TABLE IF EXISTS songs;
DROP TABLE IF EXISTS vic_coords;
"""
