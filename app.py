from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_mail import Mail
from modelos import db, Tarea
from controlador import GestorTareas
from config import MAIL_CONFIG
from userController import UserController
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/gestor_tareas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(MAIL_CONFIG)

db.init_app(app)
mail = Mail(app)

gestor = GestorTareas()

user = UserController()
currentSession = False

# 🔔 Verifica tareas vencidas automáticamente
@app.before_request
def verificar_tareas_vencidas_automaticamente():
    if request.endpoint == "listar_tareas":
        gestor.verificar_vencidas()

@app.route('/')
def index():
    return redirect(url_for('login'))
    if currentSession:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))
        

@app.route('/login')
def login():
    return render_template('login.html')

# Ruta para ver el gestor de tareas
@app.route('/home')
def home():
    return render_template('index.html')
    if currentSession:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))                

# 📋 Listar tareas con filtros
@app.route('/tareas', methods=['GET'])
def listar_tareas():
    filtros = {
        'nombre': request.args.get('nombre'),
        'estado': request.args.get('estado'),
        'fecha_inicio': request.args.get('fecha_inicio'),
        'fecha_vencimiento': request.args.get('fecha_vencimiento'),
        'prioridad': request.args.get('prioridad')
    }
    filtros = {k: v for k, v in filtros.items() if v}  # Elimina campos vacíos
    tareas = gestor.listar_tareas(filtros)
    return jsonify([
        {
            'id': t.id,
            'nombre': t.nombre,
            'descripcion': t.descripcion,
            'fecha_inicio': t.fecha_inicio.isoformat() if t.fecha_inicio else None,
            'fecha_vencimiento': t.fecha_vencimiento.isoformat() if t.fecha_vencimiento else None,
            'estado': t.estado,
            'prioridad': t.prioridad,
            'usuario_id': t.usuario_id
        } for t in tareas
    ])

# ➕ Agregar tarea
@app.route('/tarea', methods=['POST'])
def agregar_tarea():
    data = request.json
    gestor.agregar_tarea(
        data['nombre'],
        data.get('descripcion'),
        data.get('fecha_inicio'),
        data.get('fecha_vencimiento'),
        data.get('estado', 'Pendiente'),
        data.get('prioridad', 'Media'),
        data.get('usuario_id')
    )
    return jsonify({'mensaje': '✅ Tarea agregada exitosamente'}), 201

# 🔄 Cambiar estado
@app.route('/tarea/<int:tarea_id>/cambiar_estado', methods=['PUT'])
def cambiar_estado(tarea_id):
    gestor.actualizar_estado_tarea(tarea_id)
    return jsonify({'mensaje': '✅ Estado de tarea actualizado'})

# 🗑 Eliminar tarea
@app.route('/tarea/<int:tarea_id>', methods=['DELETE'])
def eliminar_tarea(tarea_id):
    gestor.eliminar_tarea(tarea_id)
    return jsonify({'mensaje': '✅ Tarea eliminada correctamente'})

# Inicio de sesión
@app.route('/initSession', methods=['POST'])
def initLogin():
    try:
        data = request.json
        login = user.login(
            data.get('email'),
            data.get('password')
        )        
        print('login',login)
        if not login:
            return jsonify({'mensaje': 'Error al inciar sesión verifique usuario y contraseña', 'login': False}), 200
        currentSession = True
        return jsonify({'mensaje': '✅ Inicio de sesión exitosamente', 'login': True}), 200
    except BadRequest as e:
        return jsonify({'mensaje': str(e), 'login' : False}), 400
    except Exception as e:
        return jsonify({'mensaje': f'Errpr intero del servidor {str(e)}', 'login' : False}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
