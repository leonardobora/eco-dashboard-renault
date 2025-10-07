# 🌱 EcoTI Dashboard - Renault Sustentabilidade Digital

[![Renault](https://img.shields.io/badge/Renault-FFCB00?style=for-the-badge&logo=renault&logoColor=black)](https://www.renault.com.br)
[![Sustentabilidade](https://img.shields.io/badge/Sustentabilidade-Digital-green?style=for-the-badge)](https://github.com/leonardobora/eco-dashboard-renault)

## 📋 Sobre o Projeto

O **EcoTI Dashboard** é a solução desenvolvida pela equipe UniBrasil para o **Desafio de Sustentabilidade Digital IS/IT** no **Transformation Day 2025** da Renault. 

Este sistema monitora e otimiza o consumo energético da infraestrutura de TI da Renault, oferecendo:
- 📊 **Monitoramento em tempo real** de workstations e servidores
- 🌍 **Cálculo de emissões de CO₂** e impacto ambiental
- 💰 **Análise de economia energética** e potencial financeiro
- 🌳 **Equivalência em árvores plantadas** para visualização do impacto
- 🤖 **Recomendações automáticas** para otimização energética
- 📈 **Análise preditiva** de consumo e tendências

## 🏗️ Arquitetura do Sistema

### 🎯 Duas Versões Disponíveis

Este projeto oferece **duas versões funcionais** do dashboard:

#### 1️⃣ Versão Flask (Desenvolvimento e Produção)
- ✅ **Backend Python completo** com API REST
- ✅ **Templates Jinja2 dinâmicos**
- ✅ **Cálculos server-side** em Python
- ✅ **Ideal para**: Desenvolvimento local e deploy em servidores
- 📍 **Arquivos**: `app_renault_mvp.py`, `templates/`, `static/`

#### 2️⃣ Versão Estática (GitHub Pages)
- ✅ **HTML puro** sem backend
- ✅ **Cálculos client-side** em JavaScript
- ✅ **Deploy gratuito** no GitHub Pages
- ✅ **Ideal para**: Demonstrações, portfólio, eventos
- 📍 **Arquivos**: `index.html`, `sobre.html`, `static/js/metrics-calculator.js`

### Como Funciona?

**Flask Version:**
```
Navegador → Flask Server → Python (cálculos) → Templates Jinja2 → HTML
```

**GitHub Pages Version:**
```
Navegador → HTML estático → JavaScript (cálculos) → Renderização
```

### Aplicação Unificada
- **Flask Backend** - Servidor web e API REST integrados
- **Template Engine** - Jinja2 para renderização dinâmica
- **Static Assets** - CSS/JS organizados em estrutura modular
- **Chart.js** - Visualizações e gráficos interativos
- **Design System** - Identidade visual Renault (#FFCB00)

### Estrutura Técnica
- **Python Flask 2.3.3** - Aplicação web completa
- **Templates** - Interface rica com abas e dashboards
- **API REST** - Endpoint `/api/metrics` para dados em tempo real
- **Cálculos Ambientais** - Métricas de sustentabilidade integradas

### Dados Simulados
- **5.376 workstations** distribuídas por setores
- **90 servidores HP** + **10 VxRail**
- **Métricas em tempo real** baseadas em padrões reais

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.8+ (apenas para versão Flask)
- Navegador web moderno
- Git

### 🐍 Opção 1: Versão Flask (Desenvolvimento)

```bash
# Clone o repositório
git clone https://github.com/leonardobora/eco-dashboard-renault.git
cd eco-dashboard-renault

# Configure o ambiente virtual (recomendado)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação Flask
python app_renault_mvp.py

# Acesse o dashboard completo
# Dashboard: http://localhost:5000
# Sobre: http://localhost:5000/sobre
# API: http://localhost:5000/api/metrics
```

**Teste da API:**
```bash
curl -s http://localhost:5000/api/metrics | python -m json.tool
```

**Resposta esperada:**
```json
{
  "consumo_atual": 841.935,
  "emissoes_co2": 602566.14,
  "economia_potencial": 352800.0,
  "arvores_equivalentes": 27389,
  "fonte": "simulado",          ← Indica origem dos dados
  "detalhes_fonte": {           ← Novo: breakdown por componente
    "servidores": "simulado",
    "workstations": "simulado"
  }
}
```

**Configuração SNMP (Opcional):**
Para habilitar monitoramento real dos servidores:
```bash
# 1. Configure SNMPv3 nos servidores (ver SNMP_SETUP.md)
# 2. Edite renault_servers.json com IPs e credenciais
# 3. Reinicie a aplicação - coleta SNMP ativa automaticamente!

# Teste a coleta SNMP:
python3 -c "from snmp_collector import SNMPCollector; \
c = SNMPCollector(); \
consumption, fonte = c.get_total_consumption_kwh(); \
print(f'Consumo: {consumption:.2f} kWh - Fonte: {fonte}')"
```

📖 **Guia completo**: [SNMP_QUICKSTART.md](SNMP_QUICKSTART.md)

### 🌐 Opção 2: Versão Estática (GitHub Pages)

#### Teste Local:
```bash
# Clone o repositório
git clone https://github.com/leonardobora/eco-dashboard-renault.git
cd eco-dashboard-renault

# Inicie um servidor HTTP simples
python3 -m http.server 8080 --bind localhost

# Acesse no navegador
# http://localhost:8080/index.html
# http://localhost:8080/sobre.html
```

#### Deploy no GitHub Pages:
1. Acesse: `Settings` → `Pages` no GitHub
2. Source: `main` branch
3. Folder: `/ (root)`
4. Salve e aguarde o build (2-5 minutos)
5. Acesse: `https://leonardobora.github.io/eco-dashboard-renault/`

### Aplicação Unificada
- **Uma única aplicação** Flask com interface rica
- **Template integrado** com visualizações avançadas
- **API interna** para dados em tempo real
- **Estrutura modular** para fácil manutenção

## 📊 Funcionalidades Principais

### Dashboard Principal
- ⚡ **Consumo Atual**: Monitoramento em kWh
- 🌍 **Emissões CO₂**: Cálculo anual em kg
- 💰 **Economia Potencial**: Valor em R$ por ano
- 🌳 **Equivalente em Árvores**: Impacto visual do carbono

### Monitoramento SNMP Real ✨ **NOVO**
- 🔌 **Coleta via SNMPv3**: Dados reais dos servidores HP DL380 e VxRail
- 🔐 **Segurança**: SHA-256 auth + AES-128 encryption
- 🚀 **Performance**: Cache 5min, rate limiting, retry automático
- 🛡️ **Resiliência**: Fallback automático para dados simulados
- 📊 **Suporte Multi-Geração**: HP Gen8/Gen9/Gen10 + Dell VxRail
- 📍 **Indicador de Fonte**: Campo `fonte` na API mostra origem dos dados

> **Modo Híbrido**: Funciona sem configuração SNMP (dados simulados) e automaticamente coleta dados reais quando configurado. Zero downtime!
>
> 📖 **Documentação**: Ver [SNMP_SETUP.md](SNMP_SETUP.md) e [SNMP_QUICKSTART.md](SNMP_QUICKSTART.md)

### Monitoramento
- 📈 **Gráficos em Tempo Real**: Consumo por horário
- 🏢 **Status por Setor**: Administrativo, Engenharia, Produção, Vendas, Suporte
- 🚨 **Alertas Inteligentes**: Oportunidades de otimização

### Análise Preditiva
- 📅 **Previsão 7 dias**: Consumo futuro estimado
- 🎯 **Recomendações Automáticas**: IA para economia energética
- 📋 **Relatórios**: Exportação de dados e métricas

## 📊 Flask vs GitHub Pages: Comparação

### Funcionalidades

| Recurso | Flask | GitHub Pages |
|---------|-------|--------------|
| **Dashboard completo** | ✅ | ✅ |
| **Métricas em tempo real** | ✅ | ✅ |
| **Gráficos Chart.js** | ✅ | ✅ |
| **Design Renault** | ✅ | ✅ |
| **API REST** | ✅ | ❌ |
| **Cálculos Python** | ✅ | ❌ |
| **Cálculos JavaScript** | ❌ | ✅ |
| **Deploy gratuito** | ❌ | ✅ |
| **Custo de hospedagem** | R$ 720-2.300/ano | R$ 0/ano |

### Quando Usar Cada Versão?

**Use Flask quando:**
- 🔧 Desenvolvimento local
- 🏢 Deploy em servidor próprio/cloud
- 🔌 Integração com dados reais (SNMP, databases)
- 👥 Autenticação de usuários necessária
- 📡 APIs externas precisam ser consumidas

**Use GitHub Pages quando:**
- 🎪 Apresentações e demonstrações
- 💼 Portfólio e eventos
- 🚀 Deploy rápido e gratuito
- 🌐 Acesso público sem infraestrutura
- 📱 Compartilhamento via URL

### 🔄 Como o `app.js` Detecta o Ambiente?

O JavaScript detecta automaticamente qual versão está rodando:

```javascript
// static/js/app.js
async function fetchMetrics() {
  // Se metrics-calculator.js foi carregado (GitHub Pages)
  if (typeof window.RenaultInfrastructure !== 'undefined') {
    // Usa cálculos locais em JavaScript
    const infra = new window.RenaultInfrastructure();
    return infra.getMetrics();
  }
  
  // Senão, tenta API Flask
  const response = await fetch('/api/metrics');
  return await response.json();
}
```

### 📁 Arquivos por Versão

**Flask:**
- `app_renault_mvp.py` - Backend principal
- `templates/dashboard.html` - Template Jinja2
- `templates/sobre.html` - Página sobre
- Acesso via: `http://localhost:5000`

**GitHub Pages:**
- `index.html` - HTML puro (convertido)
- `sobre.html` - HTML puro (convertido)
- `static/js/metrics-calculator.js` - Cálculos em JS
- Acesso via: `https://leonardobora.github.io/eco-dashboard-renault/`

## 🔧 Configuração Técnica

### Estrutura de Arquivos
```
eco-dashboard-renault/
├── app_renault_mvp.py          # 🐍 Aplicação Flask principal
├── index.html                  # 🌐 Dashboard estático (GitHub Pages)
├── sobre.html                  # 🌐 Página sobre estática (GitHub Pages)
├── templates/                  # 🐍 Templates Flask (Jinja2)
│   ├── dashboard.html          # Interface rica com abas
│   └── sobre.html              # Página sobre o projeto
├── static/                     # 📦 Assets compartilhados
│   ├── css/
│   │   └── style.css          # Estilos Renault (#FFCB00)
│   └── js/
│       ├── app.js             # 🔄 Auto-detecta Flask/Pages
│       └── metrics-calculator.js  # 🌐 Cálculos JavaScript (Pages)
├── requirements.txt            # Dependências Python
├── config/                     # Configurações avançadas
├── data_sources/              # Abstração de dados
├── tests/                     # Framework de testes
├── docs/                      # 📚 Documentação técnica
└── examples/                  # Implementações exemplo
```

**Legenda:**
- 🐍 Usado apenas na versão Flask
- 🌐 Usado apenas na versão GitHub Pages
- 🔄 Inteligente: funciona em ambas versões
- 📦 Compartilhado entre ambas versões

### APIs Disponíveis

#### GET /api/metrics
Retorna métricas atuais do sistema:
```json
{
  "consumo_atual": 1344.0,
  "emissoes_co2": 219610.2,
  "economia_potencial": 1612800.0,
  "arvores_equivalentes": 9982
}
```

### Cálculos Implementados

#### Consumo Energético
```python
# Baseado no horário e fator de uso
consumo = workstations_ativas * consumo_medio * fator_horario
```

#### Emissões CO₂
```python
# Fator de emissão brasileiro: 0.0817 kg CO₂/kWh
emissoes = consumo_anual_kwh * 0.0817
```

#### Equivalência em Árvores
```python
# Sequestro médio: 22 kg CO₂/ano por árvore
arvores = emissoes_co2 / 22
```

## 🌱 Estado "Tabula Rasa"

Este projeto foi desenvolvido em **estado de máxima flexibilidade** para facilitar a integração com dados reais:

### 🔄 Adaptação de Dados
- **Estruturas flexíveis** para receber dados de sensores
- **APIs modulares** para integração com sistemas externos
- **Cálculos parametrizáveis** conforme orientações ambientais

### 🛠️ Extensibilidade
- **Modelos de dados** prontos para expansão
- **Interface configurável** para novos KPIs
- **Sistema de alertas** personalizável

### 📈 Escalabilidade
- **Arquitetura modular** para crescimento
- **Separação clara** entre frontend e backend
- **Documentação técnica** para desenvolvimento futuro

## 🎯 Próximos Passos

### Integração com Dados Reais
1. **Conectores de Sensores**: Integração com hardware de monitoramento
2. **APIs Externas**: Conexão com sistemas de gerenciamento de energia
3. **Banco de Dados**: Persistência de histórico e métricas
4. **Machine Learning**: Modelos preditivos avançados

### Funcionalidades Avançadas
1. **Alertas Push**: Notificações em tempo real
2. **Relatórios Automáticos**: Geração periódica de insights
3. **Dashboard Mobile**: Aplicativo para gestores
4. **Integração ERP**: Conexão com sistemas corporativos

## 🤝 Colaboração e Desenvolvimento

### Estrutura para Equipe Multidisciplinar
- **Desenvolvedores**: Foco em APIs e integrações
- **Especialistas Ambientais**: Configuração de cálculos e métricas
- **Gestores de TI**: Definição de KPIs e alertas
- **UX/UI**: Evolução da interface e experiência

### Metodologia Ágil
- **Sprints curtos** para iteração rápida
- **Feedback contínuo** com stakeholders
- **Documentação viva** atualizada constantemente

## 📞 Contato e Suporte

- **Equipe**: UniBrasil
- **Evento**: Transformation Day 2025 - Renault
- **Categoria**: Sustentabilidade Digital IS/IT

---

### 🏆 Objetivo Final
Criar um sistema robusto e flexível que sirva como base para o monitoramento real da sustentabilidade digital na Renault, permitindo economia energética significativa e contribuindo para os objetivos ambientais da empresa.

**🌍 Sustentabilidade Digital é o futuro da TI responsável!**