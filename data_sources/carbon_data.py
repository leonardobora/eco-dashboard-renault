"""
Carbon Data Loader - Real data integration from PDF studies
Loads and processes carbon consumption data from Renault's infrastructure studies
"""

import json
from typing import Dict, List, Optional
from pathlib import Path


class CarbonDataLoader:
    """
    Loads real carbon consumption data from PDF studies and configuration files
    
    Based on the 'Relação de consumo de carbono' PDF study for Renault
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the carbon data loader
        
        Args:
            config_path: Path to carbon_data.json configuration file
        """
        self.config_path = config_path or "config/carbon_data.json"
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """
        Load carbon data from configuration file
        Falls back to default values if file doesn't exist
        """
        config_file = Path(self.config_path)
        
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Default data based on Brazilian energy matrix and Renault infrastructure
        return {
            "emission_factors": {
                "brazil_grid": 0.0817,  # kg CO2/kWh (ONS 2024)
                "renewable_energy": 0.0200,  # kg CO2/kWh (solar/wind)
                "diesel_generator": 0.7500  # kg CO2/kWh (backup)
            },
            "infrastructure": {
                "workstations": {
                    "total": 5376,
                    "avg_consumption_w": 250,
                    "idle_consumption_w": 100,
                    "by_sector": {
                        "engineering": {"count": 1200, "utilization": 0.85},
                        "administration": {"count": 1500, "utilization": 0.70},
                        "production": {"count": 1800, "utilization": 0.90},
                        "quality": {"count": 576, "utilization": 0.75},
                        "logistics": {"count": 300, "utilization": 0.80}
                    }
                },
                "servers": {
                    "hp_proliant": {
                        "count": 90,
                        "avg_consumption_w": 400,
                        "utilization": 0.65
                    },
                    "vxrail": {
                        "count": 10,
                        "avg_consumption_w": 800,
                        "utilization": 0.85
                    }
                }
            },
            "carbon_sequestration": {
                "tree_annual_kg_co2": 22,  # Average tree CO2 absorption per year
                "area_per_tree_m2": 12  # Space needed per tree
            },
            "energy_costs": {
                "tariff_brl_kwh": 0.60,  # R$/kWh average industrial rate
                "peak_multiplier": 1.5,  # Peak hours cost multiplier
                "peak_hours": {
                    "start": 18,
                    "end": 21
                }
            },
            "usage_patterns": {
                "commercial_hours": {"start": 8, "end": 18, "utilization": 0.80},
                "reduced_hours": {"start": 19, "end": 22, "utilization": 0.40},
                "night_hours": {"start": 23, "end": 7, "utilization": 0.20}
            }
        }
    
    def get_emission_factor(self, source: str = "brazil_grid") -> float:
        """
        Get CO2 emission factor for specified energy source
        
        Args:
            source: Energy source type (brazil_grid, renewable_energy, diesel_generator)
            
        Returns:
            Emission factor in kg CO2/kWh
        """
        return self.data["emission_factors"].get(source, 0.0817)
    
    def get_infrastructure_data(self) -> Dict:
        """Get complete infrastructure data"""
        return self.data["infrastructure"]
    
    def get_workstation_data(self) -> Dict:
        """Get workstation-specific data"""
        return self.data["infrastructure"]["workstations"]
    
    def get_server_data(self) -> Dict:
        """Get server-specific data"""
        return self.data["infrastructure"]["servers"]
    
    def get_sector_consumption(self) -> List[Dict]:
        """
        Calculate consumption by sector
        
        Returns:
            List of dicts with sector consumption details
        """
        sectors_data = self.data["infrastructure"]["workstations"]["by_sector"]
        avg_consumption = self.data["infrastructure"]["workstations"]["avg_consumption_w"]
        
        sectors = []
        for sector_name, sector_info in sectors_data.items():
            count = sector_info["count"]
            utilization = sector_info["utilization"]
            
            # Calculate consumption (kW)
            consumption_kw = (count * avg_consumption * utilization) / 1000
            
            sectors.append({
                "name": sector_name,
                "workstations": count,
                "utilization": utilization,
                "consumption_kw": consumption_kw,
                "annual_consumption_kwh": consumption_kw * 24 * 365,
                "annual_co2_kg": consumption_kw * 24 * 365 * self.get_emission_factor()
            })
        
        return sectors
    
    def get_carbon_sequestration_data(self) -> Dict:
        """Get tree planting equivalency data"""
        return self.data["carbon_sequestration"]
    
    def get_energy_costs(self) -> Dict:
        """Get energy cost configuration"""
        return self.data["energy_costs"]
    
    def get_usage_patterns(self) -> Dict:
        """Get hourly usage patterns"""
        return self.data["usage_patterns"]
    
    def calculate_utilization_factor(self, hour: int) -> float:
        """
        Calculate utilization factor based on time of day
        
        Args:
            hour: Hour of day (0-23)
            
        Returns:
            Utilization factor (0.0-1.0)
        """
        patterns = self.get_usage_patterns()
        
        if patterns["commercial_hours"]["start"] <= hour <= patterns["commercial_hours"]["end"]:
            return patterns["commercial_hours"]["utilization"]
        elif patterns["reduced_hours"]["start"] <= hour <= patterns["reduced_hours"]["end"]:
            return patterns["reduced_hours"]["utilization"]
        else:
            return patterns["night_hours"]["utilization"]
    
    def get_optimization_potential(self) -> Dict:
        """
        Calculate potential savings from optimization
        
        Returns:
            Dictionary with optimization metrics
        """
        workstation_data = self.get_workstation_data()
        total_workstations = workstation_data["total"]
        avg_consumption = workstation_data["avg_consumption_w"]
        idle_consumption = workstation_data["idle_consumption_w"]
        
        # Calculate potential savings from turning off idle workstations
        # Assuming 20% of workstations could be optimized
        optimizable_workstations = int(total_workstations * 0.20)
        
        # Annual savings (assuming 8h/day, 250 days/year of idle time)
        hours_per_year = 8 * 250
        savings_kwh = (optimizable_workstations * avg_consumption * hours_per_year) / 1000
        
        energy_costs = self.get_energy_costs()
        savings_brl = savings_kwh * energy_costs["tariff_brl_kwh"]
        co2_reduction_kg = savings_kwh * self.get_emission_factor()
        
        carbon_data = self.get_carbon_sequestration_data()
        trees_equivalent = int(co2_reduction_kg / carbon_data["tree_annual_kg_co2"])
        
        return {
            "optimizable_workstations": optimizable_workstations,
            "annual_savings_kwh": savings_kwh,
            "annual_savings_brl": savings_brl,
            "co2_reduction_kg": co2_reduction_kg,
            "trees_equivalent": trees_equivalent,
            "reduction_percentage": 20.0
        }


# Singleton instance for easy access
_carbon_data_loader = None

def get_carbon_data_loader() -> CarbonDataLoader:
    """Get or create singleton instance of CarbonDataLoader"""
    global _carbon_data_loader
    if _carbon_data_loader is None:
        _carbon_data_loader = CarbonDataLoader()
    return _carbon_data_loader
