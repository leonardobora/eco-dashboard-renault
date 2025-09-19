# ⚙️ Arquivo de Configuração - EcoTI Dashboard

"""
Configurações centralizadas do sistema EcoTI Dashboard.
Este arquivo permite fácil customização dos parâmetros do sistema.
"""

import os
from typing import Dict, Any


class Config:
    """Configuração base do sistema"""

    # Configurações da aplicação
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    DEBUG = os.environ.get("FLASK_ENV") == "development"

    # Configurações do servidor
    HOST = os.environ.get("HOST") or "127.0.0.1"
    PORT = int(os.environ.get("PORT") or 5000)

    # Configurações de infraestrutura (facilmente editáveis)
    INFRASTRUCTURE = {
        "workstations_total": 5376,
        "servidores_hp": 90,
        "vxrail_clusters": 10,
        "consumo_medio_workstation_watts": 250,
        "consumo_medio_servidor_watts": 400,
        "fator_emissao_co2_kg_kwh": 0.0817,  # Brasil 2024
        "sequestro_arvore_kg_co2_ano": 22,
        "tarifa_energia_reais_kwh": 0.60,
        "horas_operacao_dia": 8,
        "dias_operacao_ano": 250,  # Dias úteis
    }

    # Configurações de setores/departamentos
    SETORES = {
        "administrativo": {
            "nome": "Administrativo",
            "workstations": 1200,
            "fator_uso_medio": 0.75,
            "horario_pico_inicio": 8,
            "horario_pico_fim": 18,
        },
        "engenharia": {
            "nome": "Engenharia",
            "workstations": 800,
            "fator_uso_medio": 0.85,
            "horario_pico_inicio": 7,
            "horario_pico_fim": 19,
        },
        "producao": {
            "nome": "Produção",
            "workstations": 1500,
            "fator_uso_medio": 0.90,
            "horario_pico_inicio": 6,
            "horario_pico_fim": 22,
        },
        "vendas": {
            "nome": "Vendas",
            "workstations": 900,
            "fator_uso_medio": 0.70,
            "horario_pico_inicio": 8,
            "horario_pico_fim": 20,
        },
        "suporte": {
            "nome": "Suporte",
            "workstations": 976,
            "fator_uso_medio": 0.80,
            "horario_pico_inicio": 7,
            "horario_pico_fim": 21,
        },
    }

    # Configurações de cálculo de economia
    ECONOMIA_CONFIG = {
        "percentual_otimizacao_possivel": 0.25,  # 25% de economia possível
        "workstations_modo_eco_percentual": 0.70,  # 70% podem usar modo eco
        "reducao_consumo_modo_eco": 0.40,  # 40% menos consumo em modo eco
        "meta_reducao_mensal": 0.08,  # Meta de 8% de redução mensal
    }

    # Configurações de alertas e thresholds
    ALERTAS = {
        "consumo_alto_threshold_kwh": 2000,
        "consumo_baixo_threshold_kwh": 500,
        "temperatura_alta_threshold_celsius": 28,
        "utilizacao_cpu_alta_threshold": 85,
        "utilizacao_memoria_alta_threshold": 90,
        "uptime_minimo_dias": 30,
    }

    # Configurações de APIs externas (para futuras integrações)
    API_CONFIG = {
        "timeout_segundos": 30,
        "retry_attempts": 3,
        "rate_limit_requests_per_minute": 60,
        "sensor_api_url": os.environ.get("SENSOR_API_URL"),
        "weather_api_key": os.environ.get("WEATHER_API_KEY"),
        "energy_grid_api_url": os.environ.get("ENERGY_GRID_API_URL"),
    }

    # Configurações de cache e performance
    CACHE_CONFIG = {
        "metrics_cache_seconds": 60,
        "charts_cache_seconds": 300,
        "static_files_cache_days": 7,
        "database_pool_size": 10,
        "max_concurrent_requests": 100,
    }

    # Configurações de logging
    LOGGING = {
        "level": os.environ.get("LOG_LEVEL", "INFO"),
        "file_path": "logs/ecoti.log",
        "max_file_size_mb": 10,
        "backup_count": 5,
        "format": "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]",
    }

    # Configurações de segurança
    SECURITY = {
        "session_timeout_minutes": 30,
        "max_login_attempts": 5,
        "password_min_length": 8,
        "csrf_protection": True,
        "force_https": os.environ.get("FORCE_HTTPS", "False").lower() == "true",
    }


class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""

    DEBUG = True
    TESTING = False

    # Dados simulados mais variados para desenvolvimento
    MOCK_DATA_VARIATION = True
    SIMULATION_SPEED_MULTIPLIER = 10  # Simula mudanças mais rápidas


class ProductionConfig(Config):
    """Configuração para produção"""

    DEBUG = False
    TESTING = False

    # Configurações mais rigorosas para produção
    API_CONFIG = {**Config.API_CONFIG, "timeout_segundos": 10, "retry_attempts": 2}

    SECURITY = {**Config.SECURITY, "session_timeout_minutes": 15, "force_https": True}


