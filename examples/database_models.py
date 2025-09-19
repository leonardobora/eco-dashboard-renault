"""
Exemplo de modelos de banco de dados para persistência.
Este arquivo demonstra como estruturar dados para armazenamento permanente.
"""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Float,
    String,
    DateTime,
    Boolean,
    Text,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from typing import Optional, List, Dict

Base = declarative_base()


class Infrastructure(Base):
    """Modelo para dados da infraestrutura"""

    __tablename__ = "infrastructure"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    location = Column(String(200))
    workstations_total = Column(Integer, nullable=False)
    servers_hp = Column(Integer, nullable=False)
    vxrail_clusters = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    metrics = relationship("EnergyMetric", back_populates="infrastructure")
    sectors = relationship("Sector", back_populates="infrastructure")


class Sector(Base):
    """Modelo para setores/departamentos"""

    __tablename__ = "sectors"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    workstations_count = Column(Integer, nullable=False)
    average_usage_factor = Column(Float, default=0.75)
    peak_hours_start = Column(Integer, default=8)
    peak_hours_end = Column(Integer, default=18)
    infrastructure_id = Column(Integer, ForeignKey("infrastructure.id"))

    # Relacionamentos
    infrastructure = relationship("Infrastructure", back_populates="sectors")
    metrics = relationship("SectorMetric", back_populates="sector")


class EnergyMetric(Base):
    """Modelo para métricas de energia"""

    __tablename__ = "energy_metrics"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    consumption_kwh = Column(Float, nullable=False)
    consumption_cost_brl = Column(Float)
    co2_emissions_kg = Column(Float)
    workstations_active = Column(Integer)
    servers_active = Column(Integer)
    eco_mode_enabled = Column(Boolean, default=False)
    infrastructure_id = Column(Integer, ForeignKey("infrastructure.id"))

    # Relacionamentos
    infrastructure = relationship("Infrastructure", back_populates="metrics")


class SectorMetric(Base):
    """Modelo para métricas por setor"""

    __tablename__ = "sector_metrics"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    sector_id = Column(Integer, ForeignKey("sectors.id"))
    workstations_active = Column(Integer)
    consumption_kwh = Column(Float)
    efficiency_percentage = Column(Float)

    # Relacionamentos
    sector = relationship("Sector", back_populates="metrics")


class SensorReading(Base):
    """Modelo para leituras de sensores IoT"""

    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True)
    sensor_id = Column(String(50), nullable=False)
    sensor_type = Column(String(30), nullable=False)  # power, temperature, humidity
    location = Column(String(100))
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    value = Column(Float, nullable=False)
    unit = Column(String(10), nullable=False)
    quality = Column(String(20), default="good")  # good, warning, error
    metadata = Column(Text)  # JSON adicional se necessário


class Alert(Base):
    """Modelo para alertas do sistema"""

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    alert_type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    severity = Column(String(20), default="info")  # info, warning, error, critical
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)
    infrastructure_id = Column(Integer, ForeignKey("infrastructure.id"))


class OptimizationRecommendation(Base):
    """Modelo para recomendações de otimização"""

    __tablename__ = "optimization_recommendations"

    id = Column(Integer, primary_key=True)
    recommendation_type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    potential_savings_kwh = Column(Float)
    potential_savings_brl = Column(Float)
    implementation_effort = Column(String(20))  # baixo, médio, alto
    priority = Column(String(20))  # baixa, média, alta, crítica
    status = Column(String(20), default="pending")  # pending, implemented, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    implemented_at = Column(DateTime)
    infrastructure_id = Column(Integer, ForeignKey("infrastructure.id"))


class EnergyForecast(Base):
    """Modelo para previsões de consumo energético"""

    __tablename__ = "energy_forecasts"

    id = Column(Integer, primary_key=True)
    forecast_date = Column(DateTime, nullable=False)
    predicted_consumption_kwh = Column(Float, nullable=False)
    optimized_consumption_kwh = Column(Float)
    confidence_level = Column(Float)  # 0.0 a 1.0
    model_version = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    infrastructure_id = Column(Integer, ForeignKey("infrastructure.id"))


# Classes para operações de banco de dados
class DatabaseManager:
    """Gerenciador de operações de banco de dados"""

    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def create_tables(self):
        """Cria todas as tabelas no banco"""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        """Retorna uma sessão do banco de dados"""
        return self.SessionLocal()


