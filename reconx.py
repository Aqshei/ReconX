import argparse
import os
from core.orchestrator import ReconXOrchestrator
from modules.discovery import DiscoveryModule
from modules.spidering import SpideringModule
from modules.scanning import ScanningModule

def main():
    parser = argparse.ArgumentParser(description="ReconX - All-in-one reconnaissance framework.")
    parser.add_argument("-d", "--domain", required=True, help="Target domain for reconnaissance.")
    parser.add_argument("-c", "--config", default="config/config.yaml", help="Path to configuration file.")
    
    args = parser.parse_args()

    orchestrator = ReconXOrchestrator(config_path=args.config)
    project_dir = orchestrator.create_project_dir(args.domain)
    orchestrator.logger.info(f"ReconX started for domain: {args.domain}")
    orchestrator.logger.info(f"Project directory: {project_dir}")

    results = {}

    # Phase 1: Subdomain Enumeration
    discovery_module = DiscoveryModule(orchestrator)
    subdomains_file = discovery_module.enumerate_subdomains(args.domain, project_dir)
    results["Subdomain Enumeration"] = {"status": "Completed" if subdomains_file else "Failed", "file": subdomains_file}

    # Phase 2: Live Host Detection
    live_hosts_file = discovery_module.detect_live_hosts(subdomains_file, project_dir)
    results["Live Host Detection"] = {"status": "Completed" if live_hosts_file else "Failed", "file": live_hosts_file}

    # Phase 3: URL Harvesting, JS Analysis, Parameter Extraction
    spidering_module = SpideringModule(orchestrator)
    urls_file = spidering_module.harvest_urls(args.domain, live_hosts_file, project_dir)
    results["URL Harvesting"] = {"status": "Completed" if urls_file else "Failed", "file": urls_file}

    js_urls_file = spidering_module.analyze_js(urls_file, project_dir)
    results["JS Analysis"] = {"status": "Completed" if js_urls_file else "Failed", "file": js_urls_file}

    params_file = spidering_module.extract_parameters(urls_file, project_dir)
    results["Parameter Extraction"] = {"status": "Completed" if params_file else "Failed", "file": params_file}

    # Phase 4: Vulnerability Scanning
    scanning_module = ScanningModule(orchestrator)
    vulns_file = scanning_module.run_nuclei(live_hosts_file, project_dir)
    results["Vulnerability Scanning"] = {"status": "Completed" if vulns_file else "Failed", "file": vulns_file}

    # Generate Report
    report_path = scanning_module.generate_report(args.domain, project_dir, results)
    orchestrator.logger.info(f"ReconX finished. Report generated at: {report_path}")

if __name__ == "__main__":
    main()
