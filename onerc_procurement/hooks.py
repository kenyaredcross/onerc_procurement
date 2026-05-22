app_name = "onerc_procurement"
app_title = "KRCS Supplier Prequalification"
app_publisher = "Kelvin Njenga"
app_description = "Supplier Prequalification Platform for Kenya Red Cross Society"
app_email = "njengasheba@gmail.com"
app_license = "mit"

# Fixtures — loaded via: bench --site <site> import-fixtures --app onerc_procurement
# Exported via:          bench --site <site> export-fixtures --app onerc_procurement
fixtures = [
    # ── Roles ───────────────────────────────────────────────────────────────
    {
        "doctype": "Role",
        "filters": [
            ["name", "in", [
                "Prequal Admin",
                "Prequal Evaluator",
                "Prequal Compliance",
                "Prequal Read Only",
                "Supplier",
            ]]
        ]
    },
    # ── Seed / configuration data (safe to re-import on every migrate) ──────
    {"doctype": "Prequal Category"},
    {"doctype": "Question Section"},
    {"doctype": "Question"},
    # ── Test / demo data (identified by name — will not touch other records) ─
    {
        "doctype": "Prequal Exercise",
        "filters": [["name", "in", [
            "EX-2024-001", "EX-2025-001",
            "EX-2026-001", "EX-2026-002", "EX-2026-003",
        ]]]
    },
    {
        "doctype": "Supplier Profile",
        "filters": [["name", "in", [
            "SUPP-2026-00001", "SUPP-2026-00002", "SUPP-2026-00003",
            "SUPP-2026-00004", "SUPP-2026-00005",
        ]]]
    },
    {
        "doctype": "Prequal Application",
        "filters": [["name", "in", [
            "APP-2026-00001", "APP-2026-00002", "APP-2026-00003",
            "APP-2026-00004", "APP-2026-00005",
            "APP-2025-00001", "APP-2025-00002",
        ]]]
    },
    {
        "doctype": "Payment Transaction",
        "filters": [["name", "in", [
            "PAY-2026-00001", "PAY-2026-00002", "PAY-2026-00003",
            "PAY-2026-00004", "PAY-2026-00005",
            "PAY-2025-00001", "PAY-2025-00002",
        ]]]
    },
]

# Scheduled Tasks
scheduler_events = {
    "hourly": [
        "onerc_procurement.api.payment.check_pending_payments",
    ],
    "daily": [
        "onerc_procurement.api.exercise.auto_close_exercises",
        "onerc_procurement.api.exercise.send_deadline_reminders",
    ],
}

# Document Events
doc_events = {
    "Score Sheet": {
        "on_submit": "onerc_procurement.api.evaluation.on_score_submit",
    },
    "Compliance Record": {
        "on_submit": "onerc_procurement.api.compliance.on_compliance_submit",
    },
}

# Expose M-Pesa callback as a public (guest) endpoint
override_whitelisted_methods = {
    "onerc_procurement.api.payment.mpesa_callback": "onerc_procurement.api.payment.mpesa_callback",
}

# After install hook
after_install = "onerc_procurement.setup.after_install"
