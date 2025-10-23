// Application Data
const appData = {
  infraestrutura: {
    workstations: 5376,
    servidores_hp: 90,
    vxrail: 10,
    consumo_medio_workstation: 250,
    fator_emissao: 0.0817,
    sequestro_arvore: 22,
    tarifa_energia: 0.60
  },
  metricas_atuais: {
    consumo_atual_kwh: 1344,
    emissoes_co2_kg_ano: 219610,
    economia_potencial_reais: 1612800,
    arvores_equivalentes: 9982,
    workstations_ativas: 4200,
    servidores_ativos: 85,
    economia_ativa: true
  },
  historico_consumo: [
    {hora: "00:00", consumo: 800},
    {hora: "01:00", consumo: 750},
    {hora: "02:00", consumo: 700},
    {hora: "08:00", consumo: 1200},
    {hora: "09:00", consumo: 1400},
    {hora: "10:00", consumo: 1500},
    {hora: "14:00", consumo: 1600},
    {hora: "18:00", consumo: 1300},
    {hora: "22:00", consumo: 900}
  ],
  previsao_7_dias: [
    {dia: "Segunda", previsto: 1400, otimizado: 1100},
    {dia: "Terça", previsto: 1450, otimizado: 1150},
    {dia: "Quarta", previsto: 1380, otimizado: 1080},
    {dia: "Quinta", previsto: 1420, otimizado: 1120},
    {dia: "Sexta", previsto: 1500, otimizado: 1200},
    {dia: "Sábado", previsto: 900, otimizado: 700},
    {dia: "Domingo", previsto: 800, otimizado: 600}
  ],
  setores: [
    {nome: "Administrativo", workstations: 1200, consumo: 300, economia: 15},
    {nome: "Engenharia", workstations: 800, consumo: 250, economia: 12},
    {nome: "Produção", workstations: 1500, consumo: 400, economia: 20},
    {nome: "Vendas", workstations: 900, consumo: 220, economia: 18},
    {nome: "Suporte", workstations: 976, consumo: 174, economia: 25}
  ]
};

// Global variables
let energyChart = null;
let sectorChart = null;
let predictionChart = null;

// API functions to connect to Flask backend or use local calculator
async function fetchMetrics() {
  // Check if RenaultInfrastructure class is available (static version)
  if (typeof window.RenaultInfrastructure !== 'undefined') {
    try {
      // Use local calculator (GitHub Pages version)
      const infra = new window.RenaultInfrastructure();
      const data = infra.getMetrics();
      
      // Update app data with calculated metrics
      appData.metricas_atuais.consumo_atual_kwh = data.consumo_atual;
      appData.metricas_atuais.emissoes_co2_kg_ano = data.emissoes_co2;
      appData.metricas_atuais.economia_potencial_reais = data.economia_potencial;
      appData.metricas_atuais.arvores_equivalentes = data.arvores_equivalentes;
      
      console.log('📊 Metrics calculated locally (GitHub Pages mode):', data);
      return data;
    } catch (error) {
      console.error('Error calculating metrics locally:', error);
    }
  }
  
  // Try Flask API (development/production mode)
  try {
    const response = await fetch('/api/metrics');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    
    // Update app data with real API data
    appData.metricas_atuais.consumo_atual_kwh = data.consumo_atual;
    appData.metricas_atuais.emissoes_co2_kg_ano = data.emissoes_co2;
    appData.metricas_atuais.economia_potencial_reais = data.economia_potencial;
    appData.metricas_atuais.arvores_equivalentes = data.arvores_equivalentes;
    
    console.log('✅ Metrics fetched from Flask API:', data);
    return data;
  } catch (error) {
    console.error('Error fetching metrics from API:', error);
    // Return mock data as ultimate fallback
    return {
      consumo_atual: appData.metricas_atuais.consumo_atual_kwh,
      emissoes_co2: appData.metricas_atuais.emissoes_co2_kg_ano,
      economia_potencial: appData.metricas_atuais.economia_potencial_reais,
      arvores_equivalentes: appData.metricas_atuais.arvores_equivalentes
    };
  }
}

