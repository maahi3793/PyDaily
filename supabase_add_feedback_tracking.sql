-- Add tracking for Automated AI Feedback
alter table public.quiz_results 
add column feedback_sent boolean default false;
