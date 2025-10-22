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


# Dados da infraestrutura Renault focada em Datacenter
class RenaultInfrastructure:
    def __init__(self):
        # Servidor infrastructure - 100 servidores no datacenter
        self.servidores_hp = 90  # HP ProLiant DL380 Gen10
        self.vxrail = 10  # Dell VxRail E560
        self.poder_hp_w = 400  # Watts por HP ProLiant
        self.poder_vxrail_w = 800  # Watts por VxRail
        
        # Datacenter metrics
        self.pue_atual = 2.0  # Power Usage Effectiveness atual
        self.pue_alvo = 1.5  # PUE alvo com otimizações
        
        # Fatores ambientais e custos
        self.fator_emissao = 0.0817  # kg CO2/kWh Brasil
        self.sequestro_arvore = 22  # kg CO2/ano por árvore
        self.tarifa_energia = 0.60  # R$/kWh
        
        # Load do CarbonDataLoader para dados reais
        from data_sources.carbon_data import get_carbon_data_loader
        self.carbon_loader = get_carbon_data_loader()
        
        self.consumo_atual = self.calcular_consumo_atual()

    def calcular_consumo_atual(self):
        """Calcula consumo total do datacenter (servidores + cooling via PUE)"""
        hora_atual = datetime.datetime.now().hour
        
        # Usar padrões de carga do carbon_data
        load_factor = self.carbon_loader.calculate_utilization_factor(hora_atual)
        
        # Consumo dos servidores HP (35% utilização média)
        consumo_hp = self.servidores_hp * self.poder_hp_w * 0.35 * load_factor / 1000
        
        # Consumo dos VxRail (65% utilização média)
        consumo_vxrail = self.vxrail * self.poder_vxrail_w * 0.65 * load_factor / 1000
        
        # Total IT equipment
        consumo_servidores = consumo_hp + consumo_vxrail
        
        # Aplicar PUE para incluir cooling, UPS, etc
        consumo_total_datacenter = consumo_servidores * self.pue_atual
        
        return consumo_total_datacenter

    def calcular_emissoes_anuais(self):
        """Calcula emissões anuais de CO2 do datacenter"""
        consumo_anual = self.consumo_atual * 24 * 365
        return consumo_anual * self.fator_emissao

    def calcular_arvores_equivalentes(self):
        """Calcula equivalência em árvores para sequestro de CO2"""
        emissoes = self.calcular_emissoes_anuais()
        return int(emissoes / self.sequestro_arvore)

    def calcular_economia_potencial(self):
        """Calcula economia potencial com consolidação + PUE otimização"""
        # Usar dados do carbon_loader
        optimization = self.carbon_loader.get_optimization_potential()
        return optimization['annual_savings_brl']


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


@app.route("/dashboard")
def dashboard_new():
    """Nova página de dashboard com métricas em tempo real e visualizações interativas"""
    return render_template("dashboard_new.html")


@app.route("/api/metrics")
def get_metrics():
    """
    Endpoint principal de métricas do datacenter (servidores apenas)
    
    Retorna métricas de consumo, PUE, emissões e economia potencial
    Tenta coletar dados via SNMP primeiro, com fallback para dados simulados
    """
    consumo_datacenter_kwh = 0
    fonte = 'simulado'
    
    # Tentar coletar via SNMP
    if snmp_collector:
        try:
            # Coletar consumo dos servidores via SNMP
            consumo_servidores_kwh, fonte_snmp = snmp_collector.get_total_consumption_kwh()
            # Aplicar PUE para obter consumo total do datacenter
            consumo_datacenter_kwh = consumo_servidores_kwh * infra.pue_atual
            fonte = fonte_snmp
            logger.info(f"Métricas coletadas via SNMP: {consumo_servidores_kwh:.2f} kWh servidores, {consumo_datacenter_kwh:.2f} kWh total (PUE: {infra.pue_atual})")
        except Exception as e:
            logger.warning(f"Erro na coleta SNMP, usando simulação: {e}")
            consumo_datacenter_kwh = infra.calcular_consumo_atual()
            fonte = 'simulado'
    else:
        # Usar dados simulados do datacenter
        consumo_datacenter_kwh = infra.calcular_consumo_atual()
    
    # Atualizar infraestrutura
    infra.consumo_atual = consumo_datacenter_kwh
    
    # Obter dados de otimização
    optimization = infra.carbon_loader.get_optimization_potential()
    consolidation = infra.carbon_loader.get_consolidation_potential()
    
    return jsonify(
        {
            "consumo_atual": round(consumo_datacenter_kwh, 2),
            "emissoes_co2": round(infra.calcular_emissoes_anuais(), 2),
            "economia_potencial": round(infra.calcular_economia_potencial(), 2),
            "arvores_equivalentes": infra.calcular_arvores_equivalentes(),
            "pue_atual": infra.pue_atual,
            "pue_alvo": infra.pue_alvo,
            "servidores_total": infra.servidores_hp + infra.vxrail,
            "consolidacao_potencial": consolidation['servers_to_consolidate'],
            "reducao_percentual": round(optimization['reduction_percentage'], 1),
            "fonte": fonte,
            "escopo": "datacenter-servidores-apenas"
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
