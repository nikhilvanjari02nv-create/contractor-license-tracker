"""
Contractor License Renewal Rules Database
Verified against official state sources — see 'source' field for each entry.
Last verified: July 2026. Re-verify periodically; rules change (e.g. GA's 2026 CE Broker mandate).
"""

RULES = {
    "Texas": {
        "Journeyman Electrician": {
            "cycle": "annual",
            "cycle_months": 12,
            "ce_hours_required": 4,
            "ce_note": "4 hours per year, National Electrical Code + Safety (NFPA 70E)",
            "renewal_fee_usd": 30,
            "authority": "Texas Department of Licensing and Regulation (TDLR)",
            "source": "https://www.tdlr.texas.gov/electricians/renew/businesses/contractor-elec.htm",
        },
        "Master Electrician": {
            "cycle": "annual",
            "cycle_months": 12,
            "ce_hours_required": 4,
            "ce_note": "4 hours per year, National Electrical Code + Safety (NFPA 70E)",
            "renewal_fee_usd": 45,
            "authority": "Texas Department of Licensing and Regulation (TDLR)",
            "source": "https://www.tdlr.texas.gov/electricians/",
        },
        "Electrical Contractor": {
            "cycle": "annual",
            "cycle_months": 12,
            "ce_hours_required": 0,
            "ce_note": "Contractors and Residential Appliance Installers are exempt from CE",
            "renewal_fee_usd": 110,
            "authority": "Texas Department of Licensing and Regulation (TDLR)",
            "source": "https://www.tdlr.texas.gov/electricians/",
        },
    },
    "Georgia": {
        "Electrical Contractor (Class I - Restricted)": {
            "cycle": "biennial",
            "cycle_months": 24,
            "fixed_expiration": "June 30 (even-numbered years)",
            "ce_hours_required": 8,
            "ce_note": "4 hours/year = 8 hours per 2-year cycle. AS OF JAN 1 2026: must log hours in CE Broker (new requirement, high audit risk if missed).",
            "renewal_fee_usd": 75,
            "authority": "Georgia Construction Industry Licensing Board (CILB) / Secretary of State",
            "source": "https://sos.ga.gov/page/board-electrical-contractors-faq",
        },
        "Electrical Contractor (Class II - Unrestricted)": {
            "cycle": "biennial",
            "cycle_months": 24,
            "fixed_expiration": "June 30 (even-numbered years)",
            "ce_hours_required": 8,
            "ce_note": "4 hours/year = 8 hours per 2-year cycle. AS OF JAN 1 2026: must log hours in CE Broker (new requirement, high audit risk if missed).",
            "renewal_fee_usd": 75,
            "authority": "Georgia Construction Industry Licensing Board (CILB) / Secretary of State",
            "source": "https://sos.ga.gov/page/board-electrical-contractors-faq",
        },
    },
    "Florida": {
        "Certified Electrical Contractor (EC)": {
            "cycle": "biennial",
            "cycle_months": 24,
            "fixed_expiration": "August 31 (even-numbered years)",
            "ce_hours_required": 11,
            "ce_note": "7 technical (incl. 1hr Building Code Advanced Module) + 1hr workers' comp + 1hr workplace safety + 1hr business practices + 1hr laws & rules. +2hrs false alarm prevention if performing alarm work.",
            "renewal_fee_usd": 209,
            "authority": "Florida Dept. of Business & Professional Regulation (DBPR) - Electrical Contractors' Licensing Board",
            "source": "https://www2.myfloridalicense.com/electrical-contractors/faqs/",
            "note": "Statewide license. Journeyman/Master licenses in Florida are issued LOCALLY by county/municipality, NOT by the state — do not apply this rule to journeyman-level clients.",
        },
        "Registered Electrical Contractor (ER)": {
            "cycle": "biennial",
            "cycle_months": 24,
            "fixed_expiration": "August 31 (even-numbered years)",
            "ce_hours_required": 11,
            "ce_note": "Same breakdown as Certified. Work authority limited to specific local jurisdictions only.",
            "renewal_fee_usd": 209,
            "authority": "Florida Dept. of Business & Professional Regulation (DBPR) - Electrical Contractors' Licensing Board",
            "source": "https://www2.myfloridalicense.com/electrical-contractors/faqs/",
            "note": "Local-jurisdiction limited license, not statewide.",
        },
    },
}

TRADE = "Electrician"  # MVP scope — single trade, 3 states
