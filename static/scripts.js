document.addEventListener("DOMContentLoaded", () => {
    cargarTareas();
    document.getElementById("form-tarea").addEventListener("submit", (e) => {
        e.preventDefault();
        agregarTarea();
    });
    document.getElementById("buscar").addEventListener("input", filtrarTareas);
});

function cargarTareas() {
    fetch("/tareas")
        .then(response => response.json())
        .then(data => {
            console.log("📌 Datos obtenidos:", data);
            mostrarTareas(data);
        })
        .catch(error => console.error("❌ Error obteniendo datos:", error));
}

function mostrarTareas(data) {
    let lista = document.getElementById("tareas-lista");
    if (!lista) {
        console.error("❌ Elemento 'tareas-lista' no encontrado en el HTML.");
        return;
    }
    lista.innerHTML = "";
    data.forEach(tarea => {
        lista.innerHTML += `
            <tr class="tarea">
                <td>${tarea.id}</td>
                <td>${tarea.nombre}</td>
                <td>${tarea.descripcion || 'N/A'}</td>
                <td>${tarea.fecha_inicio ? new Date(tarea.fecha_inicio).toLocaleDateString() : 'N/A'}</td>
                <td>${tarea.fecha_vencimiento ? new Date(tarea.fecha_vencimiento).toLocaleDateString() : 'N/A'}</td>
                <td>${tarea.estado}</td>
                <td>${tarea.prioridad || 'N/A'}</td>
                <td>
                    <button class="btn btn-success" onclick="cambiarEstado(${tarea.id})">✔ Completar</button>
                    <button class="btn btn-danger" onclick="eliminarTarea(${tarea.id})">🗑 Eliminar</button>
                </td>
            </tr>`;
    });
}

function filtrarTareas() {
    let filtro = document.getElementById("buscar").value.toLowerCase();
    document.querySelectorAll(".tarea").forEach(row => {
        let texto = row.innerText.toLowerCase();
        row.style.display = texto.includes(filtro) ? "" : "none";
    });
}

function agregarTarea() {
    let nombre = document.getElementById("nombre").value;
    let descripcion = document.getElementById("descripcion").value;
    let fecha_inicio = document.getElementById("fecha_inicio").value;
    let fecha_vencimiento = document.getElementById("fecha_vencimiento").value;
    let estado = document.getElementById("estado").value;
    let prioridad = document.getElementById("prioridad").value;
    let usuario_id = document.getElementById("usuario_id").value || null;

    fetch("/tarea", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre, descripcion, fecha_inicio, fecha_vencimiento, estado, prioridad, usuario_id })
    })
    .then(response => response.json())
    .then(() => {
        cargarTareas();
        document.getElementById("form-tarea").reset();
    })
    .catch(error => console.error("❌ Error agregando tarea:", error));
}

function cambiarEstado(id) {
    fetch(`/tarea/${id}/cambiar_estado`, { method: "PUT" })
        .then(() => cargarTareas())
        .catch(error => console.error("❌ Error cambiando estado:", error));
}

function eliminarTarea(id) {
    fetch(`/tarea/${id}`, { method: "DELETE" })
        .then(() => cargarTareas())
        .catch(error => console.error("❌ Error eliminando tarea:", error));
}
