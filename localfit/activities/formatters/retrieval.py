# 3rd Party
import pytz

# local
from localfit.db.crud import get_activity_by_filename
from localfit.utilities import localize_datetime_for_display, format_datetime_for_display


def get_activity_metadata_by_filename(db, filename):
    """
    TODO: Support secondary activities

    """
    activity = get_activity_by_filename(db, filename)
    return {
        'activity_type': activity.activity_type,
        'start_time_utc': format_datetime_for_display(localize_datetime_for_display(activity.start_time_utc)),
        'activity_collection': activity.activity_collection,
        'total_elapsed_time': activity.total_elapsed_time,
        'total_distance': activity.total_distance,
        'total_calories': activity.total_calories,
        'start_location': activity.start_location,
    }

