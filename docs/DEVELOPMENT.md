# 🛠️ Guia de Desenvolvimento e Contribuição

## 🎯 Visão Geral

Este guia destina-se a desenvolvedores, especialistas ambientais e demais profissionais que contribuirão para a evolução do EcoTI Dashboard. O sistema foi projetado para máxima flexibilidade e facilidade de extensão.

## 🏗️ Arquitetura de Desenvolvimento

### Princípios de Design
- **Modularidade**: Componentes independentes e reutilizáveis
- **Flexibilidade**: Fácil adaptação a novos requisitos
- **Escalabilidade**: Preparado para crescimento
- **Manutenibilidade**: Código limpo e bem documentado

### Estrutura do Projeto
```
eco-dashboard-renault/
├── app_renault_mvp.py      # Aplicação Flask principal
├── config.py               # Configurações centralizadas
├── index.html              # Interface web principal
├── app.js                  # Lógica JavaScript
├── style.css               # Estilos e design system
├── requirements.txt        # Dependências Python
├── docs/                   # Documentação técnica
│   ├── TECHNICAL.md
│   ├── INSTALLATION.md
│   └── API.md
├── scripts/                # Scripts auxiliares
│   ├── data_generator.py
│   ├── chart_examples.py
│   └── mock_sensors.py
├── examples/               # Exemplos de integração
│   ├── sensor_integration.py
│   ├── database_models.py
│   └── api_clients.py
└── tests/                  # Testes (a serem criados)
    ├── unit/
    ├── integration/
    └── e2e/
```

## 🚀 Setup do Ambiente de Desenvolvimento

### 1. Preparação Inicial
```bash
# Clone e configuração
git clone https://github.com/leonardobora/eco-dashboard-renault.git
cd eco-dashboard-renault

# Ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Dependências
pip install -r requirements.txt

# Dependências de desenvolvimento (adicionar ao requirements-dev.txt)
pip install pytest black flake8 mypy pre-commit
```

### 2. Configuração do Ambiente
```bash
# Criar arquivo .env
cat > .env << EOF
FLASK_ENV=development
SECRET_KEY=dev-secret-key
DEBUG=True
LOG_LEVEL=DEBUG
EOF

# Configurar pre-commit hooks
pre-commit install
```

### 3. Executar em Modo Desenvolvimento
```bash
# Com auto-reload
export FLASK_ENV=development
python app_renault_mvp.py

# Ou usando Flask CLI
export FLASK_APP=app_renault_mvp.py
flask run --debug
```

## 📝 Padrões de Código

### Python (Backend)
```python
# Estrutura de classe para novos módulos
class EnergyCalculator:
    """
    Classe responsável por cálculos de energia.
    
    Attributes:
        config (dict): Configurações do sistema
        infrastructure (dict): Dados da infraestrutura
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.infrastructure = config.get('INFRASTRUCTURE', {})
    
    def calculate_consumption(self, hours: int = 24) -> float:
        """
        Calcula consumo energético para um período.
        
        Args:
            hours (int): Período em horas para cálculo
            
        Returns:
            float: Consumo em kWh
            
        Raises:
            ValueError: Se hours <= 0
        """
        if hours <= 0:
            raise ValueError("Período deve ser maior que zero")
        
        # Implementação...
        return 0.0
```

### JavaScript (Frontend)
```javascript
// Estrutura de módulos JavaScript
const EnergyDashboard = {
    // Configurações
    config: {
        updateInterval: 5000,
        chartAnimation: true
    },
    
    // Estado da aplicação
    state: {
        currentMetrics: {},
        isLoading: false,
        lastUpdate: null
    },
    
    // Métodos públicos
    init() {
        this.setupEventListeners();
        this.loadInitialData();
        this.startRealTimeUpdates();
    },
    
    // Métodos privados
    _updateMetrics(data) {
        // Implementação...
    },
    
    _formatCurrency(value) {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    }
};
```

### CSS (Estilos)
```css
/* Convenções de nomenclatura BEM */
.metric-card {
    /* Estilos base */
}

.metric-card__header {
    /* Elemento do card */
}

.metric-card--featured {
    /* Modificador para card em destaque */
}

/* Variáveis CSS para temas */
:root {
    --color-primary: #FFCB00;
    --color-text: #333333;
    --spacing-sm: 8px;
    --spacing-md: 16px;
    --spacing-lg: 24px;
}
```

## 🔧 Adicionando Novas Funcionalidades

### 1. Nova Métrica de Sustentabilidade

