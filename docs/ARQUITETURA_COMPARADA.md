# 🏗️ Arquitetura: Flask vs GitHub Pages

## 📊 Visão Geral das Arquiteturas

### Arquitetura Atual (Flask)

```
┌─────────────────────────────────────────────────────────┐
│                    USUÁRIO                              │
│                  (Navegador Web)                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTP Request
                     ▼
┌─────────────────────────────────────────────────────────┐
│              SERVIDOR FLASK (Python)                    │
│  ┌────────────────────────────────────────────────┐    │
│  │  app_renault_mvp.py                            │    │
│  │  ├── Route: /                                  │    │
│  │  │   └── render_template('dashboard.html')    │    │
│  │  ├── Route: /sobre                             │    │
│  │  │   └── render_template('sobre.html')        │    │
│  │  └── Route: /api/metrics                       │    │
│  │      └── jsonify(métricas)                     │    │
│  └────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────┐    │
│  │  RenaultInfrastructure (Python)                │    │
│  │  ├── calcular_consumo_atual()                  │    │
│  │  ├── calcular_emissoes_anuais()                │    │
│  │  ├── calcular_economia_potencial()             │    │
│  │  └── calcular_arvores_equivalentes()           │    │
│  └────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────┐    │
│  │  Templates Jinja2                              │    │
│  │  ├── dashboard.html {{ url_for() }}            │    │
│  │  └── sobre.html {{ conteudo }}                 │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                     │
                     │ Renderizado
                     ▼
┌─────────────────────────────────────────────────────────┐
│              STATIC FILES                               │
│  ├── static/css/style.css                              │
│  └── static/js/app.js                                  │
│      └── fetch('/api/metrics')                         │
└─────────────────────────────────────────────────────────┘

CUSTO: R$ 720-2.300/ano
SETUP: 5-8 horas
MANUTENÇÃO: ~2-4 horas/mês
```

---

### Arquitetura Proposta (GitHub Pages)

```
┌─────────────────────────────────────────────────────────┐
│                    USUÁRIO                              │
│                  (Navegador Web)                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTPS Request
                     ▼
┌─────────────────────────────────────────────────────────┐
│            GITHUB PAGES (CDN Global)                    │
│  ┌────────────────────────────────────────────────┐    │
│  │  Arquivos Estáticos                            │    │
│  │  ├── index.html (HTML puro)                    │    │
│  │  ├── sobre.html (HTML puro)                    │    │
│  │  ├── static/css/style.css                      │    │
│  │  └── static/js/                                │    │
│  │      ├── app.js (modificado)                   │    │
│  │      └── metrics-calculator.js (novo)          │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                     │
                     │ Download para navegador
                     ▼
┌─────────────────────────────────────────────────────────┐
│          EXECUÇÃO NO NAVEGADOR (Client-Side)            │
│  ┌────────────────────────────────────────────────┐    │
│  │  metrics-calculator.js                         │    │
│  │  ┌──────────────────────────────────────────┐  │    │
│  │  │ RenaultInfrastructure (JavaScript)       │  │    │
│  │  │ ├── calcularConsumoAtual()               │  │    │
│  │  │ ├── calcularEmissoesAnuais()             │  │    │
│  │  │ ├── calcularEconomiaPotencial()          │  │    │
│  │  │ └── calcularArvoresEquivalentes()        │  │    │
│  │  └──────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────┐    │
│  │  app.js                                        │    │
│  │  └── const infra = new RenaultInfrastructure() │    │
│  │      const metrics = infra.getMetrics()        │    │
│  └────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────┐    │
│  │  Chart.js                                      │    │
│  │  └── Renderização de gráficos                  │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘

CUSTO: R$ 0/ano ✨
SETUP: 4-6 horas
MANUTENÇÃO: ~0 horas/mês
```

---

## 🔄 Fluxo de Dados Comparado

### Flask - Fluxo de Dados

