# 🛡️ LicenseGuard

Never miss a contractor license renewal again. Automated tracking for electricians in TX, GA & FL — built with Streamlit and Supabase.

---

## What it does

LicenseGuard tracks contractor license renewals so nothing slips through the cracks:

1. **Add a business** — name, client email, state, license type, and last renewal date
2. **Auto-calculate the next renewal deadline** — handles two different renewal patterns automatically:
   - **Rolling** (e.g. Texas, North Carolina — annual; Tennessee — every 2 years): next deadline = last renewal + cycle length
   - **Fixed biennial date** (e.g. Georgia — every June 30; Florida — every Aug 31 on even years): next deadline = the correct upcoming fixed date
3. **See status at a glance** — every tracked license is color-coded: 🔴 Urgent (≤30 days), 🟡 Due Soon (31–60 days), 🟢 On Track (60+ days)
4. **View full requirements per license** — CE hours required, renewal fee, licensing authority, and a 60/30/7-day reminder schedule
5. **Remove entries** you no longer need to track

---

## Features

- Dashboard with summary counts (urgent / due soon / on track)
- Full sortable table of every tracked license
- Expandable detail view per business — deadline, CE hours, fee, authority, reminder dates
- State-specific rules engine (`rules_data.py`) — easy to extend with more states or license types
- Renewal-date math that correctly handles month-end edge cases and even/odd year cycles
- Backed by Supabase, so data persists across sessions

---

## Tech stack

- [Streamlit](https://streamlit.io/) — UI
- [Supabase](https://supabase.com/) — database
- [pandas](https://pandas.pydata.org/) — table display and sorting

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/nikhilvanjari02nv-create/contractor-license-tracker.git
cd contractor-license-tracker
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2. Set up Supabase

- Create a project at [supabase.com](https://supabase.com/)
- Go to **SQL Editor → New Query**, paste in the contents of `supabase_schema.sql`, and run it
- This creates the `businesses` table that stores every tracked license

> **Note:** the app also reads/writes a `client_email` field per business. If you hit an error inserting a new entry, add that column manually in Supabase: `alter table businesses add column client_email text;`

### 3. Add your Supabase credentials

Create `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "your_supabase_project_url"
SUPABASE_KEY = "your_supabase_anon_or_service_key"
```

### 4. Run it

```bash
streamlit run app.py
```

---

## How to use

1. In the sidebar, enter the business name, client email, state, license type, and last renewal date
2. Click **Add to Tracker** — the next renewal date is calculated automatically
3. The dashboard shows all tracked licenses, sorted by urgency
4. Click any entry to expand full details: CE requirements, fees, licensing authority, and reminder dates
5. Delete an entry from its expanded view when it's no longer needed

---

## Extending it

- Add more states/license types by editing `rules_data.py`
- Renewal math for both rolling and fixed-date cycles lives in `renewal_logic.py` — reusable if you add new states with different renewal patterns

---

## Disclaimer

LicenseGuard provides informational tracking only, not legal advice. Always verify deadlines and requirements with the official state licensing authority.

---

## License

MIT — free to use, modify, and build on.

---

## About

Built by [Nikhil Vanjari](https://linkedin.com/in/nikhil-vanjari-7006a0204).
