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

