from app import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<Usuario {self.username}>'

class Repuesto(db.Model):
    __tablename__ = 'repuesto'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_repuesto = db.Column(db.String(50), nullable=False)
    descripcion_repuesto = db.Column(db.String(200), nullable=False)
    precio_repuesto = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Repuesto {self.nombre_repuesto}>'
