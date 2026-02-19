from typing import Dict, List, Optional
import json

class OptimizationEngine:
    """Handles performance analysis and optimization of APIs."""
    
    def __init__(self):
        self.performance_data = {}
        self.historical_data = []
        
    def record_success(self, platform: str) -> None:
        """Record successful API integration."""
        self.performance_data[platform] = {
            "status": "success",
            "timestamp": self._get_current_time()
        }
        self._update_historical_data(platform)
        
    def record_failure(self, platform: str, error: str) -> None:
        """Record failed API integration."""
        self.performance_data[platform] = {
            "status": "failure",
            "error": error,
            "timestamp": self._get_current_time()
        }
        self._update_historical_data(platform)
        
    def optimize(self, platform: str) -> Optional[Dict]:
        """Optimize API usage based on historical performance."""
        if platform not in self.performance_data:
            return None
            
        # Analyze historical data for this platform
        history = self.get_platform_history(platform)
        recommendations = {
            "rate_limit": self._calculate_rate_limit(history),
            "optimization_strategies": self._suggest_optimizations(history)
        }
        
        return recommendations
    
    def _get_current_time(self) -> str:
        """Helper method to get current timestamp."""
        import datetime
        return datetime.datetime.now().isoformat()
    
    def _update_historical_data(self, platform: str) -> None:
        """Update historical data with recent performance metrics."""
        self.historical_data.append({
            "platform": platform,
            "timestamp": self._get_current_time(),
            **self.performance_data[platform]
        })
        # Maintain only the last 100 records for efficiency
        if len(self.historical_data) > 100:
            self.historical_data.pop(0)
    
    def get_platform_history(self, platform: str) -> List[Dict]:
        """Retrieve historical data for a specific platform."""
        return [data