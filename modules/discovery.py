import os
from core.orchestrator import ReconXOrchestrator

class DiscoveryModule:
    def __init__(self, orchestrator: ReconXOrchestrator):
        self.orch = orchestrator

    def enumerate_subdomains(self, domain, project_dir):
        self.orch.logger.info(f"Starting subdomain enumeration for {domain}")
        subdomains_file = os.path.join(project_dir, "subdomains_raw.txt")
        
        # Subfinder
        subfinder_cmd = [self.orch.config['tools']['subfinder'], "-d", domain, "-silent"]
        subdomains = self.orch.run_command(subfinder_cmd)
        self.orch.logger.info(f"Subfinder output length: {len(subdomains) if subdomains else 0}")
        
        if subdomains:
            with open(subdomains_file, "w") as f:
                f.write(subdomains)
            
            # Count unique subdomains
            unique_subs = set(subdomains.splitlines())
            self.orch.logger.info(f"Found {len(unique_subs)} unique subdomains.")
            return subdomains_file
        return None

    def detect_live_hosts(self, subdomains_file, project_dir):
        if not subdomains_file or not os.path.exists(subdomains_file):
            return None
            
        self.orch.logger.info("Detecting live hosts using httpx")
        live_hosts_file = os.path.join(project_dir, "live_hosts.txt")
        json_output = os.path.join(project_dir, "live_hosts.json")
        
        httpx_cmd = [
            self.orch.config['tools']['httpx'],
            "-l", subdomains_file,
            "-silent",
            "-status-code",
            "-title",
            "-tech-detect",
            "-follow-redirects",
            "-o", live_hosts_file,
            "-json", "-oj", json_output
        ]
        
        self.orch.run_command(httpx_cmd)
        
        if os.path.exists(live_hosts_file):
            with open(live_hosts_file, "r") as f:
                count = len(f.readlines())
            self.orch.logger.info(f"Detected {count} live hosts.")
            return live_hosts_file
        return None
