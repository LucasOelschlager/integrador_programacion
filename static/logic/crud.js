function abrirModalEditar(id_curso, dni, nombre, apellido, email) {
  document.getElementById("id_curso-edit").value = id_curso;
  document.getElementById("dni-edit").value = dni;
  document.getElementById("nombre-edit").value = nombre;
  document.getElementById("apellido-edit").value = apellido;
  document.getElementById("email-edit").value = email;
  modal.show();
}

function guardarCambios(event) {
  event.preventDefault();

  const id_curso = document.getElementById("id_curso-edit").value;
  const dni = document.getElementById("dni-edit").value;
  const nombre = document.getElementById("nombre-edit").value;
  const apellido = document.getElementById("apellido-edit").value;
  const email = document.getElementById("email-edit").value;

  fetch(`/admin/${id_curso}/${dni}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ nombre, apellido, email }),
  })
    .then((res) => res.json())
    .then((data) => {
      alert(data.mensaje);
      const fila = document.getElementById(`fila-${id_curso}-${dni}`);
      if (fila) {
        fila.querySelector(".nombre").textContent = nombre;
        fila.querySelector(".apellido").textContent = apellido;
        fila.querySelector(".email").textContent = email;
      }
      modal.hide();
    })
    .catch((err) => {
      console.error("Error:", err);
      alert("Ocurrió un error al actualizar.");
    });
}

function eliminarInscripto(id_curso, dni) {
  if (confirm("¿Estás seguro de que querés eliminar este inscripto?")) {
    fetch(`/admin/${id_curso}/${dni}`, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then((data) => {
        alert(data.mensaje);
        if (data.mensaje.includes("eliminada")) {
          const fila = document.getElementById(`fila-${id_curso}-${dni}`);
          if (fila) fila.remove();
        }
      })
      .catch((error) => {
        console.error("Error al eliminar:", error);
        alert("Ocurrió un error al eliminar.");
      });
  }
}
