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

@app.route('/')
def dashboard():
    return '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EcoTI Dashboard - Renault</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .header { background: #FFCB00; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .value { font-size: 32px; font-weight: bold; color: #FFCB00; }
        .btn { background: #FFCB00; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="header">
        <h1>🌱 EcoTI Dashboard - Renault Sustentabilidade Digital</h1>
    </div>

    <div class="metrics">
        <div class="card">
            <h3>⚡ Consumo Atual</h3>
            <div class="value" id="consumption">-</div>
            <div>kWh</div>
        </div>
        <div class="card">
            <h3>🌍 Emissões CO₂</h3>
            <div class="value" id="emissions">-</div>
            <div>kg/ano</div>
        </div>
        <div class="card">
            <h3>💰 Economia Potencial</h3>
            <div class="value" id="savings">-</div>
            <div>R$/ano</div>
        </div>
        <div class="card">
            <h3>🌳 Árvores Equivalentes</h3>
            <div class="value" id="trees">-</div>
            <div>plantadas</div>
        </div>
    </div>

    <div class="card">
        <h3>Recomendações IA</h3>
        <div style="margin: 10px 0;">
            <strong>Auto-shutdown Workstations:</strong> Economia estimada R$ 270/mês
            <button class="btn" onclick="implementar('shutdown')">Implementar</button>
        </div>
        <div style="margin: 10px 0;">
            <strong>Otimizar Refrigeração:</strong> Economia estimada R$ 120/mês
            <button class="btn" onclick="implementar('cooling')">Implementar</button>
        </div>
    </div>

    <script>
        function updateMetrics() {
            fetch('/api/metrics')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('consumption').textContent = data.consumo_atual.toFixed(0);
                    document.getElementById('emissions').textContent = data.emissoes_co2.toLocaleString('pt-BR');
                    document.getElementById('savings').textContent = data.economia_potencial.toLocaleString('pt-BR');
                    document.getElementById('trees').textContent = data.arvores_equivalentes.toLocaleString('pt-BR');
                });
        }

        function implementar(tipo) {
            alert('Implementando: ' + tipo + ' - Funcionalidade ativa no sistema real!');
        }

        updateMetrics();
        setInterval(updateMetrics, 10000);
    </script>
</body>
</html>'''

@app.route('/api/metrics')
def get_metrics():
    infra.consumo_atual = infra.calcular_consumo_atual()
    return jsonify({
        'consumo_atual': infra.consumo_atual,
        'emissoes_co2': infra.calcular_emissoes_anuais(),
        'economia_potencial': infra.calcular_economia_potencial(),
        'arvores_equivalentes': infra.calcular_arvores_equivalentes()
    })

if __name__ == '__main__':
    print("🌱 EcoTI Dashboard - Sustentabilidade Digital Renault")
    print("Acesse: http://localhost:5000")
    app.run(debug=True, port=5000)
