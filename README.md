# Global Emergency Map AI

An automated, portfolio-ready project that tracks **live global emergencies** (earthquakes, wildfires, storms, etc.), processes them with a lightweight AI pipeline, and publishes an **interactive map** via GitHub Pages. The pipeline runs **daily at 9 AM ET** (and on-demand) using GitHub Actions and commits updated data to this repo automatically.

> **No server needed.** Everything runs in CI and serves as static files from the `docs/` folder.

## Data sources
- **USGS Earthquakes** (past 24h, GeoJSON)
- **NASA EONET** (open natural events)
- *(Optional)* ReliefWeb disasters

## Hugging Face (optional)
- Add a token as `HF_TOKEN` secret to enable automatic translation to English (via Inference API). Works without it too.

## One-time Setup
1. Create a new GitHub repo (e.g., `global-emergency-map-ai`).
2. Upload the files from this ZIP to that repo.
3. In repo: **Settings → Actions → General → Workflow permissions → Read and write** → Save.
4. (Optional) Add **HF_TOKEN**: **Settings → Secrets and variables → Actions → New repository secret**.
5. Enable **Pages**: **Settings → Pages → Branch: main → Folder: /docs** → Save.
6. Trigger first run: **Actions → Global Emergency Map → Run workflow**.

After the first successful run, open your GitHub Pages URL to see the map.
