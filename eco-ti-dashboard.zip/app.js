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

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM loaded, initializing app...');
  initializeApp();
});

function initializeApp() {
  console.log('Initializing application...');
  setupTabNavigation();
  updateCurrentTime();
  updateMetrics();
  
  // Initialize charts after a short delay to ensure DOM is ready
  setTimeout(() => {
    initializeCharts();
  }, 100);
  
  setupEventListeners();
  
  // Start real-time updates
  setInterval(updateCurrentTime, 1000);
  setInterval(simulateRealTimeData, 5000);
  
  console.log('Application initialized successfully');
}

// Tab Navigation - Fixed implementation
function setupTabNavigation() {
  console.log('Setting up tab navigation...');
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');
  
  console.log('Found', tabBtns.length, 'tab buttons and', tabContents.length, 'tab contents');
  
  tabBtns.forEach((btn, index) => {
    console.log('Setting up tab button:', btn.getAttribute('data-tab'));
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const targetTab = btn.getAttribute('data-tab');
      console.log('Tab clicked:', targetTab);
      
      // Remove active class from all tabs and contents
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(content => {
        content.classList.remove('active');
        content.style.display = 'none';
      });
      
      // Add active class to clicked tab
      btn.classList.add('active');
      
      // Show corresponding content
      const targetContent = document.getElementById(`${targetTab}-tab`);
      if (targetContent) {
        targetContent.classList.add('active');
        targetContent.style.display = 'block';
        targetContent.classList.add('fade-in');
        console.log('Showing tab content:', targetTab);
        
        // Initialize charts for specific tabs
        if (targetTab === 'monitoring' && !sectorChart) {
          setTimeout(initializeSectorChart, 100);
        }
        if (targetTab === 'analytics' && !predictionChart) {
          setTimeout(initializePredictionChart, 100);
        }
        
        // Update charts when switching tabs
        if (targetTab === 'analytics' && predictionChart) {
          setTimeout(() => predictionChart.update(), 100);
        }
        if (targetTab === 'monitoring' && sectorChart) {
          setTimeout(() => sectorChart.update(), 100);
        }
      } else {
        console.error('Target content not found:', `${targetTab}-tab`);
      }
    });
  });
}

// Update current time
function updateCurrentTime() {
  const now = new Date();
  const timeString = now.toLocaleString('pt-BR', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
  
  const timeElement = document.getElementById('currentTime');
  if (timeElement) {
    timeElement.textContent = timeString;
  }
}

// Update metrics display
function updateMetrics() {
  const metrics = appData.metricas_atuais;
  
  // Update consumption
  const consumptionEl = document.getElementById('currentConsumption');
  if (consumptionEl) {
    consumptionEl.textContent = `${metrics.consumo_atual_kwh.toLocaleString('pt-BR')} kWh`;
  }
  
  // Update CO2 emissions
  const co2El = document.getElementById('co2Emissions');
  if (co2El) {
    co2El.textContent = `${metrics.emissoes_co2_kg_ano.toLocaleString('pt-BR')} kg`;
  }
  
  // Update potential savings
  const savingsEl = document.getElementById('potentialSavings');
  if (savingsEl) {
    savingsEl.textContent = `R$ ${metrics.economia_potencial_reais.toLocaleString('pt-BR')}`;
  }
  
  // Update tree equivalent
  const treeEl = document.getElementById('treeEquivalent');
  if (treeEl) {
    treeEl.textContent = metrics.arvores_equivalentes.toLocaleString('pt-BR');
  }
}

// Initialize Charts
function initializeCharts() {
  console.log('Initializing charts...');
  initializeEnergyChart();
  // Other charts will be initialized when their tabs are first opened
}

function initializeEnergyChart() {
  const ctx = document.getElementById('energyChart');
  if (!ctx) {
    console.error('Energy chart canvas not found');
    return;
  }
  
  const chartData = appData.historico_consumo;
  
  energyChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: chartData.map(item => item.hora),
      datasets: [{
        label: 'Consumo (kWh)',
        data: chartData.map(item => item.consumo),
        borderColor: '#1FB8CD',
        backgroundColor: 'rgba(31, 184, 205, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#1FB8CD',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        pointRadius: 6
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
            color: 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            callback: function(value) {
              return value + ' kWh';
            }
          }
        },
        x: {
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          }
        }
      },
      elements: {
        point: {
          hoverRadius: 8
        }
      }
    }
  });
  
  console.log('Energy chart initialized');
}

