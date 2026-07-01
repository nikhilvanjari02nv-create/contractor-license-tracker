"""
Renewal date calculation engine.
Handles both simple annual cycles (Texas) and fixed-date biennial cycles (Georgia, Florida).
"""

from datetime import date, timedelta
import calendar


def calculate_next_renewal(state, license_type, last_renewal_date, rules):
    """
    Given a state, license type, and last renewal date, return the next renewal deadline.
    Handles two patterns:
      1. Rolling annual (e.g. Texas): next_date = last_renewal_date + 1 year
      2. Fixed biennial date (e.g. Georgia June 30, Florida Aug 31 even years):
         next_date = the next occurrence of that fixed date on the correct even/odd year cycle
    """
    rule = rules[state][license_type]

    if rule["cycle"] == "annual":
        # Rolling: same month/day, next year
        try:
            next_date = last_renewal_date.replace(year=last_renewal_date.year + 1)
        except ValueError:
            # handles Feb 29 edge case
            next_date = last_renewal_date.replace(
                year=last_renewal_date.year + 1, day=28
            )
        return next_date

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
