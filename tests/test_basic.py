"""
Simple unit tests for basic functionality
"""

import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class TestBasicFunctionality(unittest.TestCase):
    """Test basic system functionality"""
    
    def test_import_config(self):
        """Test that configuration module can be imported"""
        try:
            from config.settings import ConfigManager
            self.assertTrue(True, "Configuration module imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import config module: {e}")
    
    def test_import_data_sources(self):
        """Test that data sources can be imported"""
        try:
            from data_sources.base import MetricsCalculator
            from data_sources.synthetic import SyntheticDataSource
            self.assertTrue(True, "Data source modules imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import data source modules: {e}")
    
    def test_metrics_calculator_basic(self):
        """Test basic metrics calculator functionality"""
        try:
            from data_sources.base import MetricsCalculator
            
            calculator = MetricsCalculator()
            
            # Test CO2 calculation
            co2 = calculator.calculate_co2_emissions(1000)
            self.assertGreater(co2, 0)
            self.assertIsInstance(co2, float)
            
            # Test tree calculation
            trees = calculator.calculate_tree_equivalent(100)
            self.assertGreater(trees, 0)
            self.assertIsInstance(trees, int)
            
        except Exception as e:
            self.fail(f"MetricsCalculator test failed: {e}")
    
    def test_synthetic_data_source_basic(self):
        """Test basic synthetic data source functionality"""
        try:
            from data_sources.synthetic import SyntheticDataSource
            
            data_source = SyntheticDataSource()
            
            # Test connection
            self.assertFalse(data_source.is_connected())
            result = data_source.connect()
            self.assertTrue(result)
            self.assertTrue(data_source.is_connected())
            
            # Test device count
            devices = data_source.get_devices()
            self.assertEqual(len(devices), 5476)  # 5376 workstations + 90 HP + 10 VxRail
            
            # Test consumption calculation
            consumption = data_source.get_current_consumption()
            self.assertGreater(consumption, 0)
            self.assertIsInstance(consumption, float)
            
        except Exception as e:
            self.fail(f"SyntheticDataSource test failed: {e}")
    
    def test_config_manager_basic(self):
        """Test basic configuration manager functionality"""
        try:
            from config.settings import ConfigManager, Environment, DataSourceType
            
            config_manager = ConfigManager()
            config = config_manager.load_config()
            
            # Test that config is loaded
            self.assertIsNotNone(config)
            
            # Test environment
            self.assertIsInstance(config.environment, Environment)
            
            # Test data source type
            self.assertIsInstance(config.data_source_type, DataSourceType)
            
            # Test environmental factors
            self.assertIsNotNone(config.environmental)
            self.assertGreater(config.environmental.emission_factor_kg_co2_per_kwh, 0)
            
        except Exception as e:
            self.fail(f"ConfigManager test failed: {e}")

if __name__ == '__main__':
    unittest.main()