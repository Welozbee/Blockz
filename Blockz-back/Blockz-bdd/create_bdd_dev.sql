DROP TABLE IF EXISTS blocks;

CREATE TABLE IF NOT EXISTS blocks (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL DEFAULT '0',
  displayName TEXT NOT NULL DEFAULT '0',
  hardness REAL NOT NULL DEFAULT 0,
  resistance REAL NOT NULL DEFAULT 0,
  stackSize INTEGER NOT NULL DEFAULT 0,
  diggable INTEGER NOT NULL DEFAULT 0,
  material TEXT NOT NULL DEFAULT '0',
  transparent INTEGER NOT NULL DEFAULT 0,
  emitLight INTEGER NOT NULL DEFAULT 0
);