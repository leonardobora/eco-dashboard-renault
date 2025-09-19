"""
Configuration tests
"""

import os
import json
import tempfile
import unittest
from unittest.mock import patch, mock_open

try:
    from config.settings import (
        ConfigManager,
        AppConfig,
        Environment,
        DataSourceType,
        EnvironmentalFactors,
    )

    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False


@unittest.skipUnless(CONFIG_AVAILABLE, "Configuration system not available")
class TestConfigManager(unittest.TestCase):
    """Test configuration management"""

    def setUp(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "test_config.json")

    def tearDown(self):
        """Cleanup test environment"""
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        os.rmdir(self.temp_dir)

    def test_default_configuration(self):
        """Test loading default configuration"""
        config_manager = ConfigManager(config_file="non_existent_file.json")
        config = config_manager.load_config()

        self.assertIsInstance(config, AppConfig)
        self.assertEqual(config.environment, Environment.DEVELOPMENT)
        self.assertEqual(config.data_source_type, DataSourceType.SYNTHETIC)
        self.assertTrue(config.debug)
        self.assertEqual(config.host, "localhost")
        self.assertEqual(config.port, 5000)

    def test_config_file_loading(self):
        """Test loading configuration from file"""
        test_config = {
            "environment": "production",
            "data_source_type": "database",
            "debug": False,
            "port": 8080,
            "environmental": {
                "emission_factor_kg_co2_per_kwh": 0.1,
                "energy_tariff_brl_per_kwh": 0.8,
            },
        }

        with open(self.config_file, "w") as f:
            json.dump(test_config, f)

        config_manager = ConfigManager(config_file=self.config_file)
        config = config_manager.load_config()

        self.assertEqual(config.environment, Environment.PRODUCTION)
        self.assertEqual(config.data_source_type, DataSourceType.DATABASE)
        self.assertFalse(config.debug)
        self.assertEqual(config.port, 8080)
        self.assertEqual(config.environmental.emission_factor_kg_co2_per_kwh, 0.1)
        self.assertEqual(config.environmental.energy_tariff_brl_per_kwh, 0.8)

    @patch.dict(
        os.environ,
        {
            "ECO_ENVIRONMENT": "production",
            "ECO_DEBUG": "false",
            "ECO_PORT": "9000",
            "ECO_EMISSION_FACTOR": "0.05",
        },
    )
    def test_environment_variables_override(self):
        """Test that environment variables override file config"""
        test_config = {"environment": "development", "debug": True, "port": 5000}

        with open(self.config_file, "w") as f:
            json.dump(test_config, f)

        config_manager = ConfigManager(config_file=self.config_file)
        config = config_manager.load_config()

        # Environment variables should override file config
        self.assertEqual(config.environment, Environment.PRODUCTION)
        self.assertFalse(config.debug)
        self.assertEqual(config.port, 9000)
        self.assertEqual(config.environmental.emission_factor_kg_co2_per_kwh, 0.05)

    def test_save_configuration(self):
        """Test saving configuration to file"""
        config = AppConfig(
            environment=Environment.TESTING,
            data_source_type=DataSourceType.HYBRID,
            debug=True,
            port=7000,
            environmental=EnvironmentalFactors(
                emission_factor_kg_co2_per_kwh=0.09, energy_tariff_brl_per_kwh=0.70
            ),
        )

        config_manager = ConfigManager(config_file=self.config_file)
        config_manager.save_config(config)

        # Verify file was created and contains correct data
        self.assertTrue(os.path.exists(self.config_file))

        with open(self.config_file, "r") as f:
            saved_data = json.load(f)

        self.assertEqual(saved_data["environment"], "testing")
        self.assertEqual(saved_data["data_source_type"], "hybrid")
        self.assertEqual(saved_data["port"], 7000)
        self.assertEqual(
            saved_data["environmental"]["emission_factor_kg_co2_per_kwh"], 0.09
        )

    def test_invalid_config_values(self):
        """Test handling of invalid configuration values"""
        test_config = {
            "environment": "invalid_environment",
            "data_source_type": "invalid_source",
            "port": "not_a_number",
        }

        with open(self.config_file, "w") as f:
            json.dump(test_config, f)

        config_manager = ConfigManager(config_file=self.config_file)

        # Should handle invalid values gracefully
        with self.assertRaises((ValueError, TypeError)):
            config_manager.load_config()

    def test_partial_config_file(self):
        """Test loading partial configuration file"""
        test_config = {
            "port": 8080,
            "environmental": {"emission_factor_kg_co2_per_kwh": 0.1},
        }

        with open(self.config_file, "w") as f:
            json.dump(test_config, f)

        config_manager = ConfigManager(config_file=self.config_file)
        config = config_manager.load_config()

        # Should use defaults for missing values
        self.assertEqual(config.environment, Environment.DEVELOPMENT)  # Default
        self.assertEqual(config.port, 8080)  # From file
        self.assertEqual(
            config.environmental.emission_factor_kg_co2_per_kwh, 0.1
        )  # From file
        self.assertEqual(
            config.environmental.tree_sequestration_kg_co2_per_year, 22.0
        )  # Default

    @patch("builtins.open", side_effect=IOError("Permission denied"))
    def test_config_file_permission_error(self, mock_file):
        """Test handling of file permission errors"""
        config_manager = ConfigManager(config_file=self.config_file)

        # Should fall back to defaults when file cannot be read
        config = config_manager.load_config()
        self.assertIsInstance(config, AppConfig)
        self.assertEqual(config.environment, Environment.DEVELOPMENT)


