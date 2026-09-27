import { BIL_CONFIG } from "./config.js";

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (!message || message.type !== "bil.preference_event") {
    return false;
  }

  fetch(BIL_CONFIG.endpoint, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(message.payload)
  })
    .then(() => sendResponse({ ok: true }))
    .catch(() => sendResponse({ ok: false, offline: true }));

  return true;
});
