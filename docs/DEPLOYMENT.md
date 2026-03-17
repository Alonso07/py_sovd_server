# Deployment Guide

This guide covers deployment and CI/CD for the SOVD Server.

## Quick Deployment

### Local Development
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
python -m sovd_server.run_enhanced_server
```

### Production
```bash
pip install .
# Or from wheel/sdist:
pip install dist/sovd_server-*.whl
python -m sovd_server.run_enhanced_server
```

Configuration is loaded from `src/sovd_server/config/` by default. Override or extend via environment or gateway YAML as needed.

## Configuration

- **Development**: Use `sovd_gateway.yaml` with host `127.0.0.1` and DEBUG logging if desired.
- **Production**: Use a dedicated gateway config with appropriate host/port and INFO (or WARNING) logging. Ensure config paths are correct for the deployment layout.

## Docker

Example Dockerfile (adjust paths to your layout):

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml setup.py README.md ./
COPY src/ ./src/

RUN pip install --no-cache-dir -e .

EXPOSE 8080

CMD ["python", "-m", "sovd_server.run_enhanced_server"]
```

Build and run:
```bash
docker build -t sovd-server .
docker run -p 8080:8080 sovd-server
```

## CI/CD (GitHub Actions)

The repository includes:

- **`.github/workflows/ci.yml`**: On push/PR to `main`/`develop`:
  - Lint (flake8), format check (black)
  - Security (bandit, safety)
  - Tests with coverage (pytest)
  - Optional: build package (on main)

No Poetry is required; the workflow uses pip and `pip install -e .`.

## System Service (systemd)

Example unit file:

```ini
[Unit]
Description=SOVD Server
After=network.target

[Service]
Type=simple
User=sovd
Group=sovd
WorkingDirectory=/opt/sovd-server
ExecStart=/opt/sovd-server/venv/bin/python -m sovd_server.run_enhanced_server
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## Monitoring and Logging

- Configure logging level and output in `sovd_gateway.yaml`.
- Use a process manager or systemd for restarts and logging.
- Optionally put a reverse proxy (e.g. nginx) in front and restrict access to the SOVD port.

## Security

- Run as a non-root user.
- Restrict network access to the SOVD port.
- Keep dependencies updated (e.g. with Dependabot or `pip install -U`).
- Do not expose the server unnecessarily to the internet.
