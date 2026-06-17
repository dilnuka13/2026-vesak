const CACHE_NAME = 'vesak-finance-v3';
const OFFLINE_URL = 'offline.html';

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll([
        OFFLINE_URL, 
        '/',
        '/index.html',
        '/logo.png', 
        '/poson_logo.png',
        '/dc.png', 
        '/ve1rify.png'
      ]);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).catch(() => {
        return caches.open(CACHE_NAME).then((cache) => {
          return cache.match(OFFLINE_URL);
        });
      })
    );
  } else {
    event.respondWith(fetch(event.request).catch(() => {
      return caches.match(event.request);
    }));
  }
});

importScripts('https://www.gstatic.com/firebasejs/9.22.2/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.22.2/firebase-messaging-compat.js');

const firebaseConfig = {
  apiKey: "AIzaSyD6yXDHsOaqVplfhsXZV8nWvMuioDulwYg",
  authDomain: "edu-login-4d05f.firebaseapp.com",
  projectId: "edu-login-4d05f",
  storageBucket: "edu-login-4d05f.firebasestorage.app",
  messagingSenderId: "197092856272",
  appId: "1:197092856272:web:444ea56fdc6f248dcca9d5"
};

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

// Handle background messages
messaging.onBackgroundMessage((payload) => {
  const notificationTitle = payload.notification?.title || "Vesak System Update";
  const notificationOptions = {
    body: payload.notification?.body || "New activity detected.",
    icon: '/logo.png',
    badge: '/logo.png',
    data: { url: '/#dashboard' }
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
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

