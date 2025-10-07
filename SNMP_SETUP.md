# 🔧 Guia de Configuração SNMP - EcoTI Dashboard Renault

## 📋 Visão Geral

Este documento fornece instruções detalhadas para configurar o monitoramento SNMP real dos servidores da infraestrutura Renault (90 HP DL380 + 10 VxRail T560F).

## ⚠️ Requisitos de Segurança

### SNMPv3 Obrigatório
- **APENAS SNMPv3** é permitido (SNMPv1/v2c são vulneráveis e **PROIBIDOS**)
- **Autenticação**: SHA (recomendado) ou MD5
- **Criptografia**: AES (recomendado) ou DES
- **Credenciais**: Nunca compartilhar ou versionar credenciais reais

### Boas Práticas
- Use senhas fortes (mínimo 8 caracteres)
- Rotacione credenciais periodicamente (a cada 90 dias)
- Restrinja acesso SNMP por firewall/ACL
- Monitore logs de acesso SNMP
- Mantenha arquivo `renault_servers.json` com permissões restritas (600)

---

## 🔌 Requisitos de Rede

### Conectividade
- Servidor Flask deve ter acesso TCP/IP aos endereços IP dos servidores
- Porta SNMP padrão: **161/UDP**
- Timeout configurado: **3 segundos por dispositivo**
- Latência de rede recomendada: < 50ms

### Firewall / ACL
Liberar tráfego SNMP (UDP 161) do servidor Flask para:
- Servidores HP iLO (geralmente na VLAN de gerenciamento)
- VxRail iDRAC (geralmente na VLAN de gerenciamento)

Exemplo de regra de firewall:
```
SOURCE: <IP_servidor_flask>
DESTINATION: <subnet_ilo_idrac>/24
PORT: 161/UDP
PROTOCOL: UDP
ACTION: ALLOW
```

---

## 🖥️ Configuração nos Servidores

### HP DL380 (iLO 4/5)

#### 1. Acessar iLO Web Interface
```
https://<ip-ilo>
Login: Administrator
Password: <senha-ilo>
```

#### 2. Configurar SNMPv3
1. Navegue para: **Administration → Management → SNMP Settings**
2. Configurar:
   - **SNMP Version**: SNMPv3 only
   - **Enable SNMP Traps**: Yes
   - **SNMPv3 User**: `renault_monitor`
   - **Authentication Protocol**: SHA
   - **Authentication Password**: `<senha-forte-auth>`
   - **Privacy Protocol**: AES
   - **Privacy Password**: `<senha-forte-priv>`

#### 3. Verificar OIDs Habilitados
Certifique-se de que os seguintes OIDs estão habilitados:
- **Power Meter**: `1.3.6.1.4.1.232.6.2.1.3.1.4.1.3` (cpqHePowerMeterCurrReading)
- **Power Supply Status**: `1.3.6.1.4.1.232.6.2.9.3.1.1.4`
- **System Health**: `1.3.6.1.4.1.232.6.2.1.3.1.3`

#### 4. Salvar e Reiniciar iLO (se necessário)

### VxRail / Dell iDRAC

#### 1. Acessar iDRAC Web Interface
```
https://<ip-idrac>
Login: root
Password: <senha-idrac>
```

#### 2. Configurar SNMPv3
1. Navegue para: **iDRAC Settings → Network → SNMP Agent**
2. Configurar:
   - **SNMP Agent**: Enable
   - **SNMP Protocol**: SNMPv3 only
   - **User Name**: `renault_monitor`
   - **Authentication Protocol**: SHA
   - **Authentication Password**: `<senha-forte-auth>`
   - **Privacy Protocol**: AES-128
   - **Privacy Password**: `<senha-forte-priv>`

#### 3. Verificar OIDs Dell
- **Power Consumption**: `1.3.6.1.4.1.674.10892.5.4.600.30.1.6.1.3`
- **Power Supply Status**: `1.3.6.1.4.1.674.10892.5.4.600.12.1.5`
- **System Health**: `1.3.6.1.4.1.674.10892.5.2.1.0`

