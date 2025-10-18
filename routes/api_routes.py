"""
Additional API routes for EcoTI Dashboard
Extended endpoints for demonstration and advanced features
"""

from flask import Blueprint, jsonify, request
from data_sources.carbon_data import get_carbon_data_loader
from ai_engine.recommendations import get_recommendations_engine

# Create blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize data sources
carbon_loader = get_carbon_data_loader()
recommendations_engine = get_recommendations_engine()


@api_bp.route('/sectors', methods=['GET'])
def get_sectors():
    """
    Get consumption data by sector/department
    
    Returns detailed breakdown of energy consumption and CO2 emissions by sector
    """
    try:
        sectors = carbon_loader.get_sector_consumption()
        
        return jsonify({
            "success": True,
            "data": {
                "sectors": sectors,
                "total_workstations": sum(s['workstations'] for s in sectors),
                "total_consumption_kw": sum(s['consumption_kw'] for s in sectors),
                "total_annual_kwh": sum(s['annual_consumption_kwh'] for s in sectors),
                "total_co2_kg": sum(s['annual_co2_kg'] for s in sectors)
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@api_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    """
    Get AI-powered optimization recommendations
    
    Query parameters:
        - limit: Number of recommendations to return (default: 5)
        - category: Filter by category (optional)
    """
    try:
        limit = request.args.get('limit', 5, type=int)
        category = request.args.get('category', None, type=str)
        
        if category:
            recommendations = recommendations_engine.get_recommendations_by_category(category)
        else:
            recommendations = recommendations_engine.get_top_recommendations(limit)
        
        # Calculate total impact
        total_impact = {
            "energy_savings_kwh": sum(r['impact']['energy_savings_kwh'] for r in recommendations),
            "co2_reduction_kg": sum(r['impact']['co2_reduction_kg'] for r in recommendations),
            "cost_savings_brl": sum(r['impact']['cost_savings_brl'] for r in recommendations)
        }
        
        return jsonify({
            "success": True,
            "data": {
                "recommendations": recommendations,
                "count": len(recommendations),
                "total_impact": total_impact
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@api_bp.route('/savings', methods=['GET'])
def get_savings():
    """
    Get detailed savings projections and optimization potential
    
    Returns comprehensive analysis of potential savings from optimization
    """
    try:
        optimization_data = carbon_loader.get_optimization_potential()
        idle_resources = recommendations_engine.detect_idle_resources()
        
        # Calculate additional savings opportunities
        server_data = carbon_loader.get_server_data()
        total_server_power = sum(
            data['count'] * data['avg_consumption_w'] 
            for data in server_data.values()
        )
        
        # Potential from server consolidation (10% savings)
        server_savings_kwh = (total_server_power * 0.10 * 24 * 365) / 1000
        server_savings_brl = server_savings_kwh * carbon_loader.get_energy_costs()['tariff_brl_kwh']
        server_co2_reduction = server_savings_kwh * carbon_loader.get_emission_factor()
        
        return jsonify({
            "success": True,
            "data": {
                "workstation_optimization": {
                    "optimizable_workstations": optimization_data['optimizable_workstations'],
                    "annual_savings_kwh": optimization_data['annual_savings_kwh'],
                    "annual_savings_brl": optimization_data['annual_savings_brl'],
                    "co2_reduction_kg": optimization_data['co2_reduction_kg'],
                    "trees_equivalent": optimization_data['trees_equivalent']
                },
                "server_optimization": {
                    "potential_savings_kwh": server_savings_kwh,
                    "potential_savings_brl": server_savings_brl,
                    "co2_reduction_kg": server_co2_reduction,
                    "strategy": "Consolidação de cargas de trabalho"
                },
                "idle_resources": idle_resources,
                "total_potential": {
                    "annual_savings_kwh": optimization_data['annual_savings_kwh'] + server_savings_kwh,
                    "annual_savings_brl": optimization_data['annual_savings_brl'] + server_savings_brl,
                    "co2_reduction_kg": optimization_data['co2_reduction_kg'] + server_co2_reduction,
                    "reduction_percentage": round(
                        ((optimization_data['annual_savings_kwh'] + server_savings_kwh) / 
                         (optimization_data['annual_savings_kwh'] / 0.20)) * 100, 1
                    )
                }
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@api_bp.route('/trends', methods=['GET'])
def get_trends():
    """
    Get consumption trends and predictive analysis
    
    Query parameters:
        - period: Time period for analysis (day, week, month, year)
    """
    try:
        import datetime
        
        period = request.args.get('period', 'day', type=str)
        
        # Generate trend data based on usage patterns
        usage_patterns = carbon_loader.get_usage_patterns()
        
        if period == 'day':
            # Hourly trend for 24 hours
            trends = []
            for hour in range(24):
                utilization = carbon_loader.calculate_utilization_factor(hour)
                workstation_data = carbon_loader.get_workstation_data()
                
                consumption_kw = (workstation_data['total'] * workstation_data['avg_consumption_w'] 
                                 * utilization) / 1000
                
                trends.append({
                    "hour": hour,
                    "timestamp": f"{hour:02d}:00",
                    "consumption_kw": round(consumption_kw, 2),
                    "utilization": round(utilization * 100, 1),
                    "co2_kg": round(consumption_kw * carbon_loader.get_emission_factor(), 2),
                    "cost_brl": round(consumption_kw * carbon_loader.get_energy_costs()['tariff_brl_kwh'], 2)
                })
            
            return jsonify({
                "success": True,
                "data": {
                    "period": period,
                    "trends": trends,
                    "peak_hour": max(trends, key=lambda x: x['consumption_kw'])['hour'],
                    "lowest_hour": min(trends, key=lambda x: x['consumption_kw'])['hour'],
                    "average_consumption_kw": sum(t['consumption_kw'] for t in trends) / len(trends)
                }
            })
        
        elif period == 'week':
            # Daily trend for 7 days
            trends = []
            for day in range(7):
                # Simulate weekly pattern (lower on weekends)
                is_weekend = day in [5, 6]  # Saturday, Sunday
                base_utilization = 0.30 if is_weekend else 0.75
                
                workstation_data = carbon_loader.get_workstation_data()
                daily_consumption_kwh = (workstation_data['total'] * workstation_data['avg_consumption_w'] 
                                        * base_utilization * 24) / 1000
                
                trends.append({
                    "day": day,
                    "day_name": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"][day],
                    "consumption_kwh": round(daily_consumption_kwh, 2),
                    "utilization": round(base_utilization * 100, 1),
                    "co2_kg": round(daily_consumption_kwh * carbon_loader.get_emission_factor(), 2),
                    "cost_brl": round(daily_consumption_kwh * carbon_loader.get_energy_costs()['tariff_brl_kwh'], 2)
                })
            
            return jsonify({
                "success": True,
                "data": {
                    "period": period,
                    "trends": trends,
                    "total_weekly_kwh": sum(t['consumption_kwh'] for t in trends),
                    "average_daily_kwh": sum(t['consumption_kwh'] for t in trends) / len(trends)
                }
            })
        
        else:
            return jsonify({
                "success": False,
                "error": "Invalid period. Use 'day', 'week', 'month', or 'year'"
            }), 400
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "status": "healthy",
        "version": "2.0.0",
        "endpoints": [
            "/api/metrics",
            "/api/sectors",
            "/api/recommendations",
            "/api/savings",
            "/api/trends"
        ]
    })
