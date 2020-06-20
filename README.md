# Description
Upload and view ANT-compatible fitness data.

# Local Development
## Prerequisites
- Python 3.8
- SQLite

## Local Server Start
```bash
python localfit_fastapi/main.py --reload
```

## Default Local Server Address
http://127.0.0.1:8005 

# API Contract

## Activities
### Upload an Activity
POST `/activities/`
```javascript
const submitForm = (contentType, data) => {
    axios({
      url: `http://127.0.0.1:8005/activities/`,
      method: "POST",
      data: data,
      headers: {
        "Content-Type": contentType,
      },
    })
      .then((response) => {
        setResponse("Success! File uploaded.");
        setFile(null);
      })
      .catch((error) => {
        if (error.response) {
          setResponse(`Error: ${error.response.data["file"]}`);
        } else {
          setResponse("An unexpected error occurred.");
        }
      });
  };

  const uploadWithFormData = () => {
    const formData = new FormData();
    formData.append("file", file);
    submitForm("multipart/form-data", formData);
  };
```
### View an Activity's Metadata
- GET `/activities/<filename>/`
```python
import requests
r = requests.get("http://127.0.0.1:8005/activities/AAABBB11/")

r
<Response [200]>

r.json()
{
    'activity_type': 'run',
    'start_time_utc': 'Monday, June 01, 2020, 01:15 PM',
    'activity_collection': 'uncategorized',
    'total_elapsed_time': 555.444,
    'total_distance': 1111.11,
    'total_calories': 100,
    'start_location': 'Empire State Building, New York, NY'
}
```

## Update an Activity's Metadata
- PATCH `/activities/<filename>/`
```python
import requests
r = requests.patch("http://127.0.0.1:8005/activities/AAABBB11/", json={"activity_collection": "neighborhood_runs"})

r
<Response [200]>

r.json()
{}
```

## View Activity GPS Data
- GET `/activities/<filename>/map/`
```python
import requests
r = requests.get("http://127.0.0.1:8005/activities/AAABBB11/map/")

r
<Response [200]>

r.json()
{
    'activitydata': [
        {'lat': 40.748400, 'lng': 73.985700},
        {'lat': 40.748401, 'lng': 73.985701},
        {'lat': 40.748402, 'lng': 73.985702},
        {'lat': 40.748403, 'lng': 73.985703}
    ],
    'midpoint_lat_deg': 40.748402,
    'midpoint_long_deg': 73.985702
}
```
- GET `/activities/<filename>/heartrate/` (view heart rate data)

### View All Activities
- GET `/activities/`
```python
import requests
r = requests.get("http://127.0.0.1:8005/activities/")

r
<Response [200]>

r.json()
[
    {
        'filename': 'AAAA1111', 
        'activity_type': 'run', 
        'is_manually_entered': False, 
        'activity_collection': 
        'uncategorized', 
        'start_time_utc': '2018-11-22T17:30:12', 
        'total_elapsed_time': 1111.111, 
        'total_timer_time': 1111.111, 
        'total_distance': 1111.11, 
        'total_strides': 3000, 
        'total_cycles': 2000, 
        'total_calories': 385, 
        'enhanced_avg_speed': 1.00, 
        'avg_speed': 1000, 
        'enhanced_max_speed': 1.000, 
        'max_speed': 1000, 
        'avg_power': None, 
        'max_power': None, 
        'total_ascent': 9, 
        'total_descent': 13, 
        'start_position_lat_sem': 000000000, 
        'start_position_long_sem': -0000000000, 
        'start_position_lat_deg': 40.748400, 
        'start_position_long_deg': -73.985700, 
        'start_location': 'Empire State Building, New York, NY'
    }
]
```


- GET `/activities/top/`

## Step Data
- GET `/steps/?start_date=`

## Stress Data

## Heart Rate Data