class TestingConfig(Config):
    """Configuração para testes"""

    DEBUG = True
    TESTING = True

    # Dados simplificados para testes
    INFRASTRUCTURE = {
        **Config.INFRASTRUCTURE,
        "workstations_total": 100,  # Dados menores para testes rápidos
        "servidores_hp": 5,
        "vxrail_clusters": 1,
    }


# Função para obter configuração baseada no ambiente
def get_config() -> Config:
    """Retorna a configuração apropriada baseada na variável de ambiente"""
    env = os.environ.get("FLASK_ENV", "development")

    if env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()


# Configurações específicas para customização fácil
CUSTOMIZATION = {
    # Cores da interface (pode ser editado pelos usuários)
    "brand_colors": {
        "primary": "#FFCB00",  # Amarelo Renault
        "secondary": "#000000",  # Preto Renault
        "success": "#28a745",  # Verde para economia
        "warning": "#ffc107",  # Amarelo para alertas
        "danger": "#dc3545",  # Vermelho para problemas
        "info": "#17a2b8",  # Azul para informações
    },
    # Textos personalizáveis
    "labels": {
        "company_name": "Renault",
        "system_title": "EcoTI Dashboard - Sustentabilidade Digital",
        "consumption_unit": "kWh",
        "emission_unit": "kg CO₂",
        "currency": "R$",
        "tree_unit": "árvores",
    },
    # Configurações de gráficos
    "charts": {
        "update_interval_ms": 5000,  # Atualização a cada 5 segundos
        "animation_duration_ms": 750,
        "point_radius": 3,
        "line_thickness": 2,
        "grid_opacity": 0.3,
    },
    # Metas de sustentabilidade (editável pelos gestores)
    "sustainability_goals": {
        "carbon_reduction_target_percent": 30,  # Meta de redução de 30%
        "energy_efficiency_target_percent": 25,  # Meta de eficiência de 25%
        "cost_savings_target_reais": 2000000,  # Meta de economia R$ 2M
        "tree_equivalent_target": 15000,  # Meta de 15k árvores equivalentes
    },
}

# Dados de exemplo para demonstração (facilmente substituíveis)
DEMO_DATA = {
    "historical_consumption": [
        {"hour": "00:00", "consumption": 800},
        {"hour": "01:00", "consumption": 750},
        {"hour": "02:00", "consumption": 700},
        {"hour": "06:00", "consumption": 900},
        {"hour": "08:00", "consumption": 1200},
        {"hour": "09:00", "consumption": 1400},
        {"hour": "10:00", "consumption": 1500},
        {"hour": "12:00", "consumption": 1600},
        {"hour": "14:00", "consumption": 1600},
        {"hour": "18:00", "consumption": 1300},
        {"hour": "20:00", "consumption": 1100},
        {"hour": "22:00", "consumption": 900},
    ],
    "weekly_prediction": [
        {"day": "Segunda", "predicted": 1400, "optimized": 1100},
        {"day": "Terça", "predicted": 1450, "optimized": 1150},
        {"day": "Quarta", "predicted": 1500, "optimized": 1200},
        {"day": "Quinta", "predicted": 1480, "optimized": 1180},
        {"day": "Sexta", "predicted": 1520, "optimized": 1220},
        {"day": "Sábado", "predicted": 900, "optimized": 700},
        {"day": "Domingo", "predicted": 800, "optimized": 600},
    ],
    "optimization_recommendations": [
        {
            "type": "auto-shutdown",
            "title": "Desligamento Automático",
            "description": "Configurar desligamento automático de workstations ociosas após 2h",
            "potential_savings_kwh": 150,
            "potential_savings_reais": 2700,
            "implementation_effort": "baixo",
            "priority": "alta",
        },
        {
            "type": "backup-schedule",
            "title": "Otimização de Backups",
            "description": "Reagendar backups para horário de menor demanda energética",
            "potential_savings_kwh": 80,
            "potential_savings_reais": 1440,
            "implementation_effort": "baixo",
            "priority": "média",
        },
        {
            "type": "server-consolidation",
            "title": "Consolidação de Servidores",
            "description": "Migrar VMs subutilizadas para servidores com maior eficiência",
            "potential_savings_kwh": 200,
            "potential_savings_reais": 3600,
            "implementation_effort": "alto",
            "priority": "alta",
        },
    ],
}


# Função de validação de configurações
def validate_config(config: Config) -> bool:
    """Valida se as configurações estão corretas"""
    required_fields = ["INFRASTRUCTURE", "SETORES", "ECONOMIA_CONFIG", "ALERTAS"]

    for field in required_fields:
        if not hasattr(config, field):
            raise ValueError(
                f"Campo obrigatório '{field}' não encontrado na configuração"
            )

    # Validar valores numéricos
    infra = config.INFRASTRUCTURE
    if infra["workstations_total"] <= 0:
        raise ValueError("Número total de workstations deve ser maior que zero")

    if infra["fator_emissao_co2_kg_kwh"] <= 0:
        raise ValueError("Fator de emissão CO₂ deve ser maior que zero")

    return True


# Exemplo de uso:
if __name__ == "__main__":
    config = get_config()
    validate_config(config)
    print("✅ Configuração validada com sucesso!")
    print(f"Ambiente: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"Total de workstations: {config.INFRASTRUCTURE['workstations_total']}")
    print(f"Setores configurados: {len(config.SETORES)}")
