# Deploy Checklist (2026-07 overhaul)

The app now requires environment variables that must be set in the Render
dashboard **before or immediately after** this deploy goes live.

## 1. Required environment variables (Render dashboard → Environment)

| Variable | Value |
|---|---|
| `OPENAI_API_KEY` | (already set) |
| `SECRET_KEY` | any long random string — keep it stable; rotating it logs everyone out |
| `ADMIN_API_KEY` | a long random string of your choosing — this is the password for the admin dashboards |
| `DATABASE_URL` | the Internal Database URL of your Render Postgres instance |

Generate strong values locally, e.g.: `python -c "import secrets; print(secrets.token_urlsafe(48))"`

## 2. Provision Postgres (free tier)

1. Render dashboard → New → PostgreSQL → free plan.
2. Copy the **Internal Database URL**.
3. Paste it as `DATABASE_URL` on the web service.
4. Redeploy. Tables are created automatically on boot.

Until `DATABASE_URL` is set, the app falls back to SQLite on an ephemeral
disk — it works, but data is wiped on every deploy.

## 3. Restore the visitor map data

The pre-migration export lives in `db_backups/live_locations_2026-07-19.json`
(local only, not in git). After `DATABASE_URL` and `ADMIN_API_KEY` are live:

```
set ADMIN_API_KEY=<your key>
python scripts/restore_locations.py db_backups/live_locations_2026-07-19.json
```

The import deduplicates, so re-running is safe.

## 4. Admin dashboards

`admin_dashboard.html` and `admin_map.html` (opened as local files) now
prompt once for the admin API key and store it in your browser's
localStorage. Enter the same value you set as `ADMIN_API_KEY`.

## 5. What changed operationally

- Server now runs under gunicorn (see `Procfile` / `render.yaml`).
- Admin API requires the `X-Admin-Key` header; unauthenticated calls get 401.
- Chat endpoint is rate-limited (20/min, 300/day per IP).
- Chat logs store a hash of the visitor IP, not the raw IP.
- Old chat logs are still auto-deleted after 7 days; the location map is
  permanent (and now survives deploys, thanks to Postgres).
