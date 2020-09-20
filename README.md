# Table of Contents
- [Description](#description)
- [Local Development](#local-development)
- [API Contract](#api-contract)

# Description
This is a FastAPI server allowing upload, management, and display of ANT-compatible fitness data.

# Local Development
## Prerequisites
- Python 3.8
- SQLite

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Local Server Start
```bash
python localfit_fastapi/main.py --reload
```

## Default Local Server Address
http://127.0.0.1:8005 

# API Contract
## Single Activity
- [Upload a Single Activity](#upload-a-single-activity)
- [Delete a Single Activity](#delete-a-single-activity)
- [View Single Activity Metadata](#view-single-activity-metadata)
- [Update Single Activity Metadata](#update-single-activity-metadata)
- [View Single Activity GPS Data](#view-single-activity-gps-data)
- [View Single Activity Heart Rate Data](#view-single-activity-heart-rate-data)

## Activities
- [View All Activities](#view-all-activities)
- [View Activities Calendar](#view-activities-calendar)
- [View Top Activities by Distance](#view-top-activities-by-distance)
- [View Activities Subset by Collection](#view-activities-subset-by-collection)

## Steps
- [View Steps by Day](#view-steps-by-day)
- [View Step Goal Achievement by Month](#view-step-goal-achievement-by-month)

## Single Activity
### Upload a Single Activity
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
### Delete a Single Activity
DELETE `/activities/<filename>/`
```python
import requests
r = requests.delete("http://127.0.0.1:8005/activities/AAABBB11/")

r
<Response [204]>

# No r.json() because the response contains no entity
```

### View Single Activity Metadata
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

## Update Single Activity Metadata
- PATCH `/activities/<filename>/`
```python
import requests
r = requests.patch("http://127.0.0.1:8005/activities/AAABBB11/", json={"activity_collection": "neighborhood_runs"})

r
<Response [200]>

r.json()
{}
```

## View Single Activity GPS Data
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

## View Single Activity Heart Rate Data
- GET `/activities/<filename>/heart/`
```python
import requests
r = requests.get("http://127.0.0.1:8005/activities/AAABBB11/heart/")

r
<Response [200]>

r.json()
{
    'start_date': '2020-06-01T12:41:13-07:00',
    'end_date': '2020-06-01T12:42:55-07:00',
    'heart_rate': [
        {
            't': '2020-06-01T12:41:13-07:00',
            'y': 75
        },
        {
            't': '2020-06-01T12:42:55-07:00',
            'y': 79
        },
    ]
}
```

## Activities
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

### View Activities Calendar
- GET `/activities/calendar/?year={year}`  
Without query parameters, it will default to the current year.
```python
import requests
r = requests.get("http://127.0.0.1:8005/activities/calendar/")

r
<Response [200]>

r.json()
{
    'start_date': '2020-01-01',
    'end_date': '2020-12-30',
    'last_year': '2019',
    'next_year': '2021',
    'activities': [
        {
            'activity_type': 'run',
            'date': '2020-01-02',
            'filename': 'AAAA1111'
        }
    ]
}
```
With query parameters, it will use the year provided.
```python
import requests
r = requests.get("http://127.0.0.1:8005/activities/calendar/?year=2020")

r
<Response [200]>

r.json()
{
    'start_date': '2020-01-01',
    'end_date': '2020-12-30',
    'last_year': '2019',
    'next_year': '2021',
    'activities': [
        {
            'activity_type': 'run',
            'date': '2020-01-02',
            'filename': 'AAAA1111'
        }
    ]
}
```
### View Top Activities by Distance
- GET `/activities/top/`
```python
import requests
r = requests.get("http://127.0.0.1:8005/activities/top/")

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
        'start_location': 'Empire State Building, New York, NY',
    },
]
```

### View Activities Subset by Collection
- GET `/activities/collection/<collection_name>/`
```python
import requests
r = requests.get("http://127.0.0.1:8005/activities/collection/neighborhood_runs/")

r
<Response [200]>

r.json()
{
    'midpoint_lat_deg': 40.748402,
    'midpoint_long_deg': 73.985702,
    'activities': [
        [
            {'lat': 40.748400, 'lng': 73.985700},
            {'lat': 40.748401, 'lng': 73.985701},
            {'lat': 40.748402, 'lng': 73.985702},
            {'lat': 40.748403, 'lng': 73.985703}
        ],
        [
            {'lat': 40.748400, 'lng': 73.985700},
            {'lat': 40.748401, 'lng': 73.985701},
            {'lat': 40.748402, 'lng': 73.985702},
            {'lat': 40.748403, 'lng': 73.985703}
        ],
    ]
}
```

## Steps
### View Steps by Day
- GET `/monitor/steps/?start_date={start_date}&end_date={end_date}`
```python
import requests
r = requests.get("http://127.0.0.1:8005/monitor/steps/?start_date=2020-06-01&end_date=2020-06-30")

r
<Response [200]>

r.json()
{
    'start_date': '2020-06-01',
    'end_date': '2020-06-30',
    'steps': [
        {
            't': '2020-06-01',
            'y': 10000
        },
        ...
        {
            't': '2020-06-30',
            'y': 5000
        },
    ]
}
```
### View Step Goal Achievement by Month
- GET `/monitor/steps/goal/?year={year}&month={month}`  
Without query parameters, it will default to the current month and year.
```python
import requests
r = requests.get("http://127.0.0.1:8005/monitor/steps/goal/")
r
<Response [200]>

r.json()
{'monthly_step_goal_percent_completed': 0.55}
```
With query paramters, it will use the month and year provided.
```python
r = requests.get("http://127.0.0.1:8005/monitor/steps/goal/?year=2020&month=6")

r
<Response [200]>

r.json()
{'monthly_step_goal_percent_completed': 0.77}
```

Coming Soon!
- Stress