#### 4. Salvar Configurações

---

## ⚙️ Configuração do Dashboard

### 1. Editar Arquivo de Configuração

Edite o arquivo `renault_servers.json`:

```bash
nano renault_servers.json
```

### 2. Preencher Credenciais SNMPv3

```json
{
  "snmp_credentials": {
    "username": "renault_monitor",
    "auth_key": "SuaSenhaDeAutenticacao123!",
    "priv_key": "SuaSenhaDePrivacidade456!",
    "auth_protocol": "SHA",
    "priv_protocol": "AES"
  }
}
```

⚠️ **IMPORTANTE**: Use as mesmas credenciais configuradas em TODOS os servidores.

### 3. Adicionar Lista de Servidores

Exemplo completo com todos os servidores:

```json
{
  "servers": [
    {
      "device_id": "SRV-HP-001",
      "ip_address": "10.10.1.101",
      "generation": "gen8",
      "location": "DataCenter-Rack-1",
      "department": "Infraestrutura",
      "enabled": true
    },
    {
      "device_id": "SRV-HP-002",
      "ip_address": "10.10.1.102",
      "generation": "gen9",
      "location": "DataCenter-Rack-1",
      "department": "Infraestrutura",
      "enabled": true
    },
    {
      "device_id": "VXRAIL-01",
      "ip_address": "10.10.2.10",
      "generation": "vxrail",
      "location": "DataCenter-HyperConverged-1",
      "department": "Infraestrutura",
      "enabled": true
    }
  ]
}
```

### 4. Instalar Dependências

```bash
pip install -r requirements.txt
```

Isso instalará:
- `flask==2.3.3`
- `pysnmp==7.1.17`

### 5. Testar Coleta SNMP

Teste manual antes de iniciar o Flask:

```bash
python3 -c "
from snmp_collector import SNMPCollector
collector = SNMPCollector()
metrics = collector.collect_all_metrics()
for m in metrics[:5]:  # Mostrar primeiros 5 servidores
    print(f'{m.device_id}: {m.power_consumption_watts}W - {m.source}')
"
```

Saída esperada:
```
SRV-HP-001: 385.2W - snmp_real
SRV-HP-002: 402.1W - snmp_real
VXRAIL-01: 950.3W - snmp_real
```

Se aparecer "simulado" ao invés de "snmp_real", verifique:
- Conectividade de rede
- Credenciais SNMPv3
- Configuração iLO/iDRAC
- Firewall

### 6. Iniciar Dashboard

```bash
python3 app_renault_mvp.py
```

### 7. Verificar Integração

```bash
curl http://localhost:5000/api/metrics | python3 -m json.tool
```

Resposta esperada:
```json
{
    "arvores_equivalentes": 28432,
    "consumo_atual": 950.5,
    "economia_potencial": 352800.0,
    "emissoes_co2": 680250.5,
    "fonte": "snmp_real",
    "detalhes_fonte": {
        "servidores": "snmp_real",
        "workstations": "simulado"
    }
}
```

✅ **Campo `fonte`** deve ser `snmp_real` ou `cached` quando SNMP está funcionando.

---

## 🔍 Troubleshooting

### Problema: "fonte": "simulado" na API

**Possíveis causas:**
1. Arquivo `renault_servers.json` não encontrado ou mal formatado
2. Credenciais SNMPv3 incorretas
3. Servidores iLO/iDRAC não configurados para SNMPv3
4. Firewall bloqueando porta 161/UDP
5. pysnmp não instalado (`pip install pysnmp==7.1.17`)

**Solução:**
```bash
# Verificar arquivo existe
ls -la renault_servers.json

# Validar JSON
python3 -c "import json; print(json.load(open('renault_servers.json')))"

# Testar conectividade
nc -zvu <ip-ilo> 161

# Ver logs do Flask
FLASK_DEBUG=1 python3 app_renault_mvp.py
```