class MetricsRepository:
    """Repositório para operações com métricas"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def save_energy_metric(self, metric_data: Dict) -> EnergyMetric:
        """Salva uma métrica de energia"""
        session = self.db_manager.get_session()
        try:
            metric = EnergyMetric(
                consumption_kwh=metric_data["consumption_kwh"],
                consumption_cost_brl=metric_data.get("cost_brl"),
                co2_emissions_kg=metric_data.get("co2_emissions_kg"),
                workstations_active=metric_data.get("workstations_active"),
                servers_active=metric_data.get("servers_active"),
                eco_mode_enabled=metric_data.get("eco_mode_enabled", False),
                infrastructure_id=metric_data.get("infrastructure_id", 1),
            )
            session.add(metric)
            session.commit()
            session.refresh(metric)
            return metric
        finally:
            session.close()

    def get_recent_metrics(self, hours: int = 24) -> List[EnergyMetric]:
        """Obtém métricas das últimas X horas"""
        session = self.db_manager.get_session()
        try:
            from datetime import timedelta

            cutoff_time = datetime.utcnow() - timedelta(hours=hours)

            metrics = (
                session.query(EnergyMetric)
                .filter(EnergyMetric.timestamp >= cutoff_time)
                .order_by(EnergyMetric.timestamp.desc())
                .all()
            )

            return metrics
        finally:
            session.close()

    def get_consumption_history(self, days: int = 7) -> List[Dict]:
        """Obtém histórico de consumo por período"""
        session = self.db_manager.get_session()
        try:
            from datetime import timedelta
            from sqlalchemy import func

            cutoff_time = datetime.utcnow() - timedelta(days=days)

            # Agregar consumo por hora
            results = (
                session.query(
                    func.date_trunc("hour", EnergyMetric.timestamp).label("hour"),
                    func.avg(EnergyMetric.consumption_kwh).label("avg_consumption"),
                )
                .filter(EnergyMetric.timestamp >= cutoff_time)
                .group_by(func.date_trunc("hour", EnergyMetric.timestamp))
                .order_by(func.date_trunc("hour", EnergyMetric.timestamp))
                .all()
            )

            return [
                {
                    "timestamp": result.hour.isoformat(),
                    "consumption_kwh": float(result.avg_consumption),
                }
                for result in results
            ]
        finally:
            session.close()


class SensorRepository:
    """Repositório para operações com sensores"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def save_sensor_reading(self, reading_data: Dict) -> SensorReading:
        """Salva uma leitura de sensor"""
        session = self.db_manager.get_session()
        try:
            reading = SensorReading(
                sensor_id=reading_data["sensor_id"],
                sensor_type=reading_data["sensor_type"],
                location=reading_data.get("location"),
                value=reading_data["value"],
                unit=reading_data["unit"],
                quality=reading_data.get("quality", "good"),
                metadata=reading_data.get("metadata"),
            )
            session.add(reading)
            session.commit()
            session.refresh(reading)
            return reading
        finally:
            session.close()

    def get_latest_readings_by_type(self, sensor_type: str) -> List[SensorReading]:
        """Obtém últimas leituras por tipo de sensor"""
        session = self.db_manager.get_session()
        try:
            # Obter última leitura de cada sensor do tipo especificado
            from sqlalchemy import func

            subquery = (
                session.query(
                    SensorReading.sensor_id,
                    func.max(SensorReading.timestamp).label("max_timestamp"),
                )
                .filter(SensorReading.sensor_type == sensor_type)
                .group_by(SensorReading.sensor_id)
                .subquery()
            )

            readings = (
                session.query(SensorReading)
                .join(
                    subquery,
                    (SensorReading.sensor_id == subquery.c.sensor_id)
                    & (SensorReading.timestamp == subquery.c.max_timestamp),
                )
                .all()
            )

            return readings
        finally:
            session.close()


