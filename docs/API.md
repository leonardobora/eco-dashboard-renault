# 🌐 Documentação da API - EcoTI Dashboard

## 📋 Visão Geral

A API REST do EcoTI Dashboard fornece acesso programático a todas as métricas de sustentabilidade, permitindo integração com sistemas externos e desenvolvimento de aplicações customizadas.

**Base URL**: `http://localhost:5000` (desenvolvimento)  
**Content-Type**: `application/json`  
**Encoding**: `UTF-8`

## 🔐 Autenticação

### Desenvolvimento
No ambiente de desenvolvimento, a API não requer autenticação.

### Produção (Planejado)
```http
Authorization: Bearer <token>
```

## 📊 Endpoints Disponíveis

### 1. Métricas Principais

#### GET /api/metrics
Retorna todas as métricas atuais do sistema.

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:5000/api/metrics" \
  -H "Content-Type: application/json"
```

**Resposta de Sucesso (200):**
```json
{
  "consumo_atual": 1344.0,
  "emissoes_co2": 219610.2,
  "economia_potencial": 1612800.0,
  "arvores_equivalentes": 9982,
  "timestamp": "2025-01-18T10:30:00Z",
  "workstations_ativas": 4200,
  "servidores_ativos": 85,
  "modo_eco_ativo": true
}
```

**Campos da Resposta:**
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `consumo_atual` | float | Consumo atual em kWh |
| `emissoes_co2` | float | Emissões anuais de CO₂ em kg |
| `economia_potencial` | float | Economia potencial anual em R$ |
| `arvores_equivalentes` | int | Número de árvores equivalentes |
| `timestamp` | string | Timestamp da última atualização (ISO 8601) |
| `workstations_ativas` | int | Número de workstations ativas |
| `servidores_ativos` | int | Número de servidores ativos |
| `modo_eco_ativo` | boolean | Status do modo economia |

---

### 2. Histórico de Consumo

#### GET /api/consumption-history
Retorna histórico de consumo energético.

**Parâmetros de Query:**
| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `hours` | int | 24 | Período em horas |
| `interval` | string | "1h" | Intervalo de agregação (1h, 6h, 1d) |

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:5000/api/consumption-history?hours=48&interval=1h"
```

**Resposta de Sucesso (200):**
```json
{
  "data": [
    {
      "timestamp": "2025-01-17T00:00:00Z",
      "consumption_kwh": 800.5,
      "workstations_active": 200,
      "servers_active": 85
    },
    {
      "timestamp": "2025-01-17T01:00:00Z",
      "consumption_kwh": 750.2,
      "workstations_active": 150,
      "servers_active": 85
    }
  ],
  "total_records": 48,
  "period_start": "2025-01-16T10:30:00Z",
  "period_end": "2025-01-18T10:30:00Z"
}
```

---

### 3. Métricas por Setor

#### GET /api/sectors/metrics
Retorna métricas detalhadas por setor/departamento.

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:5000/api/sectors/metrics"
```

**Resposta de Sucesso (200):**
```json
{
  "sectors": [
    {
      "id": "administrativo",
      "name": "Administrativo",
      "workstations_total": 1200,
      "workstations_active": 900,
      "consumption_kwh": 225.0,
      "efficiency_percentage": 75.0,
      "savings_potential_brl": 48600.0
    },
    {
      "id": "engenharia",
      "name": "Engenharia",
      "workstations_total": 800,
      "workstations_active": 680,
      "consumption_kwh": 170.0,
      "efficiency_percentage": 85.0,
      "savings_potential_brl": 29440.0
    }
  ],
  "total_consumption": 1344.0,
  "total_workstations": 5376,
  "total_active": 4200
}
```

---

### 4. Alertas e Recomendações

#### GET /api/alerts
Retorna alertas ativos do sistema.

**Parâmetros de Query:**
| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `severity` | string | "all" | Filtrar por severidade (info, warning, error) |
| `active_only` | boolean | true | Apenas alertas ativos |

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:5000/api/alerts?severity=warning"
```

