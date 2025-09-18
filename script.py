# Vamos estruturar os dados coletados sobre o projeto de sustentabilidade da Renault
import pandas as pd
import json

# Dados da reunião com mentores Renault
reuniao_data = {
    "infraestrutura": {
        "datacenters": "2 datacenters Tier 3 no Complexo Ayrton Senna",
        "cloud": "Google Cloud Platform (GCP) na Bélgica",
        "servidores": "90 Servidores HP DL380 (ger. 8,9,10) + 10 VxRail T560F",
        "workstations": "5.376 estações no Brasil (ambiente office)",
        "energia_renovavel": "Não implementada atualmente",
        "area_verde": "Complexo possui área verde significativa"
    },
    "limitacoes_atuais": {
        "cloud": "Sem controle de consumo atual - estudo FinOps em andamento",
        "on_premise": "Ausência total de controle de horários, métricas de uso, monitoramento energético"
    },
    "escopo_projeto": {
        "foco": "Servidores e cloud (não equipamentos usuário final)",
        "exclusoes": "Equipamentos da produção industrial"
    }
}

# Tecnologias e funcionalidades identificadas
tecnologias_mvp = {
    "monitoramento": {
        "windows_registry": "Monitoramento via PowerShell e WMI",
        "acesso_remoto": "AnyDesk, TeamViewer para suporte",
        "sensores": "Coleta de dados de consumo em tempo real"
    },
    "analise_preditiva": {
        "machine_learning": "Algoritmos para previsão de demanda energética",
        "manutencao_preditiva": "Detecção de falhas antes que ocorram",
        "otimizacao": "Identificação de recursos ociosos"
    },
    "dashboard": {
        "tempo_real": "Métricas de consumo energético",
        "calculadora_carbono": "Conversão energia -> CO2 -> árvores",
        "alertas": "Notificações para economia de energia",
        "relatórios": "Informações executivas"
    }
}

# Cálculos básicos de sustentabilidade
calculos_sustentabilidade = {
    "fator_emissao_energia": "0.0817 kg CO2/kWh (Brasil - matriz energética 2023)",
    "arvore_sequestro_anual": "22 kg CO2/ano (árvore adulta média)",
    "economia_energia_shutdown": "150-300W por workstation ociosa",
    "potencial_economia_anual": "5376 workstations * 250W * 8h/dia * 250 dias = 2.688 MWh/ano"
}

print("=== RESUMO DOS DADOS COLETADOS ===\n")
print("1. INFRAESTRUTURA ATUAL RENAULT:")
for key, value in reuniao_data["infraestrutura"].items():
    print(f"   {key}: {value}")

print("\n2. LIMITAÇÕES IDENTIFICADAS:")
for key, value in reuniao_data["limitacoes_atuais"].items():
    print(f"   {key}: {value}")

print("\n3. TECNOLOGIAS PARA MVP:")
for categoria, techs in tecnologias_mvp.items():
    print(f"   {categoria.upper()}:")
    for tech, desc in techs.items():
        print(f"     - {tech}: {desc}")

print("\n4. CÁLCULOS DE SUSTENTABILIDADE:")
for calc, value in calculos_sustentabilidade.items():
    print(f"   {calc}: {value}")

# Estimativa de impacto potencial
workstations = 5376
potencia_media_w = 250  # watts por workstation
horas_ociosas_dia = 8   # assumindo 8h ociosas por dia
dias_uteis_ano = 250

consumo_anual_kwh = (workstations * potencia_media_w * horas_ociosas_dia * dias_uteis_ano) / 1000
emissoes_co2_kg = consumo_anual_kwh * 0.0817  # fator de emissão Brasil
arvores_equivalentes = emissoes_co2_kg / 22  # sequestro médio por árvore/ano

print(f"\n=== ESTIMATIVA DE IMPACTO POTENCIAL ===")
print(f"Consumo anual potencial de economia: {consumo_anual_kwh:,.0f} kWh")
print(f"Emissões CO2 evitadas: {emissoes_co2_kg:,.0f} kg/ano")
print(f"Equivalente a plantar: {arvores_equivalentes:,.0f} árvores")
print(f"Economia financeira estimada: R$ {consumo_anual_kwh * 0.6:,.2f}/ano (R$ 0,60/kWh)")