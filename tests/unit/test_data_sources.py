"""
Unit tests for data sources
"""

import unittest
import unittest.mock as mock
from datetime import datetime, timedelta

# Try to import our modules, skip tests if not available
try:
    from data_sources.base import MetricsCalculator, DeviceInfo, EnergyReading
    from data_sources.synthetic import SyntheticDataSource
    MODULES_AVAILABLE = True
except ImportError:
    MODULES_AVAILABLE = False

@unittest.skipUnless(MODULES_AVAILABLE, "Data source modules not available")
class TestMetricsCalculator(unittest.TestCase):
    """Test suite for MetricsCalculator"""
    
    def setUp(self):
        """Setup for each test"""
        self.calculator = MetricsCalculator()
    
    def test_default_values(self):
        """Test calculator initialization with default values"""
        self.assertEqual(self.calculator.emission_factor, 0.0817)
        self.assertEqual(self.calculator.tree_sequestration, 22.0)
        self.assertEqual(self.calculator.energy_tariff, 0.60)
    
    def test_custom_values(self):
        """Test calculator with custom environmental factors"""
        calculator = MetricsCalculator(
            emission_factor=0.100,
            tree_sequestration=25.0,
            energy_tariff=0.75
        )
        self.assertEqual(calculator.emission_factor, 0.100)
        self.assertEqual(calculator.tree_sequestration, 25.0)
        self.assertEqual(calculator.energy_tariff, 0.75)
    
    def test_co2_emissions_calculation(self):
        """Test CO2 emissions calculation"""
        kwh = 1000
        expected_co2 = kwh * 0.0817
        result = self.calculator.calculate_co2_emissions(kwh)
        self.assertEqual(result, expected_co2)
    
    def test_tree_equivalent_calculation(self):
        """Test tree equivalent calculation"""
        co2_kg = 440  # Should equal 20 trees
        expected_trees = 20
        result = self.calculator.calculate_tree_equivalent(co2_kg)
        self.assertEqual(result, expected_trees)
    
    def test_cost_savings_calculation(self):
        """Test cost savings calculation"""
        kwh_savings = 1000
        expected_savings = kwh_savings * 0.60
        result = self.calculator.calculate_cost_savings(kwh_savings)
        assert result == expected_savings
    
    def test_complete_metrics_calculation(self):
        """Test complete metrics calculation"""
        current_kwh = 100
        annual_kwh = 876000  # 100 kWh * 24 * 365
        
        metrics = self.calculator.calculate_metrics(current_kwh, annual_kwh)
        
        assert metrics.total_consumption_kwh == current_kwh
        assert metrics.co2_emissions_kg == annual_kwh * 0.0817
        assert metrics.trees_equivalent == int((annual_kwh * 0.0817) / 22.0)
        assert metrics.cost_savings_potential == annual_kwh * 0.15 * 0.60
        assert isinstance(metrics.calculation_timestamp, datetime)