**Resposta de Sucesso (200):**
```json
{
  "alerts": [
    {
      "id": "alert_001",
      "type": "high_consumption",
      "title": "Consumo Elevado Detectado",
      "description": "Consumo 15% acima da média nas últimas 2 horas",
      "severity": "warning",
      "created_at": "2025-01-18T08:15:00Z",
      "location": "Setor Administrativo",
      "suggested_action": "Verificar workstations ociosas"
    }
  ],
  "total_alerts": 1,
  "severity_counts": {
    "info": 0,
    "warning": 1,
    "error": 0
  }
}
```

#### GET /api/recommendations
Retorna recomendações de otimização.

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:5000/api/recommendations"
```

**Resposta de Sucesso (200):**
```json
{
  "recommendations": [
    {
      "id": "rec_001",
      "type": "auto_shutdown",
      "title": "Desligamento Automático",
      "description": "Configurar desligamento automático após 2h de inatividade",
      "priority": "high",
      "effort": "low",
      "potential_savings_kwh": 150.0,
      "potential_savings_brl": 2700.0,
      "implementation_time": "1-2 horas",
      "affected_workstations": 1200
    }
  ],
  "total_recommendations": 1,
  "total_potential_savings": 2700.0
}
```

---

### 5. Previsões

#### GET /api/forecast
Retorna previsões de consumo energético.

**Parâmetros de Query:**
| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `days` | int | 7 | Período de previsão em dias |
| `include_optimized` | boolean | true | Incluir cenário otimizado |

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:5000/api/forecast?days=7"
```

**Resposta de Sucesso (200):**
```json
{
  "forecast": [
    {
      "date": "2025-01-19",
      "day_of_week": "Segunda",
      "predicted_consumption_kwh": 1400.0,
      "optimized_consumption_kwh": 1100.0,
      "confidence_level": 0.85,
      "potential_savings_kwh": 300.0,
      "weather_impact": "minimal"
    }
  ],
  "model_info": {
    "version": "v1.0",
    "accuracy": 0.89,
    "last_trained": "2025-01-15T12:00:00Z"
  }
}
```

---

### 6. Configurações

#### GET /api/config
Retorna configurações atuais do sistema.

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:5000/api/config"
```

**Resposta de Sucesso (200):**
```json
{
  "infrastructure": {
    "workstations_total": 5376,
    "servers_hp": 90,
    "vxrail_clusters": 10,
    "consumption_per_workstation_w": 250
  },
  "calculation_params": {
    "co2_emission_factor": 0.0817,
    "tree_sequestration_kg_year": 22,
    "energy_tariff_brl_kwh": 0.60
  },
  "thresholds": {
    "high_consumption_kwh": 2000,
    "temperature_warning_celsius": 25,
    "efficiency_target_percentage": 80
  }
}
```

#### PUT /api/config
Atualiza configurações do sistema.

**Exemplo de Requisição:**
```bash
curl -X PUT "http://localhost:5000/api/config" \
  -H "Content-Type: application/json" \
  -d '{
    "thresholds": {
      "high_consumption_kwh": 1800,
      "temperature_warning_celsius": 23
    }
  }'
```

**Resposta de Sucesso (200):**
```json
{
  "message": "Configurações atualizadas com sucesso",
  "updated_fields": ["thresholds.high_consumption_kwh", "thresholds.temperature_warning_celsius"],
  "timestamp": "2025-01-18T10:30:00Z"
}
```

---

### 7. Ações de Otimização

#### POST /api/optimize/implement
Implementa uma recomendação de otimização.

**Exemplo de Requisição:**
```bash
curl -X POST "http://localhost:5000/api/optimize/implement" \
  -H "Content-Type: application/json" \
  -d '{
    "recommendation_id": "rec_001",
    "confirm": true,
    "scheduled_time": "2025-01-18T22:00:00Z"
  }'
