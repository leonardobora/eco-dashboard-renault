"""
Unit tests for SNMP Collector module
"""

import unittest
import sys
import os
import json
import tempfile
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class TestSNMPCollector(unittest.TestCase):
    """Test SNMP Collector functionality"""

    def test_import_snmp_collector(self):
        """Test that SNMP collector module can be imported"""
        try:
            from snmp_collector import SNMPCollector, ServerMetrics, HPServerOIDs
            self.assertTrue(True, "SNMP collector module imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import SNMP collector module: {e}")

    def test_snmp_collector_initialization_no_config(self):
        """Test SNMP collector initializes without config file"""
        from snmp_collector import SNMPCollector
        
        # Should initialize even without config file
        collector = SNMPCollector(config_file="non_existent_file.json")
        self.assertIsNotNone(collector)
        self.assertEqual(len(collector.servers_config), 0)
        self.assertIsNone(collector.credentials)

    def test_snmp_collector_with_valid_config(self):
        """Test SNMP collector loads valid configuration"""
        from snmp_collector import SNMPCollector
        
        # Create temporary config file
        config = {
            "snmp_credentials": {
                "username": "test_user",
                "auth_key": "test_auth",
                "priv_key": "test_priv",
                "auth_protocol": "SHA",
                "priv_protocol": "AES"
            },
            "servers": [
                {
                    "device_id": "TEST-HP-001",
                    "ip_address": "192.168.1.100",
                    "generation": "gen9",
                    "enabled": True
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            config_file = f.name
        
        try:
            # Temporarily disable testing mode
            old_testing = os.environ.get('TESTING')
            if old_testing:
                del os.environ['TESTING']
            
            collector = SNMPCollector(config_file=config_file)
            
            # Restore testing mode
            if old_testing:
                os.environ['TESTING'] = old_testing
            
            # Verify credentials loaded
            self.assertIsNotNone(collector.credentials)
            self.assertEqual(collector.credentials.username, "test_user")
            self.assertEqual(collector.credentials.auth_protocol, "SHA")
            self.assertEqual(collector.credentials.priv_protocol, "AES")
            
            # Verify servers loaded
            self.assertEqual(len(collector.servers_config), 1)
            self.assertEqual(collector.servers_config[0]["device_id"], "TEST-HP-001")
            
        finally:
            os.unlink(config_file)

    def test_hp_server_oids(self):
        """Test HP Server OID mappings"""
        from snmp_collector import HPServerOIDs
        
        # Test Gen8 OIDs
        gen8_oids = HPServerOIDs.get_oids_for_generation("gen8")
        self.assertIn("power_consumption", gen8_oids)
        self.assertIn("power_supply_status", gen8_oids)
        
        # Test Gen9 OIDs
        gen9_oids = HPServerOIDs.get_oids_for_generation("gen9")
        self.assertIn("power_consumption", gen9_oids)
        
        # Test Gen10 OIDs
        gen10_oids = HPServerOIDs.get_oids_for_generation("gen10")
        self.assertIn("power_consumption", gen10_oids)
        
        # Test VxRail OIDs
        vxrail_oids = HPServerOIDs.get_oids_for_generation("vxrail")
        self.assertIn("power_consumption", vxrail_oids)
        
        # Test default (unknown generation defaults to Gen9)
        default_oids = HPServerOIDs.get_oids_for_generation("unknown")
        self.assertEqual(default_oids, gen9_oids)

    def test_simulated_metrics_generation(self):
        """Test that simulated metrics are generated correctly"""
        from snmp_collector import SNMPCollector
        
        collector = SNMPCollector(config_file="non_existent.json")
        
        # Test default simulated metrics (90 HP + 10 VxRail)
        metrics = collector._get_default_simulated_metrics()
        
        self.assertEqual(len(metrics), 100)  # 90 + 10
        
        # Count by type
        hp_count = sum(1 for m in metrics if 'SRV-HP' in m.device_id)
        vxrail_count = sum(1 for m in metrics if 'VXRAIL' in m.device_id)
        
        self.assertEqual(hp_count, 90)
        self.assertEqual(vxrail_count, 10)
        
        # Verify all have positive power consumption
        for metric in metrics:
            self.assertGreater(metric.power_consumption_watts, 0)
            self.assertEqual(metric.source, 'simulado')

    def test_cache_functionality(self):
        """Test cache TTL and retrieval"""
        from snmp_collector import SNMPCollector, ServerMetrics
        from datetime import datetime
        
        collector = SNMPCollector(config_file="non_existent.json")
        
        # Create a test metric
        test_metric = ServerMetrics(
            device_id="TEST-001",
            power_consumption_watts=350.0,
            timestamp=datetime.now(),
            source='snmp_real',
            status='success'
        )
        
        # Update cache
        collector._update_cache("TEST-001", test_metric)
        
        # Verify cache is valid
        self.assertTrue(collector._is_cache_valid("TEST-001"))
        
        # Retrieve from cache
        cached_metric = collector._get_from_cache("TEST-001")
        self.assertIsNotNone(cached_metric)
        self.assertEqual(cached_metric.device_id, "TEST-001")
        self.assertEqual(cached_metric.source, 'cached')  # Source should be updated

    def test_get_total_consumption(self):
        """Test total consumption calculation"""
        from snmp_collector import SNMPCollector
        
        collector = SNMPCollector(config_file="non_existent.json")
        
        # Get total consumption (should fallback to simulated)
        consumption_kwh, fonte = collector.get_total_consumption_kwh()
        
        # Verify reasonable values
        self.assertGreater(consumption_kwh, 0)
        self.assertLess(consumption_kwh, 200)  # 100 servers * ~500W avg = ~50kW max
        self.assertEqual(fonte, 'simulado')  # No real SNMP, should be simulated

    def test_get_server_count(self):
        """Test server count functionality"""
        from snmp_collector import SNMPCollector
        
        # Test with no config (default values)
        collector = SNMPCollector(config_file="non_existent.json")
        counts = collector.get_server_count()
        
        self.assertEqual(counts['servidores_hp'], 90)
        self.assertEqual(counts['vxrail'], 10)
        self.assertEqual(counts['total'], 100)

    def test_server_metrics_dataclass(self):
        """Test ServerMetrics dataclass"""
        from snmp_collector import ServerMetrics
        from datetime import datetime
        
        metric = ServerMetrics(
            device_id="TEST-001",
            power_consumption_watts=425.5,
            timestamp=datetime.now(),
            source='snmp_real',
            status='success'
        )
        
        self.assertEqual(metric.device_id, "TEST-001")
        self.assertEqual(metric.power_consumption_watts, 425.5)
        self.assertEqual(metric.source, 'snmp_real')
        self.assertEqual(metric.status, 'success')
        self.assertIsNone(metric.error_message)

    def test_snmp_credentials_dataclass(self):
        """Test SNMPCredentials dataclass"""
        from snmp_collector import SNMPCredentials
        
        creds = SNMPCredentials(
            username="test_user",
            auth_key="auth_password",
            priv_key="priv_password",
            auth_protocol="SHA",
            priv_protocol="AES"
        )
        
        self.assertEqual(creds.username, "test_user")
        self.assertEqual(creds.auth_protocol, "SHA")
        self.assertEqual(creds.priv_protocol, "AES")


class TestFlaskIntegration(unittest.TestCase):
    """Test Flask app integration with SNMP collector"""

    def test_flask_app_imports_snmp(self):
        """Test that Flask app successfully imports SNMP collector"""
        try:
            import app_renault_mvp
            self.assertTrue(hasattr(app_renault_mvp, 'SNMP_COLLECTOR_AVAILABLE'))
        except ImportError as e:
            self.fail(f"Failed to import Flask app: {e}")

    def test_api_metrics_endpoint_with_fonte(self):
        """Test that /api/metrics includes fonte field and datacenter metrics"""
        try:
            import app_renault_mvp
            
            app = app_renault_mvp.app
            client = app.test_client()
            
            response = client.get('/api/metrics')
            self.assertEqual(response.status_code, 200)
            
            data = response.get_json()
            
            # Verify fonte field exists
            self.assertIn('fonte', data)
            self.assertIn(data['fonte'], ['snmp_real', 'cached', 'simulado', 'mixed'])
            
            # Verify datacenter-specific fields (new scope)
            self.assertIn('escopo', data)
            self.assertEqual(data['escopo'], 'datacenter-servidores-apenas')
            self.assertIn('pue_atual', data)
            self.assertIn('pue_alvo', data)
            self.assertIn('servidores_total', data)
            
            # Verify backward compatibility - old fields still exist
            self.assertIn('consumo_atual', data)
            self.assertIn('emissoes_co2', data)
            self.assertIn('economia_potencial', data)
            self.assertIn('arvores_equivalentes', data)
            
        except Exception as e:
            self.fail(f"API metrics test failed: {e}")


if __name__ == "__main__":
    unittest.main()
