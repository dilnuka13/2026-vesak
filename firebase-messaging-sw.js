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

messaging.onBackgroundMessage((payload) => {
  const notificationTitle = payload.notification?.title || "Vesak System Notification";
  const notificationOptions = {
    body: payload.notification?.body || "New activity detected.",
    icon: '/logo.png',
    data: payload.data
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});
