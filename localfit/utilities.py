# stdlib
from datetime import datetime

# 3rd Party
from geopy.geocoders import Nominatim
import pytz


def convert_semicircles_to_degrees(semicircles):
    """
    ANT FIT files store coordinates as semicircles. This
    allows for a standard 32 bit integer to represent 360
    degrees with high precision.

    Google Maps API, which will be used to display the data,
    accepts coordinates according to the World Geodetic System WGS84
    standard, as degrees.

    ANT is highly concerned with storage limits due to saving data on GPS watches.
    This (web)app is more concerned with browser-side rendering times. Therefor,
    it will convert semicircles to degrees before storing the data the DB to speed
    up the render of the maps in the browser.

    Precision:
    Latitude  range is -90  and +90  degrees respective to the Equator.
    Longitude range is -180 and +180 degrees respective to the Prime Meridian.

    .000001 decimal degree is approximately 0.1m (10cm).
    Google Maps resolution is approximately 1.0m.

    Storage with with 6 decimal point precision should more than suffice.

    Semicircle to Degrees Equation:
    180 degrees = 2^31 semicircles

    Example:
    Degrees = Semicircles*(180/2^31)
    41.364685 = 493499921*(180/2^31)
    """
    return round(semicircles * (180/(2**31)), 6)


def convert_lat_long_to_location_name(lat, long):
    try:
        # TODO call to geolocator can fail and should be made async
        geolocator = Nominatim(user_agent="localfit")
        address = geolocator.reverse(f"{round(lat, 6)}, {round(long, 6)}").raw['address']
        small_location = address.get('path') or address.get('footway') or address.get('road') or address.get('street')
        med_location = address.get('hamlet') or address.get('village') or address.get('city')
        full_address = f"{small_location}, {med_location}, {address.get('county')}, {address.get('state')}"
    except Exception:
        full_address = 'Unknown'
    return full_address


def localize_datetime_to_utc_for_storage(datetime):
    return pytz.utc.localize(datetime)


def localize_datetime_for_display(dt_unaware, tz='America/Los_Angeles'):
    timezone_to_localize_from = pytz.utc
    timezone_to_localize_to = pytz.timezone(tz)

    dt_utc = dt_unaware.replace(tzinfo=timezone_to_localize_from)
    return dt_utc.replace(tzinfo=timezone_to_localize_from).astimezone(tz=timezone_to_localize_to)


def format_datetime_for_display(dt):
    """
    Format:
    04:10PM, Monday, December 30, 2019
    """
    return dt.strftime("%A, %B %d, %Y, %I:%M %p")

