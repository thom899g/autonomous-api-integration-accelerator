import logging
from typing import Dict, List, Optional
import requests
from .optimization_engine import OptimizationEngine
from .monitoring_analytics import ApiMonitor

class ApiIntegrationAgent:
    """Handles the discovery, integration, and optimization of APIs."""
    
    def __init__(self):
        self.optimization_engine = OptimizationEngine()
        self.monitor = ApiMonitor()
        logging.basicConfig(level=logging.INFO)
        
    def _discoverApis(self, platforms: List[str]) -> Dict[str, str]:
        """Discover API endpoints for specified platforms."""
        api_endpoints = {}
        for platform in platforms:
            try:
                response = requests.get(f"https://api.{platform}/v1/endpoints")
                if response.status_code == 200:
                    endpoints = response.json()
                    api_endpoints[platform] = endpoints.get("endpoint_url", "")
                    self.monitor.log_event(f"Successfully discovered API for {platform}")
            except Exception as e:
                logging.error(f"Failed to discover API for {platform}: {str(e)}")
        return api_endpoints
    
    def automateIntegration(self, platforms: List[str], config: Dict) -> bool:
        """Automatically integrate APIs with the system."""
        success = True
        endpoints = self._discoverApis(platforms)
        
        for platform in platforms:
            endpoint = endpoints.get(platform, "")
            if not endpoint:
                logging.error(f"No API endpoint found for {platform}")
                continue
                
            try:
                response = requests.post(
                    endpoint,
                    json=config,
                    headers={"Authorization": "Bearer " + config["api_key"]}
                )
                
                if response.status_code == 200:
                    self.monitor.log_event(f"Successfully integrated API for {platform}")
                    # Feed success metrics into optimization engine
                    self.optimization_engine.record_success(platform)
                else:
                    logging.error(f"Integration failed for {platform}: {response.status_code}")
                    self.monitor.log_event(f"Integration failure for {platform}")
            except Exception as e:
                logging.error(f"Exception during API integration: {str(e)}")
                success = False
        
        return success
    
    def optimize(self, platform: str) -> Optional[Dict]:
        """Optimize API usage based on historical data."""
        return self.optimization_engine.optimize(platform)