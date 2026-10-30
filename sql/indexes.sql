CREATE INDEX IF NOT EXISTS idx_students_room_id
    ON students (room_id);

CREATE INDEX IF NOT EXISTS idx_students_room_birthday
    ON students (room_id, birthday);

CREATE INDEX IF NOT EXISTS idx_students_room_sex
    ON students (room_id, sex);
