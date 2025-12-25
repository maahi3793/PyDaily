
-- Create a table to store Quiz Performance
create table public.quiz_results (
  id uuid default gen_random_uuid() primary key,
  student_id uuid references auth.users(id) on delete cascade not null,
  day int not null,
  score int not null,
  total_questions int not null,
  answers_json jsonb, -- Stores the full answer map keys: question_id, values: user_choice
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- RLS Policies
alter table public.quiz_results enable row level security;

-- 1. Students can INSERT their own results
create policy "Students can insert their own results"
on public.quiz_results for insert
to authenticated
with check ( auth.uid() = student_id );

-- 2. Students can VIEW their own results
create policy "Students can view their own results"
on public.quiz_results for select
to authenticated
using ( auth.uid() = student_id );

-- 3. Admins (Service Role) can VIEW ALL
-- (Service Role bypasses RLS, but if using an Admin *User*, we need a policy)
-- Assuming we use Service Role Key for the "Nightly Job", we are fine.