```

**Resposta de Sucesso (202):**
```json
{
  "status": "accepted",
  "job_id": "job_12345",
  "message": "Otimização agendada para implementação",
  "estimated_completion": "2025-01-18T22:30:00Z",
  "expected_impact": {
    "savings_kwh": 150.0,
    "savings_brl": 2700.0,
    "affected_devices": 1200
  }
}
```

#### GET /api/optimize/status/{job_id}
Verifica status de uma implementação.

**Exemplo de Requisição:**
```bash
curl -X GET "http://localhost:5000/api/optimize/status/job_12345"
```

**Resposta de Sucesso (200):**
```json
{
  "job_id": "job_12345",
  "status": "completed",
  "progress_percentage": 100,
  "started_at": "2025-01-18T22:00:00Z",
  "completed_at": "2025-01-18T22:25:00Z",
  "result": {
    "devices_affected": 1150,
    "actual_savings_kwh": 145.0,
    "success_rate": 95.8
  }
}
```

---

## 📈 Webhooks (Planejado)

### Configuração de Webhooks
Para receber notificações em tempo real sobre eventos importantes.

#### POST /api/webhooks/register
```json
{
  "url": "https://seu-sistema.com/webhook/ecoti",
  "events": ["high_consumption", "optimization_completed"],
  "secret": "seu_secret_key"
}
```

### Eventos Disponíveis
- `high_consumption`: Consumo acima do limite
- `low_efficiency`: Eficiência abaixo da meta
- `optimization_completed`: Otimização concluída
- `alert_created`: Novo alerta criado
- `forecast_updated`: Previsão atualizada

---

## 🔧 Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 201 | Criado com sucesso |
| 202 | Aceito (processamento assíncrono) |
| 400 | Requisição inválida |
| 401 | Não autorizado |
| 403 | Proibido |
| 404 | Não encontrado |
| 429 | Muitas requisições |
| 500 | Erro interno do servidor |

---

## 🚨 Tratamento de Erros

### Formato de Erro Padrão
```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "Parâmetro 'hours' deve ser um número inteiro positivo",
    "details": {
      "parameter": "hours",
      "provided_value": "-5",
      "expected_type": "positive integer"
    },
    "timestamp": "2025-01-18T10:30:00Z",
    "request_id": "req_12345"
  }
}
```

### Códigos de Erro Comuns
| Código | Descrição |
|--------|-----------|
| `INVALID_PARAMETER` | Parâmetro inválido |
| `MISSING_REQUIRED_FIELD` | Campo obrigatório ausente |
| `RESOURCE_NOT_FOUND` | Recurso não encontrado |
| `CALCULATION_ERROR` | Erro nos cálculos |
| `EXTERNAL_SERVICE_ERROR` | Erro em serviço externo |

---

## 📊 Rate Limiting

### Limites por Endpoint
| Endpoint | Limite | Janela |
|----------|--------|--------|
| `/api/metrics` | 60 req/min | Por IP |
| `/api/consumption-history` | 30 req/min | Por IP |
| `/api/optimize/implement` | 10 req/min | Por usuário |

### Headers de Rate Limiting
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1642518600
```

---

## 🔄 Versionamento

### URL Versioning
```http
GET /api/v1/metrics
GET /api/v2/metrics
```

### Header Versioning
```http
API-Version: v1
```

---

## 🧪 Ambiente de Teste

### Base URL de Teste
```
https://api-test.ecoti.renault.com
```

### Dados de Teste
A API de teste contém dados simulados que são redefinidos a cada 24 horas.

---

## 📚 SDKs e Bibliotecas

### Python
```python
from ecoti_client import EcoTIClient

client = EcoTIClient(base_url="http://localhost:5000")
metrics = client.get_metrics()
print(f"Consumo atual: {metrics['consumo_atual']} kWh")
```

### JavaScript
```javascript
import { EcoTIClient } from 'ecoti-js-client';

const client = new EcoTIClient('http://localhost:5000');
const metrics = await client.getMetrics();
console.log(`Consumo atual: ${metrics.consumo_atual} kWh`);
```

---

## 📞 Suporte

### Documentação Interativa
- **Swagger/OpenAPI**: `http://localhost:5000/api/docs`
- **Postman Collection**: [Download](link-para-collection)

### Contato
- **Email**: ecoti-api@renault.com
- **Slack**: #ecoti-dashboard
- **Issues**: [GitHub Issues](https://github.com/leonardobora/eco-dashboard-renault/issues)

---

Esta documentação evolui constantemente com o desenvolvimento do sistema. Sempre consulte a versão mais recente para obter informações atualizadas sobre a API.