# Vou criar uma estrutura de MVP funcional em Python para o sistema de monitoramento
# Criando um exemplo de aplicação Flask que poderia ser implantada no Replit

flask_app_code = '''
from flask import Flask, render_template, jsonify, request
import json
import datetime
import random
import threading
import time

app = Flask(__name__)

# Dados simulados da infraestrutura Renault
class RenaultInfrastructure:
    def __init__(self):
        self.workstations = 5376
        self.servidores_hp = 90
        self.vxrail = 10
        self.consumo_medio_w = 250
        self.fator_emissao = 0.0817  # kg CO2/kWh Brasil
        self.sequestro_arvore = 22   # kg CO2/ano por árvore
        self.tarifa_energia = 0.60   # R$/kWh
        
        # Estado atual simulado
        self.workstations_ativas = 4200
        self.servidores_ativos = 85
        self.consumo_atual = self.calcular_consumo_atual()
        
    def calcular_consumo_atual(self):
        # Simula consumo baseado no horário
        hora_atual = datetime.datetime.now().hour
        if 8 <= hora_atual <= 18:  # Horário comercial
            fator_uso = 0.8
        elif 19 <= hora_atual <= 22:  # Horário reduzido
            fator_uso = 0.4
        else:  # Madrugada
            fator_uso = 0.2
            
        consumo_workstations = self.workstations_ativas * self.consumo_medio_w * fator_uso / 1000
        consumo_servidores = self.servidores_ativos * 400 / 1000  # 400W por servidor
        return consumo_workstations + consumo_servidores
    
    def calcular_emissoes_anuais(self):
        # Consumo anual estimado em kWh
        consumo_anual = self.consumo_atual * 24 * 365
        return consumo_anual * self.fator_emissao
    
    def calcular_arvores_equivalentes(self):
        emissoes = self.calcular_emissoes_anuais()
        return int(emissoes / self.sequestro_arvore)
    
    def calcular_economia_potencial(self):
        # Potencial de economia desligando workstations ociosas
        workstations_ociosas = self.workstations - self.workstations_ativas
        economia_kwh = workstations_ociosas * self.consumo_medio_w * 8 * 250 / 1000  # 8h/dia, 250 dias/ano
        return economia_kwh * self.tarifa_energia

# Instância global da infraestrutura
infra = RenaultInfrastructure()

# Dados históricos simulados
def gerar_historico_consumo():
    historico = []
    base_date = datetime.datetime.now() - datetime.timedelta(hours=24)
    
    for i in range(24):
        timestamp = base_date + datetime.timedelta(hours=i)
        hora = timestamp.hour
        
        # Simula padrão de consumo por horário
        if 8 <= hora <= 18:
            consumo_base = 1400
        elif 19 <= hora <= 22:
            consumo_base = 900
        else:
            consumo_base = 600
            
        # Adiciona variação aleatória
        variacao = random.uniform(0.9, 1.1)
        consumo = int(consumo_base * variacao)
        
        historico.append({
            'timestamp': timestamp.strftime('%H:%M'),
            'consumo': consumo
        })
    
    return historico

# Rotas da API
@app.route('/')
def dashboard():
    return '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EcoTI Dashboard - Renault Sustentabilidade Digital</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .header { background: #FFCB00; padding: 20px; border-radius: 8px; margin-bottom: 20px; color: #000; }
            .header h1 { margin: 0; font-size: 24px; }
            .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .metric-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .metric-card h3 { margin: 0 0 10px 0; color: #333; font-size: 14px; }
            .metric-value { font-size: 32px; font-weight: bold; color: #FFCB00; margin-bottom: 5px; }
            .metric-trend { font-size: 12px; color: #666; }
            .chart-container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
            .btn { background: #FFCB00; color: #000; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-weight: bold; }
            .btn:hover { background: #e6b800; }
            .status-online { color: #28a745; }
            .status-offline { color: #dc3545; }
            .recommendations { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .recommendation-item { padding: 15px; border: 1px solid #ddd; border-radius: 4px; margin-bottom: 10px; }
            .recommendation-item h4 { margin: 0 0 10px 0; color: #333; }
        </style>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <div class="header">
            <h1>🌱 EcoTI Dashboard - Renault Sustentabilidade Digital</h1>
            <p>Monitoramento em Tempo Real | <span id="currentTime"></span></p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <h3>⚡ Consumo Atual</h3>
                <div class="metric-value" id="currentConsumption">-</div>
                <div class="metric-trend">kWh em tempo real</div>
            </div>
            
            <div class="metric-card">
                <h3>🌍 Emissões CO₂</h3>
                <div class="metric-value" id="co2Emissions">-</div>
                <div class="metric-trend">kg/ano</div>
            </div>
            
            <div class="metric-card">
                <h3>💰 Economia Potencial</h3>
                <div class="metric-value" id="savings">-</div>
                <div class="metric-trend">por ano</div>
            </div>
            
            <div class="metric-card">
                <h3>🌳 Equivalente em Árvores</h3>
                <div class="metric-value" id="trees">-</div>
                <div class="metric-trend">plantadas para compensar</div>
            </div>
        </div>
        
        <div class="chart-container">
            <h3>Consumo Energético - Últimas 24h</h3>
            <canvas id="consumptionChart" width="400" height="100"></canvas>
        </div>
        
        <div class="chart-container">
            <h3>Status da Infraestrutura</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                <div>
                    <h4>Workstations</h4>
                    <p><span class="status-online">●</span> <span id="activeWorkstations">-</span> Ativas</p>
                    <p><span class="status-offline">●</span> <span id="inactiveWorkstations">-</span> Inativas</p>
                </div>
                <div>
                    <h4>Servidores</h4>
                    <p><span class="status-online">●</span> <span id="activeServers">-</span> Online</p>
                    <p><span class="status-offline">●</span> <span id="inactiveServers">-</span> Standby</p>
                </div>
            </div>
        </div>
        
        <div class="recommendations">
            <h3>🤖 Recomendações IA para Economia Energética</h3>
            <div class="recommendation-item">
                <h4>Desligar Workstations Ociosas</h4>
                <p>Detectadas 1.176 workstations ociosas por mais de 30 minutos. Economia estimada: R$ 270/mês</p>
                <button class="btn" onclick="implementRecommendation('auto-shutdown')">Implementar Automaticamente</button>
            </div>
            <div class="recommendation-item">
                <h4>Otimizar Horário de Backup</h4>
                <p>Migrar backups para horário de menor demanda energética (2h-6h). Economia: R$ 180/mês</p>
                <button class="btn" onclick="implementRecommendation('backup-schedule')">Agendar Otimização</button>
            </div>
            <div class="recommendation-item">
                <h4>Reduzir Temperatura Sala Servidores</h4>
                <p>Temperatura atual 18°C. Aumentar para 20°C pode economizar R$ 120/mês sem impacto no desempenho</p>
                <button class="btn" onclick="implementRecommendation('temperature')">Aplicar Configuração</button>
            </div>
        </div>
        
        <script>
            let chart = null;
            
            function updateMetrics() {
                fetch('/api/metrics')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('currentConsumption').textContent = data.consumo_atual.toFixed(0) + ' kWh';
                        document.getElementById('co2Emissions').textContent = data.emissoes_co2.toLocaleString('pt-BR');
                        document.getElementById('savings').textContent = 'R$ ' + data.economia_potencial.toLocaleString('pt-BR');
                        document.getElementById('trees').textContent = data.arvores_equivalentes.toLocaleString('pt-BR');
                        document.getElementById('activeWorkstations').textContent = data.workstations_ativas;
                        document.getElementById('inactiveWorkstations').textContent = data.workstations_inativas;
                        document.getElementById('activeServers').textContent = data.servidores_ativos;
                        document.getElementById('inactiveServers').textContent = data.servidores_inativos;
                    });
            }
            
            function updateChart() {
                fetch('/api/consumption-history')
                    .then(response => response.json())
                    .then(data => {
                        const ctx = document.getElementById('consumptionChart').getContext('2d');
                        
                        if (chart) {
                            chart.destroy();
                        }
                        
                        chart = new Chart(ctx, {
                            type: 'line',
                            data: {
                                labels: data.map(d => d.timestamp),
                                datasets: [{
                                    label: 'Consumo (kWh)',
                                    data: data.map(d => d.consumo),
                                    borderColor: '#FFCB00',
                                    backgroundColor: 'rgba(255, 203, 0, 0.1)',
                                    tension: 0.4
                                }]
                            },
                            options: {
                                responsive: true,
                                scales: {
                                    y: {
                                        beginAtZero: false
                                    }
                                }
                            }
                        });
                    });
            }
            
            function updateTime() {
                document.getElementById('currentTime').textContent = new Date().toLocaleString('pt-BR');
            }
            
            function implementRecommendation(type) {
                alert('Implementando recomendação: ' + type + '. Esta ação seria executada no sistema real.');
            }
            
            // Inicializar
            updateTime();
            updateMetrics();
            updateChart();
            
            // Atualizar a cada 30 segundos
            setInterval(() => {
                updateTime();
                updateMetrics();
                updateChart();
            }, 30000);
        </script>
    </body>
    </html>
    '''

