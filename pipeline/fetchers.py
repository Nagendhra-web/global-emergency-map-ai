import requests

def fetch_json(url, params=None):
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def fetch_usgs():
    # USGS Earthquakes - all magnitudes, last 24 hours (GeoJSON)
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
    data = fetch_json(url)
    return data.get("features", [])

def fetch_eonet():
    # NASA EONET v3 - open natural events
    url = "https://eonet.gsfc.nasa.gov/api/v3/events"
    data = fetch_json(url, params={"status": "open"})
    return data.get("events", [])

def fetch_reliefweb(limit=20):
    # ReliefWeb disasters - best-effort
    url = "https://api.reliefweb.int/v1/disasters"
    data = fetch_json(url, params={"limit": limit})
    return data.get("data", [])
