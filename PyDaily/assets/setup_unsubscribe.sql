-- Add Subscription Columns to Profiles
ALTER TABLE profiles 
ADD COLUMN IF NOT EXISTS sub_morning BOOLEAN DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS sub_evening BOOLEAN DEFAULT TRUE;

-- Function to safely update preferences (Accessible via RPC if needed, or direct update)
-- We will use direct update via Streamlit Service Role or Authenticated User.

-- Ensure RLS allows users to update their own profile (usually standard, but good to verify)
-- If you have a specific policy for UPDATE, ensure it covers these columns.
-- Example Policy (if not exists):
-- CREATE POLICY "Users can update own profile" ON profiles FOR UPDATE USING (auth.uid() = id);
