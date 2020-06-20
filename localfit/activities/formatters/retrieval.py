# 3rd Party
import pytz

# local
from localfit.db.crud import get_activity_by_filename, get_activity_records_by_filename
from localfit.utilities import localize_datetime_for_display, format_datetime_for_display, calculate_geographic_midpoint


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


def get_activity_map_by_filename(db, filename):
    records = get_activity_records_by_filename(db, filename)

    # not every record has GPS data. remove all null GPS records.
    records = list(filter((None).__ne__, records))

    # get geographic midpoint to center the map
    midpoint_lat_deg, midpoint_long_deg = calculate_geographic_midpoint(records)

    return {
        'activitydata': records,
        'midpoint_lat_deg': midpoint_lat_deg,
        'midpoint_long_deg': midpoint_long_deg
    }
