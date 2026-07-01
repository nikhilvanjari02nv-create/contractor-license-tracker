import streamlit as st
from datetime import date
import pandas as pd
from supabase import create_client

from rules_data import RULES
from renewal_logic import calculate_next_renewal, days_until, get_status, get_reminder_schedule

st.set_page_config(page_title="LicenseGuard — Compliance Tracker", page_icon="🛡️", layout="wide")

# --- Custom CSS polish ---
st.markdown("""
<style>
    .main .block-container { padding-top: 2rem; }
    [data-testid="stMetric"] {
        background-color: #F4F7FA;
        border: 1px solid #E3E9EF;
        border-radius: 10px;
        padding: 16px 12px;
    }
    [data-testid="stMetricLabel"] { font-size: 0.85rem; }
    div[data-testid="stExpander"] {
        border: 1px solid #E3E9EF;
        border-radius: 10px;
        margin-bottom: 8px;
    }
    .lg-tagline {
        color: #5A6B7B;
        font-size: 1.05rem;
        margin-top: -8px;
        margin-bottom: 1.5rem;
    }
    .lg-badge {
        display: inline-block;
        background-color: #EAF2F8;
        color: #1E5F8C;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## 🛡️ LicenseGuard")
st.markdown(
    '<p class="lg-tagline">Never miss a contractor license renewal again. '
    'Automated tracking for electricians in TX, GA & FL. '
    '<span class="lg-badge">MVP</span></p>',
    unsafe_allow_html=True,
)

# --- Supabase connection ---
# Reads from Streamlit secrets — never hardcode keys directly in this file.
@st.cache_resource
def get_supabase_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = get_supabase_client()
except Exception:
    st.error("Supabase connection not configured. Add SUPABASE_URL and SUPABASE_KEY to your Streamlit secrets.")
    st.stop()


def load_businesses():
    response = supabase.table("businesses").select("*").execute()
    businesses = []
    for row in response.data:
        businesses.append({
            "id": row["id"],
            "business_name": row["business_name"],
            "state": row["state"],
            "license_type": row["license_type"],
            "last_renewal": date.fromisoformat(row["last_renewal"]),
            "next_renewal": date.fromisoformat(row["next_renewal"]),
        })
    return businesses


def add_business(business_name, state, license_type, last_renewal, next_renewal):
    supabase.table("businesses").insert({
        "business_name": business_name,
        "state": state,
        "license_type": license_type,
        "last_renewal": last_renewal.isoformat(),
        "next_renewal": next_renewal.isoformat(),
    }).execute()


def delete_business(business_id):
    supabase.table("businesses").delete().eq("id", business_id).execute()


st.session_state.businesses = load_businesses()

# --- Sidebar: Add a business ---
with st.sidebar:
    st.markdown("### ➕ Track a New License")
    st.caption("Add a contractor to start monitoring their renewal.")
    business_name = st.text_input("Business or Contractor Name", placeholder="e.g. Rodriguez Electrical LLC")
    state = st.selectbox("State", list(RULES.keys()))
    license_type = st.selectbox("License Type", list(RULES[state].keys()))
    last_renewal = st.date_input("Last Renewal Date", value=date.today())

    if st.button("Add to Tracker", type="primary", use_container_width=True):
        if business_name:
            next_date = calculate_next_renewal(state, license_type, last_renewal, RULES)
            add_business(business_name, state, license_type, last_renewal, next_date)
            st.success(f"Added! Next renewal: {next_date.strftime('%B %d, %Y')}")
            st.rerun()
        else:
            st.error("Please enter a business name.")

    st.divider()
    st.caption("🔒 Data sourced from official state licensing boards.")

# --- Main dashboard ---
if not st.session_state.businesses:
    st.info("👈 **Add your first license using the sidebar** to see it appear on your dashboard here. Takes about 15 seconds.")
else:
    rows = []
    for b in st.session_state.businesses:
        days_left = days_until(b["next_renewal"])
        status_label, status_color = get_status(days_left)
        rule = RULES[b["state"]][b["license_type"]]
        rows.append({
            "Business": b["business_name"],
            "State": b["state"],
            "License Type": b["license_type"],
            "Next Renewal": b["next_renewal"].strftime("%b %d, %Y"),
            "Days Left": days_left,
            "Status": status_label,
            "CE Hours Needed": rule["ce_hours_required"],
            "Renewal Fee": f"${rule['renewal_fee_usd']}",
        })

    df = pd.DataFrame(rows).sort_values("Days Left")

    # Summary metrics
    col1, col2, col3 = st.columns(3)
    urgent_count = len(df[df["Days Left"] <= 30])
    soon_count = len(df[(df["Days Left"] > 30) & (df["Days Left"] <= 60)])
    ok_count = len(df[df["Days Left"] > 60])
    col1.metric("🔴 Urgent (≤30 days)", urgent_count)
    col2.metric("🟡 Due Soon (31-60 days)", soon_count)
    col3.metric("🟢 On Track (60+ days)", ok_count)

    st.divider()
    st.markdown("#### 📊 All Tracked Licenses")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Detail view per business
    st.divider()
    st.markdown("#### 📋 Renewal Details")
    st.caption("Click any row to see full requirements, fees, and the reminder schedule.")
    for b in st.session_state.businesses:
        rule = RULES[b["state"]][b["license_type"]]
        days_left = days_until(b["next_renewal"])
        status_label, _ = get_status(days_left)
        with st.expander(f"{status_label} — {b['business_name']} ({b['state']}, {b['license_type']})"):
            st.write(f"**Next Renewal Deadline:** {b['next_renewal'].strftime('%B %d, %Y')} ({days_left} days)")
            st.write(f"**CE Requirement:** {rule['ce_hours_required']} hours — {rule.get('ce_note', '')}")
            st.write(f"**Renewal Fee:** ${rule['renewal_fee_usd']}")
            st.write(f"**Authority:** {rule['authority']}")
            if rule.get("note"):
                st.warning(rule["note"])
            reminders = get_reminder_schedule(b["next_renewal"])
            st.write("**Reminder Schedule:**")
            for label, d in reminders.items():
                st.write(f"- {label.replace('_', ' ').title()}: {d.strftime('%B %d, %Y')}")
            st.caption(f"Source: {rule['source']}")
            if st.button("🗑️ Delete this entry", key=f"delete_{b['id']}"):
                delete_business(b["id"])
                st.rerun()

st.divider()
st.caption("🛡️ LicenseGuard provides informational tracking only, not legal advice. Always verify with the official licensing authority before your deadline.")
