// Referencias a los elementos del menú flotante
const menuNota = document.getElementById("menu-nota");
const selectNota = document.getElementById("select-nota");
const hiddenAvisoId = document.getElementById("menu-aviso-id");

// Funcion para cargar los avisos de forma asincrona.
async function cargarAvisos() {
  try {
    const response = await fetch("/api/avisos"); //Llamamos a nuestro endpoint

    if (!response.ok) {
      throw new Error("Error en la red: " + response.statusText);
    }

    // Convertimos la response con el la lista de DTO a JSON
    const data = await response.json();

    // Obtenemos y limpiamos el cuerpo de la tabla
    const tbody = document.getElementById("cuerpo-tabla");
    tbody.innerHTML = "";

    // Recorremos cada elemento del array de avisos y lo agregamos a la tabla
    //'data' es nuestro List<AvisoDto> en formato JSON
    data.forEach((aviso) => {
      const tr = tbody.insertRow();

      tr.insertCell().textContent = aviso.id;
      tr.insertCell().textContent = new Date(aviso.fechaPublicacion).toLocaleDateString(
        "es-CL",
      );
      tr.insertCell().textContent = aviso.sector;
      tr.insertCell().textContent = aviso.cantidadTipoEdad;
      tr.insertCell().textContent = aviso.comuna;

      // Construimos el string de la nota ('-' si no hay nota)
      const notaPromedio = aviso.notaPromedio;
      const textoNota =
        notaPromedio === 0.0 || notaPromedio === 0 ? "-" : notaPromedio.toFixed(1);
      tr.insertCell().textContent = textoNota;

      // Columna del boton
      const cellAcciones = tr.insertCell();
      const btnNota = document.createElement("button");
      btnNota.textContent = "Agregar Nota";

      // Asignamos evento al boton, pasando el evento y el ID del aviso
      btnNota.onclick = (event) => {
        mostrarMenuNota(event, aviso.id);
      };
      cellAcciones.appendChild(btnNota);
    });
  } catch (error) {
    console.error("Error al cargar los avisos: ", error);
    const tbody = document.getElementById("cuerpo-tabla");
    tbody.innerHTML = '<tr><td colspan="7">Error al cargar los datos.</td></tr>';
  }
}

// Logica del menu flotante ############################################################

function mostrarMenuNota(event, avisoId) {
  event.stopPropagation(); // Evita que el clic se propague al body

  // Obtenemos la posición del botón que fue clickeado
  const rect = event.target.getBoundingClientRect();

  // Posicionamos el menú flotante justo debajo del botón
  menuNota.style.display = "block";
  menuNota.style.top = rect.bottom + window.scrollY + "px";
  menuNota.style.left = rect.left + window.scrollX + "px";

  // Guardamos el ID del aviso en el campo oculto
  hiddenAvisoId.value = avisoId;
}

function ocultarMenuNota() {
  menuNota.style.display = "none";
  hiddenAvisoId.value = "";
}

async function enviarNota() {
  const avisoId = hiddenAvisoId.value;
  const valorNota = selectNota.value;

  // Creamos el cuerpo de la petición (DTO)
  const body = {
    nota: parseInt(valorNota), // Aseguramos que sea un número
  };

  try {
    // Hacemos la llamada POST asíncrona a nuestro endpoint
    const response = await fetch(`/api/avisos/${avisoId}/notas`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || "Error al guardar la nota");
    }

    // Si hubo exito
    alert("¡Nota guardada exitosamente!");
    ocultarMenuNota(); // Ocultamos el menú
    cargarAvisos(); // Refrescamos la tabla para ver el nuevo promedio
  } catch (error) {
    console.error("Error al enviar la nota:", error);
    alert("Error al enviar la nota: " + error.message);
  }
}

// Asignacion de eventos ############################################################

// Asignar la función de enviar al botón "Enviar"
document.getElementById("btn-enviar-nota").addEventListener("click", enviarNota);

// Asignar la función de ocultar al botón "Cancelar"
document.getElementById("btn-cancelar-nota").addEventListener("click", ocultarMenuNota);

// Ocultar el menú si se hace clic en cualquier otro lugar
document.addEventListener("click", (event) => {
  if (!menuNota.contains(event.target)) {
    // Si el clic fue fuera del menú y el menú está visible
    if (menuNota.style.display === "block") {
      // Solo lo ocultamos si el clic no fue en un botón "Agregar Nota"
      if (
        !event.target.matches("button") ||
        !event.target.textContent.includes("Agregar Nota")
      ) {
        ocultarMenuNota();
      }
    }
  }
});

// Cargar los avisos cuando la página esté lista
// El script se carga con defer en el HTML
cargarAvisos();
