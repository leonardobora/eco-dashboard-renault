# 🚀 Guia Rápido: Duas Versões do Dashboard

## 📋 Visão Geral

Este repositório contém **duas versões completas e funcionais** do EcoTI Dashboard:

### 1️⃣ **Versão Flask** (Backend Completo)
- ✅ Python + API REST
- ✅ Templates Jinja2 dinâmicos
- ✅ Ideal para desenvolvimento e produção

### 2️⃣ **Versão GitHub Pages** (Frontend Puro)
- ✅ HTML/CSS/JS puro
- ✅ Deploy gratuito
- ✅ Ideal para demonstrações e portfólio

---

## 🐍 Versão Flask - Guia Rápido

### Iniciar Localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python app_renault_mvp.py

# Acessar:
# Dashboard: http://localhost:5000
# Sobre: http://localhost:5000/sobre
# API: http://localhost:5000/api/metrics
```

### Arquivos Principais
- `app_renault_mvp.py` - Backend Flask
- `templates/dashboard.html` - Interface do dashboard
- `templates/sobre.html` - Página sobre o projeto

### Como Funciona
```
Cliente → Flask Server → Python calcula métricas → Templates Jinja2 → HTML
```

### Vantagens
- ✅ Cálculos server-side precisos
- ✅ API REST disponível
- ✅ Fácil integração com databases
- ✅ Autenticação possível

---

## 🌐 Versão GitHub Pages - Guia Rápido

### Testar Localmente

```bash
# Servir arquivos estáticos
python3 -m http.server 8080 --bind localhost

# Acessar:
# Dashboard: http://localhost:8080/index.html
# Sobre: http://localhost:8080/sobre.html
```

### Deploy no GitHub Pages

1. Vá em: **Settings** → **Pages**
2. Source: **main** branch
3. Folder: **/ (root)**
4. Clique em **Save**
5. Aguarde 2-5 minutos
6. Acesse: `https://leonardobora.github.io/eco-dashboard-renault/`

### Arquivos Principais
- `index.html` - Dashboard estático
- `sobre.html` - Página sobre estática
- `static/js/metrics-calculator.js` - Cálculos em JavaScript

### Como Funciona
```
Cliente → HTML estático → JavaScript calcula métricas → Renderização
```

### Vantagens
- ✅ Deploy 100% gratuito
- ✅ HTTPS automático
- ✅ CDN global do GitHub
- ✅ Sem servidor necessário

---

## 🔄 Como o Sistema Detecta Automaticamente?

O arquivo `static/js/app.js` é **inteligente** e detecta qual ambiente está rodando:

```javascript
async function fetchMetrics() {
  // Se metrics-calculator.js foi carregado (GitHub Pages)
  if (typeof window.RenaultInfrastructure !== 'undefined') {
    console.log('📊 Usando calculadora local (GitHub Pages)');
    const infra = new window.RenaultInfrastructure();
    return infra.getMetrics();
  }
  
  // Senão, usa API Flask
  console.log('✅ Usando API Flask');
  const response = await fetch('/api/metrics');
  return await response.json();
}
```

**Resultado:**
- No Flask: Usa `/api/metrics` (cálculos Python)
- No Pages: Usa `RenaultInfrastructure` (cálculos JavaScript)

---

## 📊 Comparação Rápida

| Característica | Flask | GitHub Pages |
|----------------|-------|--------------|
| **Backend** | ✅ Python | ❌ Não |
| **API REST** | ✅ `/api/metrics` | ❌ Não |
| **Cálculos** | 🐍 Python | 📜 JavaScript |
| **Templates** | Jinja2 | HTML puro |
| **Deploy** | Servidor | GitHub |
| **Custo** | R$ 720-2.300/ano | **R$ 0/ano** |
| **Setup** | 5 min | 2 min |
| **URLs** | `localhost:5000` | `github.io` |

---

## 📁 Estrutura de Arquivos

```
eco-dashboard-renault/
├── 🐍 FLASK VERSION
│   ├── app_renault_mvp.py
│   ├── templates/
│   │   ├── dashboard.html
│   │   └── sobre.html
│   └── requirements.txt
│
├── 🌐 GITHUB PAGES VERSION
│   ├── index.html
│   ├── sobre.html
│   └── static/js/metrics-calculator.js
│
└── 📦 COMPARTILHADO
    └── static/
        ├── css/style.css
        └── js/app.js (auto-detecta ambiente)
```

---

## 🎯 Quando Usar Cada Versão?

### Use **Flask** quando:
- 🔧 Desenvolvendo localmente
- 🏢 Fazendo deploy em servidor/cloud
- 🔌 Precisa integrar com bancos de dados
- 👥 Precisa de autenticação de usuários
- 📡 Vai consumir APIs externas

### Use **GitHub Pages** quando:
- 🎪 Fazendo apresentações
- 💼 Colocando no portfólio
- 🌐 Quer URL pública grátis
- 🚀 Precisa de deploy rápido
- 📱 Vai compartilhar em eventos

---

## ✅ Checklist de Validação

### Versão Flask ✓
- [x] `pip install -r requirements.txt` funciona
- [x] `python app_renault_mvp.py` inicia sem erros
- [x] `http://localhost:5000` exibe dashboard
- [x] `http://localhost:5000/api/metrics` retorna JSON
- [x] `http://localhost:5000/sobre` exibe página sobre

### Versão GitHub Pages ✓
- [x] `index.html` existe na raiz
- [x] `sobre.html` existe na raiz
- [x] Links entre páginas funcionam (`sobre.html`)
- [x] `metrics-calculator.js` incluído no HTML
- [x] Servidor estático serve todos os arquivos

---

## 📚 Documentação Adicional

- **Comparação Detalhada**: `docs/FLASK_VS_GITHUB_PAGES.md`
- **Implementação Pages**: `docs/GITHUB_PAGES_IMPLEMENTATION.md`
- **Guia Rápido Pages**: `docs/GITHUB_PAGES_QUICKSTART.md`
- **README Principal**: `README.md`

---

## 🆘 Troubleshooting

### Flask não inicia
```bash
# Verificar se porta 5000 está livre
lsof -i :5000
# Matar processo se necessário
kill -9 <PID>
```

### GitHub Pages não atualiza
- Aguarde 2-5 minutos após push
- Verifique: Settings → Pages → Status
- Force refresh: `Ctrl+Shift+R` (Chrome/Firefox)

### JavaScript não calcula métricas
- Verificar console do navegador (F12)
- Confirmar que `metrics-calculator.js` foi carregado
- Verificar mensagem: "Running in static mode"

---

**Desenvolvido por:** Equipe UniBrasil - EcoCode.AI  
**Evento:** Renault Transformation Day 2025  
**Licença:** MIT
