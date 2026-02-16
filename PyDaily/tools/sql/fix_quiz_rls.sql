-- FIX: Allow Students to UPDATE their own quiz results (Retakes)
-- Run this in the Supabase SQL Editor

-- 1. Enable RLS (Ensure it's on)
ALTER TABLE quiz_results ENABLE ROW LEVEL SECURITY;

-- 2. Drop existing restrictive policies (Best guess names, or generic drop to be safe)
-- We use DO generic block to avoid errors if policies don't exist, 
-- but standard SQL is just simpler: we add a NEW broad policy.

-- Policy: Allow INSERT (User can create their own row)
CREATE POLICY "Users can insert their own results" 
ON quiz_results FOR INSERT 
WITH CHECK (auth.uid() = student_id);

-- Policy: Allow UPDATE (User can update their own row) - THIS WAS MISSING
CREATE POLICY "Users can update their own results" 
ON quiz_results FOR UPDATE 
USING (auth.uid() = student_id)
WITH CHECK (auth.uid() = student_id);

-- Policy: Allow SELECT (User can see their own history)
CREATE POLICY "Users can view their own results" 
ON quiz_results FOR SELECT 
USING (auth.uid() = student_id);
