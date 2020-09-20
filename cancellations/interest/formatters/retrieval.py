# stdlib
from datetime import datetime, timedelta

# 3rd Party

# local
from cancellations.interest import crud


def _format_cancellations_for_display(cancellations):
    response_body = []
    for cancellation in cancellations:
        response_body.append({
            "meta": {
                "name": cancellation.name,
                "abbrev": cancellation.abbrev,
                "location_name": cancellation.location_name,
                "state": cancellation.state
            },
            "lat_deg": cancellation.lat_deg,
            "long_deg": cancellation.long_deg
        })
    return response_body


def get_formatted_points_of_interest(db, skip, limit):
    cancellations = crud.get_points_of_interest(db, skip=skip, limit=limit)
    return _format_cancellations_for_display(cancellations)

