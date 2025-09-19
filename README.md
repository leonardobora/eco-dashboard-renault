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
- Python 3.8+
- Navegador web moderno
- Git

### Instalação e Execução

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
# http://localhost:5000
```

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

### Monitoramento
- 📈 **Gráficos em Tempo Real**: Consumo por horário
- 🏢 **Status por Setor**: Administrativo, Engenharia, Produção, Vendas, Suporte
- 🚨 **Alertas Inteligentes**: Oportunidades de otimização

### Análise Preditiva
- 📅 **Previsão 7 dias**: Consumo futuro estimado
- 🎯 **Recomendações Automáticas**: IA para economia energética
- 📋 **Relatórios**: Exportação de dados e métricas

## 🔧 Configuração Técnica

### Estrutura de Arquivos
```
eco-dashboard-renault/
├── app_renault_mvp.py          # Aplicação Flask principal
├── templates/
│   └── dashboard.html          # Interface rica com abas
├── static/
│   ├── css/
│   │   └── style.css          # Estilos Renault
│   └── js/
│       └── app.js             # JavaScript integrado
├── requirements.txt            # Dependências Python
├── config/                     # Configurações avançadas
├── data_sources/              # Abstração de dados
├── tests/                     # Framework de testes
├── docs/                      # Documentação técnica
└── examples/                  # Implementações exemplo
```

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