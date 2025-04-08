from flask_mail import Message
from modelos import db, Usuario
from flask import current_app

class Observador:
    def actualizar(self, tarea, accion="creada"):
        pass

class NotificacionCorreo(Observador):
    def actualizar(self, tarea, accion="creada"):
        usuario = Usuario.query.get(tarea.usuario_id)
        if usuario and usuario.correo:
            asunto = f"📌 Notificación de Tarea: {accion.capitalize()}"
            cuerpo = f"Hola {usuario.nombre},\n\n"

            if accion == "creada":
                cuerpo += (
                    f"Se te ha asignado una nueva tarea:\n\n"
                    f"📌 {tarea.nombre}\n📖 {tarea.descripcion or 'Sin descripción'}\n"
                    f"🗓️ Vence: {tarea.fecha_vencimiento or 'Sin fecha'}"
                )
            elif accion == "actualizada":
                cuerpo += f"El estado de la tarea '{tarea.nombre}' ha sido actualizado a: {tarea.estado}."
            elif accion == "completada":
                cuerpo += f"¡Felicidades! Completaste la tarea '{tarea.nombre}'."
            elif accion == "eliminada":
                cuerpo += f"La tarea '{tarea.nombre}' ha sido eliminada del sistema."
            elif accion == "vencida":
                cuerpo += f"La tarea '{tarea.nombre}' ha vencido. Por favor revisa su estado."

            cuerpo += "\n\nGestor de Tareas - Sistema de Notificación"

            enviar_correo(usuario.correo, asunto, cuerpo)

def enviar_correo(destinatario, asunto, cuerpo):
    try:
        mail = current_app.extensions.get('mail')
        if not mail:
            raise RuntimeError("Flask-Mail no está configurado.")
        msg = Message(asunto, sender=current_app.config.get("MAIL_DEFAULT_SENDER"), recipients=[destinatario])
        msg.body = cuerpo
        mail.send(msg)
        print(f"✅ Correo enviado a {destinatario}")
    except Exception as e:
        print(f"❌ Error al enviar correo: {e}")
