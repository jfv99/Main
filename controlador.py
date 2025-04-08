from modelos import db, Tarea, Usuario
from observador import NotificacionCorreo
from datetime import date

class GestorTareas:
    def __init__(self):
        self.observadores = [NotificacionCorreo()]

    def notificar(self, tarea, accion):
        for observador in self.observadores:
            observador.actualizar(tarea, accion)

    def listar_tareas(self, filtros=None):
        consulta = Tarea.query
        if filtros:
            if 'nombre' in filtros:
                consulta = consulta.filter(Tarea.nombre.ilike(f"%{filtros['nombre']}%"))
            if 'estado' in filtros:
                consulta = consulta.filter_by(estado=filtros['estado'])
            if 'fecha_inicio' in filtros:
                consulta = consulta.filter(Tarea.fecha_inicio >= filtros['fecha_inicio'])
            if 'fecha_vencimiento' in filtros:
                consulta = consulta.filter(Tarea.fecha_vencimiento <= filtros['fecha_vencimiento'])
            if 'prioridad' in filtros:
                consulta = consulta.filter_by(prioridad=filtros['prioridad'])
        return consulta.all()

    def agregar_tarea(self, nombre, descripcion, fecha_inicio, fecha_vencimiento, estado, prioridad, usuario_id):
        nueva = Tarea(
            nombre=nombre,
            descripcion=descripcion,
            fecha_inicio=fecha_inicio,
            fecha_vencimiento=fecha_vencimiento,
            estado=estado,
            prioridad=prioridad,
            usuario_id=usuario_id
        )
        db.session.add(nueva)
        db.session.commit()
        self.notificar(nueva, "creada")

    def actualizar_estado_tarea(self, tarea_id):
        tarea = Tarea.query.get(tarea_id)
        if tarea:
            tarea.estado = "Completada" if tarea.estado != "Completada" else "Pendiente"
            db.session.commit()
            self.notificar(tarea, "actualizada")
            if tarea.estado == "Completada":
                self.notificar(tarea, "completada")

    def eliminar_tarea(self, tarea_id):
        tarea = Tarea.query.get(tarea_id)
        if tarea:
            self.notificar(tarea, "eliminada")
            db.session.delete(tarea)
            db.session.commit()

    def verificar_vencidas(self):
        hoy = date.today()
        vencidas = Tarea.query.filter(
            Tarea.fecha_vencimiento < hoy, Tarea.estado != "Completada"
        ).all()
        for t in vencidas:
            self.notificar(t, "vencida")
