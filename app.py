from flask import Flask, request, jsonify, render_template
from flask_mail import Mail
from modelos import db, Tarea
from controlador import GestorTareas
from config import MAIL_CONFIG

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/gestor_tareas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(MAIL_CONFIG)

db.init_app(app)
mail = Mail(app)

gestor = GestorTareas()

# 🔔 Verifica tareas vencidas automáticamente
@app.before_request
def verificar_tareas_vencidas_automaticamente():
    if request.endpoint == "listar_tareas":
        gestor.verificar_vencidas()

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
