# 📊 Dashboard EcoTI - Guia de Uso

## 🎯 Acesso Rápido

**URL:** http://localhost:5000/dashboard

## 🚀 Iniciando o Dashboard

### Passo 1: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 2: Iniciar o Servidor Flask
```bash
python3 app_renault_mvp.py
```

### Passo 3: Acessar o Dashboard
Abra o navegador em: **http://localhost:5000/dashboard**

## 📱 Funcionalidades

### Métricas em Tempo Real
O dashboard atualiza automaticamente a cada 10 segundos, exibindo:

- **⚡ PUE Atual**: Power Usage Effectiveness do datacenter
  - Valor atual: 2.00
  - Meta: 1.50
  - Potencial de melhoria: 25%

- **🖥️ Consolidação**: Análise de consolidação de servidores
  - Servidores atuais: 100
  - Servidores após consolidação: 73
  - Redução: 27%

- **🔋 Economia de Energia**: Potencial de economia
  - Redução: 100%
  - Economia anual: 287.328 kWh/ano

- **💰 Economia Anual**: Impacto financeiro
  - Economia: R$ 172.396,8/ano
  - ROI: 13 meses

### Visualizações

#### Servidores Ativos
- HP ProLiant DL380: 90 servidores
- Dell VxRail E560: 10 servidores
- Total: 100 servidores

#### Breakdown PUE
Visualização em barras de progresso mostrando:
- Consumo de servidores (verde)
- Consumo de cooling (laranja)

#### Impacto Ambiental e Econômico
Seção destacada em verde com:
- Redução de CO₂: 23.5 ton/ano
- Economia de Energia: 287 MWh/ano
- Redução de Custos: R$ 172k/ano

## 📲 Responsividade

O dashboard é totalmente responsivo e funciona perfeitamente em:

- **Desktop** (1920x1080+): Layout completo com 4 colunas de métricas
- **Tablet** (768x1024): Layout adaptado com 2 colunas
- **Mobile** (375x667): Layout em coluna única

## 🔄 Auto-Refresh

- O dashboard atualiza automaticamente a cada **10 segundos**
- Busca dados em paralelo de 5 endpoints da API
- Não recarrega a página completa, apenas os dados

## 🎨 Design

### Tema de Cores
- **Fundo**: Gradiente emerald/teal/cyan (#ecfdf5 → #f0fdfa → #cffafe)
- **Cards de Métricas**: Branco com sombra
- **Trends**: Gradientes coloridos (emerald, teal, cyan, green)
- **Impacto**: Gradiente verde (#10b981 → #14b8a6)

### Animações
- Spinner de loading animado
- Indicador de status pulsante
- Transições suaves em hover
- Barras de progresso animadas

## 🛠️ Troubleshooting

### Dashboard não carrega
1. Verifique se o Flask está rodando: `curl http://localhost:5000/api/health`
2. Verifique a porta: O Flask deve estar na porta 5000
3. Veja os logs do Flask para erros

### Dados não atualizam
1. Abra o Console do navegador (F12)
2. Verifique se há erros de JavaScript
3. Verifique a aba Network para ver as chamadas da API

### Erro ao carregar
- Clique no botão "Tentar Novamente"
- Ou recarregue a página (F5)

## 📊 APIs Utilizadas

O dashboard consome os seguintes endpoints:

- `GET /api/servers` - Métricas detalhadas dos servidores
- `GET /api/pue` - Dados de Power Usage Effectiveness
- `GET /api/consolidation` - Análise de consolidação
- `GET /api/savings` - Projeções de economia
- `GET /api/health` - Status do sistema

## 🎯 Para Apresentação

### Checklist Antes da Demo
- [ ] Servidor Flask rodando
- [ ] Dashboard acessível em http://localhost:5000/dashboard
- [ ] Navegador em tela cheia (F11)
- [ ] Auto-refresh funcionando (verificar logs)
- [ ] Testar responsividade se for usar tablet

### Pontos de Destaque
1. **Métricas em tempo real** com auto-refresh
2. **ROI claro**: 13 meses de payback
3. **Impacto ambiental**: 23.5 ton CO₂/ano reduzidas
4. **Consolidação**: 27% de redução de servidores
5. **Economia**: R$ 172k/ano

## 📈 Evolução Futura

Possíveis melhorias para versões futuras:
- [ ] Gráficos com Chart.js para tendências históricas
- [ ] Filtros por período (dia/semana/mês)
- [ ] Export de relatórios em PDF
- [ ] Alertas configuráveis
- [ ] Comparação com benchmarks da indústria
- [ ] Integração com dados SNMP reais

## 📞 Suporte

Para dúvidas ou problemas:
- Verifique a documentação: `/docs`
- Logs do Flask: Console onde executou `python3 app_renault_mvp.py`
- Issues no GitHub: https://github.com/leonardobora/eco-dashboard-renault/issues

---

**Desenvolvido para o Renault Transformation Day 2025** 🌱
