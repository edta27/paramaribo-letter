/**
 * Loads free Microsoft Clarity and/or GA4 only when IDs are set in site-config.js.
 * Safe no-op when IDs are empty. Does not send email or other PII.
 */
(function () {
  var cfg = window.PARAMARIBO_SITE || {};
  var clarityId = (cfg.clarityProjectId || "").trim();
  var ga4Id = (cfg.ga4MeasurementId || "").trim();

  if (clarityId) {
    (function (c, l, a, r, i, t, y) {
      c[a] =
        c[a] ||
        function () {
          (c[a].q = c[a].q || []).push(arguments);
        };
      t = l.createElement(r);
      t.async = 1;
      t.src = "https://www.clarity.ms/tag/" + i;
      y = l.getElementsByTagName(r)[0];
      y.parentNode.insertBefore(t, y);
    })(window, document, "clarity", "script", clarityId);
  }

  if (ga4Id) {
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(ga4Id);
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    function gtag() {
      window.dataLayer.push(arguments);
    }
    window.gtag = gtag;
    gtag("js", new Date());
    gtag("config", ga4Id, { anonymize_ip: true });
  }
})();
