"""
SNMP Collector para EcoTI Dashboard - Renault Sustentabilidade Digital

Módulo responsável por coletar métricas de consumo de energia via SNMPv3
dos servidores HP DL380 (G8/G9/G10) e VxRail T560F da infraestrutura Renault.

Características:
- SNMPv3 com autenticação SHA + criptografia AES (seguro)
- Suporte a múltiplas gerações HP com OIDs diferentes
- Rate limiting (max 10 conexões simultâneas)
- Cache com TTL de 5 minutos
- Retry logic com backoff exponencial
- Fallback automático para dados simulados
"""

import asyncio
import json
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verificar disponibilidade do pysnmp
try:
    # pysnmp 7.x imports
    from pysnmp.hlapi.v3arch.asyncio import (
        get_cmd,
        SnmpEngine,
        UsmUserData,
        UdpTransportTarget,
        ContextData,
        ObjectType,
        ObjectIdentity
    )
    from pysnmp.proto.secmod.rfc3414.auth import hmacsha, hmacmd5
    from pysnmp.proto.secmod.rfc3826.priv import aes
    from pysnmp.proto.secmod.rfc3414.priv import des
    
    # Auth/Priv protocol IDs
    usmHMACSHAAuthProtocol = hmacsha.HmacSha.SERVICE_ID
    usmHMACMD5AuthProtocol = hmacmd5.HmacMd5.SERVICE_ID
    usmAesCfb128Protocol = aes.Aes.SERVICE_ID
    usmDESPrivProtocol = des.Des.SERVICE_ID
    
    SNMP_AVAILABLE = True
except ImportError:
    SNMP_AVAILABLE = False
    logger.warning("pysnmp not available - SNMP collector will use fallback mode")


@dataclass
class ServerMetrics:
    """Métricas coletadas de um servidor"""
    device_id: str
    power_consumption_watts: float
    timestamp: datetime
    source: str  # 'snmp_real', 'cached', 'simulated'
    status: str  # 'success', 'timeout', 'error'
    error_message: Optional[str] = None


@dataclass
class SNMPCredentials:
    """Credenciais SNMPv3"""
    username: str
    auth_key: str
    priv_key: str
    auth_protocol: str = "SHA"
    priv_protocol: str = "AES"


class HPServerOIDs:
    """OIDs para diferentes gerações de servidores HP DL380"""
    
    # HP DL380 Gen8
    GEN8 = {
        "power_consumption": "1.3.6.1.4.1.232.6.2.1.3.1.4.1.3",  # cpqHePowerMeterCurrReading
        "power_supply_status": "1.3.6.1.4.1.232.6.2.9.3.1.1.4",
        "system_health": "1.3.6.1.4.1.232.6.2.1.3.1.3"
    }
    
    # HP DL380 Gen9
    GEN9 = {
        "power_consumption": "1.3.6.1.4.1.232.6.2.1.3.1.4.1.3",
        "power_supply_status": "1.3.6.1.4.1.232.6.2.9.3.1.1.4",
        "system_health": "1.3.6.1.4.1.232.6.2.1.3.1.3"
    }
    
    # HP DL380 Gen10
    GEN10 = {
        "power_consumption": "1.3.6.1.4.1.232.6.2.1.3.1.4.1.3",
        "power_supply_status": "1.3.6.1.4.1.232.6.2.9.3.1.1.4",
        "system_health": "1.3.6.1.4.1.232.6.2.1.3.1.3"
    }
    
    # VxRail (Dell EMC - using iDRAC OIDs)
    VXRAIL = {
        "power_consumption": "1.3.6.1.4.1.674.10892.5.4.600.30.1.6.1.3",  # Dell iDRAC power reading
        "power_supply_status": "1.3.6.1.4.1.674.10892.5.4.600.12.1.5",
        "system_health": "1.3.6.1.4.1.674.10892.5.2.1.0"
    }
    
    @classmethod
    def get_oids_for_generation(cls, generation: str) -> Dict[str, str]:
        """Retorna OIDs para uma geração específica"""
        generation_map = {
            "gen8": cls.GEN8,
            "gen9": cls.GEN9,
            "gen10": cls.GEN10,
            "vxrail": cls.VXRAIL
        }
        return generation_map.get(generation.lower(), cls.GEN9)  # Default para Gen9


