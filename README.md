
# Coming Soon!

# Local Development
## Prerequisites
- Python 3.8

## Local Server Start
python localfit_fastapi/main.py --reload

# API Contract

## Activity
- POST /activities/ (upload activity file)
- GET /activities/<filename>/ (view metadata)
- PATCH /activities/<filename> (edit metadata)
- GET /activities/<filename>/map/ (view map)
- GET /activities/<filename>/heartrate/ (view heart rate data)

## Actvities
- GET /activities/
- GET /activities/top/

## Step Data
- GET /steps/?start_date=

## Stress Data

## Heart Rate Data