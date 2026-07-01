import streamlit as st
from datetime import date
import pandas as pd

from rules_data import RULES
from renewal_logic import calculate_next_renewal, days_until, get_status, get_reminder_schedule

st.set_page_config(page_title="Contractor License Renewal Tracker", page_icon="🛠️", layout="wide")

st.title("🛠️ Contractor License Renewal Tracker")
st.caption("MVP — Electricians in TX, GA, FL. Never miss a renewal deadline again.")

# --- In-memory storage for MVP (replace with Supabase before real launch) ---
if "businesses" not in st.session_state:
    st.session_state.businesses = []

# --- Sidebar: Add a business ---
with st.sidebar:
    st.header("➕ Add a License to Track")
    business_name = st.text_input("Business / Contractor Name")
    state = st.selectbox("State", list(RULES.keys()))
    license_type = st.selectbox("License Type", list(RULES[state].keys()))
    last_renewal = st.date_input("Last Renewal Date", value=date.today())

    if st.button("Add to Tracker", type="primary"):
        if business_name:
            next_date = calculate_next_renewal(state, license_type, last_renewal, RULES)
            st.session_state.businesses.append({
                "business_name": business_name,
                "state": state,
                "license_type": license_type,
                "last_renewal": last_renewal,
                "next_renewal": next_date,
            })
            st.success(f"Added {business_name}! Next renewal: {next_date.strftime('%B %d, %Y')}")
        else:
            st.error("Please enter a business name.")

    st.divider()
    st.caption("Data sources verified against official state licensing boards. See rules_data.py for citations.")

# --- Main dashboard ---
if not st.session_state.businesses:
    st.info("👈 Add your first license using the sidebar to see it appear on the dashboard here.")
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
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Detail view per business
    st.divider()
    st.subheader("📋 Renewal Details")
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

st.divider()
st.caption("⚠️ This tool provides informational tracking only, not legal advice. Always verify with the official licensing authority before your deadline.")
