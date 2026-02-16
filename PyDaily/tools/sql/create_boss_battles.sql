-- Boss Battles Table
-- Stores high-difficulty "Real World" scenarios separate from daily drills.

create table boss_battles (
  id uuid default gen_random_uuid() primary key,
  day int not null,
  topic text not null,
  title text not null,
  scenario text not null, -- The "Real World" context (Markdown)
  requirements jsonb not null, -- List of specific requirements (Array of Strings)
  hints jsonb, -- Optional hints (Array of Strings)
  created_at timestamp with time zone default now()
);

-- Index for faster lookup by day
create index idx_boss_battles_day on boss_battles(day);

-- RLS: Read-Only for Students
alter table boss_battles enable row level security;

-- Policy: Everyone (Students) can read questions
create policy "Students can read battles" 
on boss_battles for select 
using (true);

-- Policy: Service Role (Admin) has full access (Implicit in Supabase, but good to be explicit if using admin user)
-- Note: Service Role bypasses RLS, so this is mainly for clarity.
