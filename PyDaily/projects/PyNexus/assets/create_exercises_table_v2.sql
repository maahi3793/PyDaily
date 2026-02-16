-- Migration: Upgrade Exercises Table for Practice Engine v2
-- Run this in the Supabase SQL Editor

-- 1. Ensure Table Exists (Idempotent)
CREATE TABLE IF NOT EXISTS exercises (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    day_number INT NOT NULL,
    filename TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Add New Columns (Safe Alter)
ALTER TABLE exercises 
ADD COLUMN IF NOT EXISTS source TEXT DEFAULT 'textbook', -- 'textbook', 'daily_mail', 'boss_battle'
ADD COLUMN IF NOT EXISTS title TEXT, -- Short display title
ADD COLUMN IF NOT EXISTS topic TEXT, -- Topic Name (e.g. "Lists")
ADD COLUMN IF NOT EXISTS description TEXT, -- Markdown problem statement
ADD COLUMN IF NOT EXISTS difficulty TEXT DEFAULT 'Easy', -- 'Easy', 'Medium', 'Hard', 'Scenario'
ADD COLUMN IF NOT EXISTS starter_code TEXT, -- Boilerplate for student
ADD COLUMN IF NOT EXISTS test_code TEXT,    -- Hidden pytest code
ADD COLUMN IF NOT EXISTS solution_code TEXT, -- For reference
ADD COLUMN IF NOT EXISTS xp_reward INT DEFAULT 10;

-- 3. Enable RLS (Security)
ALTER TABLE exercises ENABLE ROW LEVEL SECURITY;

-- 4. Policy: Authenticated Users can READ (Safe Re-run)
DROP POLICY IF EXISTS "Enable read access for all users" ON exercises;
CREATE POLICY "Enable read access for all users" ON exercises 
FOR SELECT USING (auth.role() = 'authenticated');

-- 5. Policy: Service Role can ALL (Safe Re-run)
DROP POLICY IF EXISTS "Enable all access for service role" ON exercises;
CREATE POLICY "Enable all access for service role" ON exercises 
FOR ALL USING (auth.role() = 'service_role');

