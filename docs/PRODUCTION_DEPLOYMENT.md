# Production deployment

Production URL: `https://job-evaluation.duckdns.org`.

## 1. DNS and firewall

Point the DuckDNS record to the server's public IPv4 address. Forward TCP ports 80 and 443 to the server; allow UDP 443 for HTTP/3. Do not expose PostgreSQL port 5432. The existing shared Caddy obtains and renews the TLS certificate automatically after DNS resolves and ports 80/443 are reachable.

## 2. Google OAuth

In the Web application OAuth client set:

- Authorized JavaScript origin: `https://job-evaluation.duckdns.org`
- Authorized redirect URI: `https://job-evaluation.duckdns.org/api/auth/google/callback`

Local entries (`http://127.0.0.1:8001` and its callback) may remain for development. The consent screen must include every tester while the app is in Testing status. For general use, publish the app to Production; only `openid`, `email`, and `profile` scopes are requested.

## 3. Server setup

Install Docker Engine with the Compose plugin, clone the repository, then create the production environment file:

```bash
cp .env.production.example .env
chmod 600 .env
```

Replace every `CHANGE_ME` value. Never commit `.env`.

Rotate any credential that has appeared in terminal output, chat, screenshots, or repository history. In particular, create a new Google client secret and a new LLM API key before the first production start.

Find the Docker network used by the existing Caddy container and set it as `CADDY_NETWORK` in `.env`:

```bash
docker inspect CADDY_CONTAINER_NAME --format '{{range $name, $_ := .NetworkSettings.Networks}}{{$name}}{{"\n"}}{{end}}'
```

Both `jeval_backend` and `jeval_frontend` join this external network. PostgreSQL stays on a separate internal network.

Add this block to the existing server Caddyfile:

```caddy
job-evaluation.duckdns.org {
    handle /api/* {
        reverse_proxy jeval_backend:8000
    }

    handle {
        reverse_proxy jeval_frontend:80
    }
}
```

Start the stack:

```bash
docker compose up -d --build
docker compose ps
docker compose logs --tail=100 backend frontend
curl -fsS https://job-evaluation.duckdns.org/health
```

Backend and frontend do not publish host ports. Public traffic enters through the existing Caddy on 80/443. Uploaded documents and PostgreSQL data use Docker volumes.

Self-registration by email and password is enabled in production. Google sign-in keeps its separate company access allowlist check while `JEVAL_DISABLE_ACCESS_GATE=false`.

## 4. Updates and backup

Before an update, back up PostgreSQL:

```bash
docker compose exec -T db pg_dump -U jeval -d jeval -Fc > jeval-$(date +%F).dump
git pull --ff-only
docker compose up -d --build
```

Also back up the `backend_uploads` Docker volume. Keep database and upload backups together: database records refer to those files.

## 5. Verification

- Open the site in a private browser window and verify HTTPS.
- Test email/password and Google login/logout.
- Verify an uninvited Google account is rejected when `JEVAL_DISABLE_ACCESS_GATE=false`.
- Upload a test document and confirm it remains after container recreation.
- Check `docker compose logs` for OAuth, database, and proxy errors.
