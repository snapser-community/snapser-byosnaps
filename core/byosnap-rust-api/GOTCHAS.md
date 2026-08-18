# GOTCHAS

Important things to keep in mind when developing this BYOSnap.

## Logging

1. **JSON lines**: Write one JSON object per line to stdout with `level`
   (`debug`/`info`/`warn`/`error`), `message` and `timestamp`. Snapser reads `level` to color the
   line in the Logs tool. See the `JsonLogger` and `log_json` in `src/main.rs`.
2. **Request Id**: Every inbound request carries an `X-Request-Id` header. Handlers extract it
   once with `request_id(&req)` and pass it to the `log_info`/`log_warn`/... helpers so every
   line carries a `request-id` field. Snapser correlates the lines of one request across Snaps by
   this field and samples logs per request, not per line.
3. **Field name**: The field must be `request-id` (kebab-case). `request_id` or `requestId` are
   not parsed.
4. **Outbound calls**: Forward `X-Request-Id` on Snap-to-Snap calls (see `publish_event`) so
   downstream logs correlate. Startup work such as event type registration has no request id, so
   the field is omitted there; boot-time lines from the standard `log::` macros also carry no id.
5. **Sanitization**: `X-Request-Id` is client-supplied. `sanitize_request_id` caps it at 128
   characters and allows only ASCII alphanumerics, `-`, `_` and `.`; anything else (including an
   empty header) yields `None` and the `request-id` field is omitted.
