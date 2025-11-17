async function obtener_comentarios() {
  // Obtenemos el path en el que estamos
  const pathname = window.location.pathname;
  const parts = pathname.split("/");

  // Obtenemos el id de la publicacion actual desde el path
  const id = parts.pop();

  // Construimos la URL para obtener los comentarios de la publicacion actual
  const url = `/api/comments/${id}`;

  return fetch(url, { mode: "same-origin", credentials: "include" })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Error de red al obtener los comentarios");
      }

      const json = response.json();
      return json;
    })

    .catch((error) => {
      console.error(
        "Hubo un problema al obtener los comentarios de la publicación",
        error,
      );

      throw error;
    });
}

function procesar_comentarios(data) {
  return data.map(({ nombre, fecha, texto }) => {
    const fechaObj = new Date(fecha);
    return [nombre, fechaObj.getTime(), texto];
  });
}

async function poblar_comentarios() {
  try {
    const data = await obtener_comentarios();
    const comentarios = procesar_comentarios(data);
    console.log(comentarios);

    const comment_list = document.getElementById("comment-list");

    comment_list.innerHTML = "";

    comentarios.forEach((comentario) => {
      // Extraemos los campos del comentario
      const [nombre, timestamp, texto] = comentario;
      const fecha = new Date(timestamp).toLocaleString();

      // Construimos el HTML del comentario
      const comment_html = `
        <div class="comment-container">

          <div class="comment-header">
            <h1 class="comment-title">
              ${nombre}
            </h1>

            <p class="comment-date">Fecha: ${fecha}</p>
          </div>

          <div class="comment-body">
            <p>${texto}</p>
          </div>
        </div>
      `;

      comment_list.insertAdjacentHTML("beforeend", comment_html);
    });
  } catch (error) {
    // Si obtener_comentarios() falla, capturamos error.
    console.error("No se pudieron poblar los comentarios:", error);
  }
}

window.onload = () => {
  poblar_comentarios();
};
