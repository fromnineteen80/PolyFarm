-- PolyFarm Dashboard — Investor Profile System
-- Run this in Supabase SQL Editor before deploying

-- New table: investor profiles
CREATE TABLE IF NOT EXISTS investor_profiles (
  id BIGSERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  display_name TEXT,
  profile_photo_url TEXT,
  initial_capital DECIMAL(10,2),
  intended_capital DECIMAL(10,2),
  joined_date DATE NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
ALTER TABLE investor_profiles DISABLE ROW LEVEL SECURITY;

-- Add new columns to existing investors table
ALTER TABLE investors ADD COLUMN IF NOT EXISTS profile_photo_url TEXT;
ALTER TABLE investors ADD COLUMN IF NOT EXISTS display_name TEXT;
-- email column may already exist from bot schema
DO $$ BEGIN
  ALTER TABLE investors ADD COLUMN email TEXT;
EXCEPTION WHEN duplicate_column THEN NULL;
END $$;

-- Create storage bucket for profile photos
-- Run this via Supabase Dashboard → Storage → New Bucket:
--   Name: profile-photos
--   Public: Yes
--   File size limit: 5MB
--   Allowed MIME types: image/jpeg, image/png, image/webp
