"""
Configuration management for EcoTI Dashboard
Supports multiple environments and data sources
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class DataSourceType(Enum):
    """Available data source types"""

    SYNTHETIC = "synthetic"
    DATABASE = "database"
    REST_API = "rest_api"
    SNMP = "snmp"
    HYBRID = "hybrid"


class Environment(Enum):
    """Application environments"""

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass
class EnvironmentalFactors:
    """Environmental calculation factors"""

    emission_factor_kg_co2_per_kwh: float = 0.0817  # Brazil grid emission factor
    tree_sequestration_kg_co2_per_year: float = 22.0  # CO2 sequestration per tree/year
    energy_tariff_brl_per_kwh: float = 0.60  # Energy cost in BRL
    efficiency_potential_percent: float = 15.0  # Potential efficiency improvement %


@dataclass
class DatabaseConfig:
    """Database connection configuration"""

    connection_string: str
    pool_size: int = 5
    timeout_seconds: int = 30


@dataclass
class APIConfig:
    """REST API configuration"""

    base_url: str
    api_key: str
    timeout_seconds: int = 30
    retry_attempts: int = 3


@dataclass
class SNMPConfig:
    """SNMP configuration"""

    community: str = "public"
    timeout_seconds: int = 10
    retries: int = 2


@dataclass
class AppConfig:
    """Main application configuration"""

    environment: Environment
    data_source_type: DataSourceType
    debug: bool
    host: str = "localhost"
    port: int = 5000
    auto_refresh_seconds: int = 10
    log_level: str = "INFO"

    # Data source configurations
    database: Optional[DatabaseConfig] = None
    api: Optional[APIConfig] = None
    snmp: Optional[SNMPConfig] = None

    # Environmental factors
    environmental: Optional[EnvironmentalFactors] = None

    # Renault specific settings
    renault_brand_color: str = "#FFCB00"
    company_name: str = "Renault"
    dashboard_title: str = "EcoTI Dashboard - Sustentabilidade Digital"

    def __post_init__(self):
        """Initialize environmental factors if not provided"""
        if self.environmental is None:
            self.environmental = EnvironmentalFactors()


class ConfigManager:
    """Manages application configuration from multiple sources"""

    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or self._find_config_file()
        self._config: Optional[AppConfig] = None

    def _find_config_file(self) -> str:
        """Find configuration file in standard locations"""
        possible_paths = [
            "config.json",
            "config/config.json",
            "eco_dashboard_config.json",
            os.path.expanduser("~/.eco_dashboard/config.json"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return path

        # Return default path if none found
        return "config/config.json"

    def load_config(self) -> AppConfig:
        """Load configuration from file and environment variables"""
        if self._config:
            return self._config

        # Start with defaults
        config_data = self._get_default_config()

        # Override with file configuration if exists
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    file_config = json.load(f)
                    config_data.update(file_config)
            except Exception as e:
                logging.warning(f"Could not load config file {self.config_file}: {e}")

        # Override with environment variables
        config_data.update(self._get_env_config())

        # Convert to AppConfig object
        self._config = self._dict_to_config(config_data)
        return self._config

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration values"""
        return {
            "environment": "development",
            "data_source_type": "synthetic",
            "debug": True,
            "host": "localhost",
            "port": 5000,
            "auto_refresh_seconds": 10,
            "log_level": "INFO",
            "environmental": {
                "emission_factor_kg_co2_per_kwh": 0.0817,
                "tree_sequestration_kg_co2_per_year": 22.0,
                "energy_tariff_brl_per_kwh": 0.60,
                "efficiency_potential_percent": 15.0,
            },
            "renault_brand_color": "#FFCB00",
            "company_name": "Renault",
            "dashboard_title": "EcoTI Dashboard - Sustentabilidade Digital",
        }

    def _get_env_config(self) -> Dict[str, Any]:
        """Get configuration from environment variables"""
        env_config = {}

        # Map environment variables to config keys
        env_mappings = {
            "ECO_ENVIRONMENT": ("environment", str),
            "ECO_DATA_SOURCE": ("data_source_type", str),
            "ECO_DEBUG": ("debug", lambda x: x.lower() == "true"),
            "ECO_HOST": ("host", str),
            "ECO_PORT": ("port", int),
            "ECO_REFRESH_SECONDS": ("auto_refresh_seconds", int),
            "ECO_LOG_LEVEL": ("log_level", str),
            # Database
            "ECO_DB_CONNECTION": ("database.connection_string", str),
            "ECO_DB_POOL_SIZE": ("database.pool_size", int),
            # API
            "ECO_API_URL": ("api.base_url", str),
            "ECO_API_KEY": ("api.api_key", str),
            # Environmental factors
            "ECO_EMISSION_FACTOR": (
                "environmental.emission_factor_kg_co2_per_kwh",
                float,
            ),
            "ECO_TREE_SEQUESTRATION": (
                "environmental.tree_sequestration_kg_co2_per_year",
                float,
            ),
            "ECO_ENERGY_TARIFF": ("environmental.energy_tariff_brl_per_kwh", float),
        }

        for env_var, (config_key, converter) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                try:
                    # Handle nested keys
                    keys = config_key.split(".")
                    current = env_config
                    for key in keys[:-1]:
                        if key not in current:
                            current[key] = {}
                        current = current[key]
                    current[keys[-1]] = converter(value)
                except (ValueError, TypeError) as e:
                    logging.warning(f"Invalid value for {env_var}: {value} ({e})")

        return env_config

    def _dict_to_config(self, config_data: Dict[str, Any]) -> AppConfig:
        """Convert dictionary to AppConfig object"""
        # Extract nested configurations
        env_data = config_data.get("environmental", {})
        environmental = EnvironmentalFactors(
            emission_factor_kg_co2_per_kwh=env_data.get(
                "emission_factor_kg_co2_per_kwh", 0.0817
            ),
            tree_sequestration_kg_co2_per_year=env_data.get(
                "tree_sequestration_kg_co2_per_year", 22.0
            ),
            energy_tariff_brl_per_kwh=env_data.get("energy_tariff_brl_per_kwh", 0.60),
            efficiency_potential_percent=env_data.get(
                "efficiency_potential_percent", 15.0
            ),
        )

        # Database config
        database = None
        if "database" in config_data:
            db_data = config_data["database"]
            database = DatabaseConfig(
                connection_string=db_data.get("connection_string", ""),
                pool_size=db_data.get("pool_size", 5),
                timeout_seconds=db_data.get("timeout_seconds", 30),
            )

        # API config
        api = None
        if "api" in config_data:
            api_data = config_data["api"]
            api = APIConfig(
                base_url=api_data.get("base_url", ""),
                api_key=api_data.get("api_key", ""),
                timeout_seconds=api_data.get("timeout_seconds", 30),
                retry_attempts=api_data.get("retry_attempts", 3),
            )

        # SNMP config
        snmp = None
        if "snmp" in config_data:
            snmp_data = config_data["snmp"]
            snmp = SNMPConfig(
                community=snmp_data.get("community", "public"),
                timeout_seconds=snmp_data.get("timeout_seconds", 10),
                retries=snmp_data.get("retries", 2),
            )

        return AppConfig(
            environment=Environment(config_data.get("environment", "development")),
            data_source_type=DataSourceType(
                config_data.get("data_source_type", "synthetic")
            ),
            debug=config_data.get("debug", True),
            host=config_data.get("host", "localhost"),
            port=config_data.get("port", 5000),
            auto_refresh_seconds=config_data.get("auto_refresh_seconds", 10),
            log_level=config_data.get("log_level", "INFO"),
            database=database,
            api=api,
            snmp=snmp,
            environmental=environmental,
            renault_brand_color=config_data.get("renault_brand_color", "#FFCB00"),
            company_name=config_data.get("company_name", "Renault"),
            dashboard_title=config_data.get(
                "dashboard_title", "EcoTI Dashboard - Sustentabilidade Digital"
            ),
        )

    def save_config(self, config: AppConfig) -> None:
        """Save configuration to file"""
        config_dict = self._config_to_dict(config)

        # Ensure directory exists
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)

        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)

    def _config_to_dict(self, config: AppConfig) -> Dict[str, Any]:
        """Convert AppConfig to dictionary"""
        config_dict = {
            "environment": config.environment.value,
            "data_source_type": config.data_source_type.value,
            "debug": config.debug,
            "host": config.host,
            "port": config.port,
            "auto_refresh_seconds": config.auto_refresh_seconds,
            "log_level": config.log_level,
            "environmental": {
                "emission_factor_kg_co2_per_kwh": config.environmental.emission_factor_kg_co2_per_kwh,
                "tree_sequestration_kg_co2_per_year": config.environmental.tree_sequestration_kg_co2_per_year,
                "energy_tariff_brl_per_kwh": config.environmental.energy_tariff_brl_per_kwh,
                "efficiency_potential_percent": config.environmental.efficiency_potential_percent,
            },
            "renault_brand_color": config.renault_brand_color,
            "company_name": config.company_name,
            "dashboard_title": config.dashboard_title,
        }

        if config.database:
            config_dict["database"] = {
                "connection_string": config.database.connection_string,
                "pool_size": config.database.pool_size,
                "timeout_seconds": config.database.timeout_seconds,
            }

        if config.api:
            config_dict["api"] = {
                "base_url": config.api.base_url,
                "api_key": config.api.api_key,
                "timeout_seconds": config.api.timeout_seconds,
                "retry_attempts": config.api.retry_attempts,
            }

        if config.snmp:
            config_dict["snmp"] = {
                "community": config.snmp.community,
                "timeout_seconds": config.snmp.timeout_seconds,
                "retries": config.snmp.retries,
            }

        return config_dict


# Global configuration manager instance
config_manager = ConfigManager()


def get_config() -> AppConfig:
    """Get the current application configuration"""
    return config_manager.load_config()
