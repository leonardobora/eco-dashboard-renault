/**
 * EcoTI Metrics Calculator - Static Version
 * 
 * JavaScript implementation of the RenaultInfrastructure class
 * Originally written in Python (app_renault_mvp.py)
 * 
 * This allows the dashboard to work on GitHub Pages without a backend server
 */

class RenaultInfrastructure {
    constructor() {
        // Infrastructure configuration
        this.workstations = 5376;
        this.servidores_hp = 90;
        this.vxrail = 10;
        this.consumo_medio_w = 250;  // Watts per workstation
        this.fator_emissao = 0.0817;  // kg CO2/kWh (Brazil grid)
        this.sequestro_arvore = 22;   // kg CO2/year per tree
        this.tarifa_energia = 0.60;   // R$/kWh
        
        // Current state (simulated)
        this.workstations_ativas = 4200;
        this.servidores_ativos = 85;
        this.consumo_atual = this.calcularConsumoAtual();
    }
    
    /**
     * Calculate current energy consumption based on time of day
     * @returns {number} Current consumption in kWh
     */
    calcularConsumoAtual() {
        const hora_atual = new Date().getHours();
        let fator_uso;
        
        if (hora_atual >= 8 && hora_atual <= 18) {
            // Business hours - 80% usage
            fator_uso = 0.8;
        } else if (hora_atual >= 19 && hora_atual <= 22) {
            // Evening - 40% usage
            fator_uso = 0.4;
        } else {
            // Night - 20% usage
            fator_uso = 0.2;
        }
        
        // Workstations consumption
        const consumo_workstations = 
            (this.workstations_ativas * this.consumo_medio_w * fator_uso) / 1000;
        
        // Servers consumption (400W per server, constant)
        const consumo_servidores = this.servidores_ativos * 400 / 1000;
        
        return consumo_workstations + consumo_servidores;
    }
    
    /**
     * Calculate annual CO2 emissions
     * @returns {number} Annual emissions in kg CO2
     */
    calcularEmissoesAnuais() {
        const consumo_anual = this.consumo_atual * 24 * 365;
        return consumo_anual * this.fator_emissao;
    }
    
    /**
     * Calculate equivalent number of trees needed
     * @returns {number} Number of trees
     */
    calcularArvoresEquivalentes() {
        const emissoes = this.calcularEmissoesAnuais();
        return Math.floor(emissoes / this.sequestro_arvore);
    }
    
    /**
     * Calculate potential cost savings
     * @returns {number} Potential savings in R$/year
     */
    calcularEconomiaPotencial() {
        const workstations_ociosas = this.workstations - this.workstations_ativas;
        // 8 hours/day, 250 working days/year
        const economia_kwh = 
            (workstations_ociosas * this.consumo_medio_w * 8 * 250) / 1000;
        return economia_kwh * this.tarifa_energia;
    }
    
    /**
     * Get all metrics at once
     * @returns {Object} All sustainability metrics
     */
    getMetrics() {
        this.consumo_atual = this.calcularConsumoAtual();
        return {
            consumo_atual: this.consumo_atual,
            emissoes_co2: this.calcularEmissoesAnuais(),
            economia_potencial: this.calcularEconomiaPotencial(),
            arvores_equivalentes: this.calcularArvoresEquivalentes()
        };
    }
}

// Export to global scope for use in app.js
if (typeof window !== 'undefined') {
    window.RenaultInfrastructure = RenaultInfrastructure;
}

// Export for Node.js/testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RenaultInfrastructure;
}
