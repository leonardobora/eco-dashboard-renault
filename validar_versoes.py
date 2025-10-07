#!/usr/bin/env python3
"""
Validação: Flask vs GitHub Pages
Compara os cálculos de métricas entre as duas versões
"""

import json
import subprocess
import sys

def test_flask_metrics():
    """Testa cálculos Python (Flask)"""
    print("🐍 Testando versão Flask (Python)...\n")
    
    # Import da aplicação Flask
    sys.path.insert(0, '.')
    from app_renault_mvp import infra
    
    metrics = {
        'consumo_atual': infra.consumo_atual,
        'emissoes_co2': infra.calcular_emissoes_anuais(),
        'economia_potencial': infra.calcular_economia_potencial(),
        'arvores_equivalentes': infra.calcular_arvores_equivalentes()
    }
    
    print("Métricas Flask:")
    print(json.dumps(metrics, indent=2))
    return metrics

def test_javascript_metrics():
    """Testa cálculos JavaScript (GitHub Pages)"""
    print("\n🌐 Testando versão GitHub Pages (JavaScript)...\n")
    
    js_code = """
    const RenaultInfrastructure = require('./static/js/metrics-calculator.js');
    const infra = new RenaultInfrastructure();
    const metrics = infra.getMetrics();
    console.log(JSON.stringify(metrics));
    """
    
    result = subprocess.run(
        ['node', '-e', js_code],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("❌ Erro ao executar JavaScript:")
        print(result.stderr)
        return None
    
    metrics = json.loads(result.stdout.strip())
    print("Métricas GitHub Pages:")
    print(json.dumps(metrics, indent=2))
    return metrics

def compare_metrics(flask_metrics, js_metrics):
    """Compara as métricas de ambas versões"""
    print("\n📊 Comparação de Resultados:\n")
    
    fields = ['consumo_atual', 'emissoes_co2', 'economia_potencial', 'arvores_equivalentes']
    all_match = True
    
    for field in fields:
        flask_val = flask_metrics.get(field, 0)
        js_val = js_metrics.get(field, 0)
        
        # Considerar valores iguais com tolerância de 0.01%
        match = abs(flask_val - js_val) < 0.01
        status = "✅" if match else "❌"
        
        print(f"{status} {field:25} | Flask: {flask_val:12.2f} | Pages: {js_val:12.2f}")
        
        if not match:
            all_match = False
    
    print("\n" + "="*70)
    if all_match:
        print("✅ SUCESSO! Ambas versões produzem métricas idênticas!")
    else:
        print("❌ FALHA! Existem diferenças entre as versões!")
    print("="*70)
    
    return all_match

def main():
    print("="*70)
    print("VALIDAÇÃO: FLASK vs GITHUB PAGES")
    print("Comparando cálculos de sustentabilidade entre versões")
    print("="*70 + "\n")
    
    try:
        # Testar ambas versões
        flask_metrics = test_flask_metrics()
        js_metrics = test_javascript_metrics()
        
        if js_metrics is None:
            print("\n❌ Não foi possível testar versão JavaScript")
            print("Certifique-se de que Node.js está instalado")
            sys.exit(1)
        
        # Comparar resultados
        success = compare_metrics(flask_metrics, js_metrics)
        
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"\n❌ Erro durante validação: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
