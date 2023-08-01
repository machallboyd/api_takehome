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
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users")
    total = Column(Integer)
    fav_compound = Column(Integer, ForeignKey("compounds.id"))
    compounds = relationship("Compounds")

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    signup_date = Column(DateTime)

class Compounds(Base):
    __tablename__ = 'compounds'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)

class AverageExperimentsReports(Base):
    __tablename__ = 'average_experiment_reports'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, onupdate=func.now())
    avg = Column(Float)

def create_test_db():
    test_registry.metadata.create_all(engine)