// Update metrics display with real data
function updateMetricsDisplay() {
  fetchMetrics().then(data => {
    // Update the main metric cards
    const consumptionEl = document.getElementById('currentConsumption');
    const emissionsEl = document.getElementById('co2Emissions');
    const savingsEl = document.getElementById('potentialSavings');
    const treesEl = document.getElementById('treeEquivalent');
    
    if (consumptionEl) {
      consumptionEl.textContent = `${Math.round(data.consumo_atual)} kWh`;
    }
    
    if (emissionsEl) {
      emissionsEl.textContent = `${Math.round(data.emissoes_co2).toLocaleString('pt-BR')} kg`;
    }
    
    if (savingsEl) {
      savingsEl.textContent = `R$ ${Math.round(data.economia_potencial).toLocaleString('pt-BR')}`;
    }
    
    if (treesEl) {
      treesEl.textContent = `${data.arvores_equivalentes.toLocaleString('pt-BR')}`;
    }
    
    // Update workstation status
    const onlineEl = document.getElementById('workstationsOnline');
    if (onlineEl) {
      onlineEl.textContent = `${appData.metricas_atuais.workstations_ativas.toLocaleString('pt-BR')} Online`;
    }
    
    const offlineEl = document.getElementById('workstationsOffline');
    if (offlineEl) {
      const offline = appData.infraestrutura.workstations - appData.metricas_atuais.workstations_ativas;
      offlineEl.textContent = `${offline.toLocaleString('pt-BR')} Offline`;
    }
    
    console.log('✅ Metrics updated from Flask API:', data);
  }).catch(error => {
    console.error('❌ Failed to update metrics:', error);
  });
}

// Tab Navigation
function initializeTabNavigation() {
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  tabButtons.forEach(button => {
    button.addEventListener('click', () => {
      // Remove active class from all buttons and contents
      tabButtons.forEach(btn => btn.classList.remove('active'));
      tabContents.forEach(content => content.classList.remove('active'));

      // Add active class to clicked button
      button.classList.add('active');

      // Show corresponding tab content
      const tabId = button.getAttribute('data-tab') + '-tab';
      const targetTab = document.getElementById(tabId);
      if (targetTab) {
        targetTab.classList.add('active');
      }
    });
  });
}

// Current Time Display
function updateCurrentTime() {
  const timeElement = document.getElementById('currentTime');
  if (timeElement) {
    const now = new Date();
    
    // Format: HH:mm DD/MM/YY
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const year = String(now.getFullYear()).slice(-2);
    
    timeElement.textContent = `${hours}:${minutes} ${day}/${month}/${year}`;
  }
}

// Initialize Charts
function initializeCharts() {
  initializeEnergyChart();
  initializeSectorChart();
  initializePredictionChart();
}

// Energy Consumption Chart
function initializeEnergyChart() {
  const ctx = document.getElementById('energyChart');
  if (!ctx) return;

  // Generate realistic hourly data for the last 24 hours
  const now = new Date();
  const labels = [];
  const data = [];
  
  for (let i = 23; i >= 0; i--) {
    const time = new Date(now.getTime() - (i * 60 * 60 * 1000));
    labels.push(time.getHours().toString().padStart(2, '0') + ':00');
    
    // Generate realistic consumption based on time of day
    let baseConsumption = 600; // Minimum consumption
    const hour = time.getHours();
    
    if (hour >= 7 && hour <= 18) {
      // Business hours - higher consumption
      baseConsumption = 1200 + Math.random() * 400;
    } else if (hour >= 19 && hour <= 22) {
      // Evening - medium consumption
      baseConsumption = 800 + Math.random() * 300;
    } else {
      // Night - lower consumption
      baseConsumption = 600 + Math.random() * 200;
    }
    
    data.push(Math.round(baseConsumption));
  }

  energyChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Consumo (kWh)',
        data: data,
        borderColor: '#32b8cd',
        backgroundColor: 'rgba(50, 184, 205, 0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: false,
          grid: {
            color: 'rgba(0,0,0,0.1)'
          }
        },
        x: {
          grid: {
            display: false
          }
        }
      }
    }
  });
}

// Sector Consumption Chart
function initializeSectorChart() {
  const ctx = document.getElementById('sectorChart');
  if (!ctx) return;

  sectorChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: appData.setores.map(s => s.nome),
      datasets: [{
        data: appData.setores.map(s => s.consumo),
        backgroundColor: [
          '#32b8cd',
          '#ffcb00',
          '#5c6ac4',
          '#f093fb',
          '#36d1dc'
        ],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            padding: 20,
            usePointStyle: true
          }
        }
      }
    }
  });
}

// Prediction Chart
function initializePredictionChart() {
  const ctx = document.getElementById('predictionChart');
  if (!ctx) return;

  predictionChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: appData.previsao_7_dias.map(d => d.dia),
      datasets: [
        {
          label: 'Consumo Previsto',
          data: appData.previsao_7_dias.map(d => d.previsto),
          borderColor: '#ff6b6b',
          backgroundColor: 'rgba(255, 107, 107, 0.1)',
          borderWidth: 2,
          fill: false
        },
        {
          label: 'Com Otimização',
          data: appData.previsao_7_dias.map(d => d.otimizado),
          borderColor: '#32b8cd',
          backgroundColor: 'rgba(50, 184, 205, 0.1)',
          borderWidth: 2,
          fill: false
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: false,
          grid: {
            color: 'rgba(0,0,0,0.1)'
          }
        }
      }
    }
  });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  console.log('🚀 EcoTI Dashboard Initialized');
  
  // Initialize components
  initializeTabNavigation();
  initializeTooltips();
  updateCurrentTime();
  initializeCharts();
  
  // Load initial metrics
  updateMetricsDisplay();
  
  // Update time every minute
  setInterval(updateCurrentTime, 60000);
  
  // Update metrics every 10 seconds (real-time)
  setInterval(updateMetricsDisplay, 10000);
  
  // Initialize button handlers
  initializeButtonHandlers();
});

