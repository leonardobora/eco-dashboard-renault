# 🚀 Guia de Implementação: GitHub Pages

## 📋 Visão Geral

Este guia detalha o processo completo para hospedar o EcoTI Dashboard no GitHub Pages, criando uma versão estática funcional ao lado da versão Flask existente.

---

## 🎯 Estratégia: Duas Versões Simultâneas

```
eco-dashboard-renault/
├── app_renault_mvp.py          # ✅ Versão Flask (mantida)
├── templates/                   # ✅ Templates Flask (mantidos)
├── static/                      # ✅ Assets compartilhados
├── docs/                        # 📚 Documentação
│   └── index.html              # 🆕 GitHub Pages (opção docs/)
├── index.html                   # 🆕 GitHub Pages (opção raiz)
└── sobre.html                   # 🆕 Página sobre estática
```

---

## 🔧 Opções de Configuração

### Opção 1: Publicar da Raiz (Recomendado)
**Vantagens**: URL mais limpa, estrutura simples  
**Desvantagens**: Arquivos HTML na raiz do repo

### Opção 2: Publicar da Pasta /docs
**Vantagens**: Organização, separa código de publicação  
**Desvantagens**: URL com /docs/ no caminho

### Opção 3: Branch gh-pages Separada
**Vantagens**: Total separação, build automático  
**Desvantagens**: Mais complexo, requer GitHub Actions

---

## 📝 Implementação Passo a Passo

### Passo 1: Converter Templates para HTML Estático

#### 1.1 Criar index.html

```bash
# Converter dashboard.html para index.html
# Substituir {{ url_for('static', filename='css/style.css') }}
# Por: static/css/style.css
```

**Mudanças Necessárias:**
```html
<!-- ANTES (Jinja2) -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/app.js') }}"></script>

<!-- DEPOIS (HTML Estático) -->
<link rel="stylesheet" href="static/css/style.css">
<script src="static/js/app.js"></script>
```

#### 1.2 Criar sobre.html

**Opção A: HTML Inline**
```html
<!-- Copiar conteúdo de SOBRE.md e converter para HTML -->
<div class="sobre-content">
    <h1>🌱 EcoCode.AI - Projeto de Sustentabilidade Digital</h1>
    <!-- Resto do conteúdo -->
</div>
```

**Opção B: Renderização Dinâmica com marked.js**
```html
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script>
    fetch('SOBRE.md')
        .then(response => response.text())
        .then(text => {
            document.getElementById('content').innerHTML = marked.parse(text);
        });
</script>
```

### Passo 2: Implementar Calculadora de Métricas em JavaScript

#### 2.1 Criar static/js/metrics-calculator.js

```javascript
/**
 * EcoTI Metrics Calculator - Versão Estática
 * Porta a lógica Python da classe RenaultInfrastructure para JavaScript
 */

class RenaultInfrastructure {
    constructor() {
        this.workstations = 5376;
        this.servidores_hp = 90;
        this.vxrail = 10;
        this.consumo_medio_w = 250;
        this.fator_emissao = 0.0817; // kg CO2/kWh Brasil
        this.sequestro_arvore = 22; // kg CO2/ano por árvore
        this.tarifa_energia = 0.60; // R$/kWh
        
        this.workstations_ativas = 4200;
        this.servidores_ativos = 85;
        this.consumo_atual = this.calcularConsumoAtual();
    }
    
    calcularConsumoAtual() {
        const hora_atual = new Date().getHours();
        let fator_uso;
        
        if (hora_atual >= 8 && hora_atual <= 18) {
            fator_uso = 0.8; // Horário comercial
        } else if (hora_atual >= 19 && hora_atual <= 22) {
            fator_uso = 0.4; // Horário reduzido
        } else {
            fator_uso = 0.2; // Madrugada
        }
        
        const consumo_workstations = 
            (this.workstations_ativas * this.consumo_medio_w * fator_uso) / 1000;
        const consumo_servidores = this.servidores_ativos * 400 / 1000;
        
        return consumo_workstations + consumo_servidores;
    }
    
    calcularEmissoesAnuais() {
        const consumo_anual = this.consumo_atual * 24 * 365;
        return consumo_anual * this.fator_emissao;
    }
    
    calcularArvoresEquivalentes() {
        const emissoes = this.calcularEmissoesAnuais();
        return Math.floor(emissoes / this.sequestro_arvore);
    }
    
    calcularEconomiaPotencial() {
        const workstations_ociosas = this.workstations - this.workstations_ativas;
        const economia_kwh = 
            (workstations_ociosas * this.consumo_medio_w * 8 * 250) / 1000;
        return economia_kwh * this.tarifa_energia;
    }
    
    getMetrics() {
        this.consumo_atual = this.calcularConsumoAtual();
        return {
            consumo_atual: this.consumo_atual,
            emissoes_co2: this.calcularEmissoesAnuais(),
            economia_potencial: this.calcularEconomiaPotencial(),
            arvores_equivalentes: this.calcularArvoresEquivalentes()
        };
    }
}

// Exportar para uso global
window.RenaultInfrastructure = RenaultInfrastructure;
```

