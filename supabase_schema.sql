-- Run this in Supabase Dashboard -> SQL Editor -> New Query -> Run
-- Creates the table that stores every tracked license/business.

create table if not exists businesses (
    id uuid primary key default gen_random_uuid(),
    business_name text not null,
    state text not null,
    license_type text not null,
    last_renewal date not null,
    next_renewal date not null,
    created_at timestamp with time zone default now()
);

-- Enable Row Level Security (Supabase best practice, even for MVP)
alter table businesses enable row level security;

-- MVP policy: allow all reads/writes via the public anon key.
-- Fine for now since you're the only user testing this.
-- Before onboarding real clients with private data, replace this with
-- per-user policies (e.g. tied to auth.uid()) so one client can't see another's data.
create policy "Allow all access for MVP"
on businesses
for all
using (true)
with check (true);