// Button Handlers
function initializeButtonHandlers() {
  // Refresh button
  const refreshBtn = document.getElementById('refreshData');
  if (refreshBtn) {
    refreshBtn.addEventListener('click', () => {
      updateMetricsDisplay();
      console.log('📊 Data refreshed manually');
    });
  }
  
  // Export button
  const exportBtn = document.getElementById('exportData');
  if (exportBtn) {
    exportBtn.addEventListener('click', () => {
      exportData();
    });
  }
  
  // Implementation buttons
  const implementBtns = document.querySelectorAll('.btn--primary');
  implementBtns.forEach(btn => {
    if (btn.textContent.includes('Implementar')) {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        showImplementationModal(btn.textContent);
      });
    }
  });
}

// Export functionality
function exportData() {
  const csvData = generateCSVData();
  downloadCSV(csvData, 'eco_dashboard_data.csv');
  console.log('📄 Data exported to CSV');
}

function generateCSVData() {
  const headers = ['Métrica', 'Valor', 'Unidade'];
  const rows = [
    ['Consumo Atual', appData.metricas_atuais.consumo_atual_kwh, 'kWh'],
    ['Emissões CO₂', appData.metricas_atuais.emissoes_co2_kg_ano, 'kg/ano'],
    ['Economia Potencial', appData.metricas_atuais.economia_potencial_reais, 'R$/ano'],
    ['Árvores Equivalentes', appData.metricas_atuais.arvores_equivalentes, 'árvores']
  ];
  
  return [headers, ...rows];
}

function downloadCSV(data, filename) {
  const csvContent = data.map(row => row.join(',')).join('\\n');
  const blob = new Blob([csvContent], { type: 'text/csv' });
  const url = window.URL.createObjectURL(blob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.style.display = 'none';
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  
  window.URL.revokeObjectURL(url);
}

// Implementation modal
function showImplementationModal(action) {
  alert(`🚀 Implementando: ${action}\\n\\nEsta funcionalidade estará disponível na versão de produção integrada com os sistemas da Renault.`);
}

// Utility functions
function formatNumber(num) {
  return new Intl.NumberFormat('pt-BR').format(num);
}

function formatCurrency(num) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(num);
}

