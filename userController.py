from modelos import db, Usuario
from observador import NotificacionCorreo
from datetime import date

class UserController:
    def __init__(self):
        self.observadores = [NotificacionCorreo()]

    def notificar(self, tarea, accion):
        for observador in self.observadores:
            observador.actualizar(tarea, accion)

    def login(self, email, password):
        try:
            consulta = Usuario.query
            print(f"Correo, {email}")
            print(f"Password, {password}")
            consulta = consulta.filter(Usuario.correo == email)
            usuario = consulta.all()
            print(f"Consulta de usuario, {usuario}")
            if not usuario or usuario.count() == 0:
                return None
            return usuario[0]
        except Exception as err:
            print(f"Error durante el login: {str(err)}")
            return None
