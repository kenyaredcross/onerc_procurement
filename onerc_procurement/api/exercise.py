"""Prequal Exercise lifecycle automation stubs."""
import frappe


def auto_close_exercises():
    """Scheduler task — daily.

    Find Published exercises whose close_date has passed and set status to Closed.
    Also lock applications (edit_locked=1) for those exercises.
    """
    # TODO Phase 2: implement auto-close logic
    pass


def send_deadline_reminders():
    """Scheduler task — daily.

    Send email/SMS reminders to suppliers who have Active (payment made but
    not yet submitted) applications for exercises closing within
    exercise.reminder_days_before days.
    """
    # TODO Phase 2: implement reminder sending
    pass
