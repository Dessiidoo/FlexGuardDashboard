import os
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import numpy as np

DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AnomalyData(Base):
    __tablename__ = 'anomaly_data'
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    x_coord = Column(Integer, nullable=False)
    y_coord = Column(Integer, nullable=False)
    intensity = Column(Float, nullable=False)

class CostData(Base):
    __tablename__ = 'cost_data'
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    component = Column(String, nullable=False)
    savings_percent = Column(Float, nullable=False)

class UptimeData(Base):
    __tablename__ = 'uptime_data'
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    uptime_percent = Column(Float, nullable=False)

def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)

def populate_historical_data():
    """Populate database with 30 days of historical data"""
    init_db()
    session = SessionLocal()
    
    try:
        # Check if data already exists
        existing_count = session.query(AnomalyData).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} anomaly records. Skipping population.")
            return
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Generate data for each day
        current_date = start_date
        while current_date <= end_date:
            # Anomaly heatmap data (10x10 grid per day)
            for x in range(10):
                for y in range(10):
                    intensity = float(np.random.rand())
                    anomaly = AnomalyData(
                        timestamp=current_date,
                        x_coord=x,
                        y_coord=y,
                        intensity=intensity
                    )
                    session.add(anomaly)
            
            # Cost data (5 components per day)
            for i in range(1, 6):
                cost = CostData(
                    timestamp=current_date,
                    component=f"Component {i}",
                    savings_percent=float(np.random.uniform(5, 25))
                )
                session.add(cost)
            
            # Uptime data (10 samples per day)
            for i in range(10):
                sample_time = current_date + timedelta(hours=i*2.4)
                uptime = UptimeData(
                    timestamp=sample_time,
                    uptime_percent=float(np.random.uniform(90, 100))
                )
                session.add(uptime)
            
            current_date += timedelta(days=1)
        
        session.commit()
        print(f"Successfully populated database with 30 days of historical data")
        
    except Exception as e:
        session.rollback()
        print(f"Error populating data: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    populate_historical_data()
