const validarNombre = (nombre) => {
  if (!nombre) return false;
  let largo = nombre.trim().length;
  let largoValido = largo >= 3 && largo <= 80;

  return largoValido;
};

const validarComentario = (comentario) => {
  if (!comentario) return false;
  let largo = comentario.trim().length;
  let largoValido = largo >= 5 && largo <= 300;

  return largoValido;
};

const validateForm = () => {
  console.log("Ejecutando validación");

  let Formulario = document.forms["formulario"];

  let nombre = Formulario["nombre"].value;
  let comentario = Formulario["comentario"].value;

  // variables auxiliares de validación y función.
  let invalidInputs = [];
  let isValid = true;
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid &&= false;
  };

  // lógica de validación
  if (!validarNombre(nombre)) {
    setInvalidInput("Nombre (Entre 3 y 80 caracteres)");
  }

  if (!validarComentario(comentario)) {
    setInvalidInput("Comentario (Entre 5 y 300 caracteres)");
  }

  // finalmente mostrar la validación
  let validationBox = document.getElementById("val-box");
  let validationMessageElem = document.getElementById("val-msg");
  let validationListElem = document.getElementById("val-list");

  let confirmationBox = document.getElementById("confirm-box");
  let confirmationMessageElem = document.getElementById("confirm-msg");
  let confirmationListElem = document.getElementById("confirm-list");

  if (!isValid) {
    validationListElem.textContent = "";

    // agregar elementos inválidos al elemento val-list.
    for (input of invalidInputs) {
      let listElement = document.createElement("li");
      listElement.innerText = input;
      validationListElem.append(listElement);
    }

    // establecer val-msg
    validationMessageElem.innerText = "Los siguientes campos son inválidos:";

    // aplicar estilos de error
    validationBox.style.backgroundColor = "#ffdddd";

    // hacer visible el mensaje de validación
    validationBox.hidden = false;
  } else {
    // Enviamos el formulario
    validationListElem.textContent = "";

    Formulario.submit();
    console.log("Formulario enviado");
  }
};

const mostrarPantallaExito = () => {
  let successBox = document.getElementById("success-box");
  let successMessageElem = document.getElementById("success-msg");
  let successListElem = document.getElementById("success-list");

  successMessageElem.innerText =
    "Hemos recibido la información de adopción, muchas gracias y suerte";
  successListElem.textContent = "";

  let submitButton = document.createElement("button");
  submitButton.innerText = "Volver al inicio";
  submitButton.style.marginRight = "10px";
  submitButton.addEventListener("click", () => {
    window.location.href = "/";
  });

  successListElem.appendChild(submitButton);
  successBox.hidden = false;
};

let submitBtn = document.getElementById("submit-btn");
submitBtn.addEventListener("click", validateForm);
