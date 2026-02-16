(function() {
  'use strict';

  // TODO: Replace with your deployed Cloudflare Worker URL
  var WORKER_URL = 'https://cherri-back-in-stock.workers.dev/tag';

  document.addEventListener('submit', function(e) {
    var form = e.target;
    if (\!form.hasAttribute('data-notification-form')) return;

    var emailInput = form.querySelector('[name="contact[email]"]');
    var tagsInput = form.querySelector('[name="contact[tags]"]');

    if (\!emailInput || \!tagsInput || \!emailInput.value) return;

    var payload = JSON.stringify({
      email: emailInput.value,
      tags: tagsInput.value
    });

    // Fire-and-forget: sendBeacon persists through page navigation.
    // Uses text/plain content type to avoid CORS preflight.
    if (navigator.sendBeacon) {
      navigator.sendBeacon(
        WORKER_URL,
        new Blob([payload], { type: 'text/plain' })
      );
    }

    // The Liquid form continues to submit normally
  });
})();