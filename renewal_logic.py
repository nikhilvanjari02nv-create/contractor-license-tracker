"""
Renewal date calculation engine.
Handles two patterns:
  1. Rolling (e.g. Texas=12mo, NC=12mo, Tennessee=24mo): next_date = last_renewal_date + cycle_months
  2. Fixed biennial date (e.g. Georgia June 30, Florida Aug 31 even years):
     next_date = the next occurrence of that fixed date on the correct even/odd year cycle
"""

from datetime import date, timedelta
import calendar


def _add_months(d, months):
    """Add a number of months to a date, handling year rollover and month-end edge cases."""
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def calculate_next_renewal(state, license_type, last_renewal_date, rules):
    """
    Given a state, license type, and last renewal date, return the next renewal deadline.
    """
    rule = rules[state][license_type]

    if rule["cycle"] == "annual":
        # Rolling: same day-of-month, cycle_months later (12 for TX/NC, 24 for TN)
        months = rule.get("cycle_months", 12)
        return _add_months(last_renewal_date, months)

    elif rule["cycle"] == "biennial":
        fixed_exp = rule.get("fixed_expiration", "")
        # Parse "June 30 (even-numbered years)" style strings
        month_name = fixed_exp.split(" ")[0]
        day = int(fixed_exp.split(" ")[1].replace(",", ""))
        month = list(calendar.month_name).index(month_name)

        # Find the next even year on/after last_renewal_date that is >= last_renewal_date
        year = last_renewal_date.year
        if year % 2 != 0:
            year += 1
        candidate = date(year, month, day)
        while candidate <= last_renewal_date:
            candidate = date(candidate.year + 2, month, day)
        return candidate

    else:
        raise ValueError(f"Unknown cycle type: {rule['cycle']}")


def days_until(target_date, today=None):
    if today is None:
        today = date.today()
    return (target_date - today).days


def get_status(days_remaining):
    """Traffic-light status for the dashboard."""
    if days_remaining < 0:
        return "🔴 EXPIRED", "red"
    elif days_remaining <= 30:
        return "🔴 URGENT", "red"
    elif days_remaining <= 60:
        return "🟡 DUE SOON", "orange"
    else:
        return "🟢 OK", "green"


def get_reminder_schedule(next_renewal_date):
    """Returns the 3 reminder trigger dates: 60/30/7 days before deadline."""
    return {
        "60_day": next_renewal_date - timedelta(days=60),
        "30_day": next_renewal_date - timedelta(days=30),
        "7_day": next_renewal_date - timedelta(days=7),
    }
