import json, pathlib
from datetime import datetime, timezone, timedelta
from fetchers import fetch_usgs, fetch_eonet, fetch_reliefweb
from normalize import normalize_usgs, normalize_eonet, normalize_reliefweb
from hf_client import translate_if_needed

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(parents=True, exist_ok=True)

def iso_now():
    return datetime.now(timezone.utc).isoformat()

def main():
    events = []

    try:
        usgs = fetch_usgs()
        events += [normalize_usgs(f) for f in usgs]
        print(f"[usgs] events: {len(usgs)}")
    except Exception as e:
        print("[usgs] error:", e)

    try:
        eonet = fetch_eonet()
        events += [normalize_eonet(ev) for ev in eonet]
        print(f"[eonet] events: {len(eonet)}")
    except Exception as e:
        print("[eonet] error:", e)

    try:
        rw = fetch_reliefweb(limit=30)
        events += [normalize_reliefweb(item) for item in rw]
        print(f"[reliefweb] items: {len(rw)}")
    except Exception as e:
        print("[reliefweb] error:", e)

    for ev in events:
        ev["title_en"] = translate_if_needed(ev.get("title", ""), ev.get("language", "en"))
        ev["summary_en"] = translate_if_needed(ev.get("summary", "") or ev.get("title", ""), ev.get("language", "en"))

    seen = set()
    dedup = []
    for ev in events:
        k = (ev.get("source"), ev.get("id"))
        if k not in seen and ev.get("lat") is not None and ev.get("lon") is not None:
            seen.add(k)
            dedup.append(ev)

    recent = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    for ev in dedup:
        try:
            dt = datetime.fromisoformat(ev["date"].replace("Z","+00:00"))
            if dt >= cutoff:
                recent.append(ev)
        except Exception:
            recent.append(ev)

    out = DOCS / "events.json"
    out.write_text(json.dumps({"updated": iso_now(), "events": recent}, ensure_ascii=False, indent=2), encoding="utf-8")
    (DOCS / "last_updated.txt").write_text(iso_now(), encoding="utf-8")
    print(f"[ok] wrote {out} with {len(recent)} events)")

if __name__ == "__main__":
    main()
