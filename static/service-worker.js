const CACHE_NAME = "remote-windows-volume-control";
const urlsToCache = [
  "/",
  "/static/manifest.json",
  "/static/favicon/android-chrome-192x192.png",
  "/favicon/android-chrome-512x512.png",
];

// Install SW
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(urlsToCache);
    })
  );
});

// Fetch
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
