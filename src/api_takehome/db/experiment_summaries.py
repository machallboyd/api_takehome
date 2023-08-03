import os

from sqlalchemy import Column, create_engine, Float, ForeignKey, Integer, String, UUID
from sqlalchemy.orm import registry, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

DB_HOSTNAME = os.environ.get("API_DB_PATH")
db_url = (
    f"postgresql+psycopg2://postgres:extremely_secure_pw@{DB_HOSTNAME}:5432/testdb"
    if DB_HOSTNAME
    else "sqlite+pysqlite:///:memory:"
)

engine = create_engine(db_url, echo=True)
test_registry = registry()
Base = test_registry.generate_base()


class ExperimentSummary(Base):
    __tablename__ = "experiment_summary"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    total = Column(Integer)
    fav_compound_id = Column(Integer, ForeignKey("compound.id"))

    user = relationship("User", back_populates="summary")
    fav_compound = relationship("Compound", back_populates="summary")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    signup_date = Column(DateTime)

    summary = relationship("ExperimentSummary", uselist=False, back_populates="user")


class Compound(Base):
    __tablename__ = "compound"

    id = Column(Integer, primary_key=True)
    compound_name = Column(String)
    compound_structure = Column(String)

    summary = relationship("ExperimentSummary", uselist=False, back_populates="fav_compound")


class AverageExperimentsReport(Base):
    __tablename__ = "average_experiment_report"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, onupdate=func.now())
    avg = Column(Float)


def create_test_db():
    test_registry.metadata.create_all(engine)

