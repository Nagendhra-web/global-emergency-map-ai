const map = L.map('map').setView([20,0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 10, attribution: '&copy; OpenStreetMap'}).addTo(map);

const typeColors = {earthquake:'#e53e3e', 'Wildfires':'#ef7d00', 'Severe Storms':'#3182ce', 'Floods':'#2f855a'};

function badge(t){return `<span class='badge'>${t}</span>`}

function load(){
  fetch('events.json?_=' + Date.now()).then(r=>r.json()).then(d=>{
    document.getElementById('updated').textContent = 'Updated: ' + new Date(d.updated).toLocaleString();
    const allowed = new Set([...document.querySelectorAll('.f-type:checked')].map(x=>x.value));
    const layer = L.layerGroup().addTo(map);
    d.events.forEach(ev=>{
      if(!allowed.has(ev.type)) return;
      if(ev.lat == null || ev.lon == null) return;
      const color = typeColors[ev.type] || '#444';
      const marker = L.circleMarker([ev.lat, ev.lon], {radius:6, color, fillColor:color, fillOpacity:0.85});
      const title = ev.title_en || ev.title || 'Event';
      const when = new Date(ev.date).toLocaleString();
      marker.bindPopup(`<div><strong>${title}</strong></div><div>${badge(ev.type)} ${when}</div><div style='max-width:260px;margin-top:6px'>${(ev.summary_en || ev.summary || '')}</div><div style='margin-top:6px'><a href='${ev.url||'#'}' target='_blank' rel='noopener'>Source</a></div>`);
      marker.addTo(layer);
    });
  }).catch(e=>console.error(e));
}

document.querySelectorAll('.f-type').forEach(el=>el.addEventListener('change', load));
load();
