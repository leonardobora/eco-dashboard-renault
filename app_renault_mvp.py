from flask import Flask, render_template, jsonify, request
import json
import datetime
import random
import threading
import time
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar SNMP collector
try:
    from snmp_collector import SNMPCollector
    SNMP_COLLECTOR_AVAILABLE = True
    logger.info("SNMP Collector carregado com sucesso")
except ImportError as e:
    SNMP_COLLECTOR_AVAILABLE = False
    logger.warning(f"SNMP Collector não disponível: {e}")

# Importar novos módulos
from data_sources.carbon_data import get_carbon_data_loader
from ai_engine.recommendations import get_recommendations_engine

app = Flask(__name__)

# Registrar blueprints para novas rotas
try:
    from routes.api_routes import api_bp
    app.register_blueprint(api_bp)
    logger.info("API routes registradas com sucesso")
except ImportError as e:
    logger.warning(f"Não foi possível carregar rotas adicionais: {e}")


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

# Instância global do SNMP collector (se disponível)
snmp_collector = None
if SNMP_COLLECTOR_AVAILABLE:
    try:
        snmp_collector = SNMPCollector()
        logger.info("SNMP Collector inicializado")
    except Exception as e:
        logger.warning(f"Erro ao inicializar SNMP Collector: {e}")
        snmp_collector = None


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/metrics")
def get_metrics():
    """
    Endpoint de métricas com suporte a SNMP
    
    Tenta coletar dados via SNMP primeiro, com fallback para dados simulados
    """
    consumo_servidores_kwh = 0
    
    # Tentar coletar via SNMP
    if snmp_collector:
        try:
            # Coletar consumo dos servidores via SNMP
            consumo_servidores_kwh, fonte_snmp = snmp_collector.get_total_consumption_kwh()
            fonte = fonte_snmp
            logger.info(f"Métricas coletadas via SNMP: {consumo_servidores_kwh:.2f} kWh (fonte: {fonte})")
        except Exception as e:
            logger.warning(f"Erro na coleta SNMP, usando simulação: {e}")
            # Fallback para cálculo simulado
            consumo_servidores_kwh = infra.servidores_ativos * 400 / 1000
            fonte = 'simulado'
    else:
        # Usar dados simulados (servidor apenas)
        consumo_servidores_kwh = infra.servidores_ativos * 400 / 1000
        fonte = 'simulado'
    
    # Calcular consumo de workstations (sempre simulado por enquanto)
    hora_atual = datetime.datetime.now().hour
    if 8 <= hora_atual <= 18:  # Horário comercial
        fator_uso = 0.8
    elif 19 <= hora_atual <= 22:  # Horário reduzido
        fator_uso = 0.4
    else:  # Madrugada
        fator_uso = 0.2
    
    consumo_workstations_kwh = (
        infra.workstations_ativas * infra.consumo_medio_w * fator_uso / 1000
    )
    
    # Consumo total
    consumo_total_kwh = consumo_workstations_kwh + consumo_servidores_kwh
    
    # Atualizar infraestrutura
    infra.consumo_atual = consumo_total_kwh
    
    return jsonify(
        {
            "consumo_atual": consumo_total_kwh,
            "emissoes_co2": infra.calcular_emissoes_anuais(),
            "economia_potencial": infra.calcular_economia_potencial(),
            "arvores_equivalentes": infra.calcular_arvores_equivalentes(),
            "fonte": fonte,  # Novo campo indicando fonte dos dados
            "detalhes_fonte": {
                "servidores": fonte,
                "workstations": "simulado"
            }
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
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug, port=5000)