#### 2.2 Modificar static/js/app.js

```javascript
// ANTES (Versão Flask)
async function fetchMetrics() {
  try {
    const response = await fetch('/api/metrics');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching metrics:', error);
    return null;
  }
}

// DEPOIS (Versão Estática)
async function fetchMetrics() {
  try {
    // Usar calculadora local em vez de API
    const infra = new RenaultInfrastructure();
    const data = infra.getMetrics();
    return data;
  } catch (error) {
    console.error('Error calculating metrics:', error);
    return null;
  }
}
```

### Passo 3: Ajustar Navegação

#### 3.1 Atualizar Links

```html
<!-- ANTES -->
<a href="/sobre" class="header-link">Sobre o Projeto</a>

<!-- DEPOIS -->
<a href="sobre.html" class="header-link">Sobre o Projeto</a>
```

#### 3.2 Adicionar Navegação de Volta

```html
<!-- Em sobre.html -->
<a href="index.html" class="back-link">
    ← Voltar para Dashboard
</a>
```

### Passo 4: Configurar GitHub Pages

#### 4.1 Via Interface do GitHub

1. Acesse: `Settings` → `Pages`
2. Em **Source**: Selecione `main` branch
3. Em **Folder**: Escolha `/ (root)` ou `/docs`
4. Clique em **Save**
5. Aguarde build (1-2 minutos)
6. Acesse: `https://leonardobora.github.io/eco-dashboard-renault/`

#### 4.2 Via Arquivo de Configuração (Opcional)

Criar `_config.yml`:
```yaml
title: EcoTI Dashboard - Renault Sustentabilidade Digital
description: Dashboard de monitoramento de sustentabilidade em TI
theme: jekyll-theme-minimal
baseurl: "/eco-dashboard-renault"
url: "https://leonardobora.github.io"
```

### Passo 5: Testar Localmente

#### 5.1 Servidor Python Simples

```bash
# Teste da raiz
python3 -m http.server 8080
# Acesse: http://localhost:8080/index.html

# Teste da pasta docs/
cd docs
python3 -m http.server 8080
# Acesse: http://localhost:8080/index.html
```

#### 5.2 Live Server (VSCode)

```bash
# Instalar extensão Live Server no VSCode
# Clicar com botão direito em index.html
# Selecionar "Open with Live Server"
```

#### 5.3 Checklist de Testes

- [ ] index.html carrega corretamente
- [ ] CSS aplicado (cores Renault, layout)
- [ ] JavaScript funcionando (métricas, gráficos)
- [ ] Navegação sobre.html funciona
- [ ] Métricas calculadas corretamente
- [ ] Charts.js renderizando gráficos
- [ ] Responsivo em mobile/desktop
- [ ] Sem erros no console do navegador

---

## 🔄 Workflow de Atualização

### Desenvolvimento Local
```bash
# 1. Trabalhar na versão Flask
python app_renault_mvp.py

# 2. Testar mudanças
# http://localhost:5000

# 3. Converter para estático (se necessário)
# Atualizar index.html, sobre.html

# 4. Testar versão estática
python3 -m http.server 8080

# 5. Commit e push
git add .
git commit -m "Update: descrição da mudança"
git push origin main
```

### Deploy Automático
GitHub Pages rebuilda automaticamente após push para `main`.

---

## 🎨 Customizações Adicionais

### Favicon e Meta Tags

