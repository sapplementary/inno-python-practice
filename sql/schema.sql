CREATE TABLE IF NOT EXISTS rooms (
    id   INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
    id       INTEGER PRIMARY KEY,
    name     VARCHAR(200) NOT NULL,
    birthday DATE NOT NULL,
    sex      CHAR(1) NOT NULL CHECK (sex IN ('M', 'F')),
    room_id  INTEGER NOT NULL REFERENCES rooms (id)
);