```
1. Usuário acessa URL
   ↓
2. Flask recebe request
   ↓
3. Flask processa rota
   ↓
4. Flask renderiza template Jinja2
   ↓
5. Flask serve HTML gerado
   ↓
6. Navegador carrega HTML
   ↓
7. JavaScript faz fetch('/api/metrics')
   ↓
8. Flask calcula métricas (Python)
   ↓
9. Flask retorna JSON
   ↓
10. JavaScript atualiza interface
```

**Latência Total**: 50-200ms (depende do servidor)

---

### GitHub Pages - Fluxo de Dados

```
1. Usuário acessa URL
   ↓
2. CDN serve HTML estático
   ↓
3. Navegador carrega HTML
   ↓
4. JavaScript carrega
   ↓
5. JavaScript cria RenaultInfrastructure
   ↓
6. JavaScript calcula métricas localmente
   ↓
7. JavaScript atualiza interface
```

**Latência Total**: 20-50ms (CDN global)

---

## 🔧 Mudanças Necessárias

### 1. Templates HTML

#### ANTES (Flask/Jinja2):
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <title>{{ title or 'EcoTI Dashboard' }}</title>
    <link href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <a href="/sobre">Sobre</a>
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
```

#### DEPOIS (GitHub Pages/HTML):
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <title>EcoTI Dashboard - Renault Sustentabilidade Digital</title>
    <link href="static/css/style.css">
</head>
<body>
    <a href="sobre.html">Sobre</a>
    <script src="static/js/metrics-calculator.js"></script>
    <script src="static/js/app.js"></script>
</body>
</html>
```

---

### 2. JavaScript - Busca de Dados

#### ANTES (Flask - API):
```javascript
// app.js
async function fetchMetrics() {
  try {
    // Busca dados do servidor Flask
    const response = await fetch('/api/metrics');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching metrics:', error);
    return null;
  }
}
```

#### DEPOIS (GitHub Pages - Local):
```javascript
// app.js (modificado)
async function fetchMetrics() {
  try {
    // Calcula dados localmente
    const infra = new RenaultInfrastructure();
    const data = infra.getMetrics();
    return data;
  } catch (error) {
    console.error('Error calculating metrics:', error);
    return null;
  }
}
```

---

### 3. Lógica de Negócio

#### ANTES (Python Server-Side):
```python
# app_renault_mvp.py
class RenaultInfrastructure:
    def calcular_consumo_atual(self):
        hora_atual = datetime.datetime.now().hour
        if 8 <= hora_atual <= 18:
            fator_uso = 0.8
        # ... resto do código
        return consumo_workstations + consumo_servidores
```

#### DEPOIS (JavaScript Client-Side):
```javascript
// metrics-calculator.js
class RenaultInfrastructure {
    calcularConsumoAtual() {
        const hora_atual = new Date().getHours();
        let fator_uso;
        if (hora_atual >= 8 && hora_atual <= 18) {
            fator_uso = 0.8;
        }
        // ... resto do código
        return consumo_workstations + consumo_servidores;
    }
}
```

---

## 📁 Estrutura de Arquivos Comparada

### Flask (Atual)
```
eco-dashboard-renault/
├── app_renault_mvp.py       ← Servidor Flask
├── templates/               ← Templates Jinja2
│   ├── dashboard.html       ← Usa {{ }}
│   └── sobre.html           ← Usa {{ }}
├── static/
│   ├── css/style.css
│   └── js/app.js            ← fetch('/api/metrics')
├── requirements.txt         ← Dependências Python
└── README.md
```

### GitHub Pages (Proposto)
```
eco-dashboard-renault/
├── app_renault_mvp.py       ← Mantido para dev local
├── templates/               ← Mantido para dev local
├── index.html               ← NOVO: HTML puro
├── sobre.html               ← NOVO: HTML puro
├── static/
│   ├── css/style.css        ← Sem mudanças
│   └── js/
│       ├── app.js           ← Modificado
│       └── metrics-calculator.js  ← NOVO
└── README.md
```

---

## 🎯 Casos de Uso

### Use Flask Quando:
```
┌─────────────────────────────────────┐
│  PRODUÇÃO COM DADOS REAIS           │
│  ├── Integração SNMP                │
│  ├── Banco de dados histórico       │
│  ├── Autenticação de usuários       │
│  ├── APIs externas                  │
│  └── Processamento complexo         │
└─────────────────────────────────────┘
```

