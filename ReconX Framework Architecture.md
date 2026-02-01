# ReconX Framework Architecture

ReconX is designed as a modular Python-based framework that orchestrates best-in-class security tools.

## 1. Core Workflow
1.  **Subdomain Discovery**: `subfinder`, `assetfinder`, `amass` (passive/active).
2.  **Live Host Detection**: `httpx` (filtering for 200/300/400/500 status codes, titles, tech stack).
3.  **Port Scanning**: `naabu` (high-speed TCP/UDP scanning).
4.  **URL Harvesting**: `gau`, `waybackurls`, `katana`.
5.  **JavaScript Analysis**: `subjs`, custom regex for secrets/endpoints.
6.  **Parameter Extraction**: `arjun`, `paramspider`.
7.  **Vulnerability Scanning**: `nuclei` (focused on critical/high impact templates).
8.  **Output Management**: Structured JSON/Markdown reports, Burp-compatible lists.

## 2. Technical Stack
- **Language**: Python 3.11+
- **Concurrency**: `asyncio` and `subprocess` for tool orchestration.
- **CLI**: `typer` or `argparse` for a modern interface.
- **Config**: YAML-based configuration for API keys and tool paths.
- **Data Storage**: Local filesystem with structured directories (e.g., `output/domain/subdomains.txt`).

## 3. Module Design
- `Core`: Orchestrator, logger, config loader.
- `Discovery`: Subdomain and host detection.
- `Spidering`: URL harvesting and JS analysis.
- `Scanning`: Vulnerability detection.
- `Reporter`: Formatting and exporting results.

## 4. Key Tools to Integrate
| Category | Tools |
| :--- | :--- |
| Subdomains | subfinder, assetfinder, amass |
| Probing | httpx |
| Ports | naabu |
| URLs | gau, katana |
| Params | arjun |
| Vulnerabilities | nuclei |
