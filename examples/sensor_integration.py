"""
Exemplo de integração com sensores IoT.
Este arquivo demonstra como conectar o EcoTI Dashboard a sensores reais.
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class SensorReading:
    """Estrutura padronizada para leituras de sensores"""
    sensor_id: str
    timestamp: datetime
    value: float
    unit: str
    sensor_type: str
    location: str
    quality: str = "good"  # good, warning, error

class BaseSensorConnector:
    """Classe base para conectores de sensores"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.api_key = config.get('api_key')
        self.base_url = config.get('base_url')
        self.timeout = config.get('timeout', 30)
    
    def get_data(self) -> List[SensorReading]:
        """Método abstrato para obter dados do sensor"""
        raise NotImplementedError("Subclasses devem implementar get_data()")
    
    def validate_reading(self, reading: SensorReading) -> bool:
        """Valida se a leitura está dentro dos parâmetros esperados"""
        if reading.value < 0:
            return False
        
        # Validações específicas por tipo de sensor
        if reading.sensor_type == "temperature" and reading.value > 50:
            reading.quality = "warning"
        elif reading.sensor_type == "power" and reading.value > 5000:
            reading.quality = "warning"
        
        return True

class PowerMeterConnector(BaseSensorConnector):
    """Conector para medidores de energia elétrica"""
    
    def get_data(self) -> List[SensorReading]:
        """Obtém dados de consumo dos medidores"""
        endpoint = f"{self.base_url}/api/v1/power-meters"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(endpoint, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            readings = []
            
            for meter_data in data.get('meters', []):
                reading = SensorReading(
                    sensor_id=meter_data['id'],
                    timestamp=datetime.fromisoformat(meter_data['timestamp']),
                    value=float(meter_data['power_kw']),
                    unit='kW',
                    sensor_type='power',
                    location=meter_data.get('location', 'unknown')
                )
                
                if self.validate_reading(reading):
                    readings.append(reading)
            
            return readings
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao conectar com medidores: {e}")
            return []

class TemperatureSensorConnector(BaseSensorConnector):
    """Conector para sensores de temperatura"""
    
    def get_data(self) -> List[SensorReading]:
        """Obtém dados de temperatura dos data centers"""
        endpoint = f"{self.base_url}/api/v1/temperature"
        headers = {'X-API-Key': self.api_key}
        
        try:
            response = requests.get(endpoint, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            readings = []
            
            for sensor_data in data.get('sensors', []):
                reading = SensorReading(
                    sensor_id=sensor_data['sensor_id'],
                    timestamp=datetime.now(),
                    value=float(sensor_data['temperature_celsius']),
                    unit='°C',
                    sensor_type='temperature',
                    location=sensor_data.get('room', 'unknown')
                )
                
                if self.validate_reading(reading):
                    readings.append(reading)
            
            return readings
            
        except requests.exceptions.RequestException as e:
            print(f"Erro ao conectar com sensores de temperatura: {e}")
            return []

class HumiditySensorConnector(BaseSensorConnector):
    """Conector para sensores de umidade"""
    
    def get_data(self) -> List[SensorReading]:
        """Obtém dados de umidade relativa"""
        # Implementação similar aos outros sensores
        pass

class SensorManager:
    """Gerenciador central de todos os sensores"""
    
    def __init__(self):
        self.connectors: Dict[str, BaseSensorConnector] = {}
        self.last_readings: Dict[str, List[SensorReading]] = {}
    
    def add_connector(self, name: str, connector: BaseSensorConnector):
        """Adiciona um novo conector de sensor"""
        self.connectors[name] = connector
        self.last_readings[name] = []
    
    def collect_all_data(self) -> Dict[str, List[SensorReading]]:
        """Coleta dados de todos os sensores conectados"""
        all_readings = {}
        
        for name, connector in self.connectors.items():
            try:
                readings = connector.get_data()
                all_readings[name] = readings
                self.last_readings[name] = readings
                print(f"Coletados {len(readings)} leituras do sensor {name}")
            except Exception as e:
                print(f"Erro ao coletar dados do sensor {name}: {e}")
                all_readings[name] = []
        
        return all_readings
    
    def get_aggregated_power_consumption(self) -> float:
        """Calcula consumo total agregado de todos os medidores"""
        total_power = 0.0
        
        for name, readings in self.last_readings.items():
            if 'power' in name:
                for reading in readings:
                    if reading.sensor_type == 'power':
                        total_power += reading.value
        
        return total_power
    
    def get_average_temperature(self) -> Optional[float]:
        """Calcula temperatura média dos data centers"""
        temperatures = []
        
        for name, readings in self.last_readings.items():
            if 'temperature' in name:
                for reading in readings:
                    if reading.sensor_type == 'temperature':
                        temperatures.append(reading.value)
        
        if temperatures:
            return sum(temperatures) / len(temperatures)
        return None
    
    def check_alerts(self) -> List[Dict]:
        """Verifica condições de alerta baseadas nos sensores"""
        alerts = []
        
        # Alerta de consumo alto
        total_power = self.get_aggregated_power_consumption()
        if total_power > 2000:  # kW
            alerts.append({
                'type': 'high_power_consumption',
                'message': f'Consumo alto detectado: {total_power:.1f} kW',
                'severity': 'warning',
                'timestamp': datetime.now().isoformat()
            })
        
        # Alerta de temperatura alta
        avg_temp = self.get_average_temperature()
        if avg_temp and avg_temp > 25:
            alerts.append({
                'type': 'high_temperature',
                'message': f'Temperatura alta no data center: {avg_temp:.1f}°C',
                'severity': 'warning',
                'timestamp': datetime.now().isoformat()
            })
        
        return alerts

# Exemplo de configuração e uso
def setup_sensors():
    """Configura e inicializa todos os sensores"""
    
    # Configurações dos sensores (normalmente vindas de arquivo de config)
    power_meter_config = {
        'api_key': 'YOUR_POWER_METER_API_KEY',
        'base_url': 'https://api.smartmeters.renault.com',
        'timeout': 30
    }
    
    temperature_config = {
        'api_key': 'YOUR_TEMPERATURE_API_KEY',
        'base_url': 'https://sensors.datacenter.renault.com',
        'timeout': 15
    }
    
    # Criar conectores
    power_connector = PowerMeterConnector(power_meter_config)
    temp_connector = TemperatureSensorConnector(temperature_config)
    
    # Criar gerenciador e adicionar conectores
    sensor_manager = SensorManager()
    sensor_manager.add_connector('power_meters', power_connector)
    sensor_manager.add_connector('temperature_sensors', temp_connector)
    
    return sensor_manager

def integrate_with_ecoti_dashboard(sensor_manager: SensorManager):
    """Integra dados dos sensores com o dashboard EcoTI"""
    
    # Coletar dados de todos os sensores
    all_readings = sensor_manager.collect_all_data()
    
    # Calcular métricas para o dashboard
    metrics = {
        'real_power_consumption_kw': sensor_manager.get_aggregated_power_consumption(),
        'average_temperature_celsius': sensor_manager.get_average_temperature(),
        'sensor_count': sum(len(readings) for readings in all_readings.values()),
        'last_update': datetime.now().isoformat()
    }
    
    # Verificar alertas
    alerts = sensor_manager.check_alerts()
    
    # Enviar dados para o dashboard (via API ou database)
    dashboard_data = {
        'metrics': metrics,
        'alerts': alerts,
        'raw_readings': all_readings
    }
    
    return dashboard_data

def simulate_sensor_data():
    """Simula dados de sensores para desenvolvimento/teste"""
    import random
    
    # Simular leituras de medidores de energia
    power_readings = []
    for i in range(5):  # 5 medidores
        reading = SensorReading(
            sensor_id=f"PM_{i+1:03d}",
            timestamp=datetime.now(),
            value=random.uniform(200, 800),  # kW
            unit='kW',
            sensor_type='power',
            location=f'Setor_{i+1}'
        )
        power_readings.append(reading)
    
    # Simular leituras de temperatura
    temp_readings = []
    for i in range(10):  # 10 sensores de temperatura
        reading = SensorReading(
            sensor_id=f"TS_{i+1:03d}",
            timestamp=datetime.now(),
            value=random.uniform(18, 28),  # °C
            unit='°C',
            sensor_type='temperature',
            location=f'DataCenter_{i+1}'
        )
        temp_readings.append(reading)
    
    return {
        'power_meters': power_readings,
        'temperature_sensors': temp_readings
    }

# Exemplo de uso prático
if __name__ == "__main__":
    print("🔌 Iniciando integração com sensores IoT...")
    
    # Para desenvolvimento, usar dados simulados
    print("📊 Gerando dados simulados...")
    simulated_data = simulate_sensor_data()
    
    print(f"Medidores de energia: {len(simulated_data['power_meters'])} leituras")
    print(f"Sensores de temperatura: {len(simulated_data['temperature_sensors'])} leituras")
    
    # Calcular consumo total simulado
    total_power = sum(reading.value for reading in simulated_data['power_meters'])
    avg_temp = sum(reading.value for reading in simulated_data['temperature_sensors']) / len(simulated_data['temperature_sensors'])
    
    print(f"Consumo total: {total_power:.1f} kW")
    print(f"Temperatura média: {avg_temp:.1f}°C")
    
    # Em produção, usar sensores reais:
    # sensor_manager = setup_sensors()
    # dashboard_data = integrate_with_ecoti_dashboard(sensor_manager)
    # print("Dados enviados para o dashboard:", dashboard_data)