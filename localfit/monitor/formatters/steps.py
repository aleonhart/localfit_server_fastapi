# local
from localfit.monitor import crud


GOAL_STEPS_PER_DAY = 5000


def format_steps_for_display(start_date, end_date, db):
    records = crud.get_monitor_steps_by_date(start_date, end_date, db)

    return {
        "start_date": start_date,
        "end_date": end_date,
        "steps": [
            {
                "t": record.step_date,
                "y": record.steps
            } for record in records
        ]
    }


def get_percent_step_goal_achievement(year, month, days_in_month, db):
    step_data = crud.get_monitor_step_goal(year, month, days_in_month, db)
    actual_total_steps = sum([s.steps for s in step_data])
    goal_total_steps = GOAL_STEPS_PER_DAY * days_in_month
    return {
        'monthly_step_goal_percent_completed': round((actual_total_steps / goal_total_steps), 2)
    }