class SNMPCollector:
    """
    Coletor SNMP para servidores Renault
    
    Coleta métricas de consumo de energia via SNMPv3 com:
    - Rate limiting (max 10 conexões simultâneas)
    - Cache com TTL de 5 minutos
    - Retry logic com backoff exponencial
    - Fallback para dados simulados
    """
    
    def __init__(self, config_file: str = "renault_servers.json"):
        """
        Inicializa o coletor SNMP
        
        Args:
            config_file: Caminho para arquivo de configuração JSON
        """
        self.config_file = config_file
        self.servers_config: List[Dict] = []
        self.credentials: Optional[SNMPCredentials] = None
        self.cache: Dict[str, Tuple[ServerMetrics, datetime]] = {}
        self.cache_ttl_seconds = 300  # 5 minutos
        self.max_concurrent = 10
        self.timeout_seconds = 3
        self.max_retries = 3
        self.cache_lock = threading.Lock()
        
        # Tentar carregar configuração
        self._load_config()
        
    def _load_config(self) -> bool:
        """Carrega configuração do arquivo JSON"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            # Carregar credenciais SNMPv3
            if 'snmp_credentials' in config:
                creds = config['snmp_credentials']
                self.credentials = SNMPCredentials(
                    username=creds.get('username', ''),
                    auth_key=creds.get('auth_key', ''),
                    priv_key=creds.get('priv_key', ''),
                    auth_protocol=creds.get('auth_protocol', 'SHA'),
                    priv_protocol=creds.get('priv_protocol', 'AES')
                )
            
            # Carregar lista de servidores
            self.servers_config = config.get('servers', [])
            
            logger.info(f"Configuração carregada: {len(self.servers_config)} servidores")
            return True
            
        except FileNotFoundError:
            logger.warning(f"Arquivo de configuração {self.config_file} não encontrado - usando modo simulado")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao parsear JSON: {e}")
            return False
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            return False
    
    def _is_cache_valid(self, device_id: str) -> bool:
        """Verifica se cache é válido para um dispositivo"""
        with self.cache_lock:
            if device_id not in self.cache:
                return False
            
            _, cached_time = self.cache[device_id]
            age = (datetime.now() - cached_time).total_seconds()
            return age < self.cache_ttl_seconds
    
    def _get_from_cache(self, device_id: str) -> Optional[ServerMetrics]:
        """Obtém métrica do cache se válida"""
        if self._is_cache_valid(device_id):
            with self.cache_lock:
                metrics, _ = self.cache[device_id]
                # Atualizar fonte para indicar que vem do cache
                metrics.source = 'cached'
                return metrics
        return None
    
    def _update_cache(self, device_id: str, metrics: ServerMetrics):
        """Atualiza cache com novas métricas"""
        with self.cache_lock:
            self.cache[device_id] = (metrics, datetime.now())
    
    def _snmp_get_power(self, server_config: Dict) -> ServerMetrics:
        """
        Coleta consumo de energia via SNMP de um servidor
        
        Args:
            server_config: Dicionário com configuração do servidor
            
        Returns:
            ServerMetrics com dados coletados ou erro
        """
        device_id = server_config.get('device_id', 'unknown')
        ip_address = server_config.get('ip_address', '')
        generation = server_config.get('generation', 'gen9')
        
        # Verificar cache primeiro
        cached = self._get_from_cache(device_id)
        if cached:
            logger.debug(f"Cache hit para {device_id}")
            return cached
        
        # Se SNMP não disponível, retornar dados simulados
        if not SNMP_AVAILABLE or not self.credentials:
            return self._simulate_server_metrics(server_config)
        
        # Obter OIDs para a geração do servidor
        oids = HPServerOIDs.get_oids_for_generation(generation)
        power_oid = oids.get('power_consumption', '')
        
        # Tentar coleta SNMP com retry
        for attempt in range(self.max_retries):
            try:
                # Criar um novo event loop para esta thread
                # Necessário pois ThreadPoolExecutor pode reusar threads
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_closed():
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                # Executar coleta SNMP assíncrona
                metrics = loop.run_until_complete(self._async_snmp_get(
                    device_id, ip_address, power_oid, attempt
                ))
                
                # Atualizar cache
                self._update_cache(device_id, metrics)
                
                logger.info(f"SNMP success: {device_id} = {metrics.power_consumption_watts}W")
                return metrics
                
            except Exception as e:
                wait_time = 2 ** attempt  # Backoff exponencial: 1s, 2s, 4s
                logger.warning(f"SNMP falhou para {device_id} (tentativa {attempt+1}/{self.max_retries}): {e}")
                
                if attempt < self.max_retries - 1:
                    time.sleep(wait_time)
                else:
                    # Última tentativa falhou - usar simulação
                    logger.error(f"SNMP falhou definitivamente para {device_id} - usando simulação")
                    return self._simulate_server_metrics(server_config, error_msg=str(e))
        
        # Fallback (não deveria chegar aqui)
        return self._simulate_server_metrics(server_config)
    
    async def _async_snmp_get(self, device_id: str, ip_address: str, power_oid: str, attempt: int) -> ServerMetrics:
        """
        Executa consulta SNMP assíncrona
        
        Args:
            device_id: ID do dispositivo
            ip_address: Endereço IP
            power_oid: OID para consumo de energia
            attempt: Número da tentativa (para logging)
            
        Returns:
            ServerMetrics com dados coletados
        """
        try:
            # Configurar autenticação SNMPv3
            auth_protocol = usmHMACSHAAuthProtocol if self.credentials.auth_protocol == 'SHA' else usmHMACMD5AuthProtocol
            priv_protocol = usmAesCfb128Protocol if self.credentials.priv_protocol == 'AES' else usmDESPrivProtocol
            
            engine = SnmpEngine()
            user_data = UsmUserData(
                self.credentials.username,
                authKey=self.credentials.auth_key,
                privKey=self.credentials.priv_key,
                authProtocol=auth_protocol,
                privProtocol=priv_protocol
            )
            
            # Criar transport target (async)
            logger.debug(f"Creating UdpTransportTarget for {ip_address}")
            target = await UdpTransportTarget.create(
                (ip_address, 161),
                timeout=self.timeout_seconds,
                retries=0
            )
            logger.debug(f"Target created: {target}")
            
            context = ContextData()
            obj_type = ObjectType(ObjectIdentity(power_oid))
            
            # Executar GET SNMP
            logger.debug(f"Calling get_cmd for {device_id}")
            errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
                engine, user_data, target, context, obj_type
            )
            
            # Fechar engine (não é async)
            engine.close_dispatcher()
            
            if errorIndication:
                raise Exception(f"SNMP error: {errorIndication}")
            elif errorStatus:
                raise Exception(f"SNMP error: {errorStatus.prettyPrint()}")
            
            # Extrair valor de consumo
            power_watts = float(varBinds[0][1])
            
            return ServerMetrics(
                device_id=device_id,
                power_consumption_watts=power_watts,
                timestamp=datetime.now(),
                source='snmp_real',
                status='success'
            )
        except Exception as e:
            logger.error(f"Error in _async_snmp_get for {device_id}: {e}", exc_info=True)
            raise
    
    def _simulate_server_metrics(self, server_config: Dict, error_msg: Optional[str] = None) -> ServerMetrics:
        """
        Gera métricas simuladas para um servidor
        
        Args:
            server_config: Configuração do servidor
            error_msg: Mensagem de erro opcional
            
        Returns:
            ServerMetrics simulado
        """
        device_id = server_config.get('device_id', 'unknown')
        generation = server_config.get('generation', 'gen9')
        
        # Potência típica por geração
        power_ranges = {
            'gen8': (350, 450),
            'gen9': (350, 450),
            'gen10': (300, 400),
            'vxrail': (800, 1200)
        }
        
        min_power, max_power = power_ranges.get(generation.lower(), (400, 400))
        
        # Simular consumo baseado no horário (servidores ficam ligados 24/7)
        hora_atual = datetime.now().hour
        if 8 <= hora_atual <= 18:  # Horário comercial - maior carga
            utilizacao = 0.9
        elif 19 <= hora_atual <= 22:  # Noite
            utilizacao = 0.7
        else:  # Madrugada
            utilizacao = 0.5
        
        # Consumo com variação realista
        base_power = (min_power + max_power) / 2
        power_watts = base_power * utilizacao
        
        return ServerMetrics(
            device_id=device_id,
            power_consumption_watts=power_watts,
            timestamp=datetime.now(),
            source='simulado',
            status='error' if error_msg else 'simulated',
            error_message=error_msg
        )
    
    def collect_all_metrics(self) -> List[ServerMetrics]:
        """
        Coleta métricas de todos os servidores configurados
        
        Usa ThreadPoolExecutor para coletar em paralelo com rate limiting
        
        Returns:
            Lista de ServerMetrics
        """
        if not self.servers_config:
            logger.warning("Nenhum servidor configurado - usando dados simulados padrão")
            return self._get_default_simulated_metrics()
        
        metrics_list = []
        
        # Coletar em paralelo com rate limiting
        with ThreadPoolExecutor(max_workers=self.max_concurrent) as executor:
            future_to_server = {
                executor.submit(self._snmp_get_power, server): server
                for server in self.servers_config
            }
            
            for future in as_completed(future_to_server):
                try:
                    metrics = future.result(timeout=self.timeout_seconds + 5)
                    metrics_list.append(metrics)
                except Exception as e:
                    server = future_to_server[future]
                    logger.error(f"Erro ao coletar métricas de {server.get('device_id', 'unknown')}: {e}")
                    # Adicionar métrica simulada em caso de erro
                    metrics_list.append(self._simulate_server_metrics(server, str(e)))
        
        return metrics_list
    
    def _get_default_simulated_metrics(self) -> List[ServerMetrics]:
        """
        Gera métricas simuladas padrão para infraestrutura Renault
        90 HP DL380 + 10 VxRail
        
        Returns:
            Lista de ServerMetrics simulados
        """
        metrics = []
        
        # 90 servidores HP DL380 (mix de gerações)
        for i in range(90):
            if i < 30:
                generation = 'gen8'
            elif i < 60:
                generation = 'gen9'
            else:
                generation = 'gen10'
            
            server_config = {
                'device_id': f'SRV-HP-{i+1:03d}',
                'generation': generation,
                'ip_address': f'10.0.1.{i+1}'
            }
            metrics.append(self._simulate_server_metrics(server_config))
        
        # 10 sistemas VxRail
        for i in range(10):
            server_config = {
                'device_id': f'VXRAIL-{i+1:02d}',
                'generation': 'vxrail',
                'ip_address': f'10.0.2.{i+1}'
            }
            metrics.append(self._simulate_server_metrics(server_config))
        
        return metrics
    
    def get_total_consumption_kwh(self) -> Tuple[float, str]:
        """
        Calcula consumo total atual em kWh
        
        Returns:
            Tupla (consumo_kwh, fonte)
            fonte: 'snmp_real', 'cached', 'simulado', 'mixed'
        """
        metrics = self.collect_all_metrics()
        
        total_watts = sum(m.power_consumption_watts for m in metrics)
        total_kwh = total_watts / 1000
        
        # Determinar fonte dominante
        sources = [m.source for m in metrics]
        if all(s == 'snmp_real' for s in sources):
            fonte = 'snmp_real'
        elif all(s == 'cached' for s in sources):
            fonte = 'cached'
        elif all(s == 'simulado' for s in sources):
            fonte = 'simulado'
        else:
            fonte = 'mixed'
        
        logger.info(f"Consumo total: {total_kwh:.2f} kWh (fonte: {fonte})")
        return total_kwh, fonte
    
    def get_server_count(self) -> Dict[str, int]:
        """
        Retorna contagem de servidores por tipo
        
        Returns:
            Dict com contagens
        """
        if self.servers_config:
            hp_count = sum(1 for s in self.servers_config if 'HP' in s.get('device_id', ''))
            vxrail_count = sum(1 for s in self.servers_config if 'VXRAIL' in s.get('device_id', ''))
        else:
            hp_count = 90
            vxrail_count = 10
        
        return {
            'servidores_hp': hp_count,
            'vxrail': vxrail_count,
            'total': hp_count + vxrail_count
        }
