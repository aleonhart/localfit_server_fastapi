# stdlib
from datetime import datetime, timedelta

# 3rd Party

# local
from localfit.activities import crud
from localfit.utilities import (localize_datetime_for_display, format_datetime_for_display,
                                format_distance_for_display, calculate_geographic_midpoint,
                                format_duration_for_display)


def get_activity_metadata_by_filename(db, filename):
    """
    TODO: Support secondary activities

    """
    activity = crud.get_activity_by_filename(db, filename)
    return {
        'activity_type': activity.activity_type,
        'start_time_utc': format_datetime_for_display(localize_datetime_for_display(activity.start_time_utc)),
        'activity_collection': activity.activity_collection,
        'total_timer_time': format_duration_for_display(activity.total_timer_time),
        'total_distance': format_distance_for_display(activity.total_distance),
        'total_calories': activity.total_calories,
        'start_location': activity.start_location,
    }


def get_activity_map_by_filename(db, filename):
    gps_records = crud.get_activity_gps_records_by_filename(db, filename)

    # get geographic midpoint to center the map
    midpoint_lat_deg, midpoint_long_deg = calculate_geographic_midpoint(gps_records)

    return {
        'activitydata': gps_records,
        'midpoint_lat_deg': midpoint_lat_deg,
        'midpoint_long_deg': midpoint_long_deg
    }


def format_activity_maps_by_collection(db, collection_name, skip, limit):
    maps = crud.get_activity_maps_by_collection(db, collection_name=collection_name, skip=skip, limit=limit)

    total_coordinates = []
    activities = []
    for map in maps:
        gps_coordinates = list(filter((None).__ne__, map))
        total_coordinates = total_coordinates + gps_coordinates
        activities.append(gps_coordinates)

    # find geographic midpoint across all activities to display
    midpoint_lat_deg, midpoint_long_deg = calculate_geographic_midpoint(total_coordinates)
    return {
        "midpoint_lat_deg": midpoint_lat_deg,
        "midpoint_long_deg": midpoint_long_deg,
        "activities": activities
    }


def _format_activities_for_display(activities):
    for activity in activities:
        activity.start_time_utc = format_datetime_for_display(localize_datetime_for_display(activity.start_time_utc))
        activity.total_distance = format_distance_for_display(activity.total_distance)
        activity.total_elapsed_time = format_duration_for_display(activity.total_elapsed_time)
    return activities


def get_formatted_recent_activities(db, skip, limit):
    activities = crud.get_activities_recent(db, skip=skip, limit=limit)
    return _format_activities_for_display(activities)


def get_formatted_top_activities(db, skip, limit):
    activities = crud.get_activities_top(db, skip, limit)
    return _format_activities_for_display(activities)


def format_activities_calendar(year, db, skip, limit):
    records = crud.get_activities_calendar(year, db, skip, limit)
    activities = [
        {
            "activity_type": r.activity_type,
            "date": localize_datetime_for_display(r.start_time_utc).date(),
            "filename": r.filename
        } for r in records
    ]
    return {
        'start_date': (datetime.strptime(year, "%Y")).strftime("%Y-%m-%d"),
        'end_date': (datetime.strptime(year, "%Y") + timedelta(days=364)).strftime("%Y-%m-%d"),
        'last_year': (datetime.strptime(year, "%Y") + timedelta(days=-365)).strftime("%Y"),
        'next_year': (datetime.strptime(year, "%Y") + timedelta(days=366)).strftime("%Y"),
        'activities': activities,
    }