### Problema: Timeout nas coletas

**Solução:**
- Aumentar timeout em `renault_servers.json`:
```json
"coleta_config": {
  "timeout_seconds": 5
}
```

### Problema: "pysnmp not available"

**Solução:**
```bash
pip install --upgrade pysnmp==7.1.17
```

### Problema: Permissão negada no arquivo

**Solução:**
```bash
chmod 600 renault_servers.json  # Apenas owner pode ler/escrever
```

---

## 📊 Monitoramento e Performance

### Cache de Dados
- **TTL**: 5 minutos (300 segundos)
- **Objetivo**: Reduzir carga nos dispositivos SNMP
- **Comportamento**: Primeira consulta via SNMP, próximas 5 minutos usam cache

### Rate Limiting
- **Máximo de conexões simultâneas**: 10
- **Objetivo**: Evitar sobrecarga de rede
- **Comportamento**: Coletas em paralelo limitadas a 10 threads

### Retry Logic
- **Tentativas**: 3 por dispositivo
- **Backoff**: Exponencial (1s, 2s, 4s)
- **Fallback**: Dados simulados se todas as tentativas falharem

### Intervalo de Coleta Recomendado
- **Dashboard**: 30 segundos (não 10)
- **Razão**: Evitar sobrecarga SNMP
- **Configuração**: Alterar `auto_refresh_seconds` no config

---

## 🔐 Segurança - Checklist

- [ ] SNMPv3 configurado (nunca v1/v2c)
- [ ] Autenticação SHA habilitada
- [ ] Criptografia AES habilitada
- [ ] Senhas fortes (8+ caracteres)
- [ ] Arquivo `renault_servers.json` com permissões 600
- [ ] Credenciais não versionadas no Git (`.gitignore`)
- [ ] Firewall restringindo acesso SNMP
- [ ] Logs de acesso SNMP monitorados
- [ ] Rotação de credenciais agendada (90 dias)

---

## 📚 Referências Técnicas

### HP iLO
- [HP iLO SNMP Configuration Guide](https://support.hpe.com/hpesc/public/docDisplay?docId=emr_na-c03334051)
- [HP MIB Files Download](https://support.hpe.com/hpesc/public/swd/detail?swItemId=MTX_53293d026fb147958b223069b6)

### Dell iDRAC
- [iDRAC9 SNMP Configuration](https://www.dell.com/support/manuals/en-us/idrac9-lifecycle-controller-v3.3-series/idrac_3.30.30.30_ug/snmp-configuration)
- [Dell OpenManage MIBs](https://www.dell.com/support/kbdoc/en-us/000177080/openmanage-server-administrator-omsa-mibs)

### pysnmp
- [pysnmp Documentation](https://pysnmp.readthedocs.io/)
- [SNMPv3 USM Configuration](https://pysnmp.readthedocs.io/en/latest/examples/hlapi/v3arch/asyncio/manager/cmdgen/usm-sha-aes128.html)

### SNMP OIDs
- [HP/HPE OID Reference](https://oidref.com/1.3.6.1.4.1.232)
- [Dell OID Reference](https://oidref.com/1.3.6.1.4.1.674)

---

## 📞 Suporte

Para dúvidas sobre configuração SNMP:
1. Consultar documentação técnica HP/Dell acima
2. Verificar logs do Flask: `tail -f logs/ecoti.log`
3. Testar manualmente com `snmpwalk`:
   ```bash
   snmpwalk -v3 -u renault_monitor \
     -l authPriv -a SHA -A <auth_key> \
     -x AES -X <priv_key> \
     <ip-ilo> 1.3.6.1.4.1.232.6.2.1.3.1.4.1.3
   ```

---

**Versão**: 1.0  
**Data**: Janeiro 2025  
**Projeto**: EcoTI Dashboard - Renault Transformation Day 2025  
**Equipe**: UniBrasil - EcoCode.AI
