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
        self.sequestro_arvore = 22  # kg CO2/ano por árvore
        self.tarifa_energia = 0.60  # R$/kWh

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

        consumo_workstations = (
            self.workstations_ativas * self.consumo_medio_w * fator_uso / 1000
        )
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
        economia_kwh = (
            workstations_ociosas * self.consumo_medio_w * 8 * 250 / 1000
        )  # 8h/dia, 250 dias/ano
        return economia_kwh * self.tarifa_energia


# Instância global da infraestrutura
infra = RenaultInfrastructure()


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/metrics")
def get_metrics():
    infra.consumo_atual = infra.calcular_consumo_atual()
    return jsonify(
        {
            "consumo_atual": infra.consumo_atual,
            "emissoes_co2": infra.calcular_emissoes_anuais(),
            "economia_potencial": infra.calcular_economia_potencial(),
            "arvores_equivalentes": infra.calcular_arvores_equivalentes(),
        }
    )


@app.route("/sobre")
def sobre():
    """Página com informações sobre o projeto EcoCode.AI e a equipe UniBrasil"""
    try:
        with open("SOBRE.md", "r", encoding="utf-8") as f:
            sobre_content = f.read()
    except FileNotFoundError:
        sobre_content = "# Página em construção\n\nConteúdo em breve..."
    
    return render_template("sobre.html", conteudo=sobre_content)


if __name__ == "__main__":
    print("🌱 EcoCode.AI - Sustentabilidade Digital Renault")
    print("Acesse: http://localhost:5000")
    print("Sobre: http://localhost:5000/sobre")
    app.run(debug=True, port=5000)
