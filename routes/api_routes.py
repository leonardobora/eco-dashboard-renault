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


@api_bp.route('/servers', methods=['GET'])
def get_servers():
    """
    Get detailed metrics for all servers
    
    Returns detailed breakdown of server consumption, utilization, and specs
    """
    try:
        server_metrics = carbon_loader.get_server_metrics()
        
        total_consumption_kw = sum(s['consumption_kw'] for s in server_metrics)
        total_annual_kwh = sum(s['annual_consumption_kwh'] for s in server_metrics)
        total_co2_kg = sum(s['annual_co2_kg'] for s in server_metrics)
        
        return jsonify({
            "success": True,
            "data": {
                "servers": server_metrics,
                "summary": {
                    "total_servers": sum(s['count'] for s in server_metrics),
                    "total_consumption_kw": round(total_consumption_kw, 2),
                    "total_annual_kwh": round(total_annual_kwh, 2),
                    "total_co2_kg": round(total_co2_kg, 2),
                    "avg_utilization_percent": round(
                        sum(s['utilization_percent'] * s['count'] for s in server_metrics) / 
                        sum(s['count'] for s in server_metrics), 1
                    ) if server_metrics else 0
                }
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@api_bp.route('/consolidation', methods=['GET'])
def get_consolidation_analysis():
    """
    Get server consolidation analysis and potential
    
    Returns analysis of consolidation opportunities via virtualization
    """
    try:
        consolidation = carbon_loader.get_consolidation_potential()
        
        return jsonify({
            "success": True,
            "data": consolidation
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@api_bp.route('/pue', methods=['GET'])
def get_pue_metrics():
    """
    Get PUE (Power Usage Effectiveness) metrics
    
    Returns current PUE, target, and breakdown of datacenter consumption
    """
    try:
        cooling = carbon_loader.get_cooling_efficiency()
        datacenter = carbon_loader.get_datacenter_data()
        consumption = carbon_loader.get_datacenter_consumption()
        
        return jsonify({
            "success": True,
            "data": {
                "pue": {
                    "current": cooling["current_pue"],
                    "target": cooling["target_pue"],
                    "best_practice": datacenter.get("pue_best_practice", 1.2)
                },
                "breakdown": {
                    "servers_kwh": consumption["servers_kwh"],
                    "cooling_kwh": consumption["cooling_kwh"],
                    "total_kwh": consumption["total_kwh"]
                },
                "cooling_efficiency": cooling,
                "location": datacenter.get("location", "Unknown")
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@api_bp.route('/virtualization', methods=['GET'])
def get_virtualization_metrics():
    """
    Get virtualization metrics and VM density
    
    Returns VM density, consolidation opportunities, and hypervisor info
    """
    try:
        server_metrics = carbon_loader.get_server_metrics()
        consolidation = carbon_loader.get_consolidation_potential()
        
        # Extract VxRail VM info
        vxrail = next((s for s in server_metrics if s["type"] == "vxrail"), None)
        
        vm_info = {}
        if vxrail:
            total_vms = vxrail["count"] * vxrail["vm_density"]
            vm_info = {
                "total_vms": total_vms,
                "vms_per_host": vxrail["vm_density"],
                "hypervisor": vxrail["virtualization"],
                "host_count": vxrail["count"]
            }
        
        return jsonify({
            "success": True,
            "data": {
                "vm_metrics": vm_info,
                "consolidation_opportunities": {
                    "servers_can_consolidate": consolidation["servers_to_consolidate"],
                    "reduction_percent": consolidation["reduction_percent"],
                    "energy_savings_kwh": consolidation["energy_savings_kwh"],
                    "cost_savings_brl": consolidation["cost_savings_brl"]
                },
                "server_details": server_metrics
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
    Get detailed savings projections from datacenter optimization
    
    Returns comprehensive analysis of potential savings from virtualization and PUE optimization
    """
    try:
        optimization_data = carbon_loader.get_optimization_potential()
        consolidation = carbon_loader.get_consolidation_potential()
        cooling = carbon_loader.get_cooling_efficiency()
        idle_resources = recommendations_engine.detect_idle_resources()
        
        return jsonify({
            "success": True,
            "data": {
                "consolidation_savings": {
                    "servers_to_consolidate": consolidation['servers_to_consolidate'],
                    "annual_savings_kwh": consolidation['energy_savings_kwh'],
                    "annual_savings_brl": consolidation['cost_savings_brl'],
                    "co2_reduction_kg": consolidation['co2_reduction_kg'],
                    "strategy": "Consolidação via virtualização"
                },
                "pue_optimization": {
                    "current_pue": cooling['current_pue'],
                    "target_pue": cooling['target_pue'],
                    "annual_savings_kwh": cooling['annual_savings_kwh'],
                    "cooling_power_kw": cooling['cooling_power_kw'],
                    "strategy": "Otimização de cooling e PUE"
                },
                "idle_resources": idle_resources,
                "total_potential": {
                    "annual_savings_kwh": optimization_data['annual_savings_kwh'],
                    "annual_savings_brl": optimization_data['annual_savings_brl'],
                    "co2_reduction_kg": optimization_data['co2_reduction_kg'],
                    "trees_equivalent": optimization_data['trees_equivalent'],
                    "reduction_percentage": optimization_data['reduction_percentage'],
                    "payback_months": 13  # From issue: R$200k investment, R$185k/year savings
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
    Get datacenter consumption trends and load patterns
    
    Query parameters:
        - period: Time period for analysis (day, week)
    """
    try:
        import datetime
        
        period = request.args.get('period', 'day', type=str)
        
        if period == 'day':
            # Hourly trend for 24 hours - server load patterns
            trends = []
            for hour in range(24):
                load_factor = carbon_loader.calculate_utilization_factor(hour)
                consumption_data = carbon_loader.get_datacenter_consumption(hour=hour)
                
                energy_costs = carbon_loader.get_energy_costs()
                is_peak = hour in energy_costs.get("peak_hours", [18, 19, 20, 21])
                cost_multiplier = energy_costs.get("peak_multiplier", 1.5) if is_peak else 1.0
                
                trends.append({
                    "hour": hour,
                    "timestamp": f"{hour:02d}:00",
                    "servers_kw": consumption_data["servers_kwh"],
                    "cooling_kw": consumption_data["cooling_kwh"],
                    "total_kw": consumption_data["total_kwh"],
                    "pue": consumption_data["pue"],
                    "load_percent": round(load_factor * 100, 1),
                    "is_peak_hour": is_peak,
                    "co2_kg": round(consumption_data["total_kwh"] * carbon_loader.get_emission_factor(), 2),
                    "cost_brl": round(consumption_data["total_kwh"] * energy_costs.get("base_rate_brl_per_kwh", 0.60) * cost_multiplier, 2)
                })
            
            return jsonify({
                "success": True,
                "data": {
                    "period": period,
                    "trends": trends,
                    "peak_hour": max(trends, key=lambda x: x['total_kw'])['hour'],
                    "lowest_hour": min(trends, key=lambda x: x['total_kw'])['hour'],
                    "average_consumption_kw": round(sum(t['total_kw'] for t in trends) / len(trends), 2),
                    "average_load_percent": round(sum(t['load_percent'] for t in trends) / len(trends), 1)
                }
            })
        
        elif period == 'week':
            # Daily trend for 7 days - datacenter runs 24/7 but with load variation
            trends = []
            for day in range(7):
                # Simulate weekly pattern (slightly lower on weekends)
                is_weekend = day in [5, 6]  # Saturday, Sunday
                avg_load = 0.50 if is_weekend else 0.60  # Servers run 24/7 but lower workload
                
                # Get average daily consumption
                daily_consumption_kwh = 0
                for hour in range(24):
                    hour_consumption = carbon_loader.get_datacenter_consumption(hour=hour)
                    daily_consumption_kwh += hour_consumption["total_kwh"]
                
                # Adjust by weekend factor
                if is_weekend:
                    daily_consumption_kwh *= 0.85
                
                energy_costs = carbon_loader.get_energy_costs()
                
                trends.append({
                    "day": day,
                    "day_name": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"][day],
                    "consumption_kwh": round(daily_consumption_kwh, 2),
                    "avg_load_percent": round(avg_load * 100, 1),
                    "co2_kg": round(daily_consumption_kwh * carbon_loader.get_emission_factor(), 2),
                    "cost_brl": round(daily_consumption_kwh * energy_costs.get("base_rate_brl_per_kwh", 0.60), 2)
                })
            
            return jsonify({
                "success": True,
                "data": {
                    "period": period,
                    "trends": trends,
                    "total_weekly_kwh": round(sum(t['consumption_kwh'] for t in trends), 2),
                    "average_daily_kwh": round(sum(t['consumption_kwh'] for t in trends) / len(trends), 2)
                }
            })
        
        else:
            return jsonify({
                "success": False,
                "error": "Invalid period. Use 'day' or 'week'"
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
        "version": "3.0.0",
        "scope": "datacenter-servers-only",
        "endpoints": [
            "/api/metrics",
            "/api/servers",
            "/api/consolidation",
            "/api/pue",
            "/api/virtualization",
            "/api/recommendations",
            "/api/savings",
            "/api/trends",
            "/api/health"
        ]
    })
