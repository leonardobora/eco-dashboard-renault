# 📋 Documentação Técnica - EcoTI Dashboard

## 🏗️ Arquitetura do Sistema

### Visão Geral
O EcoTI Dashboard é projetado com uma arquitetura modular que separa claramente as responsabilidades entre frontend, backend e camada de dados, facilitando futuras integrações e expansões.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Data Layer    │
│   (Web UI)      │◄──►│   (Flask API)   │◄──►│  (Simulação)    │
│                 │    │                 │    │                 │
│ • HTML/CSS/JS   │    │ • Python Flask  │    │ • Dados Mock    │
│ • Chart.js      │    │ • REST APIs     │    │ • Cálculos      │
│ • Responsivo    │    │ • Business Logic│    │ • Métricas      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 Modelo de Dados

### Infraestrutura Base
```python
infraestrutura = {
    "workstations": 5376,           # Total de workstations
    "servidores_hp": 90,            # Servidores HP físicos
    "vxrail": 10,                   # Clusters VxRail
    "consumo_medio_workstation": 250, # Watts por workstation
    "fator_emissao": 0.0817,        # kg CO₂/kWh (Brasil)
    "sequestro_arvore": 22,         # kg CO₂/ano por árvore
    "tarifa_energia": 0.60          # R$/kWh
}
```

### Métricas Calculadas
```python
metricas = {
    "consumo_atual_kwh": float,      # Consumo instantâneo
    "emissoes_co2_kg_ano": float,    # Emissões anuais
    "economia_potencial_reais": float, # Economia em R$
    "arvores_equivalentes": int,     # Número de árvores
    "workstations_ativas": int,      # Equipamentos ligados
    "servidores_ativos": int,        # Servidores em uso
    "economia_ativa": bool           # Status do modo eco
}
```

## 🔌 APIs REST

### Endpoint Principal: `/api/metrics`
**Método**: `GET`  
**Descrição**: Retorna todas as métricas atuais do sistema

**Resposta**:
```json
{
  "consumo_atual": 1344.0,
  "emissoes_co2": 219610.2,
  "economia_potencial": 1612800.0,
  "arvores_equivalentes": 9982,
  "workstations_ativas": 4200,
  "servidores_ativos": 85,
  "timestamp": "2025-01-18T10:30:00Z"
}
```

### Extensões Futuras
```python
# Endpoints planejados para integração real
/api/sensors/consumption     # Dados de sensores IoT
/api/servers/status         # Status detalhado de servidores
/api/workstations/usage     # Uso por workstation
/api/alerts/active          # Alertas ativos
/api/reports/export         # Exportação de relatórios
/api/config/settings        # Configurações do sistema
```

## ⚙️ Algoritmos de Cálculo

### 1. Consumo Energético
```python
def calcular_consumo_atual(self):
    hora_atual = datetime.now().hour
    
    # Fator de uso baseado no horário
    if 8 <= hora_atual <= 18:      # Horário comercial
        fator_uso = 0.8
    elif 19 <= hora_atual <= 22:   # Horário reduzido
        fator_uso = 0.4
    else:                          # Madrugada
        fator_uso = 0.2
    
    # Cálculo do consumo
    consumo_ws = self.workstations_ativas * self.consumo_medio_w * fator_uso / 1000
    consumo_srv = self.servidores_ativos * 400 / 1000  # 400W por servidor
    
    return consumo_ws + consumo_srv
```

### 2. Emissões de CO₂
```python
def calcular_emissoes_anuais(self):
    # Projeção anual baseada no consumo atual
    consumo_anual_kwh = self.consumo_atual * 24 * 365
    
    # Fator de emissão da matriz energética brasileira
    emissoes_kg = consumo_anual_kwh * self.fator_emissao
    
    return emissoes_kg
```

### 3. Economia Potencial
```python
def calcular_economia_potencial(self):
    # Cenário otimizado: 70% das workstations em modo eco
    workstations_economizadas = self.workstations * 0.7
    consumo_economizado = workstations_economizadas * self.consumo_medio_w * 8 / 1000  # 8h/dia
    
    # Cálculo financeiro anual
    economia_anual = consumo_economizado * 365 * self.tarifa_energia
    
    return economia_anual
```

