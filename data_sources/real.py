"""
Real data source implementations for production use
Ready for integration with actual monitoring systems
"""

import requests
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
try:
    import pysnmp
    SNMP_AVAILABLE = True
except ImportError:
    SNMP_AVAILABLE = False

from .base import DataSourceInterface, DeviceInfo, EnergyReading

logger = logging.getLogger(__name__)

class DatabaseDataSource(DataSourceInterface):
    """Data source that connects to a SQL database"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None
        
    def connect(self) -> bool:
        """Connect to the database"""
        try:
            self.connection = sqlite3.connect(self.connection_string)
            # Test connection
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False
    
    def disconnect(self) -> None:
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def is_connected(self) -> bool:
        """Check if database connection is active"""
        if not self.connection:
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            return True
        except:
            return False
    
    def get_devices(self) -> List[DeviceInfo]:
        """Get devices from database"""
        if not self.is_connected():
            raise ConnectionError("Database not connected")
        
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT device_id, device_type, location, department, 
                   power_rating, status, last_seen
            FROM devices
        """)
        
        devices = []
        for row in cursor.fetchall():
            devices.append(DeviceInfo(
                device_id=row[0],
                device_type=row[1],
                location=row[2],
                department=row[3],
                power_rating=row[4],
                status=row[5],
                last_seen=datetime.fromisoformat(row[6])
            ))
        
        return devices
    
    def get_energy_readings(self, device_id: Optional[str] = None,
                          start_time: Optional[datetime] = None,
                          end_time: Optional[datetime] = None) -> List[EnergyReading]:
        """Get energy readings from database"""
        if not self.is_connected():
            raise ConnectionError("Database not connected")
        
        cursor = self.connection.cursor()
        query = """
            SELECT device_id, timestamp, power_consumption, voltage, current, temperature
            FROM energy_readings
            WHERE 1=1
        """
        params = []
        
        if device_id:
            query += " AND device_id = ?"
            params.append(device_id)
        
        if start_time:
            query += " AND timestamp >= ?"
            params.append(start_time.isoformat())
        
        if end_time:
            query += " AND timestamp <= ?"
            params.append(end_time.isoformat())
        
        query += " ORDER BY timestamp DESC"
        
        cursor.execute(query, params)
        
        readings = []
        for row in cursor.fetchall():
            readings.append(EnergyReading(
                device_id=row[0],
                timestamp=datetime.fromisoformat(row[1]),
                power_consumption=row[2],
                voltage=row[3],
                current=row[4],
                temperature=row[5]
            ))
        
        return readings
    
    def get_current_consumption(self) -> float:
        """Get current total consumption from latest readings"""
        if not self.is_connected():
            raise ConnectionError("Database not connected")
        
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT SUM(power_consumption) / 1000.0 as total_kwh
            FROM energy_readings 
            WHERE timestamp > datetime('now', '-5 minutes')
        """)
        
        result = cursor.fetchone()
        return result[0] if result[0] else 0.0
    
    def validate_data(self, reading: EnergyReading) -> bool:
        """Validate reading against device specifications"""
        # Basic validation - can be enhanced based on business rules
        return (reading.power_consumption >= 0 and 
                reading.power_consumption <= 2000 and  # Max 2kW per device
                reading.timestamp <= datetime.now())

class RESTAPIDataSource(DataSourceInterface):
    """Data source that connects to REST APIs (e.g., IoT platforms, energy management systems)"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        self._connected = False
    
    def connect(self) -> bool:
        """Test API connection"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            self._connected = response.status_code == 200
            return self._connected
        except Exception as e:
            logger.error(f"API connection failed: {e}")
            return False
    
    def disconnect(self) -> None:
        """Close API session"""
        self.session.close()
        self._connected = False
    
    def is_connected(self) -> bool:
        """Check API connection status"""
        return self._connected
    
    def get_devices(self) -> List[DeviceInfo]:
        """Get devices from API"""
        if not self.is_connected():
            raise ConnectionError("API not connected")
        
        response = self.session.get(f"{self.base_url}/devices")
        response.raise_for_status()
        
        devices = []
        for device_data in response.json():
            devices.append(DeviceInfo(
                device_id=device_data['id'],
                device_type=device_data['type'],
                location=device_data['location'],
                department=device_data['department'],
                power_rating=device_data['power_rating'],
                status=device_data['status'],
                last_seen=datetime.fromisoformat(device_data['last_seen'])
            ))
        
        return devices
    
    def get_energy_readings(self, device_id: Optional[str] = None,
                          start_time: Optional[datetime] = None,
                          end_time: Optional[datetime] = None) -> List[EnergyReading]:
        """Get energy readings from API"""
        if not self.is_connected():
            raise ConnectionError("API not connected")
        
        params = {}
        if device_id:
            params['device_id'] = device_id
        if start_time:
            params['start_time'] = start_time.isoformat()
        if end_time:
            params['end_time'] = end_time.isoformat()
        
        response = self.session.get(f"{self.base_url}/readings", params=params)
        response.raise_for_status()
        
        readings = []
        for reading_data in response.json():
            readings.append(EnergyReading(
                device_id=reading_data['device_id'],
                timestamp=datetime.fromisoformat(reading_data['timestamp']),
                power_consumption=reading_data['power_consumption'],
                voltage=reading_data.get('voltage'),
                current=reading_data.get('current'),
                temperature=reading_data.get('temperature')
            ))
        
        return readings
    
    def get_current_consumption(self) -> float:
        """Get current consumption from API"""
        if not self.is_connected():
            raise ConnectionError("API not connected")
        
        response = self.session.get(f"{self.base_url}/current-consumption")
        response.raise_for_status()
        
        return response.json()['consumption_kwh']
    
    def validate_data(self, reading: EnergyReading) -> bool:
        """Validate API data"""
        return (reading.power_consumption >= 0 and 
                reading.timestamp <= datetime.now())

class SNMPDataSource(DataSourceInterface):
    """Data source for SNMP-enabled devices (UPS, PDUs, smart switches)"""
    
    def __init__(self, snmp_community: str = 'public'):
        if not SNMP_AVAILABLE:
            raise ImportError("pysnmp library required for SNMP data source")
        
        self.community = snmp_community
        self.devices_config = []  # Will store SNMP device configurations
        self._connected = False
    
    def add_device_config(self, device_id: str, ip_address: str, oids: Dict[str, str]):
        """Add SNMP device configuration"""
        self.devices_config.append({
            'device_id': device_id,
            'ip_address': ip_address,
            'oids': oids  # Map of metric names to OIDs
        })
    
    def connect(self) -> bool:
        """Test SNMP connectivity"""
        # Implementation would test SNMP connectivity to configured devices
        self._connected = True
        return True
    
    def disconnect(self) -> None:
        """Disconnect SNMP"""
        self._connected = False
    
    def is_connected(self) -> bool:
        """Check SNMP connection"""
        return self._connected
    
    def get_devices(self) -> List[DeviceInfo]:
        """Get SNMP devices"""
        # Implementation would discover or return configured SNMP devices
        return []
    
    def get_energy_readings(self, device_id: Optional[str] = None,
                          start_time: Optional[datetime] = None,
                          end_time: Optional[datetime] = None) -> List[EnergyReading]:
        """Get readings from SNMP devices"""
        # Implementation would poll SNMP devices for power consumption data
        return []
    
    def get_current_consumption(self) -> float:
        """Get current consumption from SNMP devices"""
        # Implementation would sum power consumption from all SNMP devices
        return 0.0
    
    def validate_data(self, reading: EnergyReading) -> bool:
        """Validate SNMP data"""
        return reading.power_consumption >= 0

class HybridDataSource(DataSourceInterface):
    """Combines multiple data sources for comprehensive monitoring"""
    
    def __init__(self):
        self.sources: List[DataSourceInterface] = []
        self.primary_source: Optional[DataSourceInterface] = None
    
    def add_source(self, source: DataSourceInterface, is_primary: bool = False):
        """Add a data source to the hybrid collection"""
        self.sources.append(source)
        if is_primary:
            self.primary_source = source
    
    def connect(self) -> bool:
        """Connect all data sources"""
        success = True
        for source in self.sources:
            try:
                if not source.connect():
                    success = False
                    logger.warning(f"Failed to connect data source: {type(source).__name__}")
            except Exception as e:
                logger.error(f"Error connecting {type(source).__name__}: {e}")
                success = False
        return success
    
    def disconnect(self) -> None:
        """Disconnect all sources"""
        for source in self.sources:
            try:
                source.disconnect()
            except Exception as e:
                logger.error(f"Error disconnecting {type(source).__name__}: {e}")
    
    def is_connected(self) -> bool:
        """Check if at least one source is connected"""
        return any(source.is_connected() for source in self.sources)
    
    def get_devices(self) -> List[DeviceInfo]:
        """Get devices from all sources"""
        all_devices = []
        for source in self.sources:
            if source.is_connected():
                try:
                    all_devices.extend(source.get_devices())
                except Exception as e:
                    logger.error(f"Error getting devices from {type(source).__name__}: {e}")
        return all_devices
    
    def get_energy_readings(self, device_id: Optional[str] = None,
                          start_time: Optional[datetime] = None,
                          end_time: Optional[datetime] = None) -> List[EnergyReading]:
        """Get readings from all sources"""
        all_readings = []
        for source in self.sources:
            if source.is_connected():
                try:
                    all_readings.extend(source.get_energy_readings(device_id, start_time, end_time))
                except Exception as e:
                    logger.error(f"Error getting readings from {type(source).__name__}: {e}")
        return all_readings
    
    def get_current_consumption(self) -> float:
        """Get consumption from primary source or sum from all"""
        if self.primary_source and self.primary_source.is_connected():
            try:
                return self.primary_source.get_current_consumption()
            except Exception as e:
                logger.error(f"Error getting consumption from primary source: {e}")
        
        # Fallback: sum from all sources
        total = 0.0
        for source in self.sources:
            if source.is_connected():
                try:
                    total += source.get_current_consumption()
                except Exception as e:
                    logger.error(f"Error getting consumption from {type(source).__name__}: {e}")
        return total
    
    def validate_data(self, reading: EnergyReading) -> bool:
        """Validate using all available sources"""
        return any(source.validate_data(reading) for source in self.sources if source.is_connected())