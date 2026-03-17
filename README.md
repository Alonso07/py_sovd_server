# SOVD Server

A **Service-Oriented Vehicle Data (SOVD)** server implementation based on **ISO/DIS 17978-3:2025**, with YAML-based configuration.

## Features

- **YAML-driven configuration** — Gateway, entities (areas, components, apps), and resources (data, operations, faults, modes) defined in YAML
- **RESTful SOVD API** — Data resources, operations, faults, and modes with JSON responses
- **No authentication** — Simplified setup for development and testing
- **CORS enabled** — Ready for web and tool clients

## Requirements

- **Python 3.9+**
- **Poetry** — [Install Poetry](https://python-poetry.org/docs/#installation) if you don’t have it

## Quick start

```bash
# Clone and enter the project
cd sovd_server

# Install dependencies (creates a virtual environment automatically)
poetry install
# or
make install

# Run the server
poetry run sovd-server
# or
make run-server
```

Server runs at **http://127.0.0.1:8080** by default. Try:

- **Health:** `curl http://localhost:8080/health`
- **Areas:** `curl http://localhost:8080/areas`
- **Engine data:** `curl http://localhost:8080/engine/data`

## Project layout

```
sovd_server/
├── src/sovd_server/           # Main package
│   ├── config/                # YAML configuration
│   │   ├── sovd_gateway.yaml  # Gateway (host, port, logging)
│   │   ├── entities/          # Areas, components, apps
│   │   └── resources/         # Data, operations, faults, modes
│   ├── config_loader.py       # YAML loader
│   ├── enhanced_server.py     # Flask/Connexion server
│   └── run_enhanced_server.py # CLI entry point
├── tests/
├── docs/                      # Additional documentation
├── pyproject.toml              # Project and dependencies (Poetry)
├── Makefile                   # Convenience commands
└── README.md
```

## Development

| Command | Description |
|--------|-------------|
| `make install` | Install dependencies (Poetry) |
| `make run-server` | Start the SOVD server |
| `make test` | Run tests |
| `make run-tests` | Run tests with coverage |
| `make lint` | Run flake8 and mypy |
| `make format` | Format code with Black |
| `make format-check` | Check formatting only |
| `make security` | Run bandit and safety |
| `make ci-local` | Lint, format-check, security, test |
| `make version` | Show package version |
| `make build` | Build wheel and sdist for distribution |
| `make clean` | Remove build artifacts and caches |

All commands run via Poetry (e.g. `poetry run pytest`). You can also run tools directly:

```bash
poetry run pytest tests/ -v
poetry run black src/ tests/
poetry run flake8 src/ tests/
```

## Configuration

- **Gateway:** `src/sovd_server/config/sovd_gateway.yaml` — host, port, logging, entity/resource file paths
- **Entities:** `config/entities/` — areas, components, applications
- **Resources:** `config/resources/` — data, operations, faults, modes

See [docs/](docs/INDEX.md) for detailed configuration and API notes.

## API overview

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `GET /version-info` | Server version |
| `GET /areas`, `/components`, `/apps` | List entities |
| `GET /{entity}/data` | Data resources for an entity |
| `GET /{entity}/data/{id}` | Single data resource |
| `GET /{entity}/operations` | Operations |
| `POST /{entity}/operations/{id}` | Execute operation |
| `GET /{entity}/faults`, `GET /{entity}/modes` | Faults and modes |

Example:

```bash
# Engine software part number
curl http://localhost:8080/engine/data/SoftwarePartNumber

# Start camera calibration
curl -X POST http://localhost:8080/camera/front/operations/calibratecamera \
  -H "Content-Type: application/json" \
  -d '{"calibration_type": "automatic", "target_distance": 10.0}'
```

## Installing the package

From PyPI (when published):

```bash
pip install sovd-server
sovd-server
```

From the project (editable):

```bash
poetry install
poetry run sovd-server
```

## Documentation

- [docs/INDEX.md](docs/INDEX.md) — Documentation index
- [docs/CONFIGURATION.md](docs/CONFIGURATION.md) — Configuration details
- [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) — How to contribute
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) — Deployment and PyPI publishing
- [docs/TESTING.md](docs/TESTING.md) — Testing
- [docs/VERSIONING.md](docs/VERSIONING.md) — Version and release process

## License

MIT. See [LICENSE](LICENSE) if present.
