# ReconX - All-in-one Reconnaissance Framework

ReconX is a high-performance, all-in-one reconnaissance framework designed for bug bounty hunters and security researchers who want maximum attack surface coverage with minimal manual effort.

## 🎯 Core Philosophy

*   Automate recon, not thinking
*   Speed + coverage > blind scanning
*   Manual testing is non-negotiable
*   Designed for real bug bounty workflows

## ⚙️ Key Capabilities

*   Passive & active subdomain enumeration
*   Fast live host probing
*   Historical + live URL and endpoint discovery
*   JavaScript file collection for manual analysis
*   Hidden parameter discovery
*   Prioritized critical/high vulnerability detection
*   Clean, structured output for easy triage

## 🧠 Why ReconX Exists

Most bugs are not missed because of lack of skill — they’re missed because:

*   Recon is incomplete
*   Targets are noisy
*   Time is wasted on repetition

ReconX solves this by giving you full visibility of the attack surface, fast — so your time is spent where it matters: logic flaws, IDORs, auth bypasses, and workflow abuse.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Aqshei/ReconX.git
    cd ReconX
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install external tools:**
    ReconX relies on several best-in-class open-source tools. Please install them and ensure they are in your system's PATH. You can find installation instructions for each tool on their respective GitHub pages:
    *   `subfinder`
    *   `httpx`
    *   `gau`
    *   `nuclei`
    *   (Optional) `assetfinder`, `amass`, `katana`, `arjun`

4.  **Configure `config/config.yaml`:**
    Update the `config/config.yaml` file with paths to your tools (if not in PATH) and any API keys for enhanced results.

## Usage

```bash
python reconx.py -d example.com
```

### Arguments:

*   `-d`, `--domain`: Target domain for reconnaissance (e.g., `example.com`).
*   `-c`, `--config`: Path to the configuration file (default: `config/config.yaml`).

## Output

ReconX will create a timestamped directory under the `output/` folder for each scan, containing:

*   `subdomains_raw.txt`: All discovered subdomains.
*   `live_hosts.txt`: Live subdomains with HTTP(S) services.
*   `live_hosts.json`: Detailed JSON output from `httpx`.
*   `urls.txt`: Harvested URLs.
*   `js_urls.txt`: Discovered JavaScript files.
*   `parameters.txt`: Extracted URL parameters.
*   `vulnerabilities.txt`: Nuclei scan results.
*   `vulnerabilities.json`: Detailed JSON output from `nuclei`.
*   `recon_summary.md`: A markdown report summarizing the scan and providing next steps.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
