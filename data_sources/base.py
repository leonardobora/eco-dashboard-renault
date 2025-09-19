"""
Base data source interface for EcoTI Dashboard
Provides abstract base classes for all data sources
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DeviceInfo:
    """Information about a monitored device"""
    device_id: str
    device_type: str  # 'workstation', 'server', 'network'
    location: str
    department: str
    power_rating: float  # Watts
    status: str  # 'active', 'idle', 'offline'
    last_seen: datetime

@dataclass
class EnergyReading:
    """Energy consumption reading from a device"""
    device_id: str
    timestamp: datetime
    power_consumption: float  # Watts
    voltage: Optional[float] = None
    current: Optional[float] = None
    temperature: Optional[float] = None

@dataclass
class EnvironmentalMetrics:
    """Calculated environmental metrics"""
    total_consumption_kwh: float
    co2_emissions_kg: float
    cost_savings_potential: float
    trees_equivalent: int
    calculation_timestamp: datetime

class DataSourceInterface(ABC):
    """Abstract base class for all data sources"""
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the data source"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Close connection to the data source"""
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """Check if connection is active"""
        pass
    
    @abstractmethod
    def get_devices(self) -> List[DeviceInfo]:
        """Get list of all monitored devices"""
        pass
    
    @abstractmethod
    def get_energy_readings(self, device_id: Optional[str] = None, 
                          start_time: Optional[datetime] = None,
                          end_time: Optional[datetime] = None) -> List[EnergyReading]:
        """Get energy readings for devices in time range"""
        pass
    
    @abstractmethod
    def get_current_consumption(self) -> float:
        """Get current total power consumption in kWh"""
        pass
    
    @abstractmethod
    def validate_data(self, reading: EnergyReading) -> bool:
        """Validate that a reading is within expected ranges"""
        pass

class MetricsCalculator:
    """Calculates environmental metrics from energy data"""
    
    def __init__(self, emission_factor: float = 0.0817, 
                 tree_sequestration: float = 22.0,
                 energy_tariff: float = 0.60):
        """
        Initialize calculator with environmental factors
        
        Args:
            emission_factor: kg CO2/kWh (default: Brazil grid factor)
            tree_sequestration: kg CO2/year per tree
            energy_tariff: R$/kWh energy cost
        """
        self.emission_factor = emission_factor
        self.tree_sequestration = tree_sequestration
        self.energy_tariff = energy_tariff
    
    def calculate_co2_emissions(self, kwh_consumption: float) -> float:
        """Calculate CO2 emissions from kWh consumption"""
        return kwh_consumption * self.emission_factor
    
    def calculate_tree_equivalent(self, co2_kg: float) -> int:
        """Calculate equivalent trees needed to sequester CO2"""
        return int(co2_kg / self.tree_sequestration)
    
    def calculate_cost_savings(self, kwh_savings_potential: float) -> float:
        """Calculate potential cost savings from efficiency improvements"""
        return kwh_savings_potential * self.energy_tariff
    
    def calculate_metrics(self, current_kwh: float, 
                         annual_kwh: float,
                         efficiency_potential: float = 0.15) -> EnvironmentalMetrics:
        """
        Calculate complete environmental metrics
        
        Args:
            current_kwh: Current consumption in kWh
            annual_kwh: Annual consumption estimate in kWh
            efficiency_potential: % potential for efficiency improvement
        """
        co2_annual = self.calculate_co2_emissions(annual_kwh)
        trees = self.calculate_tree_equivalent(co2_annual)
        savings_kwh = annual_kwh * efficiency_potential
        cost_savings = self.calculate_cost_savings(savings_kwh)
        
        return EnvironmentalMetrics(
            total_consumption_kwh=current_kwh,
            co2_emissions_kg=co2_annual,
            cost_savings_potential=cost_savings,
            trees_equivalent=trees,
            calculation_timestamp=datetime.now()
        )