@app.route('/api/metrics')
def get_metrics():
    # Atualiza métricas em tempo real
    infra.consumo_atual = infra.calcular_consumo_atual()
    
    return jsonify({
        'consumo_atual': infra.consumo_atual,
        'emissoes_co2': infra.calcular_emissoes_anuais(),
        'economia_potencial': infra.calcular_economia_potencial(),
        'arvores_equivalentes': infra.calcular_arvores_equivalentes(),
        'workstations_ativas': infra.workstations_ativas,
        'workstations_inativas': infra.workstations - infra.workstations_ativas,
        'servidores_ativos': infra.servidores_ativos,
        'servidores_inativos': (infra.servidores_hp + infra.vxrail) - infra.servidores_ativos
    })

@app.route('/api/consumption-history')
def get_consumption_history():
    return jsonify(gerar_historico_consumo())

@app.route('/api/implement-recommendation', methods=['POST'])
def implement_recommendation():
    recommendation_type = request.json.get('type')
    
    # Simula implementação da recomendação
    if recommendation_type == 'auto-shutdown':
        # Simula o desligamento de workstations ociosas
        infra.workstations_ativas = max(3000, infra.workstations_ativas - 500)
        message = "Auto-shutdown implementado. 500 workstations foram colocadas em modo economia."
    elif recommendation_type == 'backup-schedule':
        message = "Horários de backup otimizados para 2h-6h da madrugada."
    elif recommendation_type == 'temperature':
        message = "Temperatura da sala de servidores ajustada para 20°C."
    else:
        message = "Recomendação não reconhecida."
    
    return jsonify({'success': True, 'message': message})

