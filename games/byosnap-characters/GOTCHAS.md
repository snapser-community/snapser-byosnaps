# Gotchas
What to Watch Out For When Working in This Repo

## Logging
- Write logs to stdout as one JSON object per line with `level`, `message`, and `timestamp`
  fields. Snapser parses `level` (debug/info/warn/error) to color the line in the Logs tool.
- Snapser correlates all log lines of one request across snaps by the `request-id` field. The
  value comes from the `X-Request-Id` request header. The app binds it once per request in a
  `before_request` hook (a contextvar), so you do not pass it to each log call.
- Snapser samples logs per-request instead of per-line, so all lines of a sampled request stay
  together.
- Forward the `X-Request-Id` header on outbound snap-to-snap calls (use `outbound_headers`) so
  the downstream snap logs the same `request-id`.
