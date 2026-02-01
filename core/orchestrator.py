import os
import subprocess
import yaml
import logging
from datetime import datetime

class ReconXOrchestrator:
    def __init__(self, config_path="config/config.yaml"):
        self.config = self.load_config(config_path)
        self.setup_logging()
        self.output_base = self.config['preferences'].get('output_dir', 'output')
        
    def load_config(self, path):
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("reconx.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("ReconX")

    def create_project_dir(self, domain):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = os.path.join(self.output_base, f"{domain}_{timestamp}")
        os.makedirs(project_dir, exist_ok=True)
        return project_dir

    def run_command(self, command, output_file=None):
        self.logger.info(f"Running: {' '.join(command)}")
        try:
            if output_file:
                with open(output_file, 'w') as f:
                    subprocess.run(command, stdout=f, stderr=subprocess.PIPE, text=True, check=True)
            else:
                result = subprocess.run(command, capture_output=True, text=True, check=False)
                return result.stdout
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {e.stderr}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return None

if __name__ == "__main__":
    # Test initialization
    orch = ReconXOrchestrator()
    print("Orchestrator initialized successfully.")
