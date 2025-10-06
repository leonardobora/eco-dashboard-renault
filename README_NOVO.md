# 🌱 EcoCode.AI - Dashboard de Sustentabilidade Digital

[![CI/CD Pipeline](https://github.com/leonardobora/eco-dashboard-renault/actions/workflows/ci.yml/badge.svg)](https://github.com/leonardobora/eco-dashboard-renault/actions/workflows/ci.yml)
[![Security Analysis](https://github.com/leonardobora/eco-dashboard-renault/actions/workflows/security.yml/badge.svg)](https://github.com/leonardobora/eco-dashboard-renault/actions/workflows/security.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![UniBrasil](https://img.shields.io/badge/universidade-UniBrasil-yellow.svg)](https://unibrasil.edu.br/)
[![Transformation Day 2025](https://img.shields.io/badge/evento-Transformation%20Day%202025-orange.svg)](https://www.renault.com.br/)

> **Solução inovadora de inteligência artificial para sustentabilidade digital desenvolvida pela equipe UniBrasil para o Transformation Day 2025 da Renault.**

## 🎯 Sobre o Projeto

O **EcoCode.AI** é uma solução de IA que une automação inteligente com responsabilidade ambiental, promovendo TI verde, eficiente e autônoma. Desenvolvido especificamente para o desafio IS/IT do Transformation Day 2025 da Renault.

### 🔍 Desafio Proposto
**Sustentabilidade Digital**: Desenvolver uma solução de IA para rastrear e reduzir a pegada de carbono da infraestrutura de TI e otimizar a utilização de recursos.

### 🏆 Competição
- **Evento**: Transformation Day 2025
- **Data**: 24 de outubro de 2025
- **Local**: Fábrica Renault, São José dos Pinhais, PR
- **Categoria**: IS/IT (Information Systems/Information Technology)
- **Competidor**: Unicesumar vs **UniBrasil**
- **Formato**: 10 minutos, máximo 5 slides

---

## 🚀 Funcionalidades Principais

### 📊 1. Rastreamento em Tempo Real
- Monitora a pegada de carbono da infraestrutura de TI
- Correlação entre consumo, tipos de energia e emissões por workload
- Dashboard executivo com métricas em tempo real

### 💡 2. Recomendações Inteligentes
- Sugestões de ações sustentáveis baseadas em IA
- Migração para regiões com energia mais limpa
- Otimização de horários de menor impacto energético
- Substituição por recursos mais eficientes

### ⚡ 3. Detecção Automática
- Identificação de recursos ociosos ou subutilizados
- Desativação automática baseada em padrões de uso
- Políticas de negócio configuráveis
- Alertas proativos de desperdício

### 📈 4. Dashboards Executivos
- Visibilidade completa do impacto ambiental
- Relatórios de sustentabilidade corporativa
- KPIs de eficiência energética
- Alertas para tomada de decisão

---

## 🎓 Equipe UniBrasil

### 👨‍🏫 Mentores Especialistas
- **Prof. Mozart Hasse** - Engenharia de Software
- **Prof. Orlei Pombeiro** - Engenharia de Software  
- **Prof. Renan Zunta Raia** - Engenharia Ambiental
- **Prof. Wilson Parisotto** - Engenharia de Produção
- **Prof. Lauro Katsumi** - Engenharia Elétrica

### 👥 Estudantes Desenvolvedores
- **Leonardo Bora** - Tech Lead e DevOps (Eng. Software) [@leonardobora](https://github.com/leonardobora)
- **Daniel Nhemihes** - Backend Developer (Eng. Software)
- **Gabriel Barvik** - Sistemas Energéticos (Eng. Elétrica)
- **Sthefany Santos** - Frontend & UX (Eng. Software)
- **Kamille Gasparin** - Processos & Otimização (Eng. Produção)
- **Meridiana** - Especialista Sustentabilidade (Eng. Ambiental)
- **Suelen** - Analista Impacto Ambiental (Eng. Ambiental)

---

## 🏗️ Arquitetura Técnica

### Stack Principal
```
Frontend:    HTML5 + CSS3 + JavaScript + Chart.js
Backend:     Python Flask 2.3.3
Database:    Simulação em memória (dados Renault)
Deploy:      Docker + GitHub Actions
Monitoring:  Prometheus-ready
```

### Estrutura do Projeto
```
eco-dashboard-renault/
├── app_renault_mvp.py          # Aplicação Flask principal
├── templates/
│   ├── dashboard.html          # Interface principal
│   └── sobre.html             # Página sobre o projeto
├── static/
│   ├── css/style.css          # Estilos personalizados
│   └── js/app.js              # JavaScript interativo
├── .github/
│   ├── workflows/             # CI/CD automatizado
│   └── ISSUE_TEMPLATE/        # Templates profissionais
├── docs/                      # Documentação completa
└── tests/                     # Testes automatizados
```

### Infraestrutura Monitorada
- **5.376 Workstations** - Estações de trabalho Renault
- **90 Servidores HP** - Infraestrutura corporativa
- **10 Sistemas VxRail** - Virtualização e containers
- **Consumo médio**: 250W por workstation
- **Tarifa energia**: R$ 0,60/kWh

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+ instalado
- Git para clonar o repositório

### Instalação e Execução
```bash
# 1. Clone o repositório
git clone https://github.com/leonardobora/eco-dashboard-renault.git
cd eco-dashboard-renault

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute a aplicação
python app_renault_mvp.py

# 4. Acesse no navegador
# Dashboard: http://localhost:5000
# Sobre: http://localhost:5000/sobre
# API: http://localhost:5000/api/metrics
```

### Teste da API
```bash
# Teste do endpoint de métricas
curl -s http://localhost:5000/api/metrics | python -m json.tool
```

---

## 📊 Métricas de Sustentabilidade

### Cálculos Implementados
- **Consumo Atual**: Baseado em horário e utilização real
- **Emissões CO₂**: 0.0817 kg CO₂/kWh (fator Brasil)
- **Sequestro de Carbono**: 22 kg CO₂/ano por árvore
- **Economia Potencial**: Análise de workstations ociosas

### Exemplo de Resposta da API
```json
{
  "consumo_atual": 874.0,
  "emissoes_co2": 625514.808,
  "economia_potencial": 352800.0,
  "arvores_equivalentes": 28432
}
```

---

## 🌱 Compromisso com Sustentabilidade

### Alinhamento com ODS da ONU
- **ODS 7**: Energia Limpa e Acessível
- **ODS 9**: Indústria, Inovação e Infraestrutura  
- **ODS 12**: Consumo e Produção Responsáveis
- **ODS 13**: Ação contra a Mudança Global do Clima

### Impacto Esperado
- **Redução**: 20-30% no consumo energético de TI
- **Economia**: R$ 350.000+ anuais potenciais
- **Carbono**: Equivalente a plantar 28.000+ árvores
- **Automação**: 95% de recursos ociosos detectados automaticamente

---

## 🔧 DevOps e CI/CD

### Pipelines Automatizados
- ✅ **Testes**: Unitários e integração (18 combinações Python/OS)
- ✅ **Segurança**: CodeQL, Bandit, Safety, TruffleHog
- ✅ **Qualidade**: Code review obrigatório
- ✅ **Deploy**: Containerização com Docker
- ✅ **Monitoramento**: Métricas de performance

### Badges de Status
[![Tests](https://img.shields.io/badge/tests-18%2F18%20passing-brightgreen.svg)](https://github.com/leonardobora/eco-dashboard-renault/actions)
[![Security](https://img.shields.io/badge/security-100%25%20clean-brightgreen.svg)](https://github.com/leonardobora/eco-dashboard-renault/actions)
[![Code Quality](https://img.shields.io/badge/code%20quality-A+-brightgreen.svg)](https://github.com/leonardobora/eco-dashboard-renault)

---

## 🏅 Histórico UniBrasil

### Transformation Day Success
- **2024**: 🥇 1º lugar categoria "Case de Compras" + 🥉 3º lugar geral
- **2023**: Participação destacada entre 12 universidades selecionadas
- **Reconhecimento**: Equipes multidisciplinares consistentemente premiadas

---

## 📝 Documentação

### Recursos Disponíveis
- 📋 [Status Funcional](STATUS_FUNCIONAL.md) - Estado atual do projeto
- 👥 [Equipe Completa](EQUIPE.md) - Informações da equipe (versão anterior)
- 🔍 [Sobre o Projeto](SOBRE.md) - Detalhes completos do EcoCode.AI
- 📊 [Implementação](IMPLEMENTATION_SUMMARY.md) - Resumo técnico
- 🧪 [Relatório de Testes](TEST_REPORT.md) - Cobertura e validação

### 🌐 GitHub Pages - Hospedagem Estática
- 📖 [Análise de Viabilidade](docs/GITHUB_PAGES_FEASIBILITY.md) - Avaliação técnica completa
- 🚀 [Guia de Implementação](docs/GITHUB_PAGES_IMPLEMENTATION.md) - Passo a passo detalhado
- ⚡ [Guia Rápido](docs/GITHUB_PAGES_QUICKSTART.md) - Deploy em 5 passos
- 📊 [Flask vs GitHub Pages](docs/FLASK_VS_GITHUB_PAGES.md) - Comparação e recomendações

### APIs e Endpoints
- `GET /` - Dashboard principal
- `GET /sobre` - Página sobre o projeto e equipe
- `GET /api/metrics` - Métricas de sustentabilidade em JSON

---

## 🤝 Contribuição

### Para a Equipe UniBrasil
1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Code Review Obrigatório
- ✅ CI/CD deve passar em todos os testes
- ✅ Código deve seguir padrões estabelecidos
- ✅ Documentação deve ser atualizada
- ✅ Impacto de sustentabilidade deve ser considerado

---

## 📞 Contato

### Equipe de Desenvolvimento
- **Email**: equipe.ecocode@unibrasil.edu.br
- **LinkedIn**: [UniBrasil EcoCode.AI Team](https://linkedin.com/company/unibrasil-ecocode)
- **Universidade**: [Centro Universitário UniBrasil](https://unibrasil.edu.br/)

### Links Importantes
- **Dashboard Live**: http://localhost:5000 (após executar localmente)
- **Documentação**: [GitHub Pages](https://leonardobora.github.io/eco-dashboard-renault/)
- **Issues**: [GitHub Issues](https://github.com/leonardobora/eco-dashboard-renault/issues)
- **Releases**: [GitHub Releases](https://github.com/leonardobora/eco-dashboard-renault/releases)

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos como parte do Transformation Day 2025 da Renault. 

**Direitos Autorais**: © 2025 UniBrasil - EcoCode.AI Team

---

## 🎯 Objetivo Final

> **"Unir automação inteligente com responsabilidade ambiental, promovendo TI verde, eficiente e autônoma."**

---

*Última atualização: 22 de setembro de 2025*

*Este projeto representa a dedicação da equipe UniBrasil em criar soluções tecnológicas que não apenas atendem às necessidades empresariais, mas também contribuem para um futuro mais sustentável.* 🌱