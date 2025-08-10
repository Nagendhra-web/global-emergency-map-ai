// Map + tiles
const map = L.map('map').setView([20,0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 10, attribution: '&copy; OpenStreetMap'
}).addTo(map);

// Colors
const typeColors = {
  earthquake: '#e53e3e',
  'Wildfires': '#ef7d00',
  'Severe Storms': '#3182ce',
  'Floods': '#2f855a'
};

// State
let allEvents = [];
let layerGroup = L.layerGroup().addTo(map);

// DOM helpers
const qs = s => document.querySelector(s);
const qsa = s => [...document.querySelectorAll(s)];
const updatedEl = qs('#updated');
const fromEl = qs('#fromDate');
const toEl = qs('#toDate');
const details = {
  el: qs('#details'),
  title: qs('#details-title'),
  body: qs('#details-body'),
  close: qs('#details-close')
};
details.close.addEventListener('click', () => {
  details.title.textContent = 'Click a marker';
  details.body.innerHTML = '<p>Select an event on the map to see details here.</p>';
});

// Fetch + init
fetch('events.json?_=' + Date.now())
  .then(r => r.json())
  .then(data => {
    updatedEl.textContent = 'Updated: ' + new Date(data.updated).toLocaleString();
    allEvents = data.events || [];

    // Init date inputs using min/max dates in data (fallback to last 7 days)
    const timestamps = allEvents
      .map(ev => Date.parse(ev.date))
      .filter(n => !Number.isNaN(n))
      .sort((a,b)=>a-b);

    const minDate = timestamps[0] ? new Date(timestamps[0]) : new Date(Date.now()-6*24*3600*1000);
    const maxDate = timestamps[timestamps.length-1] ? new Date(timestamps[timestamps.length-1]) : new Date();

    // format yyyy-mm-dd
    const fmt = d => new Date(d.getTime() - d.getTimezoneOffset()*60000).toISOString().slice(0,10);
    fromEl.value = fmt(minDate);
    toEl.value = fmt(maxDate);

    // Wire filters
    qsa('.f-type').forEach(el => el.addEventListener('change', render));
    fromEl.addEventListener('change', render);
    toEl.addEventListener('change', render);

    render(); // first draw
  })
  .catch(e => console.error(e));

function inRange(dateISO, fromISO, toISO){
  try{
    const d = Date.parse(dateISO);
    const f = Date.parse(fromISO);
    const t = Date.parse(toISO) + 24*3600*1000 - 1; // inclusive end of day
    return d >= f && d <= t;
  }catch{ return true; }
}

function quakeColorByMag(m){
  if (m == null || Number.isNaN(m)) return typeColors.earthquake;
  if (m >= 6) return '#8b0000';
  if (m >= 5) return '#e53e3e';
  if (m >= 4) return '#ff7b7b';
  return '#f6b8b8';
}

function render(){
  layerGroup.clearLayers();
  const allowed = new Set(qsa('.f-type:checked').map(x=>x.value));
  const fromISO = fromEl.value;
  const toISO = toEl.value;

  allEvents.forEach(ev=>{
    if (!allowed.has(ev.type)) return;
    if (ev.lat == null || ev.lon == null) return;
    if (!inRange(ev.date, fromISO, toISO)) return;

    // Color + radius
    let color = typeColors[ev.type] || '#444';
    let radius = 6;
    if (ev.type === 'earthquake'){
      color = quakeColorByMag(ev.severity);
      radius = Math.max(4, Math.min(12, (ev.severity || 0) * 1.4));
    }

    const marker = L.circleMarker([ev.lat, ev.lon], {
      radius, color, fillColor: color, fillOpacity: 0.85
    });

    const title = ev.title_en || ev.title || 'Event';
    const when = new Date(ev.date).toLocaleString();
    const summary = ev.summary_en || ev.summary || '';
    const source = ev.url ? `<a href="${ev.url}" target="_blank" rel="noopener">Source</a>` : '';

    // Popup (quick)
    marker.bindPopup(
      `<div><strong>${title}</strong></div>
       <div class="meta">${ev.type} • ${when}</div>
       <div style="max-width:260px;margin-top:6px">${summary}</div>
       <div style="margin-top:6px">${source}</div>`
    );

    // Side panel (rich)
    marker.on('click', ()=>{
      details.title.textContent = title;
      details.body.innerHTML = `
        <div class="meta">${ev.type} • ${when}</div>
        ${ev.severity != null ? `<div class="meta">Severity: ${ev.severity}${ev.type==='earthquake'?' (magnitude)':''}</div>`:''}
        <p>${summary}</p>
        ${ev.url ? `<p><a href="${ev.url}" target="_blank" rel="noopener">Open original source</a></p>` : ''}
        <p class="meta">Lat: ${ev.lat.toFixed(3)}, Lon: ${ev.lon.toFixed(3)}</p>
      `;
    });

    marker.addTo(layerGroup);
  });
}
