from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, Float
from sqlalchemy.orm import registry, relationship
from sqlalchemy.types import DateTime
from sqlalchemy.sql import func

#in production, grab url from env variable to swap between prod and dev dbs.
db_url = "sqlite+pysqlite:///:memory:"

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
test_registry = registry()
Base = test_registry.generate_base()

class ExperimentSummary(Base):
    __tablename__ = 'experiment_summary'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")
    total = Column(Integer)
    fav_compound = Column(Integer, ForeignKey("compound.id"))
    compounds = relationship("Compound")

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    signup_date = Column(DateTime)


class Compound(Base):
    __tablename__ = 'compound'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)

class AverageExperimentsReport(Base):
    __tablename__ = 'average_experiment_report'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, onupdate=func.now())
    avg = Column(Float)

def create_test_db():
    test_registry.metadata.create_all(engine)

def test_engine():
    return engine
