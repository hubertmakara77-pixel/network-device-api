from datetime import datetime
from .database import db

class Device(db.Model):
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False, unique=True)
    snmp_community = db.Column(db.String(50), nullable=False, default='public')
    port = db.Column(db.Integer, default=161)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacja - jedno urządzenie może mieć wiele metryk
    metrics = db.relationship('Metric', backref='device', lazy=True, cascade="all, delete-orphan")

class Metric(db.Model):
    __tablename__ = 'metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    metric_type = db.Column(db.String(50), nullable=False) # np. 'signal_gain', 'temperature'
    value = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)