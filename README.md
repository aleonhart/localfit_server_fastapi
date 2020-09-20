# Table of Contents
- [Description](#description)
- [Local Development](#local-development)
- [API Contract](#api-contract)

# Description
This is a FastAPI server.

Scrape https://shop.americasnationalparks.org/documents/cancellations.pdf


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

## Cancellations Map
- [View Cancellations Map](#view-cancellations-map)


## Cancellations
### View Cancellations Map
- GET `/points/`
```python
import requests
r = requests.get("http://127.0.0.1:8005/points/")

r
<Response [200]>

r.json()
[
    {
        "meta": {
            "name": "Cabrillo NM",
            "abbrev": "NM",
            "location_name": "San Diego",
            "state": "CA"
        },
        "lat_deg": 32.673828,
        "long_deg": -117.241345
    }
]
```
