class EstrategiaOrdenamiento:
    def ordenar(self, tareas):
        pass

class OrdenarPorNombre(EstrategiaOrdenamiento):
    def ordenar(self, tareas):
        return sorted(tareas, key=lambda t: t.nombre)

class OrdenarPorEstado(EstrategiaOrdenamiento):
    def ordenar(self, tareas):
        return sorted(tareas, key=lambda t: t.estado)
 