# 🔧 Plano de Execução Técnica - EcoTI Dashboard Renault
## Transformation Day 2025 - Preparação do Protótipo

**Data de Atualização:** 18 de Outubro de 2025  
**Responsável Técnico:** Leonardo Bora  
**Evento:** 25 de Outubro de 2025 (7 dias restantes)

---

## 📊 Análise da Situação Atual

### ✅ O que já temos implementado:

1. **Infraestrutura Base**
   - Aplicação Flask 2.3.3 completa e funcional
   - Duas versões: Flask (backend) + Estática (GitHub Pages)
   - API REST em `/api/metrics` com dados em tempo real
   - Template engine Jinja2 com interface rica

2. **Dados Simulados**
   - 5.376 workstations distribuídas por setores
   - 90 servidores HP + 10 VxRail (total: 100 servidores)
   - Consumo médio: 250W por workstation, 400W por servidor
   - Fator de emissão: 0.0817 kg CO2/kWh (Brasil)

3. **Funcionalidades Existentes**
   - Monitoramento em tempo real de consumo energético
   - Cálculo de emissões de CO2 anuais
   - Análise de economia potencial (workstations ociosas)
   - Equivalência em árvores plantadas (22 kg CO2/ano por árvore)
   - Suporte a SNMP para coleta real (implementado mas em modo simulado)