// Tooltip functionality
function initializeTooltips() {
  const tooltipModal = document.getElementById('tooltipModal');
  const tooltipClose = document.getElementById('tooltipClose');
  const tooltipBody = document.getElementById('tooltipBody');
  const infoLinks = document.querySelectorAll('.info-link');
  
  // Tooltip content
  const tooltipContent = {
    energy: {
      title: '⚡ Consumo Energético Atual',
      content: `
        <h3>Como calculamos?</h3>
        <div class="formula-box">
          <code>Consumo (kWh) = (Servidores × Potência × Utilização + Workstations × Potência × Fator de Uso) ÷ 1000</code>
        </div>
        <p><strong>Componentes do cálculo:</strong></p>
        <ul>
          <li>90 Servidores HP ProLiant DL380 Gen10: 400W cada (35% utilização média)</li>
          <li>10 VxRail E560: 800W cada (65% utilização média)</li>
          <li>PUE (Power Usage Effectiveness): 2.0 - inclui refrigeração, UPS e infraestrutura</li>
        </ul>
        <div class="example-highlight">
          <strong>📊 Exemplo de cálculo em tempo real:</strong>
          <p>Consumo servidores HP: 90 × 400W × 0.35 = 12,6 kW</p>
          <p>Consumo VxRail: 10 × 800W × 0.65 = 5,2 kW</p>
          <p>Total IT: 17,8 kW</p>
          <p>Total Datacenter (com PUE 2.0): 17,8 × 2.0 = <strong>35,6 kW</strong></p>
        </div>
        <p><em>O valor varia conforme a hora do dia, refletindo padrões reais de utilização.</em></p>
      `
    },
    co2: {
      title: '🌍 Emissões de CO₂',
      content: `
        <h3>Como calculamos?</h3>
        <div class="formula-box">
          <code>CO₂ (kg/ano) = Consumo Anual (kWh) × Fator de Emissão</code>
        </div>
        <p><strong>Parâmetros utilizados:</strong></p>
        <ul>
          <li>Fator de emissão: 0,0817 kg CO₂/kWh (matriz energética brasileira 2024)</li>
          <li>Fonte: Empresa de Pesquisa Energética (EPE) - Balanço Energético Nacional</li>
          <li>Consumo anual: Consumo atual × 24 horas × 365 dias</li>
        </ul>
        <div class="example-highlight">
          <strong>📊 Exemplo de cálculo:</strong>
          <p>Se consumo atual = 874 kWh:</p>
          <p>Consumo anual: 874 × 24 × 365 = 7.656.240 kWh/ano</p>
          <p>CO₂ emitido: 7.656.240 × 0,0817 = <strong>625.515 kg/ano</strong></p>
        </div>
        <p><em>A matriz energética brasileira é relativamente limpa devido às hidrelétricas (~60% renovável).</em></p>
      `
    },
    savings: {
      title: '💰 Economia Potencial',
      content: `
        <h3>Como calculamos?</h3>
        <div class="formula-box">
          <code>Economia (R$/ano) = Redução de Consumo (kWh) × Tarifa (R$/kWh)</code>
        </div>
        <p><strong>Fontes de economia identificadas:</strong></p>
        <ul>
          <li>Consolidação de servidores com baixa utilização</li>
          <li>Otimização do PUE (de 2.0 para 1.5) - melhorias em refrigeração</li>
          <li>Desligamento automático de recursos ociosos</li>
          <li>Migração de cargas para horários de menor demanda</li>
        </ul>
        <div class="example-highlight">
          <strong>📊 Potencial de otimização:</strong>
          <p>Redução esperada no consumo: 15-30%</p>
          <p>Tarifa industrial média: R$ 0,60/kWh (Copel 2024)</p>
          <p>Exemplo: 20% de redução em 874 kWh = 174,8 kWh economizados/dia</p>
          <p>Economia anual: 174,8 × 365 × R$ 0,60 = <strong>R$ 38.276/ano</strong></p>
        </div>
        <p><em>Baseado em estudos de eficiência energética em data centers e melhores práticas do setor.</em></p>
      `
    },
    trees: {
      title: '🌳 Equivalente em Árvores',
      content: `
        <h3>Como calculamos?</h3>
        <div class="formula-box">
          <code>Árvores = Emissões CO₂ (kg/ano) ÷ 22 kg/árvore/ano</code>
        </div>
        <p><strong>Referência científica:</strong></p>
        <ul>
          <li>Sequestro médio: 22 kg CO₂/árvore/ano</li>
          <li>Baseado em árvore adulta de médio porte em clima tropical</li>
          <li>Considera espécies nativas brasileiras típicas</li>
          <li>Período de maturidade: árvore com 10+ anos</li>
        </ul>
        <div class="example-highlight">
          <strong>📊 O que isso significa?</strong>
          <p>Se emitimos 625.515 kg CO₂/ano:</p>
          <p>Árvores necessárias: 625.515 ÷ 22 = <strong>28.432 árvores</strong></p>
          <p>Isso representa quantas árvores precisariam ser plantadas e mantidas por um ano inteiro para compensar nossas emissões.</p>
        </div>
        <p><em>Este indicador ajuda a visualizar o impacto ambiental em termos tangíveis e compreensíveis.</em></p>
      `
    }
  };
  
  // Add click handlers to info links
  infoLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const tooltipType = link.getAttribute('data-tooltip');
      const content = tooltipContent[tooltipType];
      
      if (content) {
        tooltipBody.innerHTML = `
          <h3>${content.title}</h3>
          ${content.content}
        `;
        tooltipModal.classList.add('active');
      }
    });
  });
  
  // Close modal on close button click
  if (tooltipClose) {
    tooltipClose.addEventListener('click', () => {
      tooltipModal.classList.remove('active');
    });
  }
  
  // Close modal on background click
  if (tooltipModal) {
    tooltipModal.addEventListener('click', (e) => {
      if (e.target === tooltipModal) {
        tooltipModal.classList.remove('active');
      }
    });
  }
  
  // Close modal on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && tooltipModal.classList.contains('active')) {
      tooltipModal.classList.remove('active');
    }
  });
}

// Error handling
window.addEventListener('error', function(e) {
  console.error('❌ Application Error:', e.error);
});

// Log successful initialization
console.log('✅ EcoTI Dashboard - Flask Integration Active');
console.log('🔄 Real-time data updates every 10 seconds');
// Log connection mode
if (typeof window.RenaultInfrastructure !== 'undefined') {
  console.log('🌐 Running in static mode (GitHub Pages) - using local metrics calculator');
} else {
  console.log('🌐 Running in Flask mode - connected to API at /api/metrics');
}