function initializeSectorChart() {
  const ctx = document.getElementById('sectorChart');
  if (!ctx) {
    console.error('Sector chart canvas not found');
    return;
  }
  
  const setores = appData.setores;
  
  sectorChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: setores.map(setor => setor.nome),
      datasets: [{
        label: 'Consumo Atual (kWh)',
        data: setores.map(setor => setor.consumo),
        backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F'],
        borderRadius: 6,
        borderSkipped: false
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
          beginAtZero: true,
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            callback: function(value) {
              return value + ' kWh';
            }
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
  
  console.log('Sector chart initialized');
}

function initializePredictionChart() {
  const ctx = document.getElementById('predictionChart');
  if (!ctx) {
    console.error('Prediction chart canvas not found');
    return;
  }
  
  const previsao = appData.previsao_7_dias;
  
  predictionChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: previsao.map(item => item.dia),
      datasets: [{
        label: 'Consumo Previsto',
        data: previsao.map(item => item.previsto),
        borderColor: '#B4413C',
        backgroundColor: 'rgba(180, 65, 60, 0.1)',
        borderWidth: 3,
        fill: false,
        tension: 0.4,
        pointBackgroundColor: '#B4413C',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        pointRadius: 6
      }, {
        label: 'Consumo Otimizado',
        data: previsao.map(item => item.otimizado),
        borderColor: '#1FB8CD',
        backgroundColor: 'rgba(31, 184, 205, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#1FB8CD',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2,
        pointRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: false,
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            callback: function(value) {
              return value + ' kWh';
            }
          }
        },
        x: {
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          }
        }
      },
      interaction: {
        intersect: false,
        mode: 'index'
      }
    }
  });
  
  console.log('Prediction chart initialized');
}

// Setup Event Listeners
function setupEventListeners() {
  console.log('Setting up event listeners...');
  
  // Refresh data button
  const refreshBtn = document.getElementById('refreshData');
  if (refreshBtn) {
    refreshBtn.addEventListener('click', () => {
      refreshBtn.innerHTML = '🔄 Atualizando...';
      refreshBtn.disabled = true;
      
      setTimeout(() => {
        simulateDataRefresh();
        refreshBtn.innerHTML = '🔄 Atualizar';
        refreshBtn.disabled = false;
        showNotification('Dados atualizados com sucesso!', 'success');
      }, 1500);
    });
  }
  
  // Export data button
  const exportBtn = document.getElementById('exportData');
  if (exportBtn) {
    exportBtn.addEventListener('click', () => {
      exportData();
      showNotification('Relatório exportado com sucesso!', 'success');
    });
  }
  
  // Chart period selector - Fixed implementation
  const chartPeriod = document.getElementById('chartPeriod');
  if (chartPeriod) {
    chartPeriod.addEventListener('change', (e) => {
      console.log('Chart period changed to:', e.target.value);
      updateChartPeriod(e.target.value);
    });
    
    // Also handle click events for better responsiveness
    chartPeriod.addEventListener('click', (e) => {
      console.log('Chart period selector clicked');
    });
  }
  
  // Recommendation buttons
  setupRecommendationButtons();
  
  // Settings form
  setupSettingsForm();
  
  // Alert action buttons
  setupAlertButtons();
}

function setupRecommendationButtons() {
  const implementBtns = document.querySelectorAll('.recommendation-card .btn--primary');
  implementBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const card = btn.closest('.recommendation-card');
      const title = card.querySelector('h4').textContent;
      
      btn.innerHTML = 'Implementando...';
      btn.disabled = true;
      
      setTimeout(() => {
        btn.innerHTML = '✅ Implementado';
        btn.classList.remove('btn--primary');
        btn.classList.add('btn--secondary');
        showNotification(`Recomendação implementada: ${title}`, 'success');
        
        // Simulate metrics improvement
        simulateMetricsImprovement();
      }, 2000);
    });
  });
}

