# ⚙️ Como Configurar GitHub Pages

## 📋 Passo a Passo Completo

### 1️⃣ Pré-requisitos

Antes de começar, certifique-se de que:
- ✅ Você tem acesso ao repositório no GitHub
- ✅ Os arquivos `index.html` e `sobre.html` estão na raiz do repositório
- ✅ A pasta `static/` contém todos os assets (CSS, JS)

### 2️⃣ Configuração no GitHub

#### Opção A: Via Interface Web

1. Acesse seu repositório: `https://github.com/leonardobora/eco-dashboard-renault`

2. Clique em **Settings** (Configurações)

3. No menu lateral, clique em **Pages**

4. Em **Source** (Origem):
   - Branch: Selecione **main** (ou master)
   - Folder: Selecione **/ (root)**

5. Clique em **Save**

6. Aguarde 2-5 minutos para o build completar

7. A URL será exibida: `https://leonardobora.github.io/eco-dashboard-renault/`

#### Opção B: Via Arquivo de Configuração

Crie `.github/workflows/static.yml`:

```yaml
name: Deploy static content to Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v5
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 3️⃣ Verificação

Após o deploy, verifique:

```bash
# Teste a URL principal
curl -I https://leonardobora.github.io/eco-dashboard-renault/

# Teste index.html
curl -I https://leonardobora.github.io/eco-dashboard-renault/index.html

# Teste sobre.html
curl -I https://leonardobora.github.io/eco-dashboard-renault/sobre.html
```

Todos devem retornar `HTTP/2 200`

### 4️⃣ Teste no Navegador

Abra no navegador:
- Dashboard: `https://leonardobora.github.io/eco-dashboard-renault/`
- Sobre: `https://leonardobora.github.io/eco-dashboard-renault/sobre.html`

**Verifique:**
- ✅ Dashboard carrega completamente
- ✅ Métricas são calculadas (não aparecem "Loading...")
- ✅ Gráficos Chart.js renderizam
- ✅ Navegação entre páginas funciona
- ✅ Console do navegador mostra: "Running in static mode"

### 5️⃣ Validação das Métricas

Abra o Console do Navegador (F12) e execute:

```javascript
// Deve mostrar a mensagem de modo estático
// "🌐 Running in static mode (GitHub Pages)"

// Verificar se calculadora foi carregada
console.log(typeof window.RenaultInfrastructure);
// Deve retornar: "function"

// Testar cálculo manual
const infra = new window.RenaultInfrastructure();
const metrics = infra.getMetrics();
console.log(metrics);
// Deve retornar objeto com métricas
```

---

## 🔧 Troubleshooting

### Problema: Página 404

**Causa:** GitHub Pages ainda não foi ativado ou build não completou

**Solução:**
1. Verifique Settings → Pages → Status
2. Aguarde 2-5 minutos após ativar
3. Force rebuild fazendo novo commit/push

### Problema: CSS/JS não carrega

**Causa:** Caminhos relativos incorretos

**Solução:**
Verifique que os links no HTML são:
```html
<link href="static/css/style.css">
<script src="static/js/app.js"></script>
```

E NÃO:
```html
<link href="/static/css/style.css">  ❌ Barra inicial
<script src="/static/js/app.js"></script>  ❌ Barra inicial
```

### Problema: Métricas não calculam

**Causa:** `metrics-calculator.js` não foi carregado

**Solução:**
1. Verifique que `index.html` inclui:
```html
<script src="static/js/metrics-calculator.js"></script>
<script src="static/js/app.js"></script>
```

2. A ordem importa! `metrics-calculator.js` deve vir ANTES de `app.js`

### Problema: Navegação entre páginas quebra

**Causa:** Links usando rotas Flask (`/sobre`)

**Solução:**
Use URLs relativas:
```html
<a href="sobre.html">Sobre</a>  ✅
```

Não use:
```html
<a href="/sobre">Sobre</a>  ❌
```

---

## 📱 URLs Importantes

### Repositório
- Código: `https://github.com/leonardobora/eco-dashboard-renault`
- Issues: `https://github.com/leonardobora/eco-dashboard-renault/issues`
- PRs: `https://github.com/leonardobora/eco-dashboard-renault/pulls`

### GitHub Pages
- Dashboard: `https://leonardobora.github.io/eco-dashboard-renault/`
- Sobre: `https://leonardobora.github.io/eco-dashboard-renault/sobre.html`

### Configuração
- Settings: `https://github.com/leonardobora/eco-dashboard-renault/settings`
- Pages: `https://github.com/leonardobora/eco-dashboard-renault/settings/pages`
- Actions: `https://github.com/leonardobora/eco-dashboard-renault/actions`

---

## 🚀 Deploy Automático

### Toda vez que você fizer push para `main`:

1. GitHub detecta mudanças
2. Inicia build automático
3. Deploy em ~2-5 minutos
4. Site atualizado automaticamente

### Para verificar status do deploy:

1. Vá em **Actions** no GitHub
2. Veja o workflow "pages build and deployment"
3. Verde ✅ = Deploy bem-sucedido
4. Vermelho ❌ = Erro no build

---

## 📊 Estrutura de URLs

```
https://leonardobora.github.io/eco-dashboard-renault/
├── index.html                           (Dashboard principal)
├── sobre.html                           (Sobre o projeto)
└── static/
    ├── css/
    │   └── style.css                    (Estilos)
    └── js/
        ├── app.js                       (Lógica da aplicação)
        └── metrics-calculator.js        (Cálculos de métricas)
```

---

## ✅ Checklist de Deploy

- [ ] Arquivos `index.html` e `sobre.html` na raiz
- [ ] Pasta `static/` completa com CSS e JS
- [ ] GitHub Pages ativado em Settings
- [ ] Branch `main` selecionado como source
- [ ] Folder `/ (root)` selecionado
- [ ] Build completado (verificar Actions)
- [ ] URL funcionando no navegador
- [ ] Métricas calculando corretamente
- [ ] Console mostra "Running in static mode"
- [ ] Navegação entre páginas funciona

---

## 🎉 Pronto!

Seu dashboard está agora hospedado gratuitamente no GitHub Pages!

**Compartilhe a URL:**
`https://leonardobora.github.io/eco-dashboard-renault/`

**Características:**
- ✅ HTTPS gratuito
- ✅ CDN global do GitHub
- ✅ Deploy automático
- ✅ Sem custo de hospedagem
- ✅ URL profissional

---

**Desenvolvido por:** Equipe UniBrasil - EcoCode.AI  
**Evento:** Renault Transformation Day 2025
