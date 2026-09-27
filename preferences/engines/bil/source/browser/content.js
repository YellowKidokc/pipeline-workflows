import { BIL_CONFIG } from "./config.js";

const startedAt = Date.now();
let maxScrollDepth = 0;

function scrollDepth() {
  const total = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
  return Math.min(1, window.scrollY / total);
}

window.addEventListener("scroll", () => {
  maxScrollDepth = Math.max(maxScrollDepth, scrollDepth());
});

window.addEventListener("beforeunload", () => {
  const dwellSeconds = Math.round((Date.now() - startedAt) / 1000);
  const signal = dwellSeconds >= BIL_CONFIG.dwellThresholdSeconds || maxScrollDepth >= BIL_CONFIG.scrollThreshold
    ? "long_dwell_scroll"
    : "accidental_visit";

  chrome.runtime.sendMessage({
    type: "bil.preference_event",
    payload: {
      source: "browser_extension",
      signal,
      subject: document.title || location.href,
      metadata: {
        url: location.href,
        title: document.title,
        dwell_seconds: dwellSeconds,
        scroll_depth: maxScrollDepth
      }
    }
  });
});