class AlertRepository:
    """Repositório para operações com alertas"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create_alert(self, alert_data: Dict) -> Alert:
        """Cria um novo alerta"""
        session = self.db_manager.get_session()
        try:
            alert = Alert(
                alert_type=alert_data["alert_type"],
                title=alert_data["title"],
                description=alert_data.get("description"),
                severity=alert_data.get("severity", "info"),
                infrastructure_id=alert_data.get("infrastructure_id", 1),
            )
            session.add(alert)
            session.commit()
            session.refresh(alert)
            return alert
        finally:
            session.close()

    def get_active_alerts(self) -> List[Alert]:
        """Obtém todos os alertas ativos"""
        session = self.db_manager.get_session()
        try:
            alerts = (
                session.query(Alert)
                .filter(Alert.is_active == True)
                .order_by(Alert.created_at.desc())
                .all()
            )
            return alerts
        finally:
            session.close()

    def resolve_alert(self, alert_id: int) -> bool:
        """Resolve um alerta"""
        session = self.db_manager.get_session()
        try:
            alert = session.query(Alert).filter(Alert.id == alert_id).first()
            if alert:
                alert.is_active = False
                alert.resolved_at = datetime.utcnow()
                session.commit()
                return True
            return False
        finally:
            session.close()


# Exemplo de uso prático
def initialize_database():
    """Inicializa o banco de dados com dados de exemplo"""

    # Configuração do banco (PostgreSQL recomendado para produção)
    DATABASE_URL = "postgresql://user:password@localhost/ecoti_dashboard"
    # Para desenvolvimento/teste, pode usar SQLite:
    # DATABASE_URL = "sqlite:///ecoti_dashboard.db"

    db_manager = DatabaseManager(DATABASE_URL)

    # Criar tabelas
    db_manager.create_tables()

    # Criar dados iniciais
    session = db_manager.get_session()
    try:
        # Criar infraestrutura
        infra = Infrastructure(
            name="Renault Brasil",
            location="São José dos Pinhais, PR",
            workstations_total=5376,
            servers_hp=90,
            vxrail_clusters=10,
        )
        session.add(infra)
        session.commit()

        # Criar setores
        sectors_data = [
            {"name": "Administrativo", "workstations_count": 1200},
            {"name": "Engenharia", "workstations_count": 800},
            {"name": "Produção", "workstations_count": 1500},
            {"name": "Vendas", "workstations_count": 900},
            {"name": "Suporte", "workstations_count": 976},
        ]

        for sector_data in sectors_data:
            sector = Sector(infrastructure_id=infra.id, **sector_data)
            session.add(sector)

        session.commit()
        print("✅ Banco de dados inicializado com sucesso!")

    finally:
        session.close()

    return db_manager


def example_usage():
    """Exemplo de uso dos repositórios"""

    # Inicializar banco
    db_manager = initialize_database()

    # Criar repositórios
    metrics_repo = MetricsRepository(db_manager)
    sensor_repo = SensorRepository(db_manager)
    alert_repo = AlertRepository(db_manager)

    # Salvar algumas métricas de exemplo
    print("📊 Salvando métricas de exemplo...")

    metric_data = {
        "consumption_kwh": 1344.5,
        "cost_brl": 806.7,
        "co2_emissions_kg": 109.8,
        "workstations_active": 4200,
        "servers_active": 85,
        "eco_mode_enabled": True,
    }

    saved_metric = metrics_repo.save_energy_metric(metric_data)
    print(f"Métrica salva com ID: {saved_metric.id}")

    # Salvar leituras de sensores
    print("🔌 Salvando leituras de sensores...")

    sensor_data = {
        "sensor_id": "PM_001",
        "sensor_type": "power",
        "location": "Data Center Principal",
        "value": 850.3,
        "unit": "kW",
    }

    saved_reading = sensor_repo.save_sensor_reading(sensor_data)
    print(f"Leitura de sensor salva com ID: {saved_reading.id}")

    # Criar um alerta
    print("🚨 Criando alerta...")

    alert_data = {
        "alert_type": "high_consumption",
        "title": "Consumo Elevado Detectado",
        "description": "Consumo acima do normal detectado no setor administrativo",
        "severity": "warning",
    }

    saved_alert = alert_repo.create_alert(alert_data)
    print(f"Alerta criado com ID: {saved_alert.id}")

    # Consultar dados
    print("📈 Consultando histórico...")

    recent_metrics = metrics_repo.get_recent_metrics(hours=24)
    print(f"Encontradas {len(recent_metrics)} métricas nas últimas 24h")

    active_alerts = alert_repo.get_active_alerts()
    print(f"Alertas ativos: {len(active_alerts)}")


if __name__ == "__main__":
    print("🗄️ Exemplo de integração com banco de dados")
    print("Este exemplo demonstra como persistir dados do EcoTI Dashboard")
    print()

    try:
        example_usage()
        print("\n✅ Exemplo executado com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro ao executar exemplo: {e}")
        print(
            "Certifique-se de ter um banco PostgreSQL rodando ou use SQLite para testes"
        )
