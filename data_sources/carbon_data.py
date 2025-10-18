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
        
        # Default data based on Brazilian energy matrix and Renault datacenter infrastructure
        return {
            "datacenter": {
                "location": "Complexo Ayrton Senna - São José dos Pinhais",
                "pue_current": 2.0,
                "pue_target": 1.5,
                "pue_best_practice": 1.2,
                "cooling_type": "CRAC (Computer Room Air Conditioning)",
                "cooling_capacity_btu": 500000,
                "temperature_setpoint_c": 22,
                "renewable_capacity_kw": 0,
                "renewable_target_kw": 100
            },
            "servers": {
                "hp_proliant": {
                    "count": 90,
                    "model": "HP ProLiant DL380 Gen10",
                    "power_w": 400,
                    "cpu": "Intel Xeon Silver 4214",
                    "ram_gb": 64,
                    "storage_tb": 4,
                    "virtualization": "ESXi 7.0",
                    "avg_utilization_percent": 35,
                    "consolidation_potential": 30
                },
                "vxrail": {
                    "count": 10,
                    "model": "Dell VxRail E560",
                    "power_w": 800,
                    "cpu": "Intel Xeon Gold 6248",
                    "ram_gb": 512,
                    "storage_tb": 20,
                    "virtualization": "vSphere 7.0",
                    "avg_utilization_percent": 65,
                    "vm_density": 45
                }
            },
            "workload_patterns": {
                "business_hours": {"start": 7, "end": 19, "avg_load_percent": 75},
                "extended_hours": {"start": 19, "end": 23, "avg_load_percent": 40},
                "night_maintenance": {"start": 23, "end": 7, "avg_load_percent": 15}
            },
            "emission_factors": {
                "grid_brazil_kg_co2_per_kwh": 0.0817,  # kg CO2/kWh (ONS 2024)
                "renewable_kg_co2_per_kwh": 0.02,  # kg CO2/kWh (solar/wind)
                "diesel_kg_co2_per_liter": 0.75  # kg CO2/liter (backup)
            },
            "energy_costs": {
                "base_rate_brl_per_kwh": 0.60,  # R$/kWh average industrial rate
                "peak_multiplier": 1.5,  # Peak hours cost multiplier
                "peak_hours": [18, 19, 20, 21]
            },
            "carbon_sequestration": {
                "tree_annual_kg_co2": 22,  # Average tree CO2 absorption per year
                "area_per_tree_m2": 12  # Space needed per tree
            }
        }
    
    def get_emission_factor(self, source: str = "grid_brazil") -> float:
        """
        Get CO2 emission factor for specified energy source
        
        Args:
            source: Energy source type (grid_brazil, renewable, diesel)
            
        Returns:
            Emission factor in kg CO2/kWh or kg CO2/liter
        """
        key_map = {
            "grid_brazil": "grid_brazil_kg_co2_per_kwh",
            "brazil_grid": "grid_brazil_kg_co2_per_kwh",  # backwards compatibility
            "renewable": "renewable_kg_co2_per_kwh",
            "renewable_energy": "renewable_kg_co2_per_kwh",  # backwards compatibility
            "diesel": "diesel_kg_co2_per_liter",
            "diesel_generator": "diesel_kg_co2_per_liter"  # backwards compatibility
        }
        key = key_map.get(source, "grid_brazil_kg_co2_per_kwh")
        return self.data["emission_factors"].get(key, 0.0817)
    
    def get_datacenter_data(self) -> Dict:
        """Get datacenter-specific data"""
        return self.data.get("datacenter", {})
    
    def get_server_data(self) -> Dict:
        """Get server-specific data"""
        return self.data.get("servers", {})
    
    def get_server_metrics(self) -> List[Dict]:
        """
        Get metrics for each server type
        
        Returns:
            List of dicts with server metrics
        """
        servers_data = self.get_server_data()
        
        metrics = []
        for server_type, server_info in servers_data.items():
            count = server_info["count"]
            power_w = server_info["power_w"]
            utilization = server_info["avg_utilization_percent"] / 100.0
            
            # Calculate consumption (kW)
            consumption_kw = (count * power_w * utilization) / 1000
            
            metrics.append({
                "type": server_type,
                "model": server_info.get("model", "Unknown"),
                "count": count,
                "power_w": power_w,
                "utilization_percent": server_info["avg_utilization_percent"],
                "consumption_kw": consumption_kw,
                "annual_consumption_kwh": consumption_kw * 24 * 365,
                "annual_co2_kg": consumption_kw * 24 * 365 * self.get_emission_factor(),
                "virtualization": server_info.get("virtualization", "N/A"),
                "consolidation_potential": server_info.get("consolidation_potential", 0),
                "vm_density": server_info.get("vm_density", 0)
            })
        
        return metrics
    
    def calculate_pue(self, include_cooling: bool = True) -> float:
        """
        Calculate Power Usage Effectiveness of the datacenter
        
        PUE = Total Facility Energy / IT Equipment Energy
        
        Args:
            include_cooling: Whether to include cooling in calculation
            
        Returns:
            PUE value (lower is better, ideal is 1.0)
        """
        datacenter = self.get_datacenter_data()
        return datacenter.get("pue_current", 2.0)
    
    def get_consolidation_potential(self) -> Dict:
        """
        Analyze potential for server consolidation via virtualization
        
        Returns:
            Dictionary with consolidation analysis
        """
        servers = self.get_server_data()
        
        # Calculate current state
        total_servers = sum(s["count"] for s in servers.values())
        
        # HP ProLiant consolidation (30% potential)
        hp_data = servers.get("hp_proliant", {})
        hp_consolidation = int(hp_data.get("count", 0) * hp_data.get("consolidation_potential", 0) / 100)
        
        # Target state after consolidation
        target_servers = total_servers - hp_consolidation
        reduction_percent = (hp_consolidation / total_servers * 100) if total_servers > 0 else 0
        
        # Energy savings
        energy_saved_kw = (hp_consolidation * hp_data.get("power_w", 400)) / 1000
        annual_savings_kwh = energy_saved_kw * 24 * 365
        
        energy_costs = self.get_energy_costs()
        cost_savings_brl = annual_savings_kwh * energy_costs.get("base_rate_brl_per_kwh", 0.60)
        co2_reduction_kg = annual_savings_kwh * self.get_emission_factor()
        
        return {
            "servers_current": total_servers,
            "servers_target": target_servers,
            "servers_to_consolidate": hp_consolidation,
            "reduction_percent": round(reduction_percent, 1),
            "energy_savings_kwh": round(annual_savings_kwh, 2),
            "cost_savings_brl": round(cost_savings_brl, 2),
            "co2_reduction_kg": round(co2_reduction_kg, 2)
        }
    
    def get_cooling_efficiency(self) -> Dict:
        """
        Get cooling efficiency metrics
        
        Returns:
            Dictionary with cooling metrics
        """
        datacenter = self.get_datacenter_data()
        pue = datacenter.get("pue_current", 2.0)
        
        # Calculate cooling overhead (PUE - 1.0)
        cooling_overhead = pue - 1.0
        
        # Get total server power
        servers = self.get_server_data()
        total_server_power_kw = sum(s["count"] * s["power_w"] for s in servers.values()) / 1000
        
        # Cooling power is the overhead
        cooling_power_kw = total_server_power_kw * cooling_overhead
        
        # Potential optimization to target PUE
        target_pue = datacenter.get("pue_target", 1.5)
        target_cooling_overhead = target_pue - 1.0
        target_cooling_kw = total_server_power_kw * target_cooling_overhead
        
        optimization_potential_kw = cooling_power_kw - target_cooling_kw
        annual_savings_kwh = optimization_potential_kw * 24 * 365
        
        return {
            "current_pue": pue,
            "target_pue": target_pue,
            "cooling_power_kw": round(cooling_power_kw, 2),
            "cooling_overhead_percent": round(cooling_overhead * 100, 1),
            "optimization_potential_kw": round(optimization_potential_kw, 2),
            "annual_savings_kwh": round(annual_savings_kwh, 2),
            "pue_contribution": round(cooling_overhead / pue * 100, 1)
        }
    
    def get_datacenter_consumption(self, hour: Optional[int] = None) -> Dict:
        """
        Get total datacenter consumption with breakdown
        
        Args:
            hour: Hour of day (0-23), if None uses current patterns average
            
        Returns:
            Dictionary with consumption breakdown
        """
        servers = self.get_server_data()
        
        # Calculate server consumption
        if hour is not None:
            load_factor = self.calculate_utilization_factor(hour)
        else:
            # Use average load factor
            load_factor = 0.55  # Average across all periods
        
        servers_kwh = 0
        for server_type, server_info in servers.items():
            base_utilization = server_info["avg_utilization_percent"] / 100.0
            effective_utilization = base_utilization * load_factor
            consumption = server_info["count"] * server_info["power_w"] * effective_utilization / 1000
            servers_kwh += consumption
        
        # Apply PUE for total facility consumption
        pue = self.calculate_pue()
        total_kwh = servers_kwh * pue
        cooling_kwh = total_kwh - servers_kwh
        
        return {
            "servers_kwh": round(servers_kwh, 2),
            "cooling_kwh": round(cooling_kwh, 2),
            "other_kwh": 0,  # UPS, lighting, etc. included in PUE
            "total_kwh": round(total_kwh, 2),
            "pue": pue,
            "hour": hour
        }
    
    def get_carbon_sequestration_data(self) -> Dict:
        """Get tree planting equivalency data"""
        return self.data["carbon_sequestration"]
    
    def get_energy_costs(self) -> Dict:
        """Get energy cost configuration"""
        return self.data["energy_costs"]
    
    def get_workload_patterns(self) -> Dict:
        """Get hourly workload patterns"""
        return self.data.get("workload_patterns", {})
    
    def calculate_utilization_factor(self, hour: int) -> float:
        """
        Calculate utilization factor based on time of day
        
        Args:
            hour: Hour of day (0-23)
            
        Returns:
            Utilization factor (0.0-1.0)
        """
        patterns = self.get_workload_patterns()
        
        # Check business hours
        business = patterns.get("business_hours", {})
        if business.get("start", 7) <= hour <= business.get("end", 19):
            return business.get("avg_load_percent", 75) / 100.0
        
        # Check extended hours
        extended = patterns.get("extended_hours", {})
        if extended.get("start", 19) <= hour <= extended.get("end", 23):
            return extended.get("avg_load_percent", 40) / 100.0
        
        # Night maintenance
        night = patterns.get("night_maintenance", {})
        return night.get("avg_load_percent", 15) / 100.0
    
    def get_optimization_potential(self) -> Dict:
        """
        Calculate potential savings from server optimization (consolidation + PUE)
        
        Returns:
            Dictionary with optimization metrics
        """
        # Get consolidation savings
        consolidation = self.get_consolidation_potential()
        
        # Get PUE optimization savings
        cooling = self.get_cooling_efficiency()
        
        # Total savings
        total_savings_kwh = consolidation["energy_savings_kwh"] + cooling["annual_savings_kwh"]
        
        energy_costs = self.get_energy_costs()
        total_savings_brl = total_savings_kwh * energy_costs.get("base_rate_brl_per_kwh", 0.60)
        total_co2_reduction_kg = total_savings_kwh * self.get_emission_factor()
        
        carbon_data = self.get_carbon_sequestration_data()
        trees_equivalent = int(total_co2_reduction_kg / carbon_data["tree_annual_kg_co2"])
        
        # Calculate current total consumption for reduction percentage
        current_consumption = self.get_datacenter_consumption()
        annual_current_kwh = current_consumption["total_kwh"] * 24 * 365
        reduction_percentage = (total_savings_kwh / annual_current_kwh * 100) if annual_current_kwh > 0 else 0
        
        return {
            "consolidation_servers": consolidation["servers_to_consolidate"],
            "pue_optimization_kwh": round(cooling["annual_savings_kwh"], 2),
            "consolidation_kwh": round(consolidation["energy_savings_kwh"], 2),
            "annual_savings_kwh": round(total_savings_kwh, 2),
            "annual_savings_brl": round(total_savings_brl, 2),
            "co2_reduction_kg": round(total_co2_reduction_kg, 2),
            "trees_equivalent": trees_equivalent,
            "reduction_percentage": round(reduction_percentage, 1),
            "target_pue": cooling["target_pue"],
            "current_pue": cooling["current_pue"]
        }


# Singleton instance for easy access
_carbon_data_loader = None

def get_carbon_data_loader() -> CarbonDataLoader:
    """Get or create singleton instance of CarbonDataLoader"""
    global _carbon_data_loader
    if _carbon_data_loader is None:
        _carbon_data_loader = CarbonDataLoader()
    return _carbon_data_loader
