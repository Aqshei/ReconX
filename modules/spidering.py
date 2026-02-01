import os
import re
from core.orchestrator import ReconXOrchestrator

class SpideringModule:
    def __init__(self, orchestrator: ReconXOrchestrator):
        self.orch = orchestrator

    def harvest_urls(self, domain, live_hosts_file, project_dir):
        self.orch.logger.info(f"Harvesting URLs for {domain}")
        urls_file = os.path.join(project_dir, "urls.txt")
        
        # Using gau (Get All URLs)
        gau_cmd = ["timeout", "60s", self.orch.config['tools']['gau'], domain, "--subs"]
        urls = self.orch.run_command(gau_cmd)
        
        if urls:
            with open(urls_file, "w") as f:
                f.write(urls)
            self.orch.logger.info(f"Harvested {len(urls.splitlines())} URLs.")
            return urls_file
        return None

    def analyze_js(self, urls_file, project_dir):
        if not urls_file or not os.path.exists(urls_file):
            return None
            
        self.orch.logger.info("Extracting and analyzing JavaScript files")
        js_urls_file = os.path.join(project_dir, "js_urls.txt")
        
        # Filter JS files from URLs
        with open(urls_file, "r") as f:
            urls = f.readlines()
        
        js_urls = [u.strip() for u in urls if u.strip().endswith(".js") or ".js?" in u]
        
        if js_urls:
            with open(js_urls_file, "w") as f:
                f.write("\n".join(js_urls))
            self.orch.logger.info(f"Found {len(js_urls)} JS files.")
            return js_urls_file
        return None

    def extract_parameters(self, urls_file, project_dir):
        self.orch.logger.info("Extracting parameters for manual testing")
        params_file = os.path.join(project_dir, "parameters.txt")
        
        # Simple regex extraction for parameters
        if not urls_file or not os.path.exists(urls_file):
            return None
            
        with open(urls_file, "r") as f:
            content = f.read()
            
        params = set(re.findall(r"[\?&]([a-zA-Z0-9_\-\[\]]+)=", content))
        
        if params:
            with open(params_file, "w") as f:
                f.write("\n".join(params))
            self.orch.logger.info(f"Extracted {len(params)} unique parameters.")
            return params_file
        return None
