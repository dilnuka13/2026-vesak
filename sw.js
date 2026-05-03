const CACHE_NAME = 'vesak-finance-v2';

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

// ── FCM Push Handler ─────────────────────────────────────────────────────────
self.addEventListener('push', (event) => {
  let payload = { title: 'Vesak System Update', body: '' };

  if (event.data) {
    try {
      const json = event.data.json();
      // FCM wraps in notification object
      payload.title = json.notification?.title || json.title || payload.title;
      payload.body  = json.notification?.body  || json.body  || '';
    } catch (_) {
      payload.body = event.data.text();
    }
  }

  // Relay to all open app tabs so the in-app popup fires
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(clientList => {
      clientList.forEach(client => {
        client.postMessage({ type: 'FCM_MESSAGE', title: payload.title, body: payload.body });
      });

      // Show OS-level notification only if no focused window is visible
      const hasFocused = clientList.some(c => c.focused);
      if (!hasFocused) {
        return self.registration.showNotification(payload.title, {
          body: payload.body,
          icon: '/logo.png',
          badge: '/logo.png',
          tag: 'vesak-update',
          renotify: true,
          data: { url: '/#dashboard' }
        });
      }
    })
  );
});

// When user taps the OS notification, open/focus the app
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  const targetUrl = event.notification.data?.url || '/';
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(clientList => {
      for (const client of clientList) {
        if (client.url.includes(self.location.origin) && 'focus' in client) {
          client.navigate(targetUrl);
          return client.focus();
        }
      }
      return self.clients.openWindow(targetUrl);
    })
  );
});

