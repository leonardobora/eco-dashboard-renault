"""
Synthetic data source for development and testing
Maintains current behavior while providing flexible structure
"""

import random
import math
from datetime import datetime, timedelta
from typing import List, Optional

from .base import DataSourceInterface, DeviceInfo, EnergyReading

class SyntheticDataSource(DataSourceInterface):
    """Synthetic data source that generates realistic test data"""
    
    def __init__(self):
        self.connected = False
        self.devices = self._generate_device_inventory()
        
    def _generate_device_inventory(self) -> List[DeviceInfo]:
        """Generate the Renault infrastructure inventory"""
        devices = []
        
        # Workstations by department
        departments = {
            'Administrativo': 1200,
            'Engenharia': 1500,
            'Produção': 1800,
            'Vendas': 600,
            'Suporte': 276
        }
        
        device_id = 1
        for dept, count in departments.items():
            for i in range(count):
                devices.append(DeviceInfo(
                    device_id=f"WS-{device_id:04d}",
                    device_type="workstation",
                    location=f"{dept}-Floor-{(i//50)+1}",
                    department=dept,
                    power_rating=random.uniform(200, 300),  # 200-300W range
                    status=self._get_device_status(),
                    last_seen=datetime.now() - timedelta(minutes=random.randint(0, 30))
                ))
                device_id += 1
        
        # HP Servers
        for i in range(90):
            devices.append(DeviceInfo(
                device_id=f"SRV-HP-{i+1:03d}",
                device_type="server",
                location=f"DataCenter-Rack-{(i//10)+1}",
                department="Infraestrutura",
                power_rating=random.uniform(350, 450),  # 350-450W range
                status="active",  # Servers usually always on
                last_seen=datetime.now() - timedelta(minutes=random.randint(0, 5))
            ))
        
        # VxRail Systems
        for i in range(10):
            devices.append(DeviceInfo(
                device_id=f"VXRAIL-{i+1:02d}",
                device_type="server",
                location=f"DataCenter-HyperConverged-{i+1}",
                department="Infraestrutura",
                power_rating=random.uniform(800, 1200),  # Higher power for VxRail
                status="active",
                last_seen=datetime.now() - timedelta(minutes=random.randint(0, 2))
            ))
        
        return devices
    
    def _get_device_status(self) -> str:
        """Generate realistic device status based on time of day"""
        hour = datetime.now().hour
        
        if 8 <= hour <= 18:  # Business hours
            return random.choices(
                ['active', 'idle', 'offline'], 
                weights=[75, 20, 5]
            )[0]
        elif 19 <= hour <= 22:  # Evening
            return random.choices(
                ['active', 'idle', 'offline'], 
                weights=[40, 50, 10]
            )[0]
        else:  # Night
            return random.choices(
                ['active', 'idle', 'offline'], 
                weights=[15, 60, 25]
            )[0]
    
    def connect(self) -> bool:
        """Simulate connection to synthetic data source"""
        self.connected = True
        return True
    
    def disconnect(self) -> None:
        """Simulate disconnection"""
        self.connected = False
    
    def is_connected(self) -> bool:
        """Check connection status"""
        return self.connected
    
    def get_devices(self) -> List[DeviceInfo]:
        """Get list of all devices in the infrastructure"""
        if not self.connected:
            raise ConnectionError("Data source not connected")
        return self.devices
    
    def get_energy_readings(self, device_id: Optional[str] = None,
                          start_time: Optional[datetime] = None,
                          end_time: Optional[datetime] = None) -> List[EnergyReading]:
        """Generate synthetic energy readings"""
        if not self.connected:
            raise ConnectionError("Data source not connected")
        
        readings = []
        devices = self.devices if device_id is None else [d for d in self.devices if d.device_id == device_id]
        
        for device in devices:
            # Generate reading based on device status and time
            base_power = device.power_rating
            if device.status == 'active':
                power = base_power * random.uniform(0.7, 1.0)
            elif device.status == 'idle':
                power = base_power * random.uniform(0.1, 0.3)
            else:  # offline
                power = 0
            
            # Add some realistic variation
            power *= random.uniform(0.95, 1.05)
            
            readings.append(EnergyReading(
                device_id=device.device_id,
                timestamp=datetime.now(),
                power_consumption=power,
                voltage=random.uniform(220, 240),
                current=power / 230,  # I = P/V
                temperature=random.uniform(35, 55)
            ))
        
        return readings
    
    def get_current_consumption(self) -> float:
        """Calculate current total consumption in kWh"""
        if not self.connected:
            raise ConnectionError("Data source not connected")
        
        # Time-based usage factor (similar to original logic)
        hour = datetime.now().hour
        if 8 <= hour <= 18:  # Business hours
            usage_factor = 0.8
        elif 19 <= hour <= 22:  # Evening
            usage_factor = 0.4
        else:  # Night
            usage_factor = 0.2
        
        # Calculate total power consumption
        total_watts = 0
        for device in self.devices:
            if device.device_type == "workstation":
                if device.status == "active":
                    total_watts += device.power_rating * usage_factor
                elif device.status == "idle":
                    total_watts += device.power_rating * 0.2
            else:  # servers
                total_watts += device.power_rating * 0.9  # Servers run at high utilization
        
        # Convert to kWh (instant reading)
        return total_watts / 1000
    
    def validate_data(self, reading: EnergyReading) -> bool:
        """Validate that readings are within expected ranges"""
        device = next((d for d in self.devices if d.device_id == reading.device_id), None)
        if not device:
            return False
        
        # Check if power consumption is reasonable for device type
        max_expected = device.power_rating * 1.1  # 10% tolerance
        min_expected = 0
        
        return min_expected <= reading.power_consumption <= max_expected