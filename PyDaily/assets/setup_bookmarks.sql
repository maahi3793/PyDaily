-- Bookmarks Table for PyDaily
-- Allows students to mark favorite lessons for quick access

-- Drop if exists (for clean re-run)
DROP TABLE IF EXISTS bookmarks;

-- Create bookmarks table
CREATE TABLE bookmarks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_email TEXT NOT NULL,
    lesson_day INT NOT NULL,
    notes TEXT DEFAULT '',  -- Optional user notes
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Prevent duplicate bookmarks for same user + day
    UNIQUE(user_email, lesson_day)
);

-- Create index for fast lookup by user
CREATE INDEX idx_bookmarks_user ON bookmarks(user_email);

-- Enable RLS
ALTER TABLE bookmarks ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own bookmarks
CREATE POLICY "Users can view own bookmarks" ON bookmarks
    FOR SELECT USING (auth.email() = user_email);

-- Policy: Users can add their own bookmarks
CREATE POLICY "Users can add own bookmarks" ON bookmarks
    FOR INSERT WITH CHECK (auth.email() = user_email);

-- Policy: Users can delete their own bookmarks
CREATE POLICY "Users can delete own bookmarks" ON bookmarks
    FOR DELETE USING (auth.email() = user_email);

-- Policy: Service role can do anything (for admin operations)
CREATE POLICY "Service role full access" ON bookmarks
    FOR ALL USING (auth.role() = 'service_role');
