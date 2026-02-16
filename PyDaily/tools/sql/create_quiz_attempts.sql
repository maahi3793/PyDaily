-- NEW TABLE: quiz_attempts
-- Logs EVERY attempt for deep analytics (not just the latest/best score)

CREATE TABLE IF NOT EXISTS quiz_attempts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    student_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    day INTEGER NOT NULL,
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    answers_json JSONB DEFAULT '{}'::jsonb,
    feedback_sent BOOLEAN DEFAULT FALSE,
    submitted_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Security
ALTER TABLE quiz_attempts ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can insert their own attempts" 
ON quiz_attempts FOR INSERT 
WITH CHECK (auth.uid() = student_id);

CREATE POLICY "Users can view their own attempts" 
ON quiz_attempts FOR SELECT 
USING (auth.uid() = student_id);

-- Indexes for Speed
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_student_day ON quiz_attempts(student_id, day);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_feedback ON quiz_attempts(feedback_sent) WHERE feedback_sent = FALSE;