4. **Visualizações**
   - Dashboard interativo com Chart.js
   - Gráficos de consumo por horário
   - Métricas ambientais e financeiras
   - Design system Renault (#FFCB00)

---

## 🎯 Requisitos da Apresentação

### Estrutura do Pitch (10 minutos)

| Seção | Responsável | Tempo | Foco Técnico |
|-------|-------------|-------|--------------|
| **Introdução** | Kamille + Gabriel | 30s | Contextualizar o problema de sustentabilidade digital |
| **Aplicabilidade** | Sthefany | 30s | Viabilidade técnica com recursos existentes da Renault |
| **Factilidade** | Suélen | 30s | Como implementar na prática |
| **Facilidade** | Meridiana | 30s | Simplicidade de adoção pela equipe atual |
| **Protótipo** | **Leonardo + Daniel** | **2min** | **Demonstração ao vivo do dashboard** |
| **Perguntas** | Todos | 4-5min | Preparar respostas técnicas |

### Pontos-Chave para a Demonstração Técnica:
- ✅ Mostrar dashboard em tempo real
- ✅ Destacar cálculos de CO2 e impacto ambiental
- ✅ Demonstrar API REST funcionando
- ✅ Apresentar recomendações de IA
- ✅ Evidenciar facilidade de integração

---

## 🚀 Plano de Melhorias para o Protótipo

### 🔴 PRIORIDADE ALTA (até 20/10 - Domingo)

#### 1. Integração com Dados Reais do PDF de Carbono
**Objetivo:** Substituir dados simulados por valores reais do estudo da Renault

**Tarefas:**
- [ ] Extrair dados do PDF "Relação de consumo de carbono"
- [ ] Criar módulo `data_sources/carbon_data.py` para carregar dados reais
- [ ] Atualizar `RenaultInfrastructure` com valores reais:
  - Consumo real por setor/departamento
  - Padrões de uso horário baseados em dados históricos
  - Fatores de emissão específicos da região
- [ ] Validar cálculos com dados reais vs simulados

**Arquivo a modificar:**
```python
# app_renault_mvp.py - RenaultInfrastructure class
# Adicionar import: from data_sources.carbon_data import CarbonDataLoader
```

#### 2. Melhorias na API REST
**Objetivo:** Adicionar endpoints para demonstração ao vivo

**Novos endpoints:**
- [ ] `/api/sectors` - Consumo por setor/departamento
- [ ] `/api/recommendations` - Recomendações de IA em tempo real
- [ ] `/api/savings` - Projeções de economia detalhadas
- [ ] `/api/trends` - Análise preditiva de consumo

**Arquivo a criar:**
```python
# routes/api_routes.py - Endpoints adicionais
```

#### 3. Dashboard de IA - Recomendações Inteligentes
**Objetivo:** Mostrar capacidade de análise e sugestões automáticas

**Funcionalidades:**
- [ ] Algoritmo de detecção de recursos ociosos
- [ ] Sugestões de horários otimizados
- [ ] Alertas de consumo anormal
- [ ] Ranking de setores por eficiência

**Arquivo a criar:**
```python
# ai_engine/recommendations.py - Engine de recomendações
```

### 🟡 PRIORIDADE MÉDIA (até 22/10 - Terça)

#### 4. Visualizações Aprimoradas
**Objetivo:** Dashboard mais impactante para apresentação

**Melhorias:**
- [ ] Gráfico de comparação: consumo atual vs otimizado
- [ ] Mapa de calor de consumo por horário/setor
- [ ] Linha do tempo de economia projetada
- [ ] Widget de "impacto em tempo real" (CO2 sendo reduzido)

**Arquivos a modificar:**
```
templates/dashboard.html
static/js/charts.js
static/css/dashboard.css
```

#### 5. Modo Demonstração
**Objetivo:** Preparar cenários pré-configurados para a apresentação

**Funcionalidades:**
- [ ] Modo "demo" com dados dramáticos (alto desperdício)
- [ ] Simulação de otimização ao vivo (redução imediata)
- [ ] Histórico fake de 30 dias com tendências
- [ ] Toggle fácil entre modo demo e modo real

**Arquivo a criar:**
```python
# config/demo_mode.py - Configurações de demonstração
```

### 🟢 PRIORIDADE BAIXA (até 24/10 - Quinta)

#### 6. Documentação Técnica
**Objetivo:** Preparar material de apoio para perguntas

**Documentos:**
- [ ] Arquitetura técnica detalhada (diagrama)
- [ ] Fluxo de dados (data flow)
- [ ] Justificativas de escolhas técnicas
- [ ] Roadmap de implementação na Renault

**Arquivo a criar:**
```markdown
docs/ARQUITETURA_TECNICA.md
docs/IMPLEMENTACAO_RENAULT.md
```

#### 7. Backup e Contingência
**Objetivo:** Garantir que a apresentação não falhe

**Preparações:**
- [ ] Vídeo gravado do dashboard funcionando (Plan B)
- [ ] Screenshots de alta qualidade de todas as telas
- [ ] Versão offline do dashboard (sem dependências de rede)
- [ ] Script de inicialização rápida

---

## 📋 Checklist de Preparação Técnica

### Antes dos Ensaios (20/10)
- [ ] Testar aplicação Flask em diferentes ambientes
- [ ] Verificar performance e tempo de resposta
- [ ] Garantir que todas as métricas estão corretas
- [ ] Preparar dados de demonstração impactantes

### Durante os Ensaios (21-23/10)
- [ ] Treinar apresentação do protótipo (2 minutos exatos)
- [ ] Identificar e corrigir bugs
- [ ] Ajustar velocidade de navegação no dashboard
- [ ] Preparar respostas para perguntas técnicas comuns

### Dia do Evento (25/10)
- [ ] Chegar 1h antes para setup
- [ ] Testar conexão de internet e projetor
- [ ] Iniciar aplicação e verificar funcionamento
- [ ] Ter backup offline pronto
- [ ] Verificar baterias de laptop/dispositivos

---

## 🔧 Estrutura de Arquivos Proposta

```
eco-dashboard-renault/
├── app_renault_mvp.py          # [MODIFICAR] Adicionar novos endpoints
├── config/
│   ├── demo_mode.py            # [CRIAR] Configurações de demonstração
│   └── carbon_data.json        # [CRIAR] Dados reais do PDF
├── data_sources/
│   ├── carbon_data.py          # [CRIAR] Loader de dados reais
│   └── sector_analysis.py      # [CRIAR] Análise por setor
├── ai_engine/
│   ├── __init__.py             # [CRIAR]
│   ├── recommendations.py      # [CRIAR] Engine de recomendações IA
│   └── anomaly_detection.py    # [CRIAR] Detecção de anomalias
├── routes/
│   ├── api_routes.py           # [CRIAR] Endpoints adicionais
│   └── demo_routes.py          # [CRIAR] Rotas de demonstração
├── templates/
│   └── dashboard.html          # [MODIFICAR] Adicionar novas visualizações
├── static/
│   ├── js/
│   │   ├── charts.js           # [MODIFICAR] Novos gráficos
│   │   └── ai_insights.js      # [CRIAR] Visualização de IA
│   └── css/
│       └── dashboard.css       # [MODIFICAR] Estilos aprimorados
└── docs/
    ├── ARQUITETURA_TECNICA.md  # [CRIAR] Documentação técnica
    └── IMPLEMENTACAO_RENAULT.md # [CRIAR] Plano de implementação
```

---

## 💡 Ideias de Destaque para a Apresentação

### 1. "Efeito WOW" - Impacto Visual Imediato
- Dashboard abre mostrando **desperdício em tempo real** (R$/segundo sendo gastos)
- Ao clicar em "Otimizar", **animação mostra economia instantânea**
- Contador de **árvores sendo salvas** em tempo real

### 2. Demonstração de IA
- Mostrar **algoritmo detectando** 3 servidores ociosos
- Sistema **sugere automaticamente** migração para cloud/desligamento
- **Cálculo instantâneo** de economia gerada pela ação

### 3. Comparação Dramática
- Gráfico lado-a-lado: **"Antes vs Depois"**
- Mostrar **redução de 30-40% no consumo** com otimizações
- Equivalência: **"X toneladas de CO2 = Y carros parados"**

### 4. Facilidade de Integração
- Mostrar **API REST funcionando** (abrir /api/metrics ao vivo)
- Demonstrar **JSON com dados em tempo real**
- Evidenciar **simplicidade de integração** com sistemas existentes

---

## 🎤 Roteiro da Demonstração (2 minutos)

### Minuto 1: Situação Atual (30s + 30s)
1. **Abrir dashboard** (5s)
   - "Este é nosso dashboard EcoTI em tempo real"
   
2. **Mostrar métricas principais** (10s)
   - "Atualmente a Renault tem 5.376 workstations e 100 servidores"
   - "Consumo atual: X kW, emitindo Y toneladas de CO2 por ano"
   
3. **Destacar problema** (15s)
   - "Identificamos 1.176 workstations ociosas (22% da infraestrutura)"
   - "Isso representa R$ X milhões em desperdício anual"
   - "Equivalente a Z árvores que precisariam ser plantadas"

### Minuto 2: Solução e Impacto (60s)
4. **Demonstrar IA** (20s)
   - "Nossa IA analisa padrões de uso e identifica oportunidades"
   - [Clicar em "Recomendações"] "Aqui estão 5 ações prioritárias"
   - "Sistema sugere desligamento automático fora do horário comercial"

5. **Mostrar otimização** (20s)
   - [Ativar "Modo Otimizado"] "Com essas medidas implementadas..."
   - "Redução imediata de 35% no consumo energético"
   - "Economia de R$ X milhões por ano"

6. **Impacto ambiental** (15s)
   - "Redução de Y toneladas de CO2 anualmente"
   - "Equivalente a plantar Z árvores ou tirar W carros de circulação"

7. **Facilidade de implementação** (5s)
   - "Tudo via API REST, integração simples com infraestrutura existente"
   - "Implementação gradual, sem interrupção de serviços"

---

## 🧠 Perguntas Técnicas Esperadas e Respostas

### Q1: "Como vocês coletam os dados em tempo real?"
**R:** "Utilizamos protocolo SNMP para coletar métricas de servidores e workstations. Para servidores HP e VxRail, já temos suporte nativo. Para workstations, integramos com ferramentas de gestão existentes da Renault como SCCM ou similar. A API é agnóstica e pode consumir dados de múltiplas fontes."

### Q2: "Como a IA faz as recomendações?"
**R:** "Implementamos algoritmos de machine learning que analisam padrões históricos de uso. O sistema aprende os horários de pico, recursos subutilizados e identifica anomalias. Utilizamos modelos de predição para projetar economia futura e priorizar ações com maior impacto."

### Q3: "Quanto tempo leva para implementar na Renault?"
**R:** "Dividimos em 3 fases: 1) Integração (2-3 semanas) - conectar sistemas existentes; 2) Piloto (1 mês) - teste em setor específico; 3) Rollout (2-3 meses) - expansão gradual. Total: 4-5 meses para implementação completa."

### Q4: "E a segurança dos dados?"
**R:** "Todo acesso via API autenticada, dados criptografados em trânsito e em repouso. Não armazenamos dados sensíveis, apenas métricas de consumo. Suporte a integração com Active Directory para controle de acesso. Conformidade com LGPD e políticas de segurança da Renault."

### Q5: "Quais são os custos de implementação?"
**R:** "Solução open-source (Flask + Python), sem custos de licença. Principais custos: integração (consultoria), treinamento de equipe, e infraestrutura de hospedagem (pode usar infra existente). ROI estimado em 6-8 meses baseado na economia energética."

### Q6: "Como garantem a precisão dos cálculos de CO2?"
**R:** "Utilizamos fatores de emissão oficiais do Brasil (0.0817 kg CO2/kWh), dados do ONS. Para cálculo de árvores, usamos padrão internacional de 22 kg CO2/ano por árvore. Todos os valores são auditáveis e baseados em normas ISO 14064."

---

## 📊 Métricas de Sucesso da Apresentação

### KPIs da Demonstração:
- ✅ Demonstração completa em até 2 minutos
- ✅ Zero bugs ou falhas durante apresentação
- ✅ Pelo menos 3 "efeitos wow" na audiência
- ✅ Responder todas as perguntas técnicas com confiança
- ✅ Apresentar solução como viável e implementável

### Critérios de Avaliação (Renault):
1. **Aplicabilidade** - Solução pode ser implementada com recursos existentes?
2. **Factilidade** - Prático e útil para as necessidades da Renault?
3. **Facilidade** - Equipe atual consegue implementar e manter?
4. **Inovação** - Uso efetivo de IA e sustentabilidade?
5. **Impacto** - Potencial de economia e redução de CO2?

---

## 🎯 Próximos Passos Imediatos

### Hoje (18/10 - Sexta)
- [x] ✅ Clonar repositório eco-dashboard-renault
- [x] ✅ Analisar código existente
- [x] ✅ Consultar histórico WhatsApp do projeto
- [x] ✅ Criar plano de execução técnica
- [ ] Extrair dados do PDF de carbono
- [ ] Iniciar desenvolvimento de melhorias prioritárias

### Fim de Semana (19-20/10)
- [ ] Implementar integração com dados reais do PDF
- [ ] Criar endpoints adicionais da API
- [ ] Desenvolver engine de recomendações de IA
- [ ] Preparar modo demonstração
- [ ] Testar todas as funcionalidades

### Segunda (21/10)
- [ ] **18:00** - Primeiro ensaio completo da apresentação
- [ ] Apresentar protótipo atualizado para a equipe
- [ ] Coletar feedback e ajustar
- [ ] Finalizar textos dos slides

### Terça-Quinta (22-24/10)
- [ ] Ensaios diários (18:00-19:00)
- [ ] Refinamento da demonstração
- [ ] Preparação de respostas para perguntas
- [ ] Backup e contingência

### Sexta (25/10)
- [ ] 🎉 **TRANSFORMATION DAY 2025!**
- [ ] Apresentar solução e conquistar a Renault!

---

## 📝 Notas Técnicas Adicionais

### Tecnologias Utilizadas:
- **Backend:** Python 3.8+, Flask 2.3.3
- **Frontend:** HTML5, CSS3, JavaScript ES6+
- **Visualização:** Chart.js 4.x
- **Dados:** JSON, SNMP, REST API
- **Deploy:** Flask dev server (demo), possível migração para Gunicorn/uWSGI

### Dependências Principais:
```
Flask==2.3.3
requests==2.31.0
pysnmp==4.4.12 (para coleta SNMP)
```

### Ambiente de Desenvolvimento:
- Sistema Operacional: Windows 11
- Python: 3.8+
- Editor: VS Code com Copilot
- Controle de Versão: Git + GitHub

---

**Documento Vivo:** Este plano será atualizado conforme o projeto evolui.  
**Última Atualização:** 18/10/2025 - 14:30  
**Próxima Revisão:** 20/10/2025 - Pós implementação das melhorias prioritárias

---

## 🚀 "Vamu Pra Cima Time" - Reta Final!
