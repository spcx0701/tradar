/* 무역풍 서비스워커 — 앱 셸·데이터 캐시(오프라인 동작). */
const CACHE = 'tradar-v2';
const ASSETS = [
  'index.html', 'home.html', 'dashboard.html', 'tradar.css', 'app.js',
  'vendor/echarts.min.js', 'manifest.json', 'icons/logo.svg',
  'data/catalog.json', 'data/forecast.json', 'data/radar.json',
  'data/treemap.json', 'data/countries.json',
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(hit => hit || fetch(e.request).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put(e.request, copy)).catch(() => {});
      return res;
    }).catch(() => caches.match('index.html')))
  );
});
