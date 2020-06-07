# 3rd Party
from fitparse import FitFile
import pytz

# local
from localfit import schemas
from localfit.utilities import convert_semicircles_to_degrees, convert_lat_long_to_location_name


def _get_activity_session_gps_data(session_data):
        start_position_lat_deg = convert_semicircles_to_degrees(session_data.get('start_position_lat').value)
        start_position_long_deg = convert_semicircles_to_degrees(session_data.get('start_position_long').value)

        return {
            'start_position_lat_sem': session_data.get('start_position_lat').value,
            'start_position_long_sem': session_data.get('start_position_long').value,
            'start_position_lat_deg': start_position_lat_deg,
            'start_position_long_deg': start_position_long_deg,
            'start_location': convert_lat_long_to_location_name(start_position_lat_deg, start_position_long_deg),
        }


def _get_activity_session_data(fit_file):
    session_data = [row for row in fit_file.get_messages('session')][0]
    formatted_session_data = {
        'start_time_utc': pytz.utc.localize(session_data.get('start_time').value),
        'total_elapsed_time': session_data.get('total_elapsed_time').value,
        'total_timer_time': session_data.get('total_timer_time').value,
        'total_distance': session_data.get('total_distance').value,
        'total_strides': session_data.get('total_strides').value if session_data.get('total_strides') else None,
        'total_cycles': session_data.get('total_cycles').value if session_data.get('total_cycles') else None,
        'total_calories': session_data.get('total_calories').value,
        'enhanced_avg_speed': session_data.get('enhanced_avg_speed').value,
        'avg_speed': session_data.get('avg_speed').value,
        'enhanced_max_speed': session_data.get('enhanced_max_speed').value,
        'max_speed': session_data.get('max_speed').value,
        'avg_power': session_data.get('avg_power').value,
        'max_power': session_data.get('max_power').value,
        'total_ascent': session_data.get('total_ascent').value,
        'total_descent': session_data.get('total_descent').value,
    }

    # GPS data is only present when GPS is enabled and relevant to the activity
    if session_data.get('start_position_lat').value and session_data.get('start_position_long').value:
        formatted_session_data.update(_get_activity_session_gps_data(session_data))

    return formatted_session_data


def _get_activity_type(fit_file):
    activity_type_map = {
        (1, 0): "run",  # Run: generic
        (1, 1): "treadmill",  # Run: Treadmill
        (4, 15): "elliptical",  # Fitness Equipment: Elliptical
        (11, 0): "walk",  # walk
        (10, 43): "yoga",  # yoga
        (4, 16): "stair",  # Fitness Equipment: Stair Climbing
        (10, 26): "cardio",  # Training: Cardio (Beat Saber)
    }
    sport_data = [r for r in fit_file.get_messages('sport') if r.type == 'data'][0]
    try:
        activity_type = activity_type_map[(sport_data.get("sport").raw_value, sport_data.get("sub_sport").raw_value)]
    except KeyError:
        raise Exception({"file": "Unsupported sport"})
    return activity_type


def get_activity_data(file):
    fit_file = FitFile(file.file)
    activity_data = _get_activity_session_data(fit_file)
    activity_data.update({
        "filename": file.filename.split(".")[0],
        "activity_type": _get_activity_type(fit_file),
        "is_manually_entered": False,
        "activity_collection": "uncategorized",

    })

    return schemas.ActivityFile(**activity_data)
