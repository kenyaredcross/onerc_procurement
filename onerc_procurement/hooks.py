app_name = "onerc_procurement"
app_title = "KRCS Supplier Prequalification"
app_publisher = "Kelvin Njenga"
app_description = "Supplier Prequalification Platform for Kenya Red Cross Society"
app_email = "njengasheba@gmail.com"
app_license = "mit"

# Fixtures — export roles on bench export-fixtures
fixtures = [
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
    }
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
