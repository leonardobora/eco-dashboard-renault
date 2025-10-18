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
        Detect idle or underutilized resources
        
        Returns:
            List of idle resource detections
        """
        workstation_data = self.carbon_loader.get_workstation_data()
        sectors = self.carbon_loader.get_sector_consumption()
        
        idle_resources = []
        
        # Analyze each sector for low utilization
        for sector in sectors:
            if sector["utilization"] < 0.75:  # Below 75% utilization
                idle_resources.append({
                    "resource_type": "workstations",
                    "sector": sector["name"],
                    "count": sector["workstations"],
                    "current_utilization": sector["utilization"],
                    "waste_percentage": round((1 - sector["utilization"]) * 100, 1),
                    "potential_savings_kwh": sector["annual_consumption_kwh"] * (0.75 - sector["utilization"])
                })
        
        return idle_resources
    
    def get_all_recommendations(self) -> List[Dict]:
        """
        Generate all AI-powered recommendations
        
        Returns:
            List of recommendations sorted by priority
        """
        recommendations = []
        
        # 1. Automatic shutdown recommendations
        recommendations.extend(self._get_shutdown_recommendations())
        
        # 2. Scheduling optimization
        recommendations.extend(self._get_scheduling_recommendations())
        
        # 3. Infrastructure optimization
        recommendations.extend(self._get_infrastructure_recommendations())
        
        # 4. Renewable energy recommendations
        recommendations.extend(self._get_renewable_recommendations())
        
        # 5. Cooling optimization
        recommendations.extend(self._get_cooling_recommendations())
        
        # Sort by priority (critical -> high -> medium -> low)
        priority_order = {
            RecommendationPriority.CRITICAL: 0,
            RecommendationPriority.HIGH: 1,
            RecommendationPriority.MEDIUM: 2,
            RecommendationPriority.LOW: 3
        }
        
        recommendations.sort(key=lambda r: priority_order[r.priority])
        
        return [r.to_dict() for r in recommendations]
    
    def _get_shutdown_recommendations(self) -> List[Recommendation]:
        """Generate recommendations for automatic shutdown"""
        recommendations = []
        
        opt_data = self.carbon_loader.get_optimization_potential()
        
        rec = Recommendation(
            title="Implementar Desligamento Automático de Workstations Ociosas",
            description=f"Identificamos {opt_data['optimizable_workstations']} workstations "
                       f"que ficam ligadas fora do horário comercial sem uso. Implementar "
                       f"desligamento automático pode reduzir o consumo em {opt_data['reduction_percentage']:.0f}%.",
            category=RecommendationCategory.AUTOMATION,
            priority=RecommendationPriority.HIGH,
            impact_kwh=opt_data['annual_savings_kwh'],
            impact_co2_kg=opt_data['co2_reduction_kg'],
            impact_brl=opt_data['annual_savings_brl'],
            implementation_effort="Médio - Requer configuração de políticas de grupo",
            estimated_time="2-3 semanas"
        )
        recommendations.append(rec)
        
        return recommendations
    
    def _get_scheduling_recommendations(self) -> List[Recommendation]:
        """Generate recommendations for task scheduling optimization"""
        recommendations = []
        
        energy_costs = self.carbon_loader.get_energy_costs()
        
        # Estimate impact of avoiding peak hours
        peak_hours_duration = 3  # 18:00 to 21:00
        daily_peak_consumption = 500  # kW estimated
        annual_peak_kwh = daily_peak_consumption * peak_hours_duration * 250  # working days
        peak_extra_cost = annual_peak_kwh * energy_costs['tariff_brl_kwh'] * (energy_costs['peak_multiplier'] - 1)
        
        rec = Recommendation(
            title="Agendar Tarefas Pesadas Fora do Horário de Pico",
            description="Processos de alta carga (backups, compilações, relatórios) estão sendo "
                       "executados durante o horário de pico (18h-21h), quando a energia é 50% "
                       "mais cara. Recomendamos agendar para madrugada (23h-6h).",
            category=RecommendationCategory.COST_OPTIMIZATION,
            priority=RecommendationPriority.MEDIUM,
            impact_kwh=0,  # Same consumption, different cost
            impact_co2_kg=0,
            impact_brl=peak_extra_cost,
            implementation_effort="Baixo - Ajuste de agendamento de tarefas",
            estimated_time="1 semana"
        )
        recommendations.append(rec)
        
        return recommendations
    
    def _get_infrastructure_recommendations(self) -> List[Recommendation]:
        """Generate infrastructure optimization recommendations"""
        recommendations = []
        
        server_data = self.carbon_loader.get_server_data()
        
        # Check for underutilized servers
        for server_type, data in server_data.items():
            if data['utilization'] < 0.70:
                potential_savings_kwh = (data['count'] * data['avg_consumption_w'] * 
                                        (0.70 - data['utilization']) * 24 * 365) / 1000
                
                rec = Recommendation(
                    title=f"Consolidar Cargas de Trabalho - {server_type.replace('_', ' ').title()}",
                    description=f"Servidores {server_type} estão com utilização de apenas "
                               f"{data['utilization']*100:.0f}%. Consolidar VMs e containers pode "
                               f"reduzir o número de servidores físicos necessários.",
                    category=RecommendationCategory.INFRASTRUCTURE,
                    priority=RecommendationPriority.MEDIUM,
                    impact_kwh=potential_savings_kwh,
                    impact_co2_kg=potential_savings_kwh * self.carbon_loader.get_emission_factor(),
                    impact_brl=potential_savings_kwh * self.carbon_loader.get_energy_costs()['tariff_brl_kwh'],
                    implementation_effort="Alto - Requer planejamento e migração de cargas",
                    estimated_time="2-3 meses"
                )
                recommendations.append(rec)
        
        return recommendations
    
    def _get_renewable_recommendations(self) -> List[Recommendation]:
        """Generate renewable energy recommendations"""
        recommendations = []
        
        # Calculate potential impact of solar panels
        workstation_data = self.carbon_loader.get_workstation_data()
        total_consumption_kwh = (workstation_data['total'] * workstation_data['avg_consumption_w'] 
                                * 0.75 * 24 * 365) / 1000  # 75% avg utilization
        
        # Assume solar could provide 20% of energy needs
        solar_potential_kwh = total_consumption_kwh * 0.20
        
        # CO2 reduction from switching to renewable
        current_emissions = solar_potential_kwh * self.carbon_loader.get_emission_factor('brazil_grid')
        renewable_emissions = solar_potential_kwh * self.carbon_loader.get_emission_factor('renewable_energy')
        co2_reduction = current_emissions - renewable_emissions
        
        rec = Recommendation(
            title="Implementar Energia Solar Fotovoltaica no Telhado",
            description="Instalação de painéis solares pode suprir 20% da demanda energética da TI. "
                       "Com o custo atual da energia, o payback é estimado em 4-5 anos, com "
                       "redução significativa de emissões de CO2.",
            category=RecommendationCategory.CARBON_REDUCTION,
            priority=RecommendationPriority.LOW,
            impact_kwh=solar_potential_kwh,
            impact_co2_kg=co2_reduction,
            impact_brl=solar_potential_kwh * self.carbon_loader.get_energy_costs()['tariff_brl_kwh'] * 0.80,  # 80% savings after installation
            implementation_effort="Muito Alto - Investimento em infraestrutura física",
            estimated_time="6-12 meses"
        )
        recommendations.append(rec)
        
        return recommendations
    
    def _get_cooling_recommendations(self) -> List[Recommendation]:
        """Generate cooling optimization recommendations"""
        recommendations = []
        
        # Estimate cooling represents 40% of datacenter energy
        server_data = self.carbon_loader.get_server_data()
        total_server_consumption = sum(
            data['count'] * data['avg_consumption_w'] 
            for data in server_data.values()
        )
        
        # Cooling consumption
        cooling_consumption_w = total_server_consumption * 0.40
        annual_cooling_kwh = (cooling_consumption_w * 24 * 365) / 1000
        
        # Potential 15% savings with optimization
        savings_kwh = annual_cooling_kwh * 0.15
        
        rec = Recommendation(
            title="Otimizar Sistema de Refrigeração do Datacenter",
            description="Ajustar temperaturas de operação para 25°C (atualmente 21°C) e "
                       "implementar corredores quentes/frios pode reduzir consumo de refrigeração "
                       "em até 15%, conforme padrões ASHRAE.",
            category=RecommendationCategory.ENERGY_SAVINGS,
            priority=RecommendationPriority.HIGH,
            impact_kwh=savings_kwh,
            impact_co2_kg=savings_kwh * self.carbon_loader.get_emission_factor(),
            impact_brl=savings_kwh * self.carbon_loader.get_energy_costs()['tariff_brl_kwh'],
            implementation_effort="Médio - Ajustes de configuração e organização física",
            estimated_time="1-2 meses"
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