### Use GitHub Pages Quando:
```
┌─────────────────────────────────────┐
│  DEMONSTRAÇÃO PÚBLICA               │
│  ├── Transformation Day 2025        │
│  ├── Portfolio acadêmico            │
│  ├── Validação de UI/UX             │
│  ├── MVP rápido                     │
│  └── Sem orçamento para hosting     │
└─────────────────────────────────────┘
```

---

## 💡 Estratégia Híbrida Recomendada

```
┌──────────────────────────────────────────────────────────┐
│                    DESENVOLVIMENTO                       │
│  ┌────────────────────────────────────────────────┐     │
│  │  Versão Flask (Local)                          │     │
│  │  ├── python app_renault_mvp.py                 │     │
│  │  ├── http://localhost:5000                     │     │
│  │  ├── Testes com dados reais                    │     │
│  │  └── Preparação para produção                  │     │
│  └────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────┘
                          ↓
                    git push
                          ↓
┌──────────────────────────────────────────────────────────┐
│                    DEMONSTRAÇÃO                          │
│  ┌────────────────────────────────────────────────┐     │
│  │  Versão GitHub Pages (Pública)                 │     │
│  │  ├── index.html + sobre.html                   │     │
│  │  ├── https://leonardobora.github.io/...        │     │
│  │  ├── Apresentações e demos                     │     │
│  │  └── R$ 0/ano                                  │     │
│  └────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────┘
                          ↓
                 (Quando necessário)
                          ↓
┌──────────────────────────────────────────────────────────┐
│                      PRODUÇÃO                            │
│  ┌────────────────────────────────────────────────┐     │
│  │  Versão Flask (Servidor)                       │     │
│  │  ├── Heroku/AWS/Azure                          │     │
│  │  ├── Dados reais + SNMP                        │     │
│  │  ├── Banco de dados                            │     │
│  │  └── Autenticação                              │     │
│  └────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────┘
```

---

## 📊 Matriz de Decisão

| Critério | Peso | Flask | GitHub Pages | Vencedor |
|----------|------|-------|--------------|----------|
| Custo | 🔥🔥🔥 | 2/10 | 10/10 | **GitHub Pages** |
| Setup rápido | 🔥🔥 | 5/10 | 10/10 | **GitHub Pages** |
| Performance | 🔥 | 7/10 | 9/10 | **GitHub Pages** |
| Escalabilidade | 🔥 | 6/10 | 10/10 | **GitHub Pages** |
| Dados dinâmicos | 🔥🔥🔥 | 10/10 | 0/10 | **Flask** |
| Integrações | 🔥🔥 | 10/10 | 2/10 | **Flask** |
| Autenticação | 🔥 | 10/10 | 2/10 | **Flask** |
| Manutenção | 🔥🔥 | 4/10 | 10/10 | **GitHub Pages** |

**Para Demo/MVP**: GitHub Pages ganha 4-1  
**Para Produção Futura**: Flask ganha 3-2

---

## ✅ Conclusão Visual

```
┌────────────────────────────────────────────────┐
│  AGORA (2024-2025)                             │
│  ┌──────────────────────────────────────┐     │
│  │  ✅ GitHub Pages                     │     │
│  │     • Deploy imediato                │     │
│  │     • R$ 0/ano                       │     │
│  │     • URL pública                    │     │
│  │     • HTTPS automático               │     │
│  └──────────────────────────────────────┘     │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│  FUTURO (2025+)                                │
│  ┌──────────────────────────────────────┐     │
│  │  ✅ Flask em Produção                │     │
│  │     • Dados reais Renault            │     │
│  │     • Integrações SNMP               │     │
│  │     • Autenticação                   │     │
│  │     • Banco de dados                 │     │
│  └──────────────────────────────────────┘     │
└────────────────────────────────────────────────┘
```

---

**Preparado por**: Análise de Arquitetura  
**Data**: Dezembro 2024  
**Versão**: 1.0  
**Status**: ✅ Documentação Completa
