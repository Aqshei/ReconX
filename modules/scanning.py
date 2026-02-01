import os
from core.orchestrator import ReconXOrchestrator

class ScanningModule:
    def __init__(self, orchestrator: ReconXOrchestrator):
        self.orch = orchestrator

    def run_nuclei(self, target_file, project_dir):
        if not target_file or not os.path.exists(target_file):
            return None
            
        self.orch.logger.info("Starting Nuclei vulnerability scan")
        vulns_file = os.path.join(project_dir, "vulnerabilities.txt")
        json_output = os.path.join(project_dir, "vulnerabilities.json")
        
        severity = self.orch.config['nuclei'].get('severity', 'critical,high')
        
        nuclei_cmd = [
            self.orch.config['tools']['nuclei'],
            "-l", target_file,
            "-severity", severity,
            "-silent",
            "-o", vulns_file,
            "-json-export", json_output
        ]
        
        self.orch.run_command(nuclei_cmd)
        
        if os.path.exists(vulns_file):
            with open(vulns_file, "r") as f:
                count = len(f.readlines())
            self.orch.logger.info(f"Nuclei found {count} potential vulnerabilities.")
            return vulns_file
        return None

    def generate_report(self, domain, project_dir, results):
        self.orch.logger.info("Generating final report")
        report_path = os.path.join(project_dir, "recon_summary.md")
        
        with open(report_path, "w") as f:
            f.write(f"# ReconX Scan Report: {domain}\n\n")
            f.write(f"**Date:** {os.path.basename(project_dir).split('_')[1]}\n\n")
            f.write("## Summary of Findings\n\n")
            
            f.write("| Module | Result | File |\n")
            f.write("| :--- | :--- | :--- |\n")
            for module, data in results.items():
                f.write(f"| {module} | {data['status']} | {os.path.basename(data['file']) if data['file'] else 'N/A'} |\n")
            
            f.write("\n\n## Next Steps for Manual Testing\n")
            f.write("1. Review `live_hosts.txt` and proxy interesting targets to Burp Suite.\n")
            f.write("2. Analyze `js_urls.txt` for sensitive endpoints or hardcoded secrets.\n")
            f.write("3. Use `parameters.txt` with Arjun or Burp Intruder for fuzzing.\n")
            f.write("4. Check `vulnerabilities.txt` for high-signal Nuclei findings.\n")
            
        return report_path