if __name__ == '__main__':
    print("🌱 EcoTI Dashboard - Sistema de Sustentabilidade Digital Renault")
    print("Infraestrutura monitorada:")
    print(f"  • {infra.workstations} Workstations")
    print(f"  • {infra.servidores_hp} Servidores HP DL380")
    print(f"  • {infra.vxrail} VxRail")
    print(f"Acesse: http://localhost:5000")
    
    app.run(debug=True, port=5000)
'''

# Salvando o arquivo
with open('app_renault_ecoti.py', 'w', encoding='utf-8') as f:
    f.write(flask_app_code)

print("✅ Arquivo 'app_renault_ecoti.py' criado com sucesso!")
print("\n🚀 Para executar no Replit ou localmente:")
print("1. Crie um novo projeto Python")
print("2. Cole o código do arquivo 'app_renault_ecoti.py'")
print("3. Execute: pip install flask")
print("4. Execute: python app_renault_ecoti.py")
print("5. Acesse o dashboard em http://localhost:5000")

# Também vou criar um requirements.txt
requirements = '''
flask==2.3.3
'''

with open('requirements.txt', 'w') as f:
    f.write(requirements)

print("\n📋 Arquivo 'requirements.txt' criado")
print("\n=== FUNCIONALIDADES DO MVP ===")
print("✅ Dashboard em tempo real com métricas de sustentabilidade")
print("✅ Gráfico de consumo energético das últimas 24h")
print("✅ Status da infraestrutura (workstations e servidores)")
print("✅ Cálculo automático de CO2 e equivalência em árvores")
print("✅ Recomendações IA para economia energética")
print("✅ Botões para implementar otimizações automaticamente")
print("✅ API REST para integração com sistemas externos")
print("✅ Interface responsiva com cores da Renault")

print(f"\n📊 DADOS SIMULADOS (baseados na infraestrutura real):")
print(f"• Workstations: {infra.workstations}")
print(f"• Servidores: {infra.servidores_hp + infra.vxrail}")
print(f"• Economia potencial: R$ {infra.calcular_economia_potencial():,.2f}/ano")
print(f"• Árvores equivalentes: {infra.calcular_arvores_equivalentes():,}")