function setupSettingsForm() {
  const saveBtn = document.querySelector('.settings-actions .btn--primary');
  if (saveBtn) {
    saveBtn.addEventListener('click', () => {
      saveBtn.innerHTML = 'Salvando...';
      saveBtn.disabled = true;
      
      setTimeout(() => {
        saveBtn.innerHTML = 'Salvar Configurações';
        saveBtn.disabled = false;
        showNotification('Configurações salvas com sucesso!', 'success');
      }, 1000);
    });
  }
  
  // Test connection button
  const testBtns = document.querySelectorAll('.settings-card .btn--primary');
  testBtns.forEach(btn => {
    if (btn.textContent.includes('Testar')) {
      btn.addEventListener('click', () => {
        btn.innerHTML = 'Testando...';
        btn.disabled = true;
        
        setTimeout(() => {
          btn.innerHTML = 'Testar Conexão';
          btn.disabled = false;
          showNotification('Conexão testada com sucesso!', 'success');
        }, 2000);
      });
    }
  });
}

function setupAlertButtons() {
  const alertBtns = document.querySelectorAll('.alert-item .btn');
  alertBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const alertItem = btn.closest('.alert-item');
      const alertTitle = alertItem.querySelector('.alert-title').textContent;
      
      if (btn.classList.contains('btn--primary')) {
        btn.innerHTML = 'Implementando...';
        btn.disabled = true;
        
        setTimeout(() => {
          alertItem.style.opacity = '0.5';
          btn.innerHTML = '✅ Implementado';
          btn.disabled = false;
          showNotification(`Ação implementada: ${alertTitle}`, 'success');
        }, 1500);
      } else {
        showNotification(`Visualizando detalhes: ${alertTitle}`, 'info');
      }
    });
  });
}

// Simulate real-time data updates
function simulateRealTimeData() {
  // Update current consumption with small random variation
  const currentConsumption = appData.metricas_atuais.consumo_atual_kwh;
  const variation = (Math.random() - 0.5) * 100; // ±50 kWh variation
  const newConsumption = Math.max(800, currentConsumption + variation);
  
  appData.metricas_atuais.consumo_atual_kwh = Math.round(newConsumption);
  
  // Update other metrics based on consumption
  updateDependentMetrics();
  
  // Update display
  updateMetrics();
  
  // Add new data point to energy chart
  if (energyChart) {
    const now = new Date();
    const timeLabel = now.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    
    energyChart.data.labels.push(timeLabel);
    energyChart.data.datasets[0].data.push(newConsumption);
    
    // Keep only last 10 data points
    if (energyChart.data.labels.length > 10) {
      energyChart.data.labels.shift();
      energyChart.data.datasets[0].data.shift();
    }
    
    energyChart.update('none');
  }
}

function updateDependentMetrics() {
  const consumption = appData.metricas_atuais.consumo_atual_kwh;
  const infraestrutura = appData.infraestrutura;
  
  // Calculate CO2 emissions
  const annualConsumption = consumption * 24 * 365;
  appData.metricas_atuais.emissoes_co2_kg_ano = Math.round(annualConsumption * infraestrutura.fator_emissao);
  
  // Calculate tree equivalent
  appData.metricas_atuais.arvores_equivalentes = Math.round(
    appData.metricas_atuais.emissoes_co2_kg_ano / infraestrutura.sequestro_arvore
  );
  
  // Calculate potential savings (assuming 30% reduction is possible)
  const potentialReduction = consumption * 0.3;
  const dailySavings = potentialReduction * 24 * infraestrutura.tarifa_energia;
  appData.metricas_atuais.economia_potencial_reais = Math.round(dailySavings * 365);
}

function simulateDataRefresh() {
  // Simulate fetching new data from server
  appData.setores.forEach(setor => {
    const variation = (Math.random() - 0.5) * 50;
    setor.consumo = Math.max(50, setor.consumo + variation);
  });
  
  // Update sector chart
  if (sectorChart) {
    sectorChart.data.datasets[0].data = appData.setores.map(setor => setor.consumo);
    sectorChart.update();
  }
}

function simulateMetricsImprovement() {
  // Simulate 5-10% improvement in metrics
  const improvement = 0.05 + Math.random() * 0.05;
  
  appData.metricas_atuais.consumo_atual_kwh *= (1 - improvement);
  appData.metricas_atuais.emissoes_co2_kg_ano *= (1 - improvement);
  appData.metricas_atuais.economia_potencial_reais *= (1 + improvement);
  
  updateMetrics();
}

