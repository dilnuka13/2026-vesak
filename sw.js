const CACHE_NAME = 'vesak-finance-v1';

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(clients.claim());
});

self.addEventListener('fetch', (event) => {
  // Simple pass-through. Essential to pass PWA installability requirements.
  event.respondWith(fetch(event.request).catch(() => new Response('Offline')));
});
