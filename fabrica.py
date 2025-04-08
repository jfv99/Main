from modelos import Tarea

class TareaFactory:
    @staticmethod
    def crear_tarea(nombre, descripcion, usuario_id):
        return Tarea(nombre=nombre, descripcion=descripcion, estado='Pendiente', usuario_id=usuario_id)