#### Backend (Python)
```python
# Em app_renault_mvp.py ou novo módulo
def calcular_pegada_hidrica(self):
    """Calcula pegada hídrica do data center"""
    # Consumo de água para refrigeração (L/kWh)
    fator_agua = 1.8  # Litros por kWh
    consumo_anual = self.consumo_atual * 24 * 365
    pegada_hidrica = consumo_anual * fator_agua
    return pegada_hidrica

# Adicionar ao endpoint /api/metrics
@app.route('/api/metrics')
def get_metrics():
    infra.consumo_atual = infra.calcular_consumo_atual()
    return jsonify({
        'consumo_atual': infra.consumo_atual,
        'emissoes_co2': infra.calcular_emissoes_anuais(),
        'economia_potencial': infra.calcular_economia_potencial(),
        'arvores_equivalentes': infra.calcular_arvores_equivalentes(),
        'pegada_hidrica': infra.calcular_pegada_hidrica()  # Nova métrica
    })
```

#### Frontend (JavaScript)
```javascript
// Em app.js
function updateMetrics() {
    fetch('/api/metrics')
        .then(response => response.json())
        .then(data => {
            // Métricas existentes...
            
            // Nova métrica
            document.getElementById('waterFootprint').textContent = 
                formatNumber(data.pegada_hidrica) + ' L';
        });
}
```

#### Interface (HTML)
```html
<!-- Adicionar novo card de métrica -->
<div class="metric-card water-card">
    <div class="metric-icon">💧</div>
    <div class="metric-content">
        <h3>Pegada Hídrica</h3>
        <div class="metric-value" id="waterFootprint">-</div>
        <div class="metric-trend neutral">Litros/ano</div>
    </div>
</div>
```

### 2. Novo Tipo de Sensor

```python
# examples/sensor_integration.py
class SensorConnector:
    """Conector genérico para sensores IoT"""
    
    def __init__(self, sensor_type: str, endpoint: str, api_key: str):
        self.sensor_type = sensor_type
        self.endpoint = endpoint
        self.api_key = api_key
    
    def get_data(self) -> dict:
        """Obtém dados do sensor"""
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(self.endpoint, headers=headers)
        return response.json()
    
    def normalize_data(self, raw_data: dict) -> dict:
        """Normaliza dados para formato padrão"""
        # Implementar normalização específica do sensor
        return {
            'timestamp': raw_data.get('timestamp'),
            'value': raw_data.get('value'),
            'unit': raw_data.get('unit'),
            'sensor_id': raw_data.get('id')
        }

# Uso do conector
temperature_sensor = SensorConnector(
    sensor_type='temperature',
    endpoint='https://api.sensor.com/v1/temperature',
    api_key='seu-api-key'
)

data = temperature_sensor.get_data()
normalized = temperature_sensor.normalize_data(data)
```

### 3. Nova Visualização/Gráfico

```javascript
// Adicionar novo tipo de gráfico
function initializeWaterUsageChart() {
    const ctx = document.getElementById('waterUsageChart').getContext('2d');
    
    waterUsageChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Refrigeração', 'Umidificação', 'Limpeza', 'Outros'],
            datasets: [{
                data: [70, 15, 10, 5],
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Distribuição do Uso de Água'
                }
            }
        }
    });
}
```

## 🔄 Integrações com Sistemas Externos

### 1. Integração com Banco de Dados

```python
# examples/database_models.py
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class EnergyMetric(Base):
    __tablename__ = 'energy_metrics'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    consumption_kwh = Column(Float, nullable=False)
    co2_emissions_kg = Column(Float, nullable=False)
    cost_brl = Column(Float, nullable=False)
    location = Column(String(100))

# Configuração da conexão
engine = create_engine('postgresql://user:pass@localhost/ecoti')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def save_metrics(metrics: dict):
    """Salva métricas no banco de dados"""
    session = SessionLocal()
    try:
        metric = EnergyMetric(
            timestamp=datetime.now(),
            consumption_kwh=metrics['consumo_atual'],
            co2_emissions_kg=metrics['emissoes_co2'],
            cost_brl=metrics['economia_potencial']
        )
        session.add(metric)
        session.commit()
    finally:
        session.close()
```

### 2. Integração com APIs Externas

```python
# examples/api_clients.py
import requests
from typing import Optional

class WeatherAPIClient:
    """Cliente para API de clima (para correlacionar com consumo)"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, city: str) -> Optional[dict]:
        """Obtém clima atual"""
        url = f"{self.base_url}/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter clima: {e}")
            return None

class EnergyGridAPIClient:
    """Cliente para API da rede elétrica"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def get_carbon_intensity(self) -> float:
        """Obtém intensidade de carbono atual da rede"""
        # Implementar integração com API da rede elétrica
        pass
```

## 🧪 Testes

### Estrutura de Testes
```python
# tests/unit/test_calculations.py
import pytest
from app_renault_mvp import RenaultInfrastructure

class TestEnergyCalculations:
    
    def setup_method(self):
        """Setup para cada teste"""
        self.infra = RenaultInfrastructure()
    
    def test_consumo_calculation(self):
        """Testa cálculo de consumo"""
        consumo = self.infra.calcular_consumo_atual()
        
        assert isinstance(consumo, float)
        assert consumo > 0
        assert consumo < 10000  # Limite razoável
    
    def test_co2_calculation(self):
        """Testa cálculo de emissões CO₂"""
        emissoes = self.infra.calcular_emissoes_anuais()
        
        assert isinstance(emissoes, float)
        assert emissoes > 0
    
    @pytest.mark.parametrize("workstations,expected_min", [
        (1000, 100),
        (5000, 500),
        (10000, 1000)
    ])
    def test_different_workstation_counts(self, workstations, expected_min):
        """Testa cálculos com diferentes quantidades de workstations"""
        self.infra.workstations = workstations
        consumo = self.infra.calcular_consumo_atual()
        
        assert consumo >= expected_min

# Executar testes
# pytest tests/ -v
```

### Testes de Integração
```python
# tests/integration/test_api.py
import json
from app_renault_mvp import app

class TestAPIEndpoints:
    
    def setup_method(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_metrics_endpoint(self):
        """Testa endpoint de métricas"""
        response = self.client.get('/api/metrics')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'consumo_atual' in data
        assert 'emissoes_co2' in data
        assert isinstance(data['consumo_atual'], (int, float))
```

## 📊 Monitoramento e Debugging

### Logging Avançado
```python
import logging
from functools import wraps

def log_performance(func):
    """Decorator para medir performance de funções"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logging.info(f"{func.__name__} executada em {end_time - start_time:.3f}s")
        return result
    return wrapper

@log_performance
def calcular_metricas_complexas():
    # Implementação...
    pass
```

### Debugging Frontend
```javascript
// Debug mode para desenvolvimento
const DEBUG = true;

function debugLog(message, data = null) {
    if (DEBUG) {
        console.log(`[EcoTI Debug] ${message}`, data);
    }
}

// Monitoramento de performance
function measurePerformance(name, fn) {
    const start = performance.now();
    const result = fn();
    const end = performance.now();
    
    debugLog(`${name} executou em ${(end - start).toFixed(2)}ms`);
    return result;
}
```

## 🤝 Fluxo de Contribuição

### 1. Preparação
```bash
# Fork do repositório no GitHub
git clone https://github.com/SEU-USUARIO/eco-dashboard-renault.git
cd eco-dashboard-renault

# Adicionar upstream
git remote add upstream https://github.com/leonardobora/eco-dashboard-renault.git

# Criar branch para feature
git checkout -b feature/nova-funcionalidade
```

### 2. Desenvolvimento
```bash
# Fazer alterações
# Testar localmente
python -m pytest tests/

# Commit seguindo convenção
git add .
git commit -m "feat: adiciona cálculo de pegada hídrica

- Implementa cálculo baseado em consumo energético
- Adiciona endpoint /api/water-footprint  
- Inclui visualização no dashboard
- Adiciona testes unitários

Closes #123"
```

### 3. Pull Request
```bash
# Push da branch
git push origin feature/nova-funcionalidade

# Criar PR no GitHub com descrição detalhada
```

### Convenções de Commit
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Atualização de documentação
- `style:` Mudanças de formatação
- `refactor:` Refatoração de código
- `test:` Adição de testes
- `chore:` Tarefas de manutenção

## 📋 Checklist para Contributors

### Antes de Contribuir
- [ ] Ler toda a documentação
- [ ] Configurar ambiente de desenvolvimento
- [ ] Executar testes existentes
- [ ] Entender a arquitetura atual

### Durante o Desenvolvimento
- [ ] Seguir padrões de código
- [ ] Escrever testes para novas funcionalidades
- [ ] Documentar mudanças significativas
- [ ] Testar em diferentes cenários

### Antes do Pull Request
- [ ] Executar todos os testes
- [ ] Verificar lint/formatação
- [ ] Atualizar documentação se necessário
- [ ] Testar integração com sistema existente

## 🎯 Roadmap de Desenvolvimento

### Fase 1: Consolidação (Atual)
- [x] Dashboard funcional
- [x] Cálculos básicos de sustentabilidade
- [x] Interface responsiva
- [x] Documentação técnica

### Fase 2: Integrações
- [ ] Conectores para sensores IoT
- [ ] Integração com banco de dados
- [ ] APIs para sistemas externos
- [ ] Autenticação e autorização

### Fase 3: Inteligência
- [ ] Machine Learning para previsões
- [ ] Alertas inteligentes
- [ ] Otimizações automáticas
- [ ] Relatórios avançados

### Fase 4: Escalabilidade
- [ ] Suporte multi-tenant
- [ ] Microserviços
- [ ] Deploy em cloud
- [ ] Monitoramento avançado

---

Este guia garante que o desenvolvimento do EcoTI Dashboard seja colaborativo, organizado e mantenha a qualidade técnica necessária para um sistema de produção robusto.