# local
from localfit.monitor import schemas
from localfit.monitor import crud
from localfit.utilities import (convert_semicircles_to_degrees, convert_lat_long_to_location_name,
    localize_datetime_to_utc_for_storage, bitswap_ant_timestamp_to_unix_timestamp,
                                localize_datetime_for_display)


STRESS_FIELDS = [
    'stress_level_value'
]


STRESS_TIME_FIELDS = [
    'stress_level_time'
]

TIME_FIELDS = [
    'timestamp'
]

TIME_16_FIELDS = [
    'timestamp_16'
]


def parse_stress_data_from_monitor_file(fit_file):
    records = []
    for row in fit_file.get_messages('stress_level'):
        record = {}
        for field in row:
            if field.name in STRESS_FIELDS:
                record[field.name] = field.value
            if field.name in STRESS_TIME_FIELDS:
                record[f'{field.name}_utc'] = localize_datetime_to_utc_for_storage(field.value)
        records.append(record)
    return records


def parse_heart_rate_data_from_monitor_file(fit_file):
    most_recent_timestamp_ant_epoch = None
    records = []
    for row in fit_file.get_messages('monitoring'):
        record = {}
        for field in row:
            if field.name == 'heart_rate':
                record[field.name] = field.value
            if field.name in TIME_FIELDS:
                record[f'{field.name}_utc'] = localize_datetime_to_utc_for_storage(field.value)
                most_recent_timestamp_ant_epoch = field.raw_value
            if field.name in TIME_16_FIELDS:
                timestamp = bitswap_ant_timestamp_to_unix_timestamp(most_recent_timestamp_ant_epoch, field.raw_value)
                record['timestamp_utc'] = timestamp

        # throw out the rows without heart rate data
        if record.get('heart_rate'):
            records.append(record)
    return records


def parse_heart_metabolic_rate_from_monitor_file(fit_file):
    records = []
    for row in fit_file.get_messages('monitoring_info'):
        record = {}
        for field in row:
            if field.name == 'resting_metabolic_rate':
                record[field.name] = field.value
            if field.name in TIME_FIELDS:
                record[f'{field.name}_utc'] = localize_datetime_to_utc_for_storage(field.value)

        records.append(record)

    return records


def parse_step_data_from_monitor_file(db, fit_file):
    """
    There is no consistency across ANT files about how many times the step data will be written per file or per day.
    The value is not consistently located in a single column or associated with a single key.
    If multiple ANT files are created in a single day (for example if activities are started and stopped), the step data
    for the day will be spread across multiple files.
    Step data values are not cumulative; they state the number of steps taken until that point in time.

    Example:
        2020-01-01 00:00:00 1 step
        2020-01-01 00:00:10 7 steps
        2020-01-01 00:00:20 23 steps
        2020-01-01 00:00:30 47 steps

    The simplest way to get the accurate step count for the day is to grab every record until no more records are found,
    and to keep only the last one found. If multiple files exist for a single day, compare across the files as well to
    ensure that the value we have is the largest.
    """
    record = {}
    for row in fit_file.get_messages('monitoring'):
        for field in row:
            if field.name in TIME_FIELDS:
                if not record.get('date'):
                    record['date'] = localize_datetime_to_utc_for_storage(field.value)
            if field.name in ['steps']:
                # step data is a mess to parse. the largest value is the final value.
                if field.value > record.get(field.name, 0):
                    record[field.name] = field.value

    # This is needed because ANT files are written from local time start to stop.
    # This ensures you grab the correct file for your device's timezone.
    #
    # For example
    # If your device is UTC+1, your file will write a "day" from 1:00 AM - 12:59 AM
    # If your device is UTC+8, your file will write a "day" from 8:00 AM - 7:59 AM
    local_date = localize_datetime_for_display(record['date']).date()


    return ""

