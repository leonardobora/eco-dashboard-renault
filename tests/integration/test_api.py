"""
Integration tests for Flask application and API endpoints
"""

import json
import unittest
from unittest.mock import patch, MagicMock

# Mock imports since the app might not be available yet
try:
    from app_renault_mvp import app, infra

    APP_AVAILABLE = True
except ImportError:
    APP_AVAILABLE = False
    app = None
    infra = None


@unittest.skipUnless(APP_AVAILABLE, "Flask app not available")
class TestFlaskAPI(unittest.TestCase):
    """Test Flask API endpoints"""

    def setUp(self):
        """Setup test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page_loads(self):
        """Test that home page loads successfully"""
        response = self.app.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"EcoTI Dashboard", response.data)
        self.assertIn(b"Renault", response.data)

    def test_metrics_api_endpoint(self):
        """Test /api/metrics endpoint"""
        response = self.app.get("/api/metrics")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

        data = json.loads(response.data)

        # Check required fields
        required_fields = [
            "consumo_atual",
            "emissoes_co2",
            "economia_potencial",
            "arvores_equivalentes",
        ]

        for field in required_fields:
            self.assertIn(field, data)
            self.assertIsInstance(data[field], (int, float))
            self.assertGreaterEqual(data[field], 0)

    def test_metrics_api_data_types(self):
        """Test that API returns correct data types"""
        response = self.app.get("/api/metrics")
        data = json.loads(response.data)

        # Test specific data types and ranges
        self.assertIsInstance(data["consumo_atual"], float)
        self.assertIsInstance(data["emissoes_co2"], float)
        self.assertIsInstance(data["economia_potencial"], float)
        self.assertIsInstance(data["arvores_equivalentes"], int)

        # Test reasonable ranges
        self.assertGreater(data["consumo_atual"], 0)
        self.assertLess(data["consumo_atual"], 10000)  # Less than 10 MW

        self.assertGreater(data["emissoes_co2"], 0)
        self.assertGreater(data["economia_potencial"], 0)
        self.assertGreater(data["arvores_equivalentes"], 0)

    def test_metrics_api_consistency(self):
        """Test that metrics are consistent between calls"""
        # Get metrics twice
        response1 = self.app.get("/api/metrics")
        response2 = self.app.get("/api/metrics")

        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)

        # Values should be similar (allowing for small variations due to time-based factors)
        consumption_diff = abs(data1["consumo_atual"] - data2["consumo_atual"])
        self.assertLess(consumption_diff, data1["consumo_atual"] * 0.1)  # Within 10%

    def test_api_response_time(self):
        """Test that API responds quickly"""
        import time

        start_time = time.time()
        response = self.app.get("/api/metrics")
        end_time = time.time()

        response_time = end_time - start_time

        self.assertEqual(response.status_code, 200)
        self.assertLess(response_time, 2.0)  # Should respond within 2 seconds


class TestInfrastructureCalculations(unittest.TestCase):
    """Test infrastructure calculation logic"""

    def setUp(self):
        """Setup test infrastructure"""
        if APP_AVAILABLE:
            from app_renault_mvp import RenaultInfrastructure

            self.infra = RenaultInfrastructure()
        else:
            self.skipTest("Infrastructure class not available")

    def test_consumption_calculation_ranges(self):
        """Test that consumption calculations are within expected ranges"""
        consumption = self.infra.calcular_consumo_atual()

        # Should be positive
        self.assertGreater(consumption, 0)

        # Should be less than theoretical maximum
        max_theoretical = (
            self.infra.workstations * self.infra.consumo_medio_w
            + self.infra.servidores_hp * 400
            + self.infra.vxrail * 1000
        ) / 1000

        self.assertLess(consumption, max_theoretical)

    def test_co2_emissions_calculation(self):
        """Test CO2 emissions calculation"""
        emissions = self.infra.calcular_emissoes_anuais()

        self.assertGreater(emissions, 0)
        self.assertIsInstance(emissions, float)

        # Check if calculation follows expected formula
        consumption_annual = self.infra.consumo_atual * 24 * 365
        expected_emissions = consumption_annual * self.infra.fator_emissao

        # Should be close to expected (within 1% due to time variations)
        difference = abs(emissions - expected_emissions)
        self.assertLess(difference, expected_emissions * 0.01)

    def test_tree_equivalent_calculation(self):
        """Test tree equivalent calculation"""
        trees = self.infra.calcular_arvores_equivalentes()

        self.assertGreater(trees, 0)
        self.assertIsInstance(trees, int)

        # Verify calculation
        emissions = self.infra.calcular_emissoes_anuais()
        expected_trees = int(emissions / self.infra.sequestro_arvore)

        self.assertEqual(trees, expected_trees)

    def test_cost_savings_calculation(self):
        """Test cost savings calculation"""
        savings = self.infra.calcular_economia_potencial()

        self.assertGreater(savings, 0)
        self.assertIsInstance(savings, float)

    @patch("app_renault_mvp.datetime")
    def test_time_based_consumption_variation(self, mock_datetime):
        """Test that consumption varies by time of day"""
        # Test business hours
        mock_datetime.datetime.now.return_value.hour = 14
        consumption_business = self.infra.calcular_consumo_atual()

        # Test night hours
        mock_datetime.datetime.now.return_value.hour = 3
        consumption_night = self.infra.calcular_consumo_atual()

        # Business hours should have higher consumption
        self.assertGreater(consumption_business, consumption_night)


class TestDataSourceIntegration(unittest.TestCase):
    """Test integration with data sources"""

    def test_synthetic_data_source_integration(self):
        """Test integration with synthetic data source"""
        try:
            from data_sources.synthetic import SyntheticDataSource
            from data_sources.base import MetricsCalculator

            data_source = SyntheticDataSource()
            calculator = MetricsCalculator()

            # Test connection
            self.assertTrue(data_source.connect())
            self.assertTrue(data_source.is_connected())

            # Test data retrieval
            devices = data_source.get_devices()
            self.assertGreater(len(devices), 0)

            readings = data_source.get_energy_readings()
            self.assertGreater(len(readings), 0)

            consumption = data_source.get_current_consumption()
            self.assertGreater(consumption, 0)

            # Test metrics calculation
            annual_consumption = consumption * 24 * 365
            metrics = calculator.calculate_metrics(consumption, annual_consumption)

            self.assertGreater(metrics.total_consumption_kwh, 0)
            self.assertGreater(metrics.co2_emissions_kg, 0)
            self.assertGreater(metrics.trees_equivalent, 0)

        except ImportError:
            self.skipTest("Data sources not available")

    def test_configuration_integration(self):
        """Test integration with configuration system"""
        try:
            from config.settings import get_config

            config = get_config()

            # Test that config is loaded
            self.assertIsNotNone(config)

            # Test required configuration fields
            self.assertIsNotNone(config.environment)
            self.assertIsNotNone(config.data_source_type)
            self.assertIsNotNone(config.environmental)

            # Test environmental factors
            self.assertGreater(config.environmental.emission_factor_kg_co2_per_kwh, 0)
            self.assertGreater(
                config.environmental.tree_sequestration_kg_co2_per_year, 0
            )
            self.assertGreater(config.environmental.energy_tariff_brl_per_kwh, 0)

        except ImportError:
            self.skipTest("Configuration system not available")


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases"""

    def setUp(self):
        """Setup test client"""
        if APP_AVAILABLE:
            self.app = app.test_client()
            self.app.testing = True
        else:
            self.skipTest("Flask app not available")

    def test_invalid_api_endpoints(self):
        """Test that invalid endpoints return 404"""
        response = self.app.get("/api/invalid-endpoint")
        self.assertEqual(response.status_code, 404)

    def test_api_with_invalid_methods(self):
        """Test API endpoints with invalid HTTP methods"""
        # Metrics endpoint should only accept GET
        response = self.app.post("/api/metrics")
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

        response = self.app.put("/api/metrics")
        self.assertEqual(response.status_code, 405)

        response = self.app.delete("/api/metrics")
        self.assertEqual(response.status_code, 405)

    def test_malformed_requests(self):
        """Test handling of malformed requests"""
        # Test with invalid headers
        response = self.app.get("/api/metrics", headers={"Content-Type": "invalid"})
        self.assertEqual(response.status_code, 200)  # Should still work

    @patch("app_renault_mvp.infra")
    def test_calculation_error_handling(self, mock_infra):
        """Test handling of calculation errors"""
        # Mock a calculation that raises an exception
        mock_infra.calcular_consumo_atual.side_effect = Exception("Calculation error")

        response = self.app.get("/api/metrics")

        # Should handle the error gracefully (either 500 or fallback values)
        self.assertIn(response.status_code, [200, 500])


if __name__ == "__main__":
    unittest.main()