```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Dashboard de Sustentabilidade Digital Renault">
    <meta name="keywords" content="sustentabilidade, TI, Renault, energia, CO2">
    <meta name="author" content="Equipe UniBrasil EcoCode.AI">
    
    <!-- Open Graph para compartilhamento -->
    <meta property="og:title" content="EcoTI Dashboard - Renault">
    <meta property="og:description" content="Monitoramento de Sustentabilidade em TI">
    <meta property="og:image" content="static/images/og-image.png">
    <meta property="og:url" content="https://leonardobora.github.io/eco-dashboard-renault/">
    
    <!-- Favicon -->
    <link rel="icon" type="image/png" href="static/images/favicon.png">
    
    <title>EcoTI Dashboard - Renault Sustentabilidade Digital</title>
</head>
```

### Google Analytics (Opcional)

```html
<!-- No final do <head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX');
</script>
```

### PWA - Progressive Web App (Opcional)

Criar `manifest.json`:
```json
{
    "name": "EcoTI Dashboard",
    "short_name": "EcoTI",
    "description": "Dashboard de Sustentabilidade Digital Renault",
    "start_url": "/eco-dashboard-renault/",
    "display": "standalone",
    "background_color": "#FFCB00",
    "theme_color": "#FFCB00",
    "icons": [
        {
            "src": "static/images/icon-192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "static/images/icon-512.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
}
```

---

## 🐛 Troubleshooting

### Problema: CSS/JS não carrega

**Causa**: Caminhos incorretos  
**Solução**: 
```html
<!-- Se na raiz -->
<link href="static/css/style.css">

<!-- Se em /docs/ -->
<link href="../static/css/style.css">
```

### Problema: GitHub Pages não atualiza

**Causa**: Cache ou build em andamento  
**Solução**:
1. Aguardar 5-10 minutos
2. Limpar cache do navegador (Ctrl+Shift+R)
3. Verificar Actions tab no GitHub

### Problema: Fetch API bloqueada (CORS)

**Causa**: Tentativa de carregar arquivos locais via fetch  
**Solução**: Sempre testar com servidor HTTP, nunca `file://`

### Problema: Métricas não atualizam

**Causa**: JavaScript não carregou calculadora  
**Solução**: 
1. Verificar console de erros
2. Incluir metrics-calculator.js antes de app.js
3. Verificar instanciação de RenaultInfrastructure

---

## 📊 Monitoramento

### GitHub Pages Insights
- Acesse: `Insights` → `Traffic`
- Visualize visitantes e páginas populares

### Performance
```bash
# Lighthouse audit
npm install -g lighthouse
lighthouse https://leonardobora.github.io/eco-dashboard-renault/ --view
```

---

## 🔒 Segurança

### HTTPS Automático
✅ GitHub Pages fornece HTTPS automático

### Content Security Policy (Opcional)
```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' https://cdn.jsdelivr.net;
               style-src 'self' 'unsafe-inline';">
```

---

## 📚 Recursos Úteis

### Documentação Oficial
- [GitHub Pages Docs](https://docs.github.com/pages)
- [Jekyll Themes](https://pages.github.com/themes/)
- [Custom Domain Setup](https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site)

### Ferramentas
- [HTML Validator](https://validator.w3.org/)
- [CSS Validator](https://jigsaw.w3.org/css-validator/)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)

---

## ✅ Checklist Final

### Antes do Deploy
- [ ] index.html criado e testado
- [ ] sobre.html criado e testado
- [ ] metrics-calculator.js implementado
- [ ] app.js modificado (sem fetch API)
- [ ] Navegação funcionando
- [ ] CSS/JS carregando
- [ ] Responsivo testado
- [ ] Console sem erros

### Configuração GitHub Pages
- [ ] Repository settings configurado
- [ ] Source definida (main branch)
- [ ] Folder escolhido (root ou docs)
- [ ] Build completado (Actions)
- [ ] URL acessível

### Pós-Deploy
- [ ] Testar em diferentes navegadores
- [ ] Testar em mobile
- [ ] Verificar métricas Google Analytics (se habilitado)
- [ ] Documentar URL no README.md
- [ ] Compartilhar com equipe

---

## 🎉 Conclusão

Seguindo este guia, você terá:
- ✅ Dashboard funcionando no GitHub Pages
- ✅ URL pública para demonstrações
- ✅ Deploy automático em commits
- ✅ Versão Flask mantida para desenvolvimento

**URL Final**: `https://leonardobora.github.io/eco-dashboard-renault/`

---

**Última atualização**: Dezembro 2024  
**Mantido por**: Equipe EcoCode.AI UniBrasil  
**Versão**: 1.0