@unittest.skipUnless(MODULES_AVAILABLE, "Data source modules not available")
class TestSyntheticDataSource(unittest.TestCase):
    """Test suite for SyntheticDataSource"""
    
    def setUp(self):
        """Setup for each test"""
        self.data_source = SyntheticDataSource()
    
    def test_initial_state(self):
        """Test initial state of synthetic data source"""
        assert not self.data_source.is_connected()
        assert len(self.data_source.devices) == 5476  # 5376 workstations + 90 HP + 10 VxRail
    
    def test_connection_management(self):
        """Test connection and disconnection"""
        # Initially disconnected
        assert not self.data_source.is_connected()
        
        # Connect
        result = self.data_source.connect()
        assert result is True
        assert self.data_source.is_connected()
        
        # Disconnect
        self.data_source.disconnect()
        assert not self.data_source.is_connected()
    
    def test_device_inventory(self):
        """Test device inventory generation"""
        devices = self.data_source.devices
        
        # Check total count
        assert len(devices) == 5476
        
        # Check device types
        workstations = [d for d in devices if d.device_type == "workstation"]
        servers = [d for d in devices if d.device_type == "server"]
        
        assert len(workstations) == 5376
        assert len(servers) == 100  # 90 HP + 10 VxRail
        
        # Check departments
        departments = set(d.department for d in workstations)
        expected_departments = {"Administrativo", "Engenharia", "Produção", "Vendas", "Suporte"}
        assert departments == expected_departments
    
    def test_device_info_structure(self):
        """Test DeviceInfo data structure"""
        device = self.data_source.devices[0]
        
        assert hasattr(device, 'device_id')
        assert hasattr(device, 'device_type')
        assert hasattr(device, 'location')
        assert hasattr(device, 'department')
        assert hasattr(device, 'power_rating')
        assert hasattr(device, 'status')
        assert hasattr(device, 'last_seen')
        
        assert isinstance(device.device_id, str)
        assert device.device_type in ["workstation", "server"]
        assert isinstance(device.power_rating, float)
        assert device.status in ["active", "idle", "offline"]
        assert isinstance(device.last_seen, datetime)
    
    def test_get_devices_requires_connection(self):
        """Test that get_devices requires connection"""
        with self.assertRaises(ConnectionError):
            self.data_source.get_devices()
    
    def test_get_devices_with_connection(self):
        """Test get_devices with proper connection"""
        self.data_source.connect()
        devices = self.data_source.get_devices()
        
        assert isinstance(devices, list)
        assert len(devices) == 5476
        assert all(isinstance(d, DeviceInfo) for d in devices)
    
    def test_energy_readings_requires_connection(self):
        """Test that energy readings require connection"""
        with self.assertRaises(ConnectionError):
            self.data_source.get_energy_readings()
    
    def test_energy_readings_with_connection(self):
        """Test energy readings with connection"""
        self.data_source.connect()
        readings = self.data_source.get_energy_readings()
        
        assert isinstance(readings, list)
        assert len(readings) == 5476  # One reading per device
        assert all(isinstance(r, EnergyReading) for r in readings)
    
    def test_energy_reading_structure(self):
        """Test EnergyReading data structure"""
        self.data_source.connect()
        readings = self.data_source.get_energy_readings()
        reading = readings[0]
        
        assert hasattr(reading, 'device_id')
        assert hasattr(reading, 'timestamp')
        assert hasattr(reading, 'power_consumption')
        assert hasattr(reading, 'voltage')
        assert hasattr(reading, 'current')
        assert hasattr(reading, 'temperature')
        
        assert isinstance(reading.device_id, str)
        assert isinstance(reading.timestamp, datetime)
        assert isinstance(reading.power_consumption, float)
        assert reading.power_consumption >= 0
    
    def test_current_consumption_calculation(self):
        """Test current consumption calculation"""
        self.data_source.connect()
        consumption = self.data_source.get_current_consumption()
        
        assert isinstance(consumption, float)
        assert consumption > 0
        assert consumption < 10000  # Reasonable upper bound (10 MW)
    
    def test_data_validation(self):
        """Test data validation logic"""
        self.data_source.connect()
        
        # Valid reading
        device = self.data_source.devices[0]
        valid_reading = EnergyReading(
            device_id=device.device_id,
            timestamp=datetime.now(),
            power_consumption=device.power_rating * 0.8,  # 80% of rating
            voltage=230.0,
            current=5.0,
            temperature=45.0
        )
        assert self.data_source.validate_data(valid_reading) is True
        
        # Invalid reading (too high power)
        invalid_reading = EnergyReading(
            device_id=device.device_id,
            timestamp=datetime.now(),
            power_consumption=device.power_rating * 2.0,  # 200% of rating
            voltage=230.0,
            current=5.0,
            temperature=45.0
        )
        assert self.data_source.validate_data(invalid_reading) is False
        
        # Invalid device ID
        unknown_reading = EnergyReading(
            device_id="UNKNOWN-DEVICE",
            timestamp=datetime.now(),
            power_consumption=100.0,
            voltage=230.0,
            current=5.0,
            temperature=45.0
        )
        assert self.data_source.validate_data(unknown_reading) is False
    
    def test_time_based_consumption_variation(self):
        """Test that consumption varies based on time of day"""
        self.data_source.connect()
        
        # Test different hours
        with mock.patch('data_sources.synthetic.datetime') as mock_datetime:
            # Business hours (high consumption)
            mock_datetime.now.return_value.hour = 14
            consumption_business = self.data_source.get_current_consumption()
            
            # Night hours (low consumption)
            mock_datetime.now.return_value.hour = 3
            consumption_night = self.data_source.get_current_consumption()
            
            # Business hours should have higher consumption
            assert consumption_business > consumption_night
    
    def test_device_filtering_by_id(self):
        """Test filtering energy readings by device ID"""
        self.data_source.connect()
        
        device_id = self.data_source.devices[0].device_id
        readings = self.data_source.get_energy_readings(device_id=device_id)
        
        assert len(readings) == 1
        assert readings[0].device_id == device_id

@unittest.skipUnless(MODULES_AVAILABLE, "Data source modules not available")
class TestDataValidation(unittest.TestCase):
    """Test data validation and integrity"""
    
    def test_device_id_uniqueness(self):
        """Test that all device IDs are unique"""
        data_source = SyntheticDataSource()
        device_ids = [d.device_id for d in data_source.devices]
        
        assert len(device_ids) == len(set(device_ids))
    
    def test_power_rating_ranges(self):
        """Test that power ratings are within expected ranges"""
        data_source = SyntheticDataSource()
        
        for device in data_source.devices:
            if device.device_type == "workstation":
                assert 200 <= device.power_rating <= 300
            elif device.device_type == "server":
                if "VXRAIL" in device.device_id:
                    assert 800 <= device.power_rating <= 1200
                else:  # HP servers
                    assert 350 <= device.power_rating <= 450
    
    def test_department_distribution(self):
        """Test correct distribution of workstations by department"""
        data_source = SyntheticDataSource()
        workstations = [d for d in data_source.devices if d.device_type == "workstation"]
        
        dept_counts = {}
        for ws in workstations:
            dept_counts[ws.department] = dept_counts.get(ws.department, 0) + 1
        
        expected_counts = {
            'Administrativo': 1200,
            'Engenharia': 1500,
            'Produção': 1800,
            'Vendas': 600,
            'Suporte': 276
        }
        
        assert dept_counts == expected_counts
    
    def test_timestamp_consistency(self):
        """Test that timestamps are recent and consistent"""
        data_source = SyntheticDataSource()
        data_source.connect()
        
        readings = data_source.get_energy_readings()
        now = datetime.now()
        
        for reading in readings:
            # All timestamps should be very recent (within last minute)
            time_diff = abs((now - reading.timestamp).total_seconds())
            assert time_diff < 60