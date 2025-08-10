from datetime import datetime, timezone
from dateutil import tz

def to_iso(ts_ms):
    try:
        return datetime.fromtimestamp(ts_ms/1000, tz=timezone.utc).isoformat()
    except Exception:
        return datetime.now(timezone.utc).isoformat()

def normalize_usgs(feat):
    props = feat.get("properties", {}) or {}
    geom = feat.get("geometry", {}) or {}
    coords = (geom.get("coordinates") or [None, None])
    lon, lat = None, None
    if isinstance(coords, (list, tuple)) and len(coords) >= 2:
        lon, lat = coords[0], coords[1]
    mag = props.get("mag")
    sev_label = None
    if isinstance(mag, (int, float)):
        if mag >= 6: sev_label = "Severe"
        elif mag >= 5: sev_label = "High"
        elif mag >= 4: sev_label = "Moderate"
        else: sev_label = "Low"
    return {
        "id": props.get("code") or props.get("ids") or props.get("url"),
        "source": "usgs",
        "type": "earthquake",
        "title": props.get("title") or f"M{mag} Earthquake",
        "summary": props.get("place") or "",
        "date": to_iso(props.get("time") or 0),
        "lat": lat, "lon": lon,
        "severity": mag,
        "severity_label": sev_label,
        "url": props.get("url"),
        "language": "en"
    }

def normalize_eonet(ev):
    cats = ev.get("categories") or []
    cat = cats[0]["title"] if cats else "Event"
    geoms = ev.get("geometry") or []
    lat = lon = None
    dt_iso = datetime.now(timezone.utc).isoformat()
    if geoms:
        g = geoms[-1]
        coords = g.get("coordinates") or []
        if isinstance(coords, (list, tuple)) and len(coords) >= 2:
            lon, lat = coords[0], coords[1]
        dt_iso = g.get("date") or dt_iso
    return {
        "id": ev.get("id"),
        "source": "eonet",
        "type": cat,
        "title": ev.get("title") or cat,
        "summary": (ev.get("description") or "")[:300],
        "date": dt_iso,
        "lat": lat, "lon": lon,
        "severity": None,
        "severity_label": None,
        "url": f"https://eonet.gsfc.nasa.gov/api/v3/events/{ev.get('id')}",
        "language": "en"
    }

def normalize_reliefweb(item):
    fields = (item or {}).get("fields", {})
    name = fields.get("name") or fields.get("headline") or "Disaster"
    country = ", ".join([c.get("name","") for c in fields.get("country",[])]) if isinstance(fields.get("country"), list) else ""
    dt = (fields.get("date",{}) or {}).get("created") or (fields.get("date",{}) or {}).get("tsunami") or (fields.get("date",{}) or {}).get("date")
    return {
        "id": item.get("id"),
        "source": "reliefweb",
        "type": (fields.get("type", [{}])[0].get("name") if fields.get("type") else "Disaster"),
        "title": name,
        "summary": f"{name} — {country}".strip(" —"),
        "date": dt or datetime.now(timezone.utc).isoformat(),
        "lat": None, "lon": None,
        "severity": None,
        "severity_label": None,
        "url": fields.get("url") or "https://reliefweb.int/",
        "language": fields.get("language","en")
    }
