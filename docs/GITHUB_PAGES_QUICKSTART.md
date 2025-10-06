# 🚀 GitHub Pages - Guia Rápido

## ⚡ Deploy em 5 Passos

### 1️⃣ Conversão dos Templates
```bash
# Criar versão estática do dashboard
cp templates/dashboard.html index.html
cp templates/sobre.html sobre.html

# Substituir sintaxe Jinja2 por HTML puro
# {{ url_for('static', filename='css/style.css') }} 
# ↓
# static/css/style.css
```

### 2️⃣ Implementar Calculadora JS
```bash
# Criar arquivo de cálculo de métricas
cat > static/js/metrics-calculator.js << 'EOF'
class RenaultInfrastructure {
    // ... código da calculadora ...
}
window.RenaultInfrastructure = RenaultInfrastructure;
EOF
```

### 3️⃣ Modificar app.js
```javascript
// Substituir fetch API por cálculo local
async function fetchMetrics() {
    const infra = new RenaultInfrastructure();
    return infra.getMetrics();
}
```

### 4️⃣ Testar Localmente
```bash
# Servidor Python simples
python3 -m http.server 8080

# Acessar: http://localhost:8080/index.html
```

### 5️⃣ Configurar GitHub Pages
1. `Settings` → `Pages`
2. Source: `main` branch
3. Folder: `/ (root)`
4. Save
5. Acessar: `https://leonardobora.github.io/eco-dashboard-renault/`

---

## 📋 Checklist Rápido

- [ ] index.html sem sintaxe Jinja2
- [ ] sobre.html sem sintaxe Jinja2
- [ ] metrics-calculator.js criado
- [ ] app.js modificado (sem fetch API)
- [ ] Testado localmente
- [ ] GitHub Pages configurado
- [ ] URL funcionando

---

## 🔧 Comandos Úteis

### Teste Local
```bash
# Raiz do projeto
python3 -m http.server 8080

# Pasta docs/
cd docs && python3 -m http.server 8080
```

### Verificar Status
```bash
# Status do repositório
git status

# Verificar build GitHub Pages
# Vá para: Actions tab no GitHub
```

### Deploy
```bash
git add .
git commit -m "Deploy: GitHub Pages static version"
git push origin main
# Aguarde 2-5 minutos para build
```

---

## 🐛 Resolução Rápida de Problemas

| Problema | Solução |
|----------|---------|
| CSS não carrega | Verificar caminho: `static/css/style.css` |
| JS não funciona | Incluir metrics-calculator.js antes de app.js |
| 404 na página | Aguardar build completar (2-5 min) |
| Métricas erradas | Verificar RenaultInfrastructure no console |

---

## 📱 URLs Importantes

- **GitHub Pages**: `https://leonardobora.github.io/eco-dashboard-renault/`
- **Repositório**: `https://github.com/leonardobora/eco-dashboard-renault`
- **Settings**: `https://github.com/leonardobora/eco-dashboard-renault/settings/pages`
- **Actions**: `https://github.com/leonardobora/eco-dashboard-renault/actions`

---

## 📚 Documentação Completa

- [Análise de Viabilidade](GITHUB_PAGES_FEASIBILITY.md)
- [Guia de Implementação](GITHUB_PAGES_IMPLEMENTATION.md)

---

**Tempo estimado**: 1-2 horas  
**Nível**: Intermediário  
**Pré-requisitos**: Git, Python 3, Editor de código
