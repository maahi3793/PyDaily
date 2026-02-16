-- Execute this in your Supabase SQL Editor to create the 'exercises' table
CREATE TABLE IF NOT EXISTS exercises (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    day_number INT NOT NULL,
    filename TEXT NOT NULL, -- e.g. "loop_practice.py"
    starter_code TEXT, -- The scaffolding
    solution_code TEXT,
    test_code TEXT -- Pytest code
);
