"""
AI-powered Recommendations Engine
Provides intelligent suggestions for energy optimization and carbon reduction
"""

import datetime
from typing import List, Dict, Optional
from enum import Enum


class RecommendationPriority(Enum):
    """Priority levels for recommendations"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecommendationCategory(Enum):
    """Categories of recommendations"""
    ENERGY_SAVINGS = "energy_savings"
    CARBON_REDUCTION = "carbon_reduction"
    COST_OPTIMIZATION = "cost_optimization"
    AUTOMATION = "automation"
    INFRASTRUCTURE = "infrastructure"


class Recommendation:
    """Individual recommendation with details"""
    
    def __init__(
        self,
        title: str,
        description: str,
        category: RecommendationCategory,
        priority: RecommendationPriority,
        impact_kwh: float,
        impact_co2_kg: float,
        impact_brl: float,
        implementation_effort: str,
        estimated_time: str
    ):
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.impact_kwh = impact_kwh
        self.impact_co2_kg = impact_co2_kg
        self.impact_brl = impact_brl
        self.implementation_effort = implementation_effort
        self.estimated_time = estimated_time
        self.created_at = datetime.datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "title": self.title,
            "description": self.description,
            "category": self.category.value,
            "priority": self.priority.value,
            "impact": {
                "energy_savings_kwh": round(self.impact_kwh, 2),
                "co2_reduction_kg": round(self.impact_co2_kg, 2),
                "cost_savings_brl": round(self.impact_brl, 2)
            },
            "implementation": {
                "effort": self.implementation_effort,
                "estimated_time": self.estimated_time
            },
            "created_at": self.created_at.isoformat()
        }


class RecommendationsEngine:
    """
    AI Engine for generating intelligent recommendations
    Analyzes consumption patterns and suggests optimization actions
    """
    
    def __init__(self, carbon_data_loader=None):
        """
        Initialize the recommendations engine
        
        Args:
            carbon_data_loader: CarbonDataLoader instance for data access
        """
        from data_sources.carbon_data import get_carbon_data_loader
        self.carbon_loader = carbon_data_loader or get_carbon_data_loader()
    
    def detect_idle_resources(self) -> List[Dict]:
        """
        Detect idle or underutilized server resources
        
        Returns:
            List of idle resource detections
        """
        server_metrics = self.carbon_loader.get_server_metrics()
        
        idle_resources = []
        
        # Analyze each server type for low utilization
        for server in server_metrics:
            if server["utilization_percent"] < 50:  # Below 50% utilization
                idle_resources.append({
                    "resource_type": "servers",
                    "server_type": server["type"],
                    "model": server["model"],
                    "count": server["count"],
                    "current_utilization": server["utilization_percent"],
                    "waste_percentage": round((50 - server["utilization_percent"]), 1),
                    "potential_savings_kwh": server["annual_consumption_kwh"] * ((50 - server["utilization_percent"]) / 100)
                })
        
        return idle_resources
    
    def get_all_recommendations(self) -> List[Dict]:
        """
        Generate all AI-powered recommendations for datacenter optimization
        
        Returns:
            List of recommendations sorted by priority
        """
        recommendations = []
        
        # 1. Virtualization and consolidation
        recommendations.extend(self._get_virtualization_recommendations())
        
        # 2. PUE optimization
        recommendations.extend(self._get_pue_optimization_recommendations())
        
        # 3. Resource scaling
        recommendations.extend(self._get_resource_scaling_recommendations())
        
        # 4. Cooling datacenter optimization
        recommendations.extend(self._get_cooling_recommendations())
        
        # 5. Renewable energy recommendations
        recommendations.extend(self._get_renewable_recommendations())
        
        # Sort by priority (critical -> high -> medium -> low)
        priority_order = {
            RecommendationPriority.CRITICAL: 0,
            RecommendationPriority.HIGH: 1,
            RecommendationPriority.MEDIUM: 2,
            RecommendationPriority.LOW: 3
        }
        
        recommendations.sort(key=lambda r: priority_order[r.priority])
        
        return [r.to_dict() for r in recommendations]
    
    def _get_virtualization_recommendations(self) -> List[Recommendation]:
        """Generate recommendations for virtualization and server consolidation"""
        recommendations = []
        
        consolidation = self.carbon_loader.get_consolidation_potential()
        
        if consolidation["servers_to_consolidate"] > 0:
            rec = Recommendation(
                title=f"Consolidar {consolidation['servers_to_consolidate']} Servidores HP ProLiant via Virtualização",
                description=f"Identificamos {consolidation['servers_to_consolidate']} servidores HP ProLiant "
                           f"com baixa utilização (35%). Consolidando cargas de trabalho para os VxRail "
                           f"existentes, podemos reduzir o consumo em {consolidation['reduction_percent']:.1f}%. "
                           f"Economia estimada: R$ {consolidation['cost_savings_brl']:,.2f}/ano.",
                category=RecommendationCategory.INFRASTRUCTURE,
                priority=RecommendationPriority.HIGH,
                impact_kwh=consolidation['energy_savings_kwh'],
                impact_co2_kg=consolidation['co2_reduction_kg'],
                impact_brl=consolidation['cost_savings_brl'],
                implementation_effort="Alto - Requer planejamento e migração de VMs",
                estimated_time="2-3 meses"
            )
            recommendations.append(rec)
        
        # VM auto-scaling recommendation
        server_metrics = self.carbon_loader.get_server_metrics()
        vxrail = next((s for s in server_metrics if s["type"] == "vxrail"), None)
        
        if vxrail and vxrail["vm_density"] > 0:
            estimated_savings_kwh = vxrail["annual_consumption_kwh"] * 0.15  # 15% savings
            estimated_co2 = estimated_savings_kwh * self.carbon_loader.get_emission_factor()
            estimated_brl = estimated_savings_kwh * self.carbon_loader.get_energy_costs().get("base_rate_brl_per_kwh", 0.60)
            
            rec = Recommendation(
                title="Implementar Auto-Scaling de VMs em Horários de Baixa Demanda",
                description=f"VMs em VxRail mantêm recursos alocados 24/7. Implementar políticas de "
                           f"auto-scaling pode reduzir alocação de CPU/RAM em 40% durante período "
                           f"noturno (23h-7h), economizando 15% do consumo total dos VxRails.",
                category=RecommendationCategory.AUTOMATION,
                priority=RecommendationPriority.MEDIUM,
                impact_kwh=estimated_savings_kwh,
                impact_co2_kg=estimated_co2,
                impact_brl=estimated_brl,
                implementation_effort="Médio - Configuração de políticas DPM",
                estimated_time="3-4 semanas"
            )
            recommendations.append(rec)
        
        return recommendations
    
    def _get_pue_optimization_recommendations(self) -> List[Recommendation]:
        """Generate recommendations for PUE optimization"""
        recommendations = []
        
        cooling = self.carbon_loader.get_cooling_efficiency()
        datacenter = self.carbon_loader.get_datacenter_data()
        
        # Temperature setpoint adjustment
        temp_savings_kwh = cooling["annual_savings_kwh"] * 0.30  # 30% from temp adjustment
        temp_co2 = temp_savings_kwh * self.carbon_loader.get_emission_factor()
        temp_brl = temp_savings_kwh * self.carbon_loader.get_energy_costs().get("base_rate_brl_per_kwh", 0.60)
        
        current_temp = datacenter.get("temperature_setpoint_c", 22)
        
        rec = Recommendation(
            title=f"Aumentar Temperatura do Datacenter de {current_temp}°C para 24°C",
            description=f"Temperatura atual ({current_temp}°C) está abaixo das recomendações ASHRAE (24-27°C). "
                       f"Aumentar setpoint para 24°C pode reduzir consumo de cooling em até 10%, "
                       f"representando economia de {temp_savings_kwh:,.0f} kWh/ano sem impacto nos equipamentos.",
            category=RecommendationCategory.ENERGY_SAVINGS,
            priority=RecommendationPriority.HIGH,
            impact_kwh=temp_savings_kwh,
            impact_co2_kg=temp_co2,
            impact_brl=temp_brl,
            implementation_effort="Baixo - Ajuste de configuração CRAC",
            estimated_time="1 semana"
        )
        recommendations.append(rec)
        
        # Hot/Cold aisle containment
        containment_savings_kwh = cooling["annual_savings_kwh"] * 0.40  # 40% from containment
        containment_co2 = containment_savings_kwh * self.carbon_loader.get_emission_factor()
        containment_brl = containment_savings_kwh * self.carbon_loader.get_energy_costs().get("base_rate_brl_per_kwh", 0.60)
        
        rec = Recommendation(
            title="Implementar Hot/Cold Aisle Containment",
            description="Segregar corredores quentes e frios com painéis de contenção melhora "
                       "eficiência do fluxo de ar e reduz mistura de temperaturas. Pode reduzir "
                       "consumo de cooling em 15-20%, melhorando PUE de 2.0 para 1.6.",
            category=RecommendationCategory.INFRASTRUCTURE,
            priority=RecommendationPriority.MEDIUM,
            impact_kwh=containment_savings_kwh,
            impact_co2_kg=containment_co2,
            impact_brl=containment_brl,
            implementation_effort="Médio - Instalação física de painéis",
            estimated_time="1-2 meses"
        )
        recommendations.append(rec)
        
        return recommendations
    
    def _get_resource_scaling_recommendations(self) -> List[Recommendation]:
        """Generate resource scaling and DPM recommendations"""
        recommendations = []
        
        # Get server consumption
        consumption = self.carbon_loader.get_datacenter_consumption()
        
        # Estimate savings from night-time scaling (23h-7h = 8 hours)
        night_hours = 8
        night_reduction = 0.40  # 40% reduction during night
        daily_night_savings_kwh = consumption["total_kwh"] * night_reduction * (night_hours / 24)
        annual_savings_kwh = daily_night_savings_kwh * 365
        
        savings_co2 = annual_savings_kwh * self.carbon_loader.get_emission_factor()
        savings_brl = annual_savings_kwh * self.carbon_loader.get_energy_costs().get("base_rate_brl_per_kwh", 0.60)
        
        rec = Recommendation(
            title="Implementar DPM (Distributed Power Management) para Horário Noturno",
            description="Reduzir alocação de CPU/RAM em 40% durante período noturno (23h-7h) "
                       "quando carga é apenas 15%. Implementar políticas de DPM em VMware para "
                       "colocar hosts em standby ou low-power mode automaticamente.",
            category=RecommendationCategory.AUTOMATION,
            priority=RecommendationPriority.HIGH,
            impact_kwh=annual_savings_kwh,
            impact_co2_kg=savings_co2,
            impact_brl=savings_brl,
            implementation_effort="Médio - Configuração vSphere DRS/DPM",
            estimated_time="2-3 semanas"
        )
        recommendations.append(rec)
        
        return recommendations
    
    def _get_renewable_recommendations(self) -> List[Recommendation]:
        """Generate renewable energy recommendations for datacenter"""
        recommendations = []
        
        # Calculate datacenter consumption
        consumption = self.carbon_loader.get_datacenter_consumption()
        annual_consumption_kwh = consumption["total_kwh"] * 24 * 365
        
        # Solar could provide 100kW capacity (target from config)
        datacenter = self.carbon_loader.get_datacenter_data()
        solar_capacity_kw = datacenter.get("renewable_target_kw", 100)
        
        # Estimate annual generation (capacity factor ~15% for Brazil)
        solar_annual_kwh = solar_capacity_kw * 24 * 365 * 0.15
        
        # CO2 reduction from switching to renewable
        current_emissions = solar_annual_kwh * self.carbon_loader.get_emission_factor('grid_brazil')
        renewable_emissions = solar_annual_kwh * self.carbon_loader.get_emission_factor('renewable')
        co2_reduction = current_emissions - renewable_emissions
        
        # Investment and payback
        solar_brl_savings = solar_annual_kwh * self.carbon_loader.get_energy_costs().get("base_rate_brl_per_kwh", 0.60)
        investment_brl = solar_capacity_kw * 4000  # R$4k per kW installed
        payback_months = int((investment_brl / solar_brl_savings) * 12) if solar_brl_savings > 0 else 0
        
        rec = Recommendation(
            title=f"Instalar {solar_capacity_kw}kW de Energia Solar no Telhado do Datacenter",
            description=f"Instalação de {solar_capacity_kw}kW em painéis solares pode suprir ~{solar_annual_kwh/annual_consumption_kwh*100:.0f}% "
                       f"da demanda do datacenter. Investimento: R$ {investment_brl:,.0f}, "
                       f"Payback: {payback_months} meses. Reduz dependência da rede e emissões de CO2.",
            category=RecommendationCategory.CARBON_REDUCTION,
            priority=RecommendationPriority.LOW,
            impact_kwh=solar_annual_kwh,
            impact_co2_kg=co2_reduction,
            impact_brl=solar_brl_savings,
            implementation_effort="Muito Alto - CAPEX R$ 400k, instalação física",
            estimated_time="6-8 meses"
        )
        recommendations.append(rec)
        
        return recommendations
    
    def _get_cooling_recommendations(self) -> List[Recommendation]:
        """Generate datacenter cooling optimization recommendations"""
        recommendations = []
        
        cooling = self.carbon_loader.get_cooling_efficiency()
        
        # Free cooling recommendation
        free_cooling_savings_kwh = cooling["annual_savings_kwh"] * 0.20  # 20% from free cooling
        free_cooling_co2 = free_cooling_savings_kwh * self.carbon_loader.get_emission_factor()
        free_cooling_brl = free_cooling_savings_kwh * self.carbon_loader.get_energy_costs().get("base_rate_brl_per_kwh", 0.60)
        
        rec = Recommendation(
            title="Implementar Free Cooling em Meses de Inverno (Jun-Ago)",
            description="São José dos Pinhais tem temperaturas de 10-15°C no inverno. "
                       "Implementar economizadores de ar externo (air-side economizers) pode "
                       "reduzir uso de CRAC em até 60% nos meses frios, economizando 8-10% "
                       "do consumo anual de cooling.",
            category=RecommendationCategory.ENERGY_SAVINGS,
            priority=RecommendationPriority.MEDIUM,
            impact_kwh=free_cooling_savings_kwh,
            impact_co2_kg=free_cooling_co2,
            impact_brl=free_cooling_brl,
            implementation_effort="Alto - Modificação de infraestrutura HVAC",
            estimated_time="3-4 meses"
        )
        recommendations.append(rec)
        
        # Sensor granularity
        sensor_savings_kwh = cooling["annual_savings_kwh"] * 0.10  # 10% from better monitoring
        sensor_co2 = sensor_savings_kwh * self.carbon_loader.get_emission_factor()
        sensor_brl = sensor_savings_kwh * self.carbon_loader.get_energy_costs().get("base_rate_brl_per_kwh", 0.60)
        
        rec = Recommendation(
            title="Instalar Sensores de Temperatura Granulares (por Rack)",
            description="Monitoramento atual é macro (sala toda). Instalar sensores por rack "
                       "permite identificar hot spots e ajustar cooling de forma localizada, "
                       "evitando super-resfriamento de áreas com baixa carga térmica.",
            category=RecommendationCategory.INFRASTRUCTURE,
            priority=RecommendationPriority.LOW,
            impact_kwh=sensor_savings_kwh,
            impact_co2_kg=sensor_co2,
            impact_brl=sensor_brl,
            implementation_effort="Baixo - Instalação de sensores IoT",
            estimated_time="2-3 semanas"
        )
        recommendations.append(rec)
        
        return recommendations
    
    def get_top_recommendations(self, limit: int = 5) -> List[Dict]:
        """
        Get top N recommendations by priority and impact
        
        Args:
            limit: Number of recommendations to return
            
        Returns:
            List of top recommendations
        """
        all_recommendations = self.get_all_recommendations()
        return all_recommendations[:limit]
    
    def get_recommendations_by_category(self, category: str) -> List[Dict]:
        """
        Get recommendations filtered by category
        
        Args:
            category: Category name (energy_savings, carbon_reduction, etc.)
            
        Returns:
            Filtered list of recommendations
        """
        all_recommendations = self.get_all_recommendations()
        return [r for r in all_recommendations if r['category'] == category]


# Singleton instance
_recommendations_engine = None

def get_recommendations_engine() -> RecommendationsEngine:
    """Get or create singleton instance of RecommendationsEngine"""
    global _recommendations_engine
    if _recommendations_engine is None:
        _recommendations_engine = RecommendationsEngine()
    return _recommendations_engine