function updateChartPeriod(period) {
  console.log('Updating chart period to:', period);
  // This would normally fetch different data based on the period
  showNotification(`Visualização alterada para: ${period === '24h' ? 'Últimas 24h' : period === '7d' ? 'Últimos 7 dias' : 'Últimos 30 dias'}`, 'info');
  
  if (energyChart) {
    // Simulate different data for different periods
    let newData = [];
    let newLabels = [];
    
    if (period === '24h') {
      newData = appData.historico_consumo.map(item => item.consumo);
      newLabels = appData.historico_consumo.map(item => item.hora);
    } else if (period === '7d') {
      newData = appData.previsao_7_dias.map(item => item.previsto);
      newLabels = appData.previsao_7_dias.map(item => item.dia);
    } else {
      // 30 days - simulate monthly data
      newData = Array.from({length: 30}, () => 1000 + Math.random() * 800);
      newLabels = Array.from({length: 30}, (_, i) => `${i + 1}/09`);
    }
    
    energyChart.data.labels = newLabels;
    energyChart.data.datasets[0].data = newData;
    energyChart.update();
  }
}

function exportData() {
  // Simulate data export
  const exportData = {
    timestamp: new Date().toISOString(),
    metrics: appData.metricas_atuais,
    sectors: appData.setores,
    consumption_history: appData.historico_consumo
  };
  
  // Create and download file
  const dataStr = JSON.stringify(exportData, null, 2);
  const dataBlob = new Blob([dataStr], {type: 'application/json'});
  const url = URL.createObjectURL(dataBlob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `renault-ecoti-report-${new Date().toISOString().split('T')[0]}.json`;
  link.click();
  URL.revokeObjectURL(url);
}

function showNotification(message, type = 'info') {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = `notification notification--${type}`;
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 16px 24px;
    border-radius: 8px;
    color: white;
    font-weight: 500;
    z-index: 1000;
    transform: translateX(100%);
    transition: transform 0.3s ease;
    max-width: 400px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  `;
  
  // Set background color based on type
  const colors = {
    success: '#1FB8CD',
    error: '#B4413C',
    warning: '#FFC185',
    info: '#5D878F'
  };
  notification.style.backgroundColor = colors[type] || colors.info;
  
  notification.textContent = message;
  document.body.appendChild(notification);
  
  // Animate in
  setTimeout(() => {
    notification.style.transform = 'translateX(0)';
  }, 100);
  
  // Remove after 3 seconds
  setTimeout(() => {
    notification.style.transform = 'translateX(100%)';
    setTimeout(() => {
      if (document.body.contains(notification)) {
        document.body.removeChild(notification);
      }
    }, 300);
  }, 3000);
}

// Utility functions
function formatNumber(num) {
  return num.toLocaleString('pt-BR');
}

function formatCurrency(value) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value);
}

function calculateCO2FromKWh(kwh) {
  return kwh * appData.infraestrutura.fator_emissao;
}

function calculateTreesFromCO2(co2Kg) {
  return Math.round(co2Kg / appData.infraestrutura.sequestro_arvore);
}

function calculateSavingsFromKWh(kwh) {
  return kwh * appData.infraestrutura.tarifa_energia;
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
  if (e.ctrlKey || e.metaKey) {
    switch (e.key) {
      case '1':
        e.preventDefault();
        document.querySelector('[data-tab="dashboard"]').click();
        break;
      case '2':
        e.preventDefault();
        document.querySelector('[data-tab="monitoring"]').click();
        break;
      case '3':
        e.preventDefault();
        document.querySelector('[data-tab="analytics"]').click();
        break;
      case '4':
        e.preventDefault();
        document.querySelector('[data-tab="settings"]').click();
        break;
      case 'r':
        e.preventDefault();
        const refreshBtn = document.getElementById('refreshData');
        if (refreshBtn) refreshBtn.click();
        break;
    }
  }
});

// Initialize tooltips and accessibility
function initializeAccessibility() {
  // Add ARIA labels to interactive elements
  const buttons = document.querySelectorAll('button');
  buttons.forEach(btn => {
    if (!btn.getAttribute('aria-label') && btn.textContent.trim()) {
      btn.setAttribute('aria-label', btn.textContent.trim());
    }
  });
  
  // Add keyboard navigation to charts
  const charts = document.querySelectorAll('canvas');
  charts.forEach(chart => {
    chart.setAttribute('tabindex', '0');
    chart.setAttribute('role', 'img');
    chart.setAttribute('aria-label', 'Gráfico interativo de dados de sustentabilidade');
  });
}

// Call accessibility setup after DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  setTimeout(initializeAccessibility, 1000);
});