### 4. Equivalência em Árvores
```python
def calcular_arvores_equivalentes(self):
    emissoes_kg = self.calcular_emissoes_anuais()
    
    # Uma árvore sequestra ~22kg CO₂/ano
    numero_arvores = int(emissoes_kg / self.sequestro_arvore)
    
    return numero_arvores
```

## 🎨 Frontend - Componentes JavaScript

### Estrutura de Dados
```javascript
const appData = {
  infraestrutura: { /* configurações base */ },
  metricas_atuais: { /* valores em tempo real */ },
  historico_consumo: [ /* array de consumo por hora */ ],
  previsao_consumo: [ /* previsão para 7 dias */ ],
  setores: [ /* dados por departamento */ ]
};
```

### Principais Funções
```javascript
// Atualização de métricas
function updateMetrics()

// Inicialização de gráficos
function initializeCharts()

// Navegação entre abas
function setupTabNavigation()

// Simulação de dados em tempo real
function simulateRealTimeData()

// Exportação de relatórios
function exportData()
```

## 🔄 Integração com Dados Reais

### 1. Conectores de Sensores
```python
# Exemplo de conector para sensores IoT
class SensorConnector:
    def __init__(self, sensor_type, endpoint):
        self.sensor_type = sensor_type
        self.endpoint = endpoint
    
    def get_consumption_data(self):
        # Integração com APIs de sensores
        pass
    
    def get_server_status(self):
        # Status de servidores via SNMP/WMI
        pass
```

### 2. Adaptadores de Dados
```python
# Adaptador para diferentes fontes de dados
class DataAdapter:
    def normalize_consumption(self, raw_data):
        # Normalização de dados de diferentes sensores
        pass
    
    def calculate_metrics(self, consumption_data):
        # Cálculo de métricas baseado em dados reais
        pass
```

### 3. Pipeline de Dados
```
Sensores → Coletores → Processamento → APIs → Dashboard
    ↓           ↓           ↓          ↓        ↓
   IoT      Adaptadores  Cálculos   REST    Frontend
```

## 📈 Escalabilidade e Performance

### Otimizações Implementadas
- **Cache de métricas**: Reduz recálculos desnecessários
- **Atualização incremental**: Apenas dados alterados
- **Lazy loading**: Carregamento sob demanda de gráficos
- **Debouncing**: Evita atualizações excessivas

### Preparação para Escala
```python
# Estrutura preparada para múltiplas plantas
class PlantManager:
    def __init__(self):
        self.plants = {}  # Suporte a múltiplas unidades
    
    def add_plant(self, plant_id, config):
        # Adicionar nova planta/escritório
        pass
    
    def get_consolidated_metrics(self):
        # Métricas consolidadas de todas as plantas
        pass
```

## 🔐 Segurança e Configuração

### Variáveis de Ambiente
```bash
# .env (exemplo)
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://...
SENSOR_API_KEY=your-api-key
ALERT_EMAIL=admin@renault.com
```

### Configurações de Produção
```python
# config.py
class ProductionConfig:
    DEBUG = False
    TESTING = False
    DATABASE_URI = os.environ.get('DATABASE_URL')
    SENSOR_TIMEOUT = 30
    CACHE_TIMEOUT = 300
```

## 🧪 Testes e Validação

### Estrutura de Testes
```
tests/
├── unit/           # Testes unitários
├── integration/    # Testes de integração
├── e2e/           # Testes end-to-end
└── fixtures/      # Dados de teste
```

### Exemplo de Teste
```python
def test_consumo_calculation():
    infra = RenaultInfrastructure()
    consumo = infra.calcular_consumo_atual()
    
    assert consumo > 0
    assert isinstance(consumo, float)
    assert consumo < infra.workstations * infra.consumo_medio_w
```

## 📚 Recursos Adicionais

### Documentação de Referência
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)
- [Cálculos de Sustentabilidade - ABNT](https://www.abnt.org.br/)

### Ferramentas Recomendadas
- **Desenvolvimento**: VSCode, Python 3.8+
- **Monitoramento**: Prometheus, Grafana
- **Deploy**: Docker, Kubernetes
- **CI/CD**: GitHub Actions

---

Esta documentação técnica serve como base para desenvolvedores e especialistas que trabalharão na evolução e integração do sistema com dados reais da infraestrutura Renault.