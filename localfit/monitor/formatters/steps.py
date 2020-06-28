# local
from localfit.monitor import crud


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
