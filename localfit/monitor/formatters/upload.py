# local
from localfit.monitor import schemas
from localfit.monitor import crud
from localfit.utilities import (convert_semicircles_to_degrees, convert_lat_long_to_location_name,
    localize_datetime_to_utc_for_storage, bitswap_ant_timestamp_to_unix_timestamp)


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
            if field.name == 'stress_level_value':
                record['stress_level'] = field.value
            if field.name == 'stress_level_time':
                record['timestamp_utc'] = localize_datetime_to_utc_for_storage(field.value)
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


def parse_step_data_from_monitor_file(fit_file):
    """
    There is no consistency across ANT files about how many times the step data will be written per file or per day.
    The value is not consistently located in a single column or associated with a single key.
    If multiple ANT files are created in a single day (for example if activities are started and stopped), the step data
    for the day will be spread across multiple monitor files.
    Step data values are not cumulative; they state the number of steps taken until that point in time.

    Example:
        2020-01-01 00:00:00 1 step
        2020-01-01 00:00:10 7 steps
        2020-01-01 00:00:20 23 steps
        2020-01-01 00:00:30 47 steps

    The simplest way to get the accurate step count for the day is to grab every record until no more records are found,
    and to keep only the largest one found. The last value found in a file is not guaranteed to be the largest.

    If multiple files exist for a single day, comparison must be done across the files associated with that day to
    ensure that the value taken is the largest.
    """
    record = {}
    timestamp_utc = None
    for row in fit_file.get_messages('monitoring'):
        for field in row:
            if field.name in TIME_FIELDS:
                timestamp_utc = localize_datetime_to_utc_for_storage(field.value)
                if not record.get('timestamp_utc'):
                    record['timestamp_utc'] = timestamp_utc
            if field.name in ['steps']:
                # step data is a mess to parse. the largest value is the correct value.
                if field.value > record.get(field.name, 0):
                    record[field.name] = field.value
                    if timestamp_utc:
                        record['timestamp_utc'] = timestamp_utc
                        timestamp_utc = None
    return record