@unittest.skipUnless(CONFIG_AVAILABLE, "Configuration system not available")
class TestEnvironmentalFactors(unittest.TestCase):
    """Test environmental factors configuration"""

    def test_default_environmental_factors(self):
        """Test default environmental factors"""
        factors = EnvironmentalFactors()

        self.assertEqual(factors.emission_factor_kg_co2_per_kwh, 0.0817)
        self.assertEqual(factors.tree_sequestration_kg_co2_per_year, 22.0)
        self.assertEqual(factors.energy_tariff_brl_per_kwh, 0.60)
        self.assertEqual(factors.efficiency_potential_percent, 15.0)

    def test_custom_environmental_factors(self):
        """Test custom environmental factors"""
        factors = EnvironmentalFactors(
            emission_factor_kg_co2_per_kwh=0.1,
            tree_sequestration_kg_co2_per_year=25.0,
            energy_tariff_brl_per_kwh=0.75,
            efficiency_potential_percent=20.0,
        )

        self.assertEqual(factors.emission_factor_kg_co2_per_kwh, 0.1)
        self.assertEqual(factors.tree_sequestration_kg_co2_per_year, 25.0)
        self.assertEqual(factors.energy_tariff_brl_per_kwh, 0.75)
        self.assertEqual(factors.efficiency_potential_percent, 20.0)

    def test_environmental_factors_validation(self):
        """Test that environmental factors are positive"""
        factors = EnvironmentalFactors()

        self.assertGreater(factors.emission_factor_kg_co2_per_kwh, 0)
        self.assertGreater(factors.tree_sequestration_kg_co2_per_year, 0)
        self.assertGreater(factors.energy_tariff_brl_per_kwh, 0)
        self.assertGreater(factors.efficiency_potential_percent, 0)


@unittest.skipUnless(CONFIG_AVAILABLE, "Configuration system not available")
class TestConfigurationIntegration(unittest.TestCase):
    """Test configuration integration with other components"""

    def test_config_with_metrics_calculator(self):
        """Test configuration integration with metrics calculator"""
        try:
            from data_sources.base import MetricsCalculator

            config = AppConfig(
                environment=Environment.TESTING,
                data_source_type=DataSourceType.SYNTHETIC,
                debug=False,
                environmental=EnvironmentalFactors(
                    emission_factor_kg_co2_per_kwh=0.1,
                    tree_sequestration_kg_co2_per_year=25.0,
                    energy_tariff_brl_per_kwh=0.8,
                ),
            )

            calculator = MetricsCalculator(
                emission_factor=config.environmental.emission_factor_kg_co2_per_kwh,
                tree_sequestration=config.environmental.tree_sequestration_kg_co2_per_year,
                energy_tariff=config.environmental.energy_tariff_brl_per_kwh,
            )

            # Test that calculator uses config values
            self.assertEqual(calculator.emission_factor, 0.1)
            self.assertEqual(calculator.tree_sequestration, 25.0)
            self.assertEqual(calculator.energy_tariff, 0.8)

            # Test calculations with custom values
            co2 = calculator.calculate_co2_emissions(1000)
            self.assertEqual(co2, 100)  # 1000 * 0.1

            trees = calculator.calculate_tree_equivalent(250)
            self.assertEqual(trees, 10)  # 250 / 25

        except ImportError:
            self.skipTest("MetricsCalculator not available")

    def test_get_config_function(self):
        """Test global get_config function"""
        try:
            from config.settings import get_config

            config = get_config()
            self.assertIsInstance(config, AppConfig)

            # Should return same instance on subsequent calls (singleton-like behavior)
            config2 = get_config()
            self.assertEqual(config.environment, config2.environment)
            self.assertEqual(config.port, config2.port)

        except ImportError:
            self.skipTest("get_config function not available")


if __name__ == "__main__":
    unittest.main()
