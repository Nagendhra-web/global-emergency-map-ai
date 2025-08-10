# Global Emergency Map AI

An automated, production-style project that tracks **live global emergencies** (earthquakes, wildfires, storms, floods), enriches them with a lightweight **NLP pipeline** (optional translation via Hugging Face), and publishes an **interactive map** with filters, a date range picker, severity legend, and a details panel.

- **Zero servers** — everything runs in GitHub Actions and serves from `docs/`.
- **Auto-refresh** — data pipeline runs daily at **9:00 AM ET** (manual run supported).
- **Live demo** — hosted on GitHub Pages.

## Features

- **Sources**: USGS (earthquakes), NASA EONET (open natural events), ReliefWeb (best-effort).
- **NLP (optional)**: translate non-English titles/descriptions to English using **Hugging Face Inference API**.
- **UI**:
  - Map pins by type, color-coded.
  - **Date range filter** (from–to calendars).
  - **Severity legend** for earthquakes (magnitude bins).
  - **Details panel** with title, time, severity, summary, coordinates, and source link.

## Quick Start (GitHub)

README.md
requirements.txt
docs/
index.html
styles.css
app.js
events.json
pipeline/
init.py
fetchers.py
normalize.py
hf_client.py
run.py
.github/
workflows/
ingest.yml
deploy.yml # optional, if using Pages via Actions

2. **Settings → Actions → General → Workflow permissions → Read and write** → Save.

3. **Pages**
- Either **Deploy from a branch** (Branch: `main`, Folder: `/docs`)
- **Or** set **Source: GitHub Actions** and include `deploy.yml` (recommended).

4. *(Optional)* **Hugging Face token**:  
**Settings → Secrets and variables → Actions → New repository secret**  
Name: `HF_TOKEN` → Value: your token.

5. **Run it**: **Actions → Global Emergency Map → Run workflow**.  
After success, your site will update automatically.

## Local Dev (optional)

python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python pipeline/run.py
# open docs/index.html in a browser
Tech Stack
Data: USGS, NASA EONET, ReliefWeb

NLP: Hugging Face Inference API (e.g., facebook/nllb-200-distilled-600M)

Frontend: Leaflet + vanilla JS/CSS (static)

CI/CD: GitHub Actions (daily cron + optional Pages deploy)

Roadmap
Event-type classifier + severity normalization (storms/floods)

Email/Slack alerts for high-severity areas

Country/region filters

Download CSV / CSV snapshot per run
