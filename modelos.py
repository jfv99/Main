from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    correo = db.Column(db.String(255), unique=True, nullable=False)
    rol = db.Column(db.Enum('Administrador', 'Empleado', 'Cliente'))
    contrasena = db.Column(db.String(255), nullable=False)

class Tarea(db.Model):
    __tablename__ = 'tareas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_inicio = db.Column(db.Date)
    fecha_vencimiento = db.Column(db.Date)
    estado = db.Column(db.Enum('Pendiente', 'En progreso', 'Completada'))
    prioridad = db.Column(db.Enum('Alta', 'Media', 'Baja'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    usuario = db.relationship('Usuario', backref='